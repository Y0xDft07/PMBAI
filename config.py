# =========================
# Import library eksternal
# =========================
from groq import Groq              # Client API Groq (LLM)
import os                          # Akses environment variable
from dotenv import load_dotenv     # Load file .env
import pandas as pd                # Manipulasi data tabel (DataFrame)

# =========================
# Load environment variable
# =========================
load_dotenv()

# =========================
# Ambil API Key Groq dari .env
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Inisialisasi client Groq
client = Groq(api_key=GROQ_API_KEY)

# =====================================================
# Fungsi untuk query ke LLM Groq
# =====================================================
def query_groq(prompt):
    """
    Mengirim prompt ke model LLM Groq
    dan mengembalikan hasil teks dari AI
    """
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # Model LLM yang digunakan
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,               # Kreativitas rendah (lebih stabil)
        max_completion_tokens=1024,    # Batas token output
        top_p=1,
        stream=False,
    )

    # Ambil hanya teks hasil jawaban AI
    return completion.choices[0].message.content

# =====================================================
# Fungsi parsing skill dari deskripsi profil anggota
# =====================================================
def parse_skills(profile_desc):
    """
    Mengubah deskripsi profil menjadi list skill
    Contoh:
    "Python, Linux; Docker"
    -> ["python", "linux", "docker"]
    """
    if not profile_desc:
        return []

    skills = [
        skill.strip().lower()
        for skill in profile_desc.replace(";", ",").split(",")
        if skill.strip()
    ]

    return skills

# =====================================================
# Fungsi utama: generate CSV lengkap hasil proyek
# =====================================================
def generate_complete_project_csv(state):
    """
    Menggabungkan seluruh hasil workflow AI menjadi CSV:
    - tasks
    - dependencies
    - schedule
    - allocations
    - risks

    Output:
    - CSV per anggota tim
    - CSV untuk task tanpa penanggung jawab
    """

    # =========================
    # Konversi state ke DataFrame
    # =========================
    tasks_df = pd.DataFrame(state.get("tasks", []))
    dependencies_df = pd.DataFrame(state.get("dependencies", []))
    schedule_df = pd.DataFrame(state.get("schedule", []))
    allocations_df = pd.DataFrame(state.get("task_allocations", []))
    risks_df = pd.DataFrame(state.get("risks", []))

    # =========================
    # Normalisasi nama kolom
    # =========================
    tasks_df = tasks_df.rename(columns={"name": "task"})
    schedule_df = schedule_df.rename(columns={"name": "task"})

    # =========================
    # Proses merge seluruh data
    # =========================
    merged_df = tasks_df.merge(
        dependencies_df,
        left_on="task",
        right_on="task",
        how="left"
    )

    merged_df = merged_df.merge(
        schedule_df,
        on="task",
        how="left"
    )

    merged_df = merged_df.merge(
        allocations_df,
        left_on="task",
        right_on="task",
        how="left"
    )

    merged_df = merged_df.merge(
        risks_df,
        on=["task", "member"],
        how="left"
    )

    # =========================
    # Pastikan semua kolom penting ada
    # =========================
    for col in ["blocking_tasks", "dependent_tasks"]:
        if col not in merged_df.columns:
            merged_df[col] = ""

    for col in ["start_day", "end_day", "duration_days", "score"]:
        if col not in merged_df.columns:
            merged_df[col] = None

    if "member" not in merged_df.columns:
        merged_df["member"] = ""

    # =========================
    # Urutan kolom final CSV
    # =========================
    cols_order = [
        "task",
        "duration_days",
        "start_day",
        "end_day",
        "member",
        "score",
        "blocking_tasks",
        "dependent_tasks",
    ]

    merged_df = merged_df[cols_order]

    # =========================
    # Pisahkan CSV per anggota tim
    # =========================
    member_files = {}

    for member, group_df in merged_df.groupby("member"):
        # Nama file berdasarkan nama anggota
        filename = (
            f"{member.lower().replace(' ', '_')}_tasks.csv"
            if member
            else "unassigned_tasks.csv"
        )

        # Simpan CSV sebagai bytes (siap download)
        csv_bytes = group_df.to_csv(index=False).encode("utf-8")
        member_files[filename] = csv_bytes

    return member_files
