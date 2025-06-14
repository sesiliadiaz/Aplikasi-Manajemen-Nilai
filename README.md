## Deskripsi
Aplikasi Manajemen Nilai Mahasiswa adalah sebuah program berbasis GUI yang dibangun menggunakan Python dan Tkinter. Aplikasi ini dirancang untuk membantu pengelolaan data nilai mahasiswa, termasuk penyimpanan, pencarian, pengurutan, dan visualisasi data nilai.

## Tujuan Sistem
  1. Untuk meningkatkan efisiensi pengolahan nilai 
  2. Untuk mempercepat proses pencarian data mahasiswa 
  3. Untuk visualisasi dan laporan akademik

## Fitur Utama
1. **Manajemen Data Mahasiswa**:
   - Tambah, edit, dan hapus data mahasiswa
   - Validasi input untuk memastikan data yang dimasukkan valid
   - Penyimpanan data dalam array dengan kapasitas maksimum 100 mahasiswa

2. **Pencarian dan Pengurutan**:
   - Pencarian berdasarkan NIM atau Nama
   - Pengurutan data berdasarkan nilai akhir (Ascending/Descending)

3. **Import/Export Data**:
   - Import data dari file CSV
   - Export data ke file CSV

4. **Visualisasi Data**:
   - Grafik distribusi nilai akhir
   - Grafik distribusi kategori nilai (A, AB, B, BC, C, D, E)

5. **Antarmuka Pengguna**:
   - Tampilan tabel untuk menampilkan data
   - Form input yang intuitif
   - Status bar yang menampilkan jumlah data

## Persyaratan Sistem
- Python 3.x
- Modul yang diperlukan:
  - tkinter
  - matplotlib
  - csv

## Instalasi
1. Pastikan Python 3.x sudah terinstall di sistem Anda
2. Clone repository ini atau download file `main.py`
3. Install modul yang diperlukan dengan perintah:
   ```bash
   pip install matplotlib
   ```

## Cara Menggunakan
1. Jalankan aplikasi dengan perintah:
   ```bash
   python main.py
   ```
2. Gunakan form input untuk menambah atau mengedit data mahasiswa
3. Gunakan fitur pencarian untuk menemukan data tertentu
4. Gunakan tombol "Urutkan" untuk mengurutkan data berdasarkan nilai akhir
5. Gunakan tombol "Lihat Statistik" untuk melihat visualisasi data nilai
6. Gunakan tombol "Ekspor CSV" atau "Impor CSV" untuk mengekspor/mengimpor data

## Struktur Kode
- **Fungsi Utama**:
  - `tambah_data()`: Menambahkan data mahasiswa baru
  - `update_data()`: Memperbarui data mahasiswa yang ada
  - `delete_data()`: Menghapus data mahasiswa
  - `cari_data()`: Mencari data berdasarkan keyword
  - `urutkan_data()`: Mengurutkan data berdasarkan nilai akhir

- **Fungsi Pembantu**:
  - `hitung_nilai_akhir()`: Menghitung nilai akhir dari komponen nilai
  - `konversi_kategori()`: Mengkonversi nilai ke kategori huruf
  - `is_valid_name()`: Memvalidasi format nama

- **Fungsi GUI**:
  - `refresh_tabel()`: Memperbarui tampilan tabel
  - `clear_form()`: Mengosongkan form input
  - `show_statistik()`: Menampilkan visualisasi data
