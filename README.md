# HealthyMe - Sistem Rekomendasi Menu

## Deskripsi Proyek
HealthyMe adalah sebuah aplikasi berbasis web yang dirancang untuk membantu pengguna dalam memilih menu makanan yang sehat dan sesuai dengan kebutuhan tubuh mereka. Aplikasi ini memberikan rekomendasi menu harian yang dipersonalisasi berdasarkan Indeks Massa Tubuh (BMI) dan preferensi makanan pengguna, dengan tujuan membantu mencapai tujuan kesehatan seperti menurunkan berat badan, mempertahankan berat badan ideal, atau meningkatkan kesehatan secara keseluruhan.

## Fitur Utama
- **Kalkulator BMI:** Menghitung BMI pengguna berdasarkan data berat badan dan tinggi badan yang diberikan.
- **Rekomendasi Menu:** Memberikan rekomendasi menu makanan harian yang sesuai dengan BMI dan preferensi makanan pengguna.
- **Autentikasi Pengguna:** Pengguna dapat membuat akun dan login menggunakan Firebase Authentication.
- **Penyimpanan Data:** Informasi pengguna disimpan dengan aman di Firebase Firestore.
- **Antarmuka Interaktif:** Antarmuka yang ramah pengguna dan mudah digunakan, dibangun menggunakan Streamlit.

## Teknologi yang Digunakan
- **Frontend:** Streamlit
- **Backend:** Python
- **Database dan Autentikasi:** Firebase
- **Pengembangan UI:** Whimsical (untuk wireframe dan flowchart)

## Cara Menggunakan
1. **Clone Repository:**
   ```bash
   git clone https://github.com/username/HealthyMe.git
   cd HealthyMe
   ```

2. **Instalasi Dependencies:**
   Pastikan Anda memiliki Python dan pip terinstal. Kemudian jalankan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfigurasi Firebase:**
   Buat proyek di Firebase dan tambahkan file `firebase_config.json` yang berisi konfigurasi Firebase Anda ke dalam direktori proyek.

4. **Menjalankan Aplikasi:**
   Jalankan aplikasi dengan perintah:
   ```bash
   streamlit run app.py
   ```

5. **Mengakses Aplikasi:**
   Buka browser dan akses `http://localhost:8501`.

## Struktur Proyek
- `app.py`: Berkas utama untuk menjalankan aplikasi Streamlit.
- `requirements.txt`: Daftar dependencies yang diperlukan untuk menjalankan aplikasi.
- `firebase_config.json`: File konfigurasi Firebase (tidak termasuk dalam repository, harus dibuat oleh pengguna).
- `assets/`: Berisi gambar dan file statis lainnya yang digunakan dalam aplikasi.

## Kontribusi
Kami menyambut kontribusi dari siapa pun. Jika Anda ingin berkontribusi, silakan fork repository ini, buat branch baru untuk fitur atau perbaikan bug Anda, dan buat pull request setelah selesai.

Terima kasih telah menggunakan HealthyMe! Jika Anda memiliki pertanyaan atau masalah, jangan ragu untuk menghubungi kami melalui issue di repository ini.
