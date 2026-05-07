# PRD — AMD Smart Product Assistant

**Nama Produk:** AMD Smart Product Assistant  
**Jenis Produk:** AI Product Assistant Chatbot  
**Target:** AMD Hackathon / AMD Developer Cloud Demo  
**Stack Utama:** FastAPI, vLLM + ROCm, Supabase PostgreSQL, AMD Developer Cloud  

---

## 1. Ringkasan Produk

**AMD Smart Product Assistant** adalah aplikasi chatbot berbasis AI yang membantu pengguna memahami produk AMD, rekomendasi perangkat, teknologi AMD, dan kebutuhan komputasi seperti gaming, AI coding, video editing, serta machine learning.

Aplikasi ini menggunakan **LLM inference** yang dijalankan di **AMD Developer Cloud** dengan dukungan **AMD GPU**. Tujuannya adalah menunjukkan bagaimana AMD GPU dapat digunakan untuk menjalankan workload AI seperti chatbot, Retrieval Augmented Generation, dan inference model secara cepat, efisien, dan scalable.

AMD ROCm menyediakan software stack terbuka untuk GPU-accelerated computing, termasuk dukungan untuk deep learning framework seperti PyTorch. AMD juga menyediakan dokumentasi untuk menjalankan LLM inference menggunakan vLLM pada AMD Instinct GPU seperti MI300X, MI325X, MI350X, dan MI355X.

---

## 2. Latar Belakang Masalah

Banyak pengguna kesulitan memahami produk teknologi karena informasi tersebar di banyak tempat, istilah teknis sulit dipahami, dan kebutuhan tiap pengguna berbeda.

Contoh masalah:

- Pengguna bingung memilih laptop/PC AMD untuk AI, gaming, coding, atau editing.
- Developer ingin tahu apakah AMD GPU cocok untuk menjalankan model AI.
- Pengguna awam sulit memahami istilah seperti ROCm, Ryzen AI, Radeon, Instinct, VRAM, NPU, dan GPU acceleration.
- Informasi produk sering berubah, sehingga chatbot perlu mengambil jawaban dari knowledge base yang dapat diperbarui.

Aplikasi ini dibuat untuk menjadi asisten AI interaktif yang menjawab pertanyaan dengan bahasa sederhana dan memberi rekomendasi berdasarkan kebutuhan pengguna.

---

## 3. Tujuan Produk

### 3.1 Tujuan Utama

Membangun chatbot AI yang dapat:

- Menjawab pertanyaan tentang produk dan teknologi AMD.
- Memberikan rekomendasi perangkat berdasarkan kebutuhan pengguna.
- Menjelaskan konsep teknis AMD dengan bahasa sederhana.
- Menggunakan AMD GPU di AMD Developer Cloud untuk menjalankan inference AI.
- Menampilkan demo nyata performa GPU AMD untuk AI chatbot.

### 3.2 Tujuan Hackathon

Menunjukkan bahwa AMD Developer Cloud dapat digunakan untuk:

- Menjalankan LLM inference.
- Menguji performa chatbot AI.
- Menggunakan ROCm, PyTorch, dan/atau vLLM.
- Membangun aplikasi AI yang real-world dan bisa dikembangkan menjadi produk komersial.

---

## 4. Target Pengguna

### 4.1 Primary User

#### Developer

- Ingin belajar AI di AMD GPU.
- Ingin tahu cara menjalankan model LLM di AMD Developer Cloud.

#### Pengguna Umum

- Ingin membeli laptop/PC AMD.
- Butuh rekomendasi berdasarkan kebutuhan.

#### Content Creator / Gamer

- Ingin tahu produk AMD yang cocok untuk editing, streaming, gaming, dan produktivitas.

#### Student / AI Enthusiast

- Ingin memahami teknologi AMD AI secara sederhana.

---

## 5. Persona Pengguna

### Persona 1 — Developer AI Pemula

| Field | Detail |
|---|---|
| Nama | Budi |
| Kebutuhan | Ingin menjalankan chatbot AI tetapi belum paham AMD GPU dan ROCm |
| Masalah | Bingung setup model AI dan memilih stack |
| Solusi | Chatbot menjelaskan langkah, teknologi, dan penggunaan AMD Developer Cloud |

### Persona 2 — Gamer

