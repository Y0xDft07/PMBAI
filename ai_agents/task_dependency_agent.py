import json
from config import query_groq
from utils.json_utils import extract_json_array


def task_dependency_node(tasks):
    """
    NODE: Task Dependency Agent

    Fungsi ini bertugas untuk:
    - Menganalisis hubungan ketergantungan antar task
    - Menentukan task mana yang harus dikerjakan terlebih dahulu
    - Menghasilkan struktur dependency dalam bentuk JSON
    """

    # =========================
    # 1. Susun prompt ke LLM
    # =========================

    # Prompt meminta AI berperan sebagai analis proyek
    # untuk menentukan dependensi antar task
    prompt = f"""
Berikut adalah daftar task dalam sebuah proyek:

{json.dumps(tasks, indent=2)}

TUGAS KAMU:
1. Identifikasi hubungan ketergantungan antar task.
2. Tentukan task mana yang HARUS selesai terlebih dahulu sebelum task lain dimulai.
3. Jika sebuah task tidak memiliki ketergantungan, isi dengan array kosong [].

ATURAN OUTPUT:
- Output HARUS berupa JSON VALID
- TIDAK boleh ada teks penjelasan, markdown, atau komentar tambahan
- HANYA JSON

FORMAT OUTPUT (JSON ARRAY):
- "task"        : nama task
- "depends_on" : daftar task yang harus selesai sebelumnya (array)

CONTOH OUTPUT:
[
  {{"task": "Implementasi Backend", "depends_on": ["Desain Sistem"]}},
  {{"task": "Testing", "depends_on": ["Implementasi Backend"]}},
  {{"task": "Dokumentasi", "depends_on": []}}
]

Mulai output di bawah ini:
"""
    # =========================
    # 2. Kirim prompt ke LLM
    # =========================

    # Memanggil Groq API dengan prompt dependency
    response = query_groq(prompt)

    # =========================
    # 3. Parsing JSON dependency
    # =========================

    # Coba ekstrak JSON array dari response
    dependencies = extract_json_array(response)

    # =========================
    # 4. Fallback jika parsing gagal
    # =========================

    # Jika regex parsing gagal:
    # - Coba parsing langsung seluruh response sebagai JSON
    if dependencies is None:
        try:
            dependencies = json.loads(response.strip())
        except Exception:
            # Jika tetap gagal, gunakan list kosong agar pipeline tidak crash
            dependencies = []

    # =========================
    # 5. Return hasil ke pipeline
    # =========================

    # Output ini akan digunakan oleh:
    # - task_scheduler_agent
    # - task_allocation_agent
    return {
        "response": response,
        "dependencies": dependencies
    }
