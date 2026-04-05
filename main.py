import streamlit as st
import pandas as pd

# =========================
# Import utilitas JSON
# =========================
from utils.json_utils import extract_json_array

# =========================
# Import AI Agents
# =========================
from ai_agents.task_generation_agent import task_generation_node
from ai_agents.task_allocation_agent import task_allocation_node
from ai_agents.task_dependency_agent import task_dependency_node
from ai_agents.task_scheduler_agent import task_scheduler_node
from ai_agents.risk_assesment_agent import risk_assessment_node
from ai_agents.insight_generation import insight_generation_node

# =========================
# Import Service CSV & Airtable
# =========================
from services.csv_service import parse_csv, create_output_csv
from services.airtable_service import (
    get_airtable_table,
    save_team_to_airtable,
    update_team_with_tasks,
    clear_airtable_table
)

# =====================================================
# Fungsi utilitas untuk styling hasil output (HTML)
# =====================================================
def style_result_box(color):
    """
    Membuat box hasil output dengan warna tertentu
    Digunakan untuk membedakan output tiap agent
    """
    return f"""
        <div style="
            background-color: {color};
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            white-space: pre-wrap;
            overflow-x: auto;
        ">
    """

def close_div():
    """Menutup tag div HTML"""
    return "</div>"

# =====================================================
# Daftar agent (urutan workflow)
# =====================================================
agents = [
    "Pembuatan Task",
    "Identifikasi Ketergantungan Task",
    "Penjadwalan Task",
    "Alokasi Task",
    "Analisis Risiko",
    "Pembuatan Insight"
]

# =====================================================
# Menampilkan status workflow (progress agent)
# =====================================================
def get_status_md(current_step):
    """
    Menampilkan status agent:
    - selesai
    - sedang berjalan
    - menunggu
    """
    status_md = "### 🧭 Status Proses Agent\n"
    for idx, agent in enumerate(agents):
        if idx < current_step:
            status_md += f"✅ **{agent}** selesai\n"
        elif idx == current_step:
            status_md += f"🟡 **{agent}** sedang berjalan...\n"
        else:
            status_md += f"⚪️ {agent} menunggu\n"
    return status_md

# =====================================================
# Konfigurasi halaman Streamlit
# =====================================================
st.set_page_config(layout="wide")
st.title("🧠 Proyek Manajemen Proyek Berbasis AI")

# =====================================================
# Upload CSV Tim & simpan ke Airtable
# =====================================================
uploaded_file = st.file_uploader(
    "Upload file CSV (kolom wajib: Name, Profile Description)",
    type=["csv"]
)

if uploaded_file:
    # Parsing CSV menjadi data tim
    team_data = parse_csv(uploaded_file)

    if team_data:
        # Simpan ke session
        st.session_state.team = team_data

        # Simpan langsung ke Airtable
        save_team_to_airtable(team_data)

        st.success(
            f"Berhasil memuat {len(team_data)} anggota tim dan menyimpannya ke Airtable."
        )

# =====================================================
# Input deskripsi proyek
# =====================================================
if "project_description" not in st.session_state:
    st.session_state.project_description = ""

st.session_state.project_description = st.text_area(
    "Masukkan Deskripsi Proyek:",
    value=st.session_state.project_description,
    height=150,
)

# Container status workflow
status_container = st.empty()