| Field | Detail |
|---|---|
| Nama | Raka |
| Kebutuhan | Ingin laptop AMD untuk gaming dan kerja ringan |
| Masalah | Tidak paham perbedaan Ryzen, Radeon, VRAM, dan GPU |
| Solusi | Chatbot memberi rekomendasi berdasarkan budget dan kebutuhan |

### Persona 3 — Content Creator

| Field | Detail |
|---|---|
| Nama | Sari |
| Kebutuhan | Laptop/PC untuk video editing, desain, dan AI tools |
| Masalah | Bingung memilih spesifikasi |
| Solusi | Chatbot memberi rekomendasi konfigurasi AMD yang sesuai |

---

## 6. Problem Statement

Pengguna membutuhkan asisten AI yang dapat memberikan informasi produk AMD dan teknologi AI secara cepat, jelas, dan personal. Saat ini informasi masih tersebar di website, dokumentasi, artikel, dan forum, sehingga pengguna perlu waktu lama untuk memahami pilihan terbaik.

---

## 7. Proposed Solution

Membangun aplikasi chatbot berbasis web/mobile bernama **AMD Smart Product Assistant**.

Aplikasi ini menggunakan:

- Frontend web/mobile untuk chat interface.
- Backend API untuk mengatur user session, prompt, dan retrieval.
- Vector database untuk knowledge base AMD.
- LLM inference server yang berjalan di AMD Developer Cloud.
- AMD GPU untuk mempercepat inference.
- ROCm, PyTorch, dan/atau vLLM sebagai stack AI.

vLLM adalah library untuk inference dan serving LLM yang cepat dan memory-efficient. Dokumentasi ROCm menjelaskan dukungan vLLM untuk AMD GPU/APU melalui Docker atau pip.

---

## 8. Core Features

### 8.1 AI Chatbot

Pengguna dapat bertanya dalam bahasa Indonesia atau Inggris.

Contoh pertanyaan:

- “Laptop AMD apa yang cocok untuk AI coding?”
- “Apa bedanya Ryzen AI dan Ryzen biasa?”
- “AMD GPU bisa dipakai untuk LLM?”
- “Apa itu ROCm?”
- “Saya punya budget 10 juta, laptop AMD apa yang cocok?”

### 8.2 Product Recommendation

Chatbot dapat memberikan rekomendasi berdasarkan:

- Budget
- Kebutuhan
- Jenis pekerjaan
- Preferensi performa
- Gaming/editing/coding/AI
- Desktop atau laptop

### 8.3 AMD Technology Explainer

Chatbot dapat menjelaskan istilah teknis:

- AMD Ryzen
- AMD Radeon
- AMD Instinct
- ROCm
- NPU
- GPU acceleration
- VRAM
- LLM inference
- Fine-tuning
- PyTorch
- vLLM

### 8.4 RAG Knowledge Base

Aplikasi menggunakan **Retrieval Augmented Generation** agar jawaban chatbot tidak hanya berasal dari model, tetapi juga dari dokumen/knowledge base.

Knowledge base dapat berisi:

- Dokumentasi AMD
- Produk AMD
- Artikel AMD
- FAQ
- Data benchmark sederhana
- Dokumentasi ROCm
- Catatan tim hackathon

### 8.5 Chat History

Pengguna dapat melihat riwayat percakapan.

Fitur:

- Simpan pertanyaan dan jawaban.
- Lanjutkan percakapan sebelumnya.
- Hapus history.

### 8.6 Feedback Jawaban

Pengguna dapat memberi feedback:

- Jawaban membantu.
- Jawaban kurang jelas.
- Jawaban salah.
- Butuh rekomendasi lebih detail.

Feedback ini dapat digunakan untuk evaluasi kualitas chatbot.

### 8.7 Admin Knowledge Management

Admin dapat:

- Upload dokumen knowledge base.
- Menambah FAQ.
- Mengedit data produk.
- Menghapus dokumen lama.
- Melihat pertanyaan populer.

---

## 9. AMD GPU Usage Plan

Pada AMD Developer Cloud, AMD GPU akan digunakan untuk:

### 9.1 LLM Inference

- Menjalankan model chatbot.
- Menghasilkan jawaban dari prompt pengguna.
- Menguji latency dan throughput.

### 9.2 Embedding Generation

- Mengubah dokumen knowledge base menjadi vector embedding.
- Digunakan untuk pencarian dokumen relevan.

### 9.3 Model Optimization

- Menguji performa model kecil vs model lebih besar.
- Menggunakan quantization jika dibutuhkan.
- Mengoptimalkan response time.

