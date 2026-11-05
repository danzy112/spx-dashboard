# Dashboard SPX - Rekap Absensi

Dashboard online untuk monitoring absensi dan gaji kerja SPX warehouse.

## Fitur

- 📊 Total hari kerja dan upah
- 📅 Rekap per periode gajian (10 & 25 tiap bulan)
- 💰 Detail upah per periode
- 🔄 Auto-refresh setiap 60 detik
- 📱 Responsive design

## Setup GitHub Pages

### 1. Buat Akun GitHub

1. Buka https://github.com/signup
2. Isi email, password, dan username
3. Verifikasi email

### 2. Install GitHub CLI (opsional)

```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 3. Push ke GitHub (Manual)

```bash
cd /home/aiagent/spx-dashboard

# Setup git
git config --global user.email "akuntiktoktes001@gmail.com"
git config --global user.name "SPX Dashboard"

# Init repo
git init
git add .
git commit -m "Initial dashboard"

# Login ke GitHub dan buat repo 'spx-dashboard'
# Kemudian push:
git branch -M main
git remote add origin https://github.com/USERNAME/spx-dashboard.git
git push -u origin main
```

### 4. Aktifkan GitHub Pages

1. Buka repository di GitHub
2. Settings → Pages
3. Source: Deploy from branch
4. Branch: `main` → folder `/root`
5. Save

Dashboard akan online di: `https://USERNAME.github.io/spx-dashboard/`

## Update Data

Jalankan script ini setiap kali ada absen baru:

```bash
cd /home/aiagent/spx-dashboard
python3 update-data.py
git add data.json
git commit -m "Update data $(date +%Y-%m-%d)"
git push
```

## Auto-Update dengan Cron

Tambahkan ke crontab untuk auto-update setiap hari jam 18:00:

```bash
0 18 * * * cd /home/aiagent/spx-dashboard && python3 update-data.py && git add data.json && git commit -m "Auto update $(date +%Y-%m-%d)" && git push
```

## Struktur File

```
spx-dashboard/
├── index.html          # Dashboard web
├── data.json           # Data absensi (auto-generated)
├── update-data.py      # Script generate data dari spx-absen.log
└── README.md           # Dokumentasi
```

## Data Source

Dashboard membaca dari: `/home/aiagent/spx-absen.log`

Format log:
```
# Tgl|Shift|Status|Catatan
2026-10-25|middle|hadir|
2026-10-26|middle|hadir|
```

## Tech Stack

- HTML5 + CSS3 + Vanilla JavaScript
- GitHub Pages (hosting gratis)
- Python 3 (data generator)

## Support

Upah: Rp245.000/hari
Jadwal gaji:
- Kerja tanggal 1-15 → dibayar tanggal 25
- Kerja tanggal 16-31 → dibayar tanggal 10 bulan depan
