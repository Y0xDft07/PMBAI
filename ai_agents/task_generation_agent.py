import json
import streamlit as st
from config import query_groq
from utils.json_utils import extract_json_array


def task_generation_node(state):
    """
    NODE: Task Generation Agent

    Fungsi ini bertugas untuk:
    - Menganalisis deskripsi proyek
    - Menghasilkan daftar task yang realistis & actionable
    - Mengestimasi durasi tiap task
    - Memecah task besar (>5 hari) menjadi sub-task yang lebih kecil
    """

    # =========================
    # 1. Ambil deskripsi proyek
    # =========================

    # Deskripsi proyek berasal dari input user / node sebelumnya
    description = state.get("project_description", "")

    # =========================
    # 2. Susun prompt ke LLM
    # =========================

    # Prompt ini meminta AI berperan sebagai project manager profesional
    # untuk mengekstrak task dari deskripsi proyek
    prompt = f"""
Kamu adalah seorang project manager profesional yang sedang menganalisis deskripsi proyek berikut:

{description}

TUGAS KAMU:
1. Identifikasi task yang:
   - Realistis
   - Bisa langsung dikerjakan (actionable)
   - Diperlukan untuk menyelesaikan proyek

2. Tentukan estimasi durasi pengerjaan setiap task (dalam hari)

3. Jika ada task dengan durasi lebih dari 5 hari:
   - Pecah menjadi sub-task yang lebih kecil
   - Pastikan sub-task saling independen

ATURAN OUTPUT:
- Output HARUS berupa JSON VALID
- TIDAK boleh ada teks tambahan, penjelasan, atau komentar
- HANYA JSON

FORMAT OUTPUT (JSON ARRAY):
- "name"           : nama task
- "duration_days" : estimasi durasi (integer)

CONTOH OUTPUT:
[
  {{ "name": "Analisis Kebutuhan Sistem", "duration_days": 3 }},
  {{ "name": "Desain Arsitektur Backend", "duration_days": 4 }}
]

Jika tidak ada task, outputkan array kosong: []

Mulai output di bawah ini:
"""

    # =========================
    # 3. Kirim prompt ke LLM
    # =========================

    # Memanggil Groq API dengan prompt yang sudah disusun
    response = query_groq(prompt)

    # =========================
    # 4. Tampilkan output mentah (debug/UI)
    # =========================

    # Menampilkan response LLM dalam format JSON di Streamlit
    st.code(response, language='json')

    # =========================
    # 5. Parsing JSON dari LLM
    # =========================

    # Mengambil JSON array dari response
    tasks = extract_json_array(response)

    # Jika parsing gagal, gunakan list kosong
    if tasks is None:
        tasks = []

    # =========================
    # 6. Return hasil ke pipeline
    # =========================

    # Output akan dipakai oleh:
    # - task_dependency_agent
    # - task_scheduler_agent
    return {"tasks": tasks}