### 9.4 Benchmarking

- Mengukur waktu respons chatbot.
- Membandingkan performa model dengan konfigurasi berbeda.
- Mengukur jumlah request yang bisa diproses.

### 9.5 Optional Fine-tuning

Jika waktu hackathon cukup, model dapat di-fine-tune ringan menggunakan data FAQ AMD. Jika tidak, cukup menggunakan RAG agar lebih cepat dan aman.

ROCm menyediakan ekosistem untuk fine-tuning dan inference menggunakan AMD GPU, termasuk library GPU-accelerated dan framework seperti PyTorch, TensorFlow, dan JAX.

---

## 10. MVP Scope

### 10.1 MVP yang Wajib Selesai

- Landing page sederhana.
- Chat interface.
- Backend API.
- LLM inference via AMD Developer Cloud.
- RAG dari knowledge base sederhana.
- Rekomendasi produk berdasarkan kebutuhan.
- Demo performa AMD GPU.
- Logging pertanyaan dan jawaban.
- Basic admin untuk upload dokumen atau FAQ.

### 10.2 Tidak Wajib untuk MVP

- Login user lengkap.
- Payment.
- Mobile native app.
- Fine-tuning besar.
- Voice assistant.
- Multi-user enterprise dashboard.

---

## 11. User Flow

### Flow 1 — Bertanya ke Chatbot

1. User membuka aplikasi.
2. User mengetik pertanyaan.
3. Backend menerima pesan.
4. Sistem mencari dokumen relevan dari vector database.
5. Prompt dikirim ke LLM inference server di AMD Developer Cloud.
6. Model menghasilkan jawaban.
7. Jawaban ditampilkan ke user.
8. User dapat memberi feedback.

### Flow 2 — Rekomendasi Produk

1. User memilih kategori kebutuhan:
   - Gaming
   - AI coding
   - Editing video
   - Office
   - Student
2. User mengisi budget.
3. Chatbot bertanya kebutuhan tambahan.
4. Sistem memberikan rekomendasi spesifikasi AMD.
5. User menerima penjelasan sederhana.

### Flow 3 — Admin Update Knowledge Base

1. Admin login.
2. Admin upload dokumen/FAQ.
3. Sistem membuat embedding.
4. Dokumen masuk ke vector database.
5. Chatbot bisa menggunakan dokumen baru untuk menjawab.

---

## 12. Functional Requirements

### 12.1 Chat

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | User dapat mengirim pesan ke chatbot | High |
| FR-002 | Chatbot dapat membalas dalam bahasa Indonesia/Inggris | High |
| FR-003 | Chatbot dapat menjawab berdasarkan knowledge base | High |
| FR-004 | User dapat melihat loading state | High |
| FR-005 | User dapat memberi feedback jawaban | Medium |
| FR-006 | User dapat melihat chat history | Medium |

### 12.2 RAG

| ID | Requirement | Priority |
|---|---|---|
| FR-007 | Sistem dapat menyimpan dokumen knowledge base | High |
| FR-008 | Sistem dapat membuat embedding dari dokumen | High |
| FR-009 | Sistem dapat mencari dokumen relevan dari vector DB | High |
| FR-010 | Sistem dapat menyisipkan context ke prompt LLM | High |

### 12.3 Recommendation

| ID | Requirement | Priority |
|---|---|---|
| FR-011 | User dapat memilih kebutuhan penggunaan | High |
| FR-012 | User dapat memasukkan budget | High |
| FR-013 | Sistem memberikan rekomendasi spesifikasi AMD | High |
| FR-014 | Sistem menjelaskan alasan rekomendasi | High |

### 12.4 Admin

| ID | Requirement | Priority |
|---|---|---|
| FR-015 | Admin dapat upload dokumen | Medium |
| FR-016 | Admin dapat menambah FAQ | Medium |
| FR-017 | Admin dapat melihat daftar pertanyaan populer | Low |
| FR-018 | Admin dapat menghapus dokumen knowledge base | Low |

---

## 13. Non-Functional Requirements

### 13.1 Performance

- Response chatbot target: maksimal 3–8 detik untuk MVP.
- Sistem harus mendukung minimal 10 request bersamaan saat demo.
- Inference harus dijalankan melalui AMD GPU.

### 13.2 Scalability

