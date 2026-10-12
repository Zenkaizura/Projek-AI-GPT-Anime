# Projek AI GPT Anime

Langkah 1: avatar desktop sederhana. Aplikasi ini belum memakai AI, mikrofon, atau API berbayar.

## Menjalankan

Gunakan Python 3.10 atau yang lebih baru. Di direktori proyek, jalankan perintah sesuai sistem operasi:

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

### macOS/Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Avatar tampil di atas jendela lain dan bisa digeser dengan mouse. Gunakan jendela **Kontrol Avatar** untuk menyembunyikan, menampilkan kembali, atau menutup aplikasi. Klik kanan avatar untuk opsi tambahan. Tutup jendela kontrol untuk keluar sepenuhnya.

Overlay harus dijalankan di komputer desktop dengan tampilan grafis; lingkungan cloud hanya bisa menguji aplikasi secara headless. Perilaku jendela yang selalu di atas dapat berbeda menurut sistem operasi dan pengelola desktop.
