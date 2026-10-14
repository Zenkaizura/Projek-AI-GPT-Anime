# Projek AI GPT Anime

Prototipe avatar tersedia dalam dua versi. Keduanya belum memakai AI, mikrofon, atau API berbayar.

## Versi browser (tanpa instalasi)

Buka [`docs/index.html`](docs/index.html) di browser. Avatar bisa disapa, disembunyikan, dan ditampilkan lagi. Ada chat teks dengan balasan otomatis **demo**, bukan AI sungguhan. Di Chrome/Edge yang mendukung Document Picture-in-Picture, tombol **Buka jendela kecil** menampilkan avatar dalam jendela mengambang. Jendela browser ini belum menjadi overlay desktop transparan.

Agar dapat dibuka lewat tautan tanpa mengunduh repo, pemilik repo dapat mengaktifkan GitHub Pages di **Settings → Pages → Build and deployment**: pilih **Deploy from a branch**, branch **main**, folder **/docs**, lalu **Save**. Setelah GitHub Pages selesai menerbitkan halaman, alamatnya adalah `https://zenkaizura.github.io/Projek-AI-GPT-Anime/`. Jangan menganggap alamat itu aktif sebelum GitHub Pages melaporkan bahwa situs berhasil diterbitkan.

## Backend Gemini untuk chat AI

Kode backend Python ada di [`backend/app.py`](backend/app.py). Backend ini belum diterbitkan sebagai layanan online, dan [`docs/config.js`](docs/config.js) sengaja belum berisi alamat backend. Karena itu website tetap memakai balasan demo. Jangan menaruh API key di `docs/`, GitHub, atau chat.

Untuk menyiapkan dan menguji backend di cloud:

```sh
python3 -m venv .backend-venv
.backend-venv/bin/python -m pip install -r backend/requirements.txt
.backend-venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Backend membaca `GEMINI_API_KEY` dari variabel rahasia server. Model bawaan adalah `gemini-2.5-flash`; `GEMINI_MODEL` dapat diatur jika model yang tersedia untuk kuota gratis akun berbeda. Untuk membuat chat AI berfungsi di website, backend perlu diterbitkan di hosting HTTPS, kunci dimasukkan melalui pengaturan rahasia hosting, dan alamat backend diisi di `docs/config.js`. Batasi pemakaian backend sebelum membukanya untuk umum agar kuota uji coba tidak habis.

## Versi desktop Python

Gunakan Python 3.10 atau yang lebih baru. Di direktori proyek, jalankan perintah sesuai sistem operasi:

### Windows (PowerShell)

Pastikan Python tersedia terlebih dahulu:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Jika `python --version` juga gagal atau membuka Microsoft Store, pasang Python 3.10+ dari [python.org](https://www.python.org/downloads/windows/), pilih **Add python.exe to PATH** saat instalasi, lalu buka PowerShell baru. Pada komputer kampus yang membatasi instalasi, minta bantuan pengelola komputer.

### macOS/Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Avatar tampil di atas jendela lain dan bisa digeser dengan mouse. Gunakan jendela **Kontrol Avatar** untuk menyembunyikan, menampilkan kembali, atau menutup aplikasi. Klik kanan avatar untuk opsi tambahan. Tutup jendela kontrol untuk keluar sepenuhnya.

Overlay harus dijalankan di komputer desktop dengan tampilan grafis; lingkungan cloud hanya bisa menguji aplikasi secara headless. Perilaku jendela yang selalu di atas dapat berbeda menurut sistem operasi dan pengelola desktop.
