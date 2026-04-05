import json
from config import query_groq
from utils.json_utils import extract_json_array


def task_scheduler_node(state):
    """
    NODE: Task Scheduler Agent

    Fungsi ini bertugas untuk:
    - Menyusun jadwal pengerjaan tugas (timeline proyek)
    - Memperhatikan dependency antar tugas
    - Mengoptimalkan durasi proyek (parallel task jika memungkinkan)
    - Memanfaatkan insight sebelumnya untuk perbaikan jadwal
    """

    # =========================
    # 1. Ambil data dari state
    # =========================

    # Daftar task hasil dari task_generation_agent
    tasks = state.get("tasks", [])

    # Dependency antar task hasil dari task_dependency_agent
    dependencies = state.get("dependencies", [])

    # Insight / pembelajaran dari iterasi sebelumnya
    insights = state.get("insights", [])

    # =========================
    # 2. Susun prompt ke LLM
    # =========================

    # Prompt ini akan dikirim ke Groq (LLM)
    # Tujuannya: meminta AI membuat jadwal proyek yang optimal
    prompt = f"""
Kamu adalah seorang project scheduler profesional yang bertugas menyusun timeline proyek secara optimal.

Data yang tersedia:

DAFTAR TASK:
{json.dumps(tasks, indent=2)}

DEPENDENCY TASK:
{json.dumps(dependencies, indent=2)}

INSIGHT SEBELUMNYA:
{insights}

TUGAS KAMU:
1. Buat jadwal pengerjaan task dengan ketentuan:
   - Setiap task memiliki "start_day" dan "end_day"
   - Dependency antar task WAJIB dipatuhi
   - Maksimalkan pengerjaan paralel jika memungkinkan
   - Durasi total proyek tidak boleh lebih lama dari iterasi sebelumnya
   - Gunakan insight sebelumnya untuk menghindari inefisiensi jadwal

2. Output HARUS berupa JSON ARRAY dengan format:
   - "name"        : nama task
   - "start_day"  : hari mulai (integer)
   - "end_day"    : hari selesai (integer)

PENTING:
- Output HANYA JSON
- Tidak boleh ada penjelasan, teks tambahan, atau markdown

CONTOH OUTPUT:
[
  {{ "name": "Task A", "start_day": 1, "end_day": 3 }},
  {{ "name": "Task B", "start_day": 2, "end_day": 4 }}
]

Mulai output di bawah ini:
"""

    # =========================
    # 3. Kirim prompt ke LLM
    # =========================

    # Memanggil Groq API via query_groq
    response = query_groq(prompt)

    # =========================
    # 4. Parsing JSON hasil LLM
    # =========================

    # Ekstrak JSON array dari response LLM
    schedule = extract_json_array(response)

    # Jika parsing gagal, fallback ke list kosong
    if schedule is None:
        schedule = []

    # =========================
    # 5. Return hasil ke pipeline
    # =========================

    # response : teks mentah dari LLM (untuk debugging/log)
    # schedule : hasil jadwal yang sudah terstruktur
    return {
        "response": response,
        "schedule": schedule
    }
