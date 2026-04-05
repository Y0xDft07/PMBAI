# =========================
# Import library
# =========================
import os
from dotenv import load_dotenv
from pyairtable import Table
import streamlit as st

# =========================
# Load environment variable
# =========================
load_dotenv()

# =========================
# Konfigurasi Airtable
# =========================
API_KEY = os.getenv("AIRTABLE_API_KEY") or "your_api_key_here"
BASE_ID = os.getenv("AIRTABLE_BASE_ID") or "your_base_id_here"
TABLE_NAME = "Team Members"

# =====================================================
# Fungsi: get_airtable_table
# =====================================================
def get_airtable_table():
    """
    Mengembalikan objek koneksi tabel Airtable
    """
    return Table(API_KEY, BASE_ID, TABLE_NAME)

# =====================================================
# Fungsi: save_team_to_airtable
# =====================================================
def save_team_to_airtable(team_data):
    """
    Menyimpan data anggota tim ke Airtable.
    Jika nama sudah ada, data tidak dibuat ulang.
    """

    table = get_airtable_table()

    for member in team_data:
        # Cek apakah anggota sudah ada
        existing = table.all(formula=f"{{Name}}='{member['name']}'")
        if existing:
            st.info(
                f"Anggota '{member['name']}' sudah ada di Airtable, dilewati."
            )
            continue

        try:
            table.create({
                "Name": member["name"],
                "Profile Description": ", ".join(member["skills"]),
            })
            st.success(
                f"Berhasil menyimpan anggota '{member['name']}' ke Airtable."
            )
        except Exception as e:
            st.error(
                f"Gagal menyimpan anggota '{member['name']}': {e}"
            )

# =====================================================
# Fungsi: update_team_with_tasks
# =====================================================
def update_team_with_tasks(task_allocations, schedule, dependencies, risk_text, insights_text):
    """
    Memperbarui data anggota tim di Airtable dengan:
    - Task yang ditugaskan
    - Jadwal
    - Dependency
    - Risiko proyek
    - Insight proyek
    """

    table = get_airtable_table()
    member_updates = {}

    # =========================
    # Mapping task ke anggota
    # =========================
    for task in task_allocations:
        assigned_to = task.get("assigned_to", [])

        # Normalisasi assigned_to agar selalu list
        if isinstance(assigned_to, str):
            assigned_to_list = [assigned_to] if assigned_to else []
        elif isinstance(assigned_to, list):
            assigned_to_list = assigned_to
        else:
            assigned_to_list = []

        for member_name in assigned_to_list:
            if member_name not in member_updates:
                member_updates[member_name] = {
                    "tasks": [],
                    "schedules": [],
                    "dependencies": []
                }

            # Tambahkan task
            member_updates[member_name]["tasks"].append(
                task.get("task", "")
            )

            # Cari jadwal task
            sched_item = next(
                (
                    item for item in schedule
                    if item.get("name", "") == task.get("task", "")
                ),
                {}
            )

            if sched_item:
                sched_str = f"{sched_item['start_day']}–{sched_item['end_day']}"
                member_updates[member_name]["schedules"].append(sched_str)

            # Ambil dependency task
            dep_list = [
                dep.get("depends_on", "")
                for dep in dependencies
                if dep.get("task", "") == task.get("task", "")
            ]

            # Ratakan dependency (list / string)
            flat_dep_list = []
            for d in dep_list:
                if isinstance(d, list):
                    flat_dep_list.extend(d)
                else:
                    flat_dep_list.append(d)

            member_updates[member_name]["dependencies"].extend(flat_dep_list)

    # =========================
    # Update data ke Airtable
    # =========================
    for member_name, info in member_updates.items():
        records = table.all(formula=f"{{Name}}='{member_name}'")

        if not records:
            st.warning(
                f"Anggota '{member_name}' tidak ditemukan di Airtable."
            )
            continue

        record_id = records[0]["id"]

        update_data = {
            "Assigned Tasks": ", ".join(sorted(set(info["tasks"]))),
            "Schedule": ", ".join(sorted(set(info["schedules"]))),
            "Dependencies": ", ".join(sorted(set(info["dependencies"]))),
            "Risk": risk_text,
            "Insights": insights_text,
        }

        try:
            table.update(record_id, update_data)
            st.success(
                f"Data anggota '{member_name}' berhasil diperbarui."
            )
        except Exception as e:
            st.error(
                f"Gagal memperbarui anggota '{member_name}': {e}"
            )

# =====================================================
# Fungsi: clear_airtable_table
# =====================================================
def clear_airtable_table():
    """
    Menghapus seluruh data pada tabel Airtable.
    Digunakan untuk reset sistem.
    """

    table = get_airtable_table()
    records = table.all()

    for record in records:
        try:
            table.delete(record["id"])
        except Exception as e:
            st.error(
                f"Gagal menghapus data ID {record['id']}: {e}"
            )
