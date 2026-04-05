import pandas as pd
import streamlit as st

# =====================================================
# Fungsi: parse_csv
# =====================================================
def parse_csv(file):
    """
    Membaca file CSV berisi data tim.
    Wajib memiliki kolom:
    - Name
    - Profile Description

    Output:
    List of dict:
    [
        {
            "name": "Nama Anggota",
            "skills": ["python", "linux", "docker"]
        }
    ]
    """

    # Baca file CSV menjadi DataFrame
    df = pd.read_csv(file)

    team = []

    # Validasi struktur CSV
    if 'Name' not in df.columns or 'Profile Description' not in df.columns:
        st.error(
            "Format CSV tidak valid.\n"
            "Kolom wajib: 'Name' dan 'Profile Description'."
        )
        return []

    # Iterasi setiap baris CSV
    for _, row in df.iterrows():
        # Ambil nama anggota
        name = str(row['Name']).strip()

        # Ambil deskripsi profil
        profile = str(row['Profile Description']).strip()

        # Pecah skill berdasarkan koma
        skills = [
            skill.strip()
            for skill in profile.split(",")
            if skill.strip()
        ]

        # Simpan ke struktur data tim
        team.append({
            "name": name,
            "skills": skills
        })

    return team

# =====================================================
# Fungsi: create_output_csv
# =====================================================
def create_output_csv(team_data, airtable_table):
    """
    Menggabungkan data tim lokal dengan data hasil AI
    yang tersimpan di Airtable.

    Output:
    pandas.DataFrame siap di-export ke CSV
    """

    output_data = []

    # Iterasi setiap anggota tim
    for member in team_data:
        name = member["name"]

        # Ambil data dari Airtable berdasarkan nama
        record = airtable_table.all(
            formula=f"{{Name}}='{name}'"
        )

        # Jika data tidak ditemukan, lewati
        if not record:
            continue

        fields = record[0]["fields"]

        # Gabungkan data lokal + Airtable
        output_data.append({
            "Name": name,
            "Profile Description": ", ".join(member["skills"]),
            "Assigned Tasks": fields.get("Assigned Tasks", ""),
            "Schedule": fields.get("Schedule", ""),
            "Dependencies": fields.get("Dependencies", ""),
            "Risk": fields.get("Risk", ""),
            "Insights": fields.get("Insights", ""),
        })

    # Konversi ke DataFrame
    return pd.DataFrame(output_data)
