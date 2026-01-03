# Auto Fill GitHub

Bot sederhana untuk menjaga grafik kontribusi GitHub tetap hijau secara otomatis. Script ini akan melakukan commit 1 kali sehari pada jam acak.

## Cara Kerja

1. **Schedule**: Menggunakan GitHub Actions cron job yang berjalan setiap jam dari jam 08:00 sampai 23:00 UTC.
2. **Logic**: `script.py` akan dijalankan.
    - Script mengecek `log.txt` untuk melihat apakah hari ini sudah ada commit.
    - Jika SUDAH, script berhenti.
    - Jika BELUM, script menghitung probabilitas (sekitar 20%) untuk melakukan commit saat itu juga.
    - Jika sudah jam 22:00 UTC dan belum ada commit, script akan **MEMAKSA** melakukan commit untuk memastikan hari itu tidak kosong.
3. **Commit**: Script mengupdate file `log.txt` dengan timestamp terbaru, lalu melakukan git commit & push.

## Cara Setup (Dari Nol)

1. **Fork atau Buat Repo Baru**
   - Jika membuat repo baru, pastikan public (agar action jalan gratis tanpa batas).

2. **Upload File**
   - Masukkan semua file dari folder ini ke repo Anda:
     - `.github/workflows/auto-commit.yml`
     - `script.py`
     - `log.txt` (isi awal bebas, misal tahun lalu)
     - `README.md` (opsional)

3. **Pastikan Permissions**
   - Masuk ke **Settings** repository Anda.
   - Pilih **Actions** -> **General**.
   - Di bagian **Workflow permissions**, pilih **Read and write permissions**.
   - Klik **Save**.

4. **Selesai!**
   - Anda bisa menunggu jadwal berjalan (setiap jam 08-23 UTC).
   - Atau tes manual: Masuk tab **Actions**, pilih **Auto Commit Bot**, lalu klik **Run workflow**.

## Kustomisasi Jam

Edit file `.github/workflows/auto-commit.yml`:
```yaml
- cron: "0 8-23 * * *"
```
Angka `8-23` adalah rentang jam dalam UTC. Sesuaikan dengan kebutuhan.

## Catatan

- Script ini **TIDAK** butuh VPS.
- **TIDAK** butuh PC menyala.
- **TIDAK** butuh token tambahan (menggunakan `GITHUB_TOKEN` bawaan).
