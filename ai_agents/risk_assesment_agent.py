from config import query_groq
import json


def risk_assessment_node(state):
    """
    NODE: Risk Assessment Agent

    Fungsi ini bertugas untuk:
    - Menganalisis risiko dari rencana proyek saat ini
    - Menilai risiko berdasarkan alokasi task & jadwal
    - Memberikan gambaran risiko proyek secara keseluruhan
    """

    # =========================
    # 1. Ambil data dari state
    # =========================

    # Jadwal task hasil task_scheduler_agent
    schedule = state.get("schedule", [])

    # Hasil alokasi task ke anggota tim
    allocations = state.get("task_allocations", [])

    # =========================
    # 2. Susun prompt analisis risiko
    # =========================

    # Prompt meminta AI berperan sebagai analis risiko proyek
    # Output sengaja berupa teks biasa (plain text)
    prompt = f"""
Kamu adalah seorang analis risiko proyek berpengalaman
yang bertugas mengevaluasi risiko dari rencana proyek berikut.

DATA PROYEK:

ALOKASI TASK:
{allocations}

JADWAL TASK:
{schedule}


TUJUAN ANALISIS:

1. PENILAIAN RISIKO:
   - Analisis setiap task berdasarkan:
     • Kompleksitas task
     • Anggota tim yang ditugaskan
     • Jadwal pengerjaan
   - Identifikasi potensi risiko akibat:
     • Jadwal terlalu padat
     • Task berurutan tanpa jeda
     • Beban kerja berlebih
     • Ketergantungan task

2. SKOR RISIKO:
   - Berikan skor risiko dari 0 (tanpa risiko) sampai 10 (risiko tinggi)
   - Jika task dan penugasan sama seperti sebelumnya, pertahankan skor
   - Kurangi risiko jika:
     • Ada jeda waktu antar task
     • Task ditangani anggota yang lebih berpengalaman

3. RISIKO PROYEK KESELURUHAN:
   - Hitung total skor risiko proyek dari seluruh task

ATURAN OUTPUT:
- Output HARUS berupa TEKS BIASA
- TANPA JSON
- TANPA bullet list
- TANPA markdown

Mulai output di bawah ini:
"""

    # =========================
    # 3. Kirim prompt ke LLM
    # =========================

    response = query_groq(prompt)

    # =========================
    # 4. Return hasil analisis
    # =========================

    # Risiko tidak diparsing karena:
    # - Digunakan sebagai insight naratif
    # - Akan diproses oleh insight_generation_agent
    return {
        "response": response,          # Teks analisis risiko dari AI
        "risks": [],                   # Placeholder (tidak digunakan saat ini)
        "project_risk_score": None,    # Placeholder (opsional dikembangkan)
    }
