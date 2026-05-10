from dataclasses import dataclass
from typing import Any

import httpx

from app.config import Settings, get_settings
from app.models.chat import ChatMessage


@dataclass(frozen=True)
class AIResult:
    content: str
    model: str
    raw_response: dict[str, Any] | None = None


class AIServiceError(Exception):
    """Base exception for AI provider failures."""


class AIProviderConfigError(AIServiceError):
    pass


class AIProviderTimeoutError(AIServiceError):
    pass


class AIProviderRequestError(AIServiceError):
    pass


class AIService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        history: list[ChatMessage],
    ) -> AIResult:
        provider = self.settings.ai_provider.lower()
        if provider == "mock":
            return self._mock_response(user_message)
        if provider == "vllm":
            return await self._vllm_response(system_prompt, user_message, history)
        if provider == "groq":
            return await self._groq_response(
                system_prompt,
                user_message,
                history,
            )
        raise AIProviderConfigError(f"Unsupported AI_PROVIDER: {self.settings.ai_provider}")

    def _mock_response(self, user_message: str) -> AIResult:
        lower_message = user_message.lower()
        if "rocm" in lower_message:
            content = (
                "ROCm adalah platform software terbuka dari AMD untuk komputasi GPU "
                "dan workload AI/HPC. Untuk mulai, pastikan GPU yang dipakai memang "
                "didukung ROCm, lalu pilih jalur yang sesuai: PyTorch ROCm untuk "
                "eksperimen model, atau vLLM di server berbasis AMD GPU untuk inference "
                "LLM yang butuh throughput tinggi."
            )
        elif "vllm" in lower_message:
            content = (
                "vLLM cocok untuk melayani LLM dengan concurrency dan throughput yang "
                "tinggi. Pada deployment AMD Developer Cloud, backend ini bisa diarahkan "
                "ke endpoint OpenAI-compatible milik vLLM lewat VLLM_BASE_URL, "
                "VLLM_MODEL, dan VLLM_API_KEY tanpa menjalankan ROCm di Mac lokal."
            )
        elif "rekomendasi" in lower_message or "recommend" in lower_message or "which" in lower_message:
            content = (
                "Untuk rekomendasi produk AMD, titik awalnya adalah workload. Ryzen "
                "tepat untuk PC produktivitas, gaming, dan development harian. Radeon "
                "lebih relevan untuk grafis, gaming, dan sebagian workflow kreator. "
                "AMD Instinct lebih cocok untuk AI inference/training skala server, "
                "terutama saat dipasangkan dengan ROCm. Jika kamu beri budget, ukuran "
                "model, dan target deployment, rekomendasinya bisa dibuat lebih spesifik."
            )
        else:
            content = (
                "Saya bisa membantu menjelaskan produk dan teknologi AMD seperti Ryzen, "
                "Radeon, AMD Instinct, ROCm, vLLM, akselerasi GPU, dan perencanaan "
                "workload AI. Secara praktis, pilihannya biasanya dipetakan dari kebutuhan: "
                "CPU client untuk aplikasi umum, GPU Radeon untuk grafis dan workstation, "
                "atau AMD Instinct untuk inference/training AI di server."
            )
        return AIResult(content=content, model=self.settings.mock_model)

    async def _vllm_response(
        self,
        system_prompt: str,
        user_message: str,
        history: list[ChatMessage],
    ) -> AIResult:
        if not self.settings.vllm_base_url:
            raise AIProviderConfigError("VLLM_BASE_URL is required when AI_PROVIDER=vllm")
        if not self.settings.vllm_model:
            raise AIProviderConfigError("VLLM_MODEL is required when AI_PROVIDER=vllm")

        base_url = self.settings.vllm_base_url.rstrip("/")
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(
            {"role": message.role, "content": message.content}
            for message in history
            if message.role in {"user", "assistant"}
        )
        messages.append({"role": "user", "content": user_message})

        headers = {}
        if self.settings.vllm_api_key:
            headers["Authorization"] = f"Bearer {self.settings.vllm_api_key}"

        try:
            timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{base_url}/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": self.settings.vllm_model,
                        "messages": messages,
                        "temperature": 0.3,
                        "max_tokens": 800,
                    },
                )
                response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise AIProviderTimeoutError("Timed out while calling vLLM provider") from exc
        except httpx.HTTPStatusError as exc:
            raise AIProviderRequestError(
                f"vLLM provider returned HTTP {exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            raise AIProviderRequestError("Unable to reach vLLM provider") from exc

        payload = response.json()
        try:
            content = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AIProviderRequestError("vLLM provider returned an invalid response") from exc

        model = payload.get("model") or self.settings.vllm_model
        return AIResult(content=content, model=model, raw_response=payload)

    async def _groq_response(
        self,
        system_prompt: str,
        user_message: str,
        history: list[ChatMessage],
    ) -> AIResult:
        if not self.settings.groq_api_key:
            raise AIProviderConfigError(
                "GROQ_API_KEY is required when AI_PROVIDER=groq"
            )

        if not self.settings.groq_model:
            raise AIProviderConfigError(
                "GROQ_MODEL is required when AI_PROVIDER=groq"
            )

        messages = [{"role": "system", "content": system_prompt}]

        messages.extend(
            {"role": message.role, "content": message.content}
            for message in history
            if message.role in {"user", "assistant"}
        )

        messages.append(
            {"role": "user", "content": user_message}
        )

        headers = {
            "Authorization": f"Bearer {self.settings.groq_api_key}",
            "Content-Type": "application/json",
        }

        try:
            timeout = httpx.Timeout(
                connect=10.0,
                read=60.0,
                write=10.0,
                pool=10.0,
            )

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": self.settings.groq_model,
                        "messages": messages,
                        "temperature": 0.3,
                        "max_tokens": 800,
                    },
                )

                response.raise_for_status()

        except httpx.TimeoutException as exc:
            raise AIProviderTimeoutError(
                "Timed out while calling Groq provider"
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise AIProviderRequestError(
                f"Groq provider returned HTTP {exc.response.status_code}"
            ) from exc

        except httpx.HTTPError as exc:
            raise AIProviderRequestError(
                "Unable to reach Groq provider"
            ) from exc

        payload = response.json()

        try:
            content = payload["choices"][0]["message"]["content"]

        except (KeyError, IndexError, TypeError) as exc:
            raise AIProviderRequestError(
                "Groq provider returned an invalid response"
            ) from exc

        model = payload.get("model") or self.settings.groq_model

        return AIResult(
            content=content,
            model=model,
            raw_response=payload,
        )