- Backend harus bisa dipisah dari inference server.
- Vector database dapat diganti sesuai kebutuhan.
- Model AI dapat diganti tanpa mengubah frontend.

### 13.3 Security

- API key disimpan di environment variable.
- Admin panel harus menggunakan login.
- Input user harus divalidasi.
- Rate limit untuk mencegah spam request.

### 13.4 Reliability

- Jika inference server gagal, sistem menampilkan error yang jelas.
- Log request disimpan untuk debugging.
- Sistem memiliki fallback response.

### 13.5 Usability

- UI sederhana.
- Jawaban mudah dipahami.
- Cocok untuk user awam dan developer.

---

## 14. Tech Stack Recommendation

### 14.1 Frontend

Pilihan:

- Next.js
- React
- Tailwind CSS

Alasan:

- Cepat dibuat.
- Cocok untuk demo hackathon.
- UI chat mudah dikembangkan.

### 14.2 Backend

Pilihan:

- Node.js + NestJS
- Express.js
- FastAPI

Rekomendasi utama:

- **FastAPI** jika fokus AI.
- **NestJS** jika ingin backend enterprise-style.

### 14.3 AI Inference

Pilihan:

- vLLM
- Hugging Face Transformers
- PyTorch
- Text Generation Inference

Rekomendasi:

- **vLLM + ROCm** untuk LLM serving di AMD GPU.

ROCm documentation menyebut ROCm-enabled vLLM Docker image sebagai environment untuk LLM inference pada AMD Instinct data center GPU, dan image tersebut mengintegrasikan ROCm, PyTorch, serta vLLM.

### 14.4 Database

- PostgreSQL untuk user, chat history, feedback.
- Redis untuk cache.
- Qdrant/Chroma/FAISS untuk vector database.

### 14.5 Deployment

- Frontend: Vercel / Netlify / server sendiri.
- Backend: Docker container.
- AI inference: AMD Developer Cloud.
- Database: Supabase / PostgreSQL server.

---

## 15. System Architecture

```text
User
 |
 | Chat message
 v
Frontend Web App
 |
 | REST API / WebSocket
 v
Backend API
 |
 | Search relevant context
 v
Vector Database
 |
 | Context + User Question
 v
LLM Inference Server on AMD Developer Cloud
 |
 | Response
 v
Backend API
 |
 v
Frontend Web App
 |
 v
User
```

---

## 16. AI Pipeline

### Step 1 — User Input

User bertanya:

```text
Saya ingin laptop AMD untuk AI coding dan video editing, budget 12 juta. Apa rekomendasinya?
```

### Step 2 — Query Understanding

Sistem membaca intent:

- Kebutuhan: AI coding + video editing
- Budget: 12 juta
- Produk: laptop AMD

### Step 3 — Retrieval

Sistem mencari dokumen relevan:

- Ryzen AI
- Radeon GPU
- RAM recommendation
- Laptop AI coding
- Video editing specs

### Step 4 — Prompt Construction

Prompt ke LLM:

```text
You are AMD Smart Product Assistant.
Answer in Indonesian.
Use the provided context.
Give practical recommendation.
Explain simply.
```

### Step 5 — LLM Inference

Model berjalan di AMD Developer Cloud menggunakan AMD GPU.

### Step 6 — Response

Chatbot menjawab dengan:

- Rekomendasi spesifikasi
- Alasan teknis
- Saran minimum RAM/VRAM
- Alternatif jika budget terbatas

---

## 17. Data Model

### 17.1 users

| Field | Type |
|---|---|
| id | UUID |
| name | string |
| email | string |
| created_at | timestamp |
| updated_at | timestamp |

### 17.2 chat_sessions

| Field | Type |
|---|---|
| id | UUID |
| user_id | UUID |
| title | string |
| created_at | timestamp |
| updated_at | timestamp |

### 17.3 chat_messages

| Field | Type |
|---|---|
| id | UUID |
| session_id | UUID |
| role | string |
| content | text |
| latency_ms | integer |
| model_name | string |
| created_at | timestamp |

### 17.4 knowledge_documents

| Field | Type |
|---|---|
| id | UUID |
| title | string |
| source | string |
| content | text |
| embedding_status | string |
| created_at | timestamp |
| updated_at | timestamp |

### 17.5 feedback

| Field | Type |
|---|---|
| id | UUID |
| message_id | UUID |
| rating | string |
| comment | text |
| created_at | timestamp |

---

## 18. API Endpoints

