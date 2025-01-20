
# Web Rekomendasi Lagu

Aplikasi web ini menghadirkan rekomendasi lagu dari Spotify berdasarkan mood. Dengan antarmuka yang sederhana dan responsif, Anda hanya perlu menggambarkan perasaan Anda, dan sistem akan menganalisisnya untuk memberikan playlist yang sesuai.

Dibangun menggunakan **Flask** sebagai backend, **Tailwind CSS** untuk desain modern, serta **Spotify API** untuk integrasi lagu. Aplikasi ini dihosting di **Vercel** untuk performa yang optimal.

## Fitur Utama
- **Rekomendasi Lagu**: Dapatkan playlist berdasarkan mood anda.
- **Input Bebas**: Jelaskan perasaan Anda untuk mendapatkan rekomendasi yang lebih tepat.
- **Integrasi Spotify**: Menggunakan Spotify API untuk pilihan lagu yang relevan.
- **Antarmuka Responsif**: Menawarkan pengalaman pengguna yang optimal di perangkat apapun.

## Teknologi yang Digunakan
- **Backend**: Flask (Python)
- **Frontend**: Tailwind CSS
- **API**: Spotify API (Spotipy)
- **Hosting**: Vercel

## Instalasi

### Persyaratan
Pastikan **Python 3** dan **pip** terinstal.

1. **Clone Repository**:

    ```bash
    git clone https://github.com/donirmdhn42/Web-Rekomendasi-Lagu.git
    cd Web-Rekomendasi-Lagu
    ```

2. **Buat Virtual Environment**:

    ```bash
    python -m venv venv
    ```

3. **Aktifkan Virtual Environment**:

    - **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```

    - **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Konfigurasi API Spotify**:
   
    Daftar di [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) untuk mendapatkan **Client ID** dan **Client Secret**.

    Masukkan kredensial di `app.py`:

    ```
    SPOTIPY_CLIENT_ID=YOUR_CLIENT_ID
    SPOTIPY_CLIENT_SECRET=YOUR_CLIENT_SECRET
    ```

6. **Jalankan Aplikasi**:

    ```bash
    python app.py
    ```

Aplikasi akan berjalan di `http://127.0.0.1:5000/`.

## Penggunaan
- Deskripsikan mood/suasana hati Anda.
- Dapatkan rekomendasi lagu dari Spotify yang sesuai dengan perasaan Anda.

## Kontribusi
1. Fork repository ini.
2. Buat cabang baru (`git checkout -b feature-branch`).
3. Lakukan perubahan dan commit (`git commit -am 'Add feature'`).
4. Push cabang baru (`git push origin feature-branch`).
5. Buat pull request untuk di-review.

## Lisensi
Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---

Untuk melihat contoh aplikasi secara langsung, kunjungi [tautan ini](https://aurora-tunes.vercel.app).

