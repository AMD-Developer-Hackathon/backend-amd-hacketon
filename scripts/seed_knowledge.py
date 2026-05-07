import requests
import json
import logging
import os
from app.config import get_settings

logging.basicConfig(level=logging.INFO)

settings = get_settings()
API_URL = "http://localhost:8000/api/admin/knowledge/upload"
HEADERS = {"Content-Type": "application/json"}
if settings.admin_api_key:
    HEADERS["x-admin-key"] = settings.admin_api_key

knowledge_docs = [
    {
        "title": "Apa itu ROCm?",
        "source": "AMD Documentation",
        "content": "ROCm (Radeon Open Compute) adalah platform software open-source dari AMD untuk komputasi GPU dan workload AI/HPC. ROCm mendukung framework populer seperti PyTorch, TensorFlow, dan JAX, memungkinkan developer untuk menjalankan model machine learning dan LLM pada AMD Instinct dan Radeon GPUs."
    },
    {
        "title": "AMD Instinct MI300X Overview",
        "source": "AMD Product Page",
        "content": "AMD Instinct MI300X adalah akselerator AI generasi terbaru dari AMD yang dirancang khusus untuk Generative AI dan LLM. Dilengkapi dengan 192GB HBM3 memory dan memory bandwidth 5.3 TB/s, MI300X menawarkan kapasitas memori tertinggi di kelasnya untuk menjalankan model besar seperti Falcon-180B atau Llama 2 70B pada satu GPU."
    },
    {
        "title": "vLLM di AMD GPU",
        "source": "vLLM Documentation",
        "content": "vLLM adalah engine untuk melayani (serving) Large Language Models dengan throughput tinggi dan latensi rendah. vLLM kini mendukung penuh AMD GPUs menggunakan ROCm. Cara termudah untuk menjalankannya adalah menggunakan official ROCm-vLLM Docker image yang sudah menyertakan PyTorch dan ROCm stack lengkap."
    },
    {
        "title": "AMD Ryzen AI Series",
        "source": "AMD Ryzen AI",
        "content": "AMD Ryzen AI adalah prosesor pertama di dunia dengan dedicated Neural Processing Unit (NPU) bawaan untuk x86 Windows laptop. NPU ini dirancang khusus untuk menangani tugas-tugas AI (seperti background blur, noise cancellation, AI copilot) secara efisien tanpa membebani CPU atau GPU utama, sehingga menghemat baterai."
    },
    {
        "title": "Perbandingan Ryzen 5 vs 7 vs 9",
        "source": "AMD Processor Guide",
        "content": "Ryzen 5: Cocok untuk gaming mainstream, produktivitas harian, dan pekerjaan kantor (6 cores). Ryzen 7: Sweet spot untuk gaming high-end, streaming, dan content creation ringan (8 cores). Ryzen 9: Untuk enthusiast, profesional video editor, 3D rendering, dan developer berat (12-16 cores)."
    },
    {
        "title": "AMD Radeon RX 7000 Series",
        "source": "AMD Radeon Series",
        "content": "Radeon RX 7000 series menggunakan arsitektur RDNA 3 berbasis chiplet. Menawarkan performa gaming 1440p hingga 4K, ray tracing hardware, dan fitur AI acceleration untuk fidelityFX Super Resolution (FSR). Contoh produk: RX 7900 XTX (flagship), RX 7800 XT (high-end 1440p), RX 7600 (1080p gaming)."
    },
    {
        "title": "Rekomendasi Laptop AMD untuk Gaming",
        "source": "Buying Guide",
        "content": "Untuk gaming, cari laptop dengan prosesor Ryzen 7 (H-series) dan GPU Radeon RX 7000M/S series (atau RTX equivalent). RAM minimal 16GB, idealnya 32GB jika sering main game AAA sambil streaming. Pastikan layar memiliki refresh rate tinggi (144Hz+) dan sistem pendingin yang memadai."
    },
    {
        "title": "Rekomendasi Laptop AMD untuk AI & Coding",
        "source": "Developer Guide",
        "content": "Untuk AI coding dan development lokal, sangat disarankan menggunakan laptop dengan prosesor AMD Ryzen AI (Ryzen 7040 atau 8040 series) yang memiliki NPU. RAM minimal 32GB sangat direkomendasikan jika ingin bereksperimen dengan model AI lokal. Storage SSD NVMe minimal 1TB."
    },
    {
        "title": "Rekomendasi Laptop AMD untuk Video Editing",
        "source": "Creator Guide",
        "content": "Video editing (terutama 4K) membutuhkan CPU multicore kuat, VRAM besar, dan RAM lega. Rekomendasi: Prosesor Ryzen 9 (HX series), GPU Radeon RX 7600M XT atau lebih tinggi, RAM minimal 32GB (ideal 64GB), dan layar dengan color gamut tinggi (100% sRGB / DCI-P3)."
    },
    {
        "title": "PyTorch + ROCm Setup Guide",
        "source": "AMD Developer Docs",
        "content": "Untuk menggunakan PyTorch dengan ROCm, instal menggunakan pip command resmi dari pytorch.org. Contoh: `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7`. Verifikasi dengan `import torch; torch.cuda.is_available()` (akan return True jika ROCm terdeteksi)."
    },
    {
        "title": "AMD Developer Cloud - Getting Started",
        "source": "AMD Cloud",
        "content": "AMD Developer Cloud menyediakan akses cloud untuk mencoba hardware terbaru AMD seperti Instinct MI210/MI250/MI300 dan EPYC processors. Cocok untuk menguji porting CUDA ke HIP, mengevaluasi ROCm, atau menjalankan LLM inference tanpa perlu investasi hardware mahal di awal."
    },
    {
        "title": "Apa itu VRAM dan berapa yang dibutuhkan?",
        "source": "Hardware Explainer",
        "content": "VRAM (Video RAM) adalah memori pada kartu grafis untuk menyimpan tekstur, frame buffer, dan data model AI. Untuk gaming 1080p, 8GB cukup. Untuk 1440p, 12GB disarankan. Untuk 4K atau menjalankan model AI/LLM secara lokal, 16GB atau 24GB (seperti pada Radeon RX 7900 XTX) sangat direkomendasikan."
    },
    {
        "title": "AMD vs NVIDIA untuk LLM Inference",
        "source": "Tech Comparison",
        "content": "NVIDIA mendominasi dengan CUDA ecosystem. Namun, AMD Instinct (MI300X) dengan ROCm menawarkan kapasitas VRAM jauh lebih besar dengan harga yang lebih kompetitif. Untuk LLM (yang sangat memory-bound), VRAM besar MI300X memungkinkan running model lebih besar pada single GPU tanpa perlu multi-GPU communication overhead."
    },
    {
        "title": "GPU Acceleration untuk AI Workloads",
        "source": "AI Concepts",
        "content": "AI workloads sangat diuntungkan oleh GPU karena GPU memiliki ribuan core kecil yang didesain untuk komputasi paralel (matrix multiplication). Ini berbeda dengan CPU yang memiliki core sedikit tapi cepat untuk proses sekuensial. ROCm adalah software layer yang menghubungkan framework AI dengan hardware paralel GPU AMD."
    },
    {
        "title": "Rekomendasi Desktop AMD untuk AI/ML",
        "source": "Workstation Build",
        "content": "Untuk workstation AI/ML, build ideal: CPU Ryzen Threadripper PRO atau Ryzen 9 (misal 7950X), RAM 64GB-128GB, dan GPU dengan VRAM besar seperti Radeon PRO W7900 (48GB VRAM) atau RX 7900 XTX (24GB VRAM). Pastikan PSU minimal 1000W."
    }
]

def seed_database():
    success_count = 0
    for doc in knowledge_docs:
        try:
            response = requests.post(API_URL, json=doc, headers=HEADERS)
            response.raise_for_status()
            logging.info(f"Successfully added: {doc['title']}")
            success_count += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to add {doc['title']}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response: {e.response.text}")
    
    logging.info(f"Seeding complete. {success_count}/{len(knowledge_docs)} documents added.")

if __name__ == "__main__":
    seed_database()