# =====================================================
# Tombol menjalankan seluruh workflow agent
# =====================================================
if st.button("🚀 Jalankan Workflow AI"):
    # Validasi CSV
    if "team" not in st.session_state or not st.session_state.team:
        st.error("Silakan upload file CSV tim terlebih dahulu.")
        st.stop()

    # Validasi deskripsi proyek
    if not st.session_state.project_description.strip():
        st.error("Deskripsi proyek tidak boleh kosong.")
        st.stop()

    # State awal untuk agent
    state = {"project_description": st.session_state.project_description}

    # =========================
    # STEP 1: Task Generation
    # =========================
    status_container.markdown(get_status_md(0))
    with st.container():
        st.markdown("### 🧠 Agent Pembuatan Task")
        st.markdown(style_result_box("#FFF3CD"), unsafe_allow_html=True)

        task_data = task_generation_node(state)

        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.tasks = task_data.get("tasks", [])

    # =========================
    # STEP 2: Dependency Agent
    # =========================
    status_container.markdown(get_status_md(1))
    with st.container():
        st.markdown("### 🔗 Agent Ketergantungan Task")
        st.markdown(style_result_box("#D1ECF1"), unsafe_allow_html=True)

        dep_data = task_dependency_node({"tasks": st.session_state.tasks})

        st.markdown("**Respon Mentah AI:**")
        st.code(dep_data.get("response", "Tidak ada respon"), language="json")

        dependencies = dep_data.get("dependencies", [])
        if dependencies:
            st.dataframe(pd.DataFrame(dependencies))
        else:
            st.warning("Tidak ada dependency yang berhasil diekstrak.")

        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.dependencies = dependencies

    # =========================
    # STEP 3: Task Scheduling
    # =========================
    status_container.markdown(get_status_md(2))
    with st.container():
        st.markdown("### 📅 Agent Penjadwalan Task")
        st.markdown(style_result_box("#CCE5FF"), unsafe_allow_html=True)

        sched_data = task_scheduler_node({
            "tasks": st.session_state.tasks,
            "dependencies": st.session_state.dependencies,
        })

        st.json(sched_data.get("schedule", []))
        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.schedule = sched_data.get("schedule", [])

    # =========================
    # STEP 4: Task Allocation
    # =========================
    status_container.markdown(get_status_md(3))
    with st.container():
        st.markdown("### 👥 Agent Alokasi Task")
        st.markdown(style_result_box("#D4EDDA"), unsafe_allow_html=True)

        alloc_data = task_allocation_node({
            "tasks": st.session_state.tasks,
            "team": st.session_state.team,
        })

        st.json(alloc_data.get("task_allocations", []))
        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.task_allocations = alloc_data.get("task_allocations", [])

    # =========================
    # STEP 5: Risk Assessment
    # =========================
    status_container.markdown(get_status_md(4))
    with st.container():
        st.markdown("### ⚠️ Agent Analisis Risiko")
        st.markdown(style_result_box("#F8D7DA"), unsafe_allow_html=True)

        risk_data = risk_assessment_node({
            "tasks": st.session_state.tasks,
            "task_allocations": st.session_state.task_allocations,
        })

        st.text(risk_data.get("response", "Tidak ada hasil analisis risiko"))
        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.risks = []
    st.session_state.project_risk_score = None

    # =========================
    # STEP 6: Insight Generation
    # =========================
    status_container.markdown(get_status_md(5))
    with st.container():
        st.markdown("### 📊 Agent Insight Proyek")
        st.markdown(style_result_box("#E2E3E5"), unsafe_allow_html=True)

        insights = insight_generation_node({
            "project_description": st.session_state.project_description,
            "tasks": st.session_state.tasks,
            "schedule": st.session_state.schedule,
            "task_allocations": st.session_state.task_allocations,
            "risks": st.session_state.risks,
        })

        st.write(insights)
        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.insights = insights

    # =========================
    # Update data ke Airtable
    # =========================
    update_team_with_tasks(
        st.session_state.task_allocations,
        st.session_state.schedule,
        st.session_state.dependencies,
        risk_data.get("response", ""),
        insights
    )

    # Workflow selesai
    status_container.markdown(get_status_md(len(agents)))
    st.success("🎉 Workflow AI berhasil dijalankan!")
    st.balloons()

    # Download CSV hasil akhir
    output_df = create_output_csv(
        st.session_state.team,
        get_airtable_table()
    )

    csv = output_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV Tim Terbaru",
        data=csv,
        file_name="hasil_manajemen_proyek.csv"
    )

# =====================================================
# Tombol hapus seluruh data Airtable
# =====================================================
if st.button("🗑️ Kosongkan Data Airtable"):
    clear_airtable_table()
    st.success("✅ Data Airtable berhasil dikosongkan.")


## 🧭 Alur Flowchart (Ringkas)

# --- Tabs for results (same as your original snippet) ---
tabs = st.tabs([
    "🧠 Task Generation",
    "🔗 Task Dependencies",
    "📅 Scheduling",
    "👥 Allocation",
    "⚠️ Risk Assessment",
    "📊 Insights"
])

with tabs[0]:
    st.header("Task Generation Agent Results")
    if "tasks" in st.session_state:
        st.json(st.session_state.tasks)
    else:
        st.info("Run the workflow to generate tasks.")

with tabs[1]:
    st.header("Task Dependency Agent Results")
    if "dependencies" in st.session_state:
        df_deps = pd.DataFrame(st.session_state.dependencies)
        st.dataframe(df_deps)
    else:
        st.info("Run the workflow to identify dependencies.")

with tabs[2]:
    st.header("Task Scheduler Agent Results")
    if "schedule" in st.session_state:
        st.json(st.session_state.schedule)
    else:
        st.info("Run the workflow to get schedule.")

with tabs[3]:
    st.header("Task Allocation Agent Results")
    if "task_allocations" in st.session_state:
        st.json(st.session_state.task_allocations)
    else:
        st.info("Run the workflow to allocate tasks.")

with tabs[4]:
    st.header("Risk Assessment Agent Results")
    if "risks" in st.session_state and "project_risk_score" in st.session_state:
        st.json(st.session_state.risks)
        st.write(f"**Overall Project Risk Score:** {st.session_state.project_risk_score}")
    else:
        st.info("Run the workflow to assess risks.")

with tabs[5]:
    st.header("Insight Generation Agent Results")
    if "insights" in st.session_state:
        st.write(st.session_state.insights)
    else:
        st.info("Run the workflow to generate insights.")

