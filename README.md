# 🤖 PMBAI


**Projeck-Manager-Basic-AI** Proyek ini adalah asisten Manajemen Proyek berbasis AI yang dibangun menggunakan **Streamlit**, terintegrasi dengan **Airtable** untuk penyimpanan data. Memanfaatkan agen AI modular untuk menghasilkan tugas, mengalokasikannya, menilai risiko, dan menghasilkan wawasan yang dapat ditindaklanjuti.

---

## 🚀 Fitur

- 📋 Unggah file CSV berisi anggota tim dan keterampilan
- 🤖 Pembuatan tugas berbasis AI dari deskripsi proyek
- 🧩 Deteksi ketergantungan tugas dan penjadwalan
- 👥 Alokasi tugas cerdas berdasarkan keterampilan anggota tim
- ⚠️ Penilaian risiko dan generasi wawasan
- 📊 Sinkronisasi semua pembaruan ke **Airtable**
- 🔄 Ekspor output terstruktur akhir sebagai CSV

## 📦 Instalasi

### 1. Clone repository

```bash
git clone https://github.com/yourusername/PMBAI.git
cd PMBAI
```

### 2. Buat environment virtual dan instal dependensi

```bash
python -m venv venv
source venv/bin/activate  # atau `venv\Scripts\activate` di Windows

pip install -r requirements.txt
```

---

## 🧪 Jalankan Aplikasi Secara Lokal

```bash
streamlit run main.py
```

---

## 📤 Setup Airtable

Tambahkan kunci API Airtable dan Base ID Anda di file `.env`:

```env
AIRTABLE_API_KEY=kunci_api_airtable_anda
AIRTABLE_BASE_ID=base_id_airtable_anda
```

> Atau tambahkan sebagai **secrets** di dashboard aplikasi Streamlit Cloud.

## 🔐 Setup Kunci API

Gunakan file `.env` di root direktori:

```env
OPENAI_API_KEY=kunci-openai-anda
GROQ_API_KEY=kunci-groq-anda
```

---

## 📊 Deployment

### Opsi 1: **[Streamlit Community Cloud](https://streamlit.io/cloud)**

- Hubungkan repository GitHub Anda
- Setel `main.py` sebagai script utama
- Tambahkan secrets yang diperlukan melalui dashboard

### Opsi 2: Self-hosted / Docker (opsional)

*Segera hadir – dukungan Dockerfile.*

---

## ✅ Format CSV Contoh

```csv
Nama,Deskripsi Profil
Alice,Python, ML, AI
Bob,Manajemen Proyek, Scrum
```

---

## 🙌 Ucapan Terima Kasih

- [Streamlit](https://streamlit.io/)
- [Airtable](https://airtable.com/)
- [Agen LangChain / LLMs]
- [OpenAI / Groq (yang digunakan)]

---

## 📄 Lisensi

[Lisensi MIT]()

---

**Dikembangkan dengan ❤️ menggunakan Streamlit dan AI**

*Manajemen proyek yang lebih cerdas dan efisien dengan kekuatan AI!* 🚀✨