### 18.1 Chat API

```http
POST /api/chat
```

Request:

```json
{
  "sessionId": "string",
  "message": "Saya ingin laptop AMD untuk AI coding"
}
```

Response:

```json
{
  "answer": "Untuk AI coding, saya sarankan...",
  "sources": [],
  "latencyMs": 3200
}
```

### 18.2 Upload Knowledge Base

```http
POST /api/admin/knowledge/upload
```

### 18.3 Get Chat History

```http
GET /api/chat/sessions/:id/messages
```

### 18.4 Submit Feedback

```http
POST /api/feedback
```

---

## 19. Prompt Design

### 19.1 System Prompt

```text
You are AMD Smart Product Assistant.

Your job is to help users understand AMD products, AMD technologies, AI workloads, GPU acceleration, and product recommendations.

Rules:
1. Answer clearly and simply.
2. Use Indonesian if the user asks in Indonesian.
3. Use English if the user asks in English.
4. If the user asks for product recommendation, ask or infer:
   - budget
   - use case
   - performance need
   - portability need
5. Do not invent product availability.
6. If unsure, say that the information needs to be verified.
7. Explain technical terms in simple language.
```

### 19.2 Recommendation Prompt

```text
User need:
- Budget:
- Use case:
- Device type:
- Performance priority:

Give recommendation:
1. Recommended AMD CPU/GPU class
2. Minimum RAM
3. Storage
4. Why this setup is suitable
5. Alternative lower-budget option
```

---

## 20. Demo Scenario untuk Hackathon

### Demo 1 — Explain AMD GPU for AI

User bertanya:

```text
How can AMD GPUs be used for AI chatbot inference?
```

Chatbot menjawab:

- AMD GPU dapat menjalankan LLM inference.
- ROCm mendukung framework AI.
- vLLM dapat digunakan untuk serving model.
- AMD Developer Cloud digunakan sebagai compute infrastructure.

### Demo 2 — Product Recommendation

User bertanya:

```text
Saya ingin laptop AMD untuk AI coding, video editing, dan gaming ringan. Budget 12 juta.
```

Chatbot memberikan:

- Rekomendasi Ryzen AI / Ryzen 7 class.
- RAM minimal 16GB, ideal 32GB.
- Storage SSD 512GB/1TB.
- GPU integrated/discrete sesuai budget.
- Penjelasan mudah.

### Demo 3 — RAG Knowledge

User bertanya:

```text
Apa itu ROCm?
```

Chatbot menjawab berdasarkan dokumen knowledge base.

### Demo 4 — Performance Dashboard

Tampilkan:

- Model yang digunakan.
- Latency.
- Token output.
- GPU usage.
- Jumlah request.
- Average response time.

---

## 21. Success Metrics

### 21.1 Technical Metrics

- Chatbot berhasil menjawab minimal 90% pertanyaan demo.
- Response time rata-rata di bawah 8 detik.
- RAG berhasil mengambil dokumen relevan.
- Inference berjalan di AMD Developer Cloud.
- Sistem stabil selama demo.

### 21.2 User Metrics

- User memahami jawaban chatbot.
- Rekomendasi terasa relevan.
- Jawaban tidak terlalu teknis.
- User dapat menggunakan aplikasi tanpa instruksi panjang.

### 21.3 Hackathon Metrics

- Demo berjalan lancar.
- Pemanfaatan AMD GPU jelas.
- Ada use case nyata.
- Ada potensi pengembangan produk.

---

## 22. MVP Timeline

| Day | Fokus | Detail |
|---|---|---|
| Day 1 | Setup awal | Finalisasi ide dan PRD, setup repo, frontend, backend, dan knowledge base awal |
| Day 2 | AMD Developer Cloud | Setup AMD Developer Cloud, jalankan model inference, integrasi backend ke inference server, buat endpoint chat |
| Day 3 | RAG | Implementasi RAG, setup vector database, upload dokumen AMD/FAQ, testing jawaban |
| Day 4 | UI dan evaluasi | Rapikan UI, tambahkan feedback, tambahkan dashboard sederhana, testing end-to-end |
| Day 5 | Finalisasi | Siapkan pitch deck, demo script, rekam video demo, final bug fixing |

---

