import streamlit as st
from config import query_groq


def insight_generation_node(state):
    """
    NODE: Insight Generation Agent

    Agent ini berfungsi sebagai tahap akhir pipeline.
    Tugasnya:
    - Menggabungkan hasil jadwal, alokasi, dan risiko
    - Menghasilkan insight & rekomendasi strategis
    - Memberikan masukan untuk iterasi proyek berikutnya
    """

    # =========================
    # 1. Ambil data dari state
    # =========================

    # Jadwal task hasil task_scheduler_agent
    schedule = state.get("schedule", [])

    # Hasil alokasi task ke anggota tim
    allocations = state.get("task_allocations", [])

    # Risiko proyek (hasil risk_assessment_agent)
    risks = state.get("risks", [])

    # =========================
    # 2. Susun prompt insight proyek
    # =========================

    prompt = f"""
Kamu adalah seorang Project Manager senior
yang bertugas memberikan insight dan rekomendasi
untuk meningkatkan kualitas rencana proyek.

DATA PROYEK:

- ALOKASI TASK:
{allocations}

- JADWAL PROYEK:
{schedule}

- ANALISIS RISIKO:
{risks}


TUJUAN UTAMA:

1. INSIGHT KRITIS:
   - Identifikasi bottleneck (hambatan proses)
   - Deteksi konflik sumber daya
   - Soroti task dengan risiko tinggi
   - Analisis pemanfaatan anggota tim

2. REKOMENDASI PERBAIKAN:
   - Saran penyesuaian alokasi task
   - Saran optimasi jadwal
   - Strategi mengurangi risiko proyek
   - Rekomendasi untuk iterasi berikutnya

PERSYARATAN OUTPUT:
- Fokus pada solusi yang bisa langsung diterapkan
- Tujuan utama adalah menurunkan risiko proyek
- Output HARUS berupa TEKS BIASA
- TANPA JSON
- TANPA markdown
- TANPA bullet list

Berikan insight singkat, jelas, dan actionable.

Mulai output di bawah ini:
"""

    # =========================
    # 3. Kirim prompt ke LLM
    # =========================

    insights = query_groq(prompt)

    # =========================
    # 4. Kembalikan hasil insight
    # =========================

    # Insight digunakan:
    # - Ditampilkan di UI
    # - Disimpan ke Airtable
    # - Menjadi pembelajaran iterasi berikutnya
    return insights
