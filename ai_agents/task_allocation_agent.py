import json
from config import query_groq
from utils.json_utils import extract_json_array


def task_allocation_node(state):
    """
    NODE: Task Allocation Agent

    Fungsi ini bertanggung jawab untuk:
    - Mengalokasikan task ke anggota tim
    - Mencocokkan task dengan skill yang dimiliki
    - Memastikan tidak ada konflik jadwal
    - Menjaga beban kerja tetap seimbang
    """

    # =========================
    # 1. Ambil data dari state
    # =========================

    # Daftar task hasil task_generation_agent
    tasks = state.get("tasks", [])

    # Data anggota tim & skill
    team = state.get("team", [])

    # Jadwal task hasil task_scheduler_agent
    schedule = state.get("schedule", [])

    # Insight dari iterasi sebelumnya (jika ada)
    insights = state.get("insights", [])

    # =========================
    # 2. Susun prompt ke LLM
    # =========================

    # Prompt meminta AI bertindak sebagai project manager
    # yang mengalokasikan task ke anggota tim secara optimal
    prompt = f"""
Kamu adalah seorang Project Manager profesional yang bertugas
mengalokasikan task kepada anggota tim secara efisien dan adil.

DATA YANG TERSEDIA:

DAFTAR TASK:
{json.dumps(tasks, indent=2)}

JADWAL TASK:
{json.dumps(schedule, indent=2)}

ANGGOTA TIM DAN SKILL:
{json.dumps(team, indent=2)}

INSIGHT SEBELUMNYA:
{insights}


TUJUAN:
1. Alokasikan setiap task ke satu atau lebih anggota tim.
2. Pastikan:
   - Skill anggota sesuai dengan task
   - Tidak ada anggota yang mengerjakan dua task di waktu yang sama
   - Setiap anggota hanya mengerjakan SATU task dalam satu periode waktu
3. Optimalkan pembagian kerja:
   - Beban kerja seimbang
   - Gunakan insight sebelumnya untuk perbaikan alokasi

BATASAN:
- Satu anggota = satu task dalam satu waktu
- Skill HARUS relevan dengan task

FORMAT OUTPUT (JSON ARRAY):
- "task": nama task
- "assigned_to": daftar nama anggota tim

ATURAN PENTING:
- Output HARUS JSON VALID
- TANPA penjelasan tambahan
- TANPA markdown atau teks lain

CONTOH OUTPUT:
[
  {{"task": "Pengembangan Backend", "assigned_to": ["Budi"]}},
  {{"task": "Desain UI", "assigned_to": ["Siti"]}}
]

Mulai output di bawah ini:
"""

    # =========================
    # 3. Kirim prompt ke LLM
    # =========================

    response = query_groq(prompt)

    # =========================
    # 4. Parsing hasil alokasi
    # =========================

    # Ekstrak JSON array dari response LLM
    allocations = extract_json_array(response)

    # Jika parsing gagal, gunakan list kosong
    # agar pipeline tetap berjalan
    if allocations is None:
        allocations = []

    # =========================
    # 5. Return hasil ke pipeline
    # =========================

    # Data ini akan digunakan oleh:
    # - airtable_service
    # - csv_service
    # - risk_assessment_agent
    return {
        "response": response,
        "task_allocations": allocations
    }