## 23. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Setup AMD GPU sulit | Demo terlambat | Gunakan Docker image ROCm/vLLM |
| Model terlalu besar | Response lambat | Gunakan model kecil/quantized |
| RAG tidak akurat | Jawaban salah | Batasi knowledge base dan buat prompt ketat |
| Waktu hackathon singkat | Fitur tidak selesai | Fokus MVP chat + RAG + demo GPU |
| Cloud quota terbatas | Inference terganggu | Siapkan fallback API/model kecil |

---

## 24. Batasan Produk

Untuk versi MVP:

- Aplikasi belum menjadi marketplace produk.
- Data harga produk belum real-time.
- Tidak melakukan transaksi pembelian.
- Tidak menggantikan dokumentasi resmi AMD.
- Rekomendasi bersifat edukatif dan perlu verifikasi ketersediaan produk.

---

## 25. Future Improvements

Setelah MVP, aplikasi dapat dikembangkan menjadi:

- Voice chatbot.
- WhatsApp chatbot.
- Product comparison tool.
- Benchmark recommendation engine.
- AI PC buying assistant.
- Local AI setup assistant untuk AMD Ryzen/Radeon.
- Fine-tuned AMD knowledge model.
- Dashboard analytics untuk pertanyaan pengguna.
- Integrasi real-time product catalog.
- Multi-language support.

---

## 26. Pitch Singkat

AMD Smart Product Assistant is an AI-powered chatbot that helps users understand AMD products, technologies, and AI workloads through simple and personalized conversations. The application uses AMD GPUs on AMD Developer Cloud to run LLM inference, retrieve relevant AMD knowledge, and generate fast, practical answers for developers, gamers, creators, and general users.

---

## 27. Jawaban untuk Form Hackathon

### Field

```text
How do you plan to use your AMD GPUs on the AMD Developer Cloud?
```

### English Version

I plan to use AMD GPUs on the AMD Developer Cloud to run LLM inference for an AI-powered chatbot called AMD Smart Product Assistant. The application will help users understand AMD products, AMD technologies, and AI workloads through interactive conversations.

The AMD GPU resources will be used to serve an open-source language model, generate responses, process embeddings for retrieval augmented generation, and benchmark chatbot performance such as latency and throughput. I also plan to explore ROCm, PyTorch, and vLLM to optimize AI inference on AMD GPUs.

The goal is to demonstrate a real-world AI application that uses AMD Developer Cloud as the compute infrastructure for scalable and efficient chatbot inference.

### Versi Bahasa Indonesia

Saya berencana menggunakan AMD GPU di AMD Developer Cloud untuk menjalankan LLM inference pada aplikasi chatbot AI bernama AMD Smart Product Assistant. Aplikasi ini akan membantu pengguna memahami produk AMD, teknologi AMD, dan penggunaan AMD GPU untuk kebutuhan AI melalui percakapan interaktif.

Resource AMD GPU akan digunakan untuk menjalankan open-source language model, menghasilkan jawaban chatbot, memproses embedding untuk retrieval augmented generation, serta melakukan benchmark performa seperti latency dan throughput. Saya juga akan mengeksplorasi ROCm, PyTorch, dan vLLM untuk mengoptimalkan inference AI di AMD GPU.

Tujuan saya adalah mendemonstrasikan aplikasi AI nyata yang menggunakan AMD Developer Cloud sebagai infrastruktur komputasi untuk chatbot yang scalable dan efisien.

---

## 28. Catatan Implementasi Backend

Bagian backend yang dikerjakan:

- FastAPI backend.
- Supabase PostgreSQL database.
- Chat API.
- Knowledge base API.
- Feedback API.
- RAG service.
- AI interface service.
- Mock AI provider untuk lokal.
- vLLM provider untuk AMD Developer Cloud.

Mode lokal:

```env
AI_PROVIDER=mock
```

Mode AMD Developer Cloud:

```env
AI_PROVIDER=vllm
VLLM_BASE_URL=https://your-amd-cloud-vllm-url
VLLM_MODEL=your-model-name
```

---

## 29. Kesimpulan

AMD Smart Product Assistant adalah aplikasi AI chatbot yang relevan untuk hackathon karena:

- Menggunakan AMD Developer Cloud secara langsung.
- Menunjukkan pemanfaatan AMD GPU untuk LLM inference.
- Memakai use case nyata: product assistant dan recommendation chatbot.
- Dapat dikembangkan menjadi produk komersial.
- MVP dapat dibangun cepat dengan FastAPI, Supabase PostgreSQL, RAG, dan vLLM + ROCm.
