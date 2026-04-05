# =========================
# Import library
# =========================
import pandas as pd     # Untuk pengolahan data tabel
import json             # Untuk parsing JSON
import re               # Untuk pencarian pola teks (regex)

# =====================================================
# Fungsi: parse_skills
# =====================================================
def parse_skills(profile_desc):
    """
    Mengubah deskripsi profil anggota menjadi list skill.
    Digunakan saat alokasi task berdasarkan kemampuan.
    """

    # Jika data kosong (NaN), kembalikan list kosong
    if pd.isna(profile_desc):
        return []

    # Ganti ';' menjadi ',' lalu pisahkan skill
    skills = [
        skill.strip().lower()
        for skill in profile_desc.replace(";", ",").split(",")
        if skill.strip()
    ]

    return skills

# =====================================================
# Fungsi: extract_json_array
# =====================================================
def extract_json_array(text):
    """
    Mengekstrak ARRAY JSON pertama dari teks AI.
    
    Biasanya respon AI berbentuk:
    - teks penjelasan
    - diikuti JSON array
    
    Fungsi ini mengambil bagian JSON-nya saja.
    """

    # Regex untuk mencari array JSON: [ ... ]
    pattern = re.compile(r'(\[.*\])', re.DOTALL)
    match = pattern.search(text)

    if match:
        try:
            # Parsing string JSON menjadi object Python
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            # Jika JSON tidak valid
            return None

    # Jika tidak ditemukan array JSON
    return None

# =====================================================
# Fungsi: json_to_csv_bytes
# =====================================================
def json_to_csv_bytes(data):
    """
    Mengubah data JSON (list of dict)
    menjadi file CSV dalam bentuk bytes.
    
    Digunakan untuk:
    - download CSV
    - upload ke Airtable
    """

    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')
