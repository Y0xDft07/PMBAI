PMBAI /
|-- ai_agents /|
|              |-- __init__.py
|              |-- insight_generation.py
|              |-- risk_assesment_agent.py
|              |-- task_allocation_agent.py
|              |-- task_dependency_agent.py
|              |-- task_generation_agent.py
|              |-- task_scheduler_agent.py
|--services /  |
|              |-- airtable_service.py
|              |-- csv_service.py
|--services /  |
|              |-- __init__.py
|              |-- json_utils.py
|-- config.py
|-- .gitignore
|-- requirements.txt
|-- main.py 
|-- readme.md
```

## 🔄 FLOWCHART KONSEP UTAMA (1 KONSEP)

```
[START]
   │
   ▼
[Upload CSV Tim]
   │
   │  (Name, Profile Description)
   ▼
[Simpan Tim ke Airtable]
   │
   ▼
[Input Deskripsi Proyek]
   │
   ▼
[Task Generation Agent]
   │
   │  Output: Daftar Task + Durasi
   ▼
[Task Dependency Agent]
   │
   │  Output: Ketergantungan Task
   ▼
[Task Scheduler Agent]
   │
   │  Output: Start Day & End Day
   ▼
[Task Allocation Agent]
   │
   │  Output: Task → Anggota Tim
   ▼
[Risk Assessment Agent]
   │
   │  Output: Analisis Risiko (Teks)
   ▼
[Insight Generation Agent]
   │
   │  Output: Insight & Rekomendasi
   ▼
[Update Data ke Airtable]
   │
   ▼
[Download CSV Hasil]
   │
   ▼
[END]
```

---

## 🧠 KETERANGAN TIAP BLOK (Singkat)

* **Upload CSV Tim**
  Input awal data anggota & skill

* **Task Generation**
  AI memecah deskripsi proyek → task realistis

* **Task Dependency**
  Menentukan urutan & ketergantungan kerja

* **Task Scheduler**
  Menyusun timeline optimal

* **Task Allocation**
  Membagi task ke tim sesuai skill & waktu

* **Risk Assessment**
  Mengevaluasi risiko beban kerja & jadwal

* **Insight Generation**
  Memberi saran perbaikan & pembelajaran

---

## 🎯 Ciri Khas Flow Ini

✔ Linear & mudah dipahami
✔ Setiap agent = **1 kotak flowchart**
✔ Cocok untuk:

* Dokumentasi skripsi / laporan
* README GitHub
* Presentasi arsitektur sistem
* Diagram BPMN sederhana
