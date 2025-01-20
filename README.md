# Web Rekomendasi Lagu

Aplikasi web rekomendasi lagu berdasarkan suasana hati pengguna. Web ini memungkinkan pengguna untuk menggambarkan suasana hati mereka secara bebas, dan sistem akan merekomendasikan lagu yang sesuai berdasarkan input tersebut. 

Web ini menggunakan **Flask** sebagai backend, **Tailwind CSS** untuk styling, dan **Spotify API** untuk memberikan rekomendasi lagu. Aplikasi ini dihosting menggunakan **Vercel**.

## Fitur
- Rekomendasi lagu berdasarkan suasana hati pengguna.
- Pengguna dapat mendeskripsikan suasana hati mereka secara bebas.
- Menggunakan API Spotify untuk mendapatkan lagu yang sesuai.
- Antarmuka yang responsif dengan menggunakan Tailwind CSS.

## Teknologi yang Digunakan
- **Backend**: Flask (Python)
- **Frontend**: Tailwind CSS
- **API**: Spotify API (Spotipy)
- **Hosting**: Vercel

## Instalasi

### Prasyarat
Pastikan kamu sudah menginstal **Python 3** dan **pip**.

1. **Clone repository ini**:

    ```bash
    git clone https://github.com/donirmdhn42/Web-Rekomendasi-Lagu.git
    cd Web-Rekomendasi-Lagu
    ```

2. **Buat virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Aktifkan virtual environment**:

    - Di Windows:
      ```bash
      .\venv\Scripts\activate
      ```

    - Di macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up Spotify API credentials**:

    Daftar dan buat aplikasi di [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) untuk mendapatkan **Client ID** dan **Client Secret**.

    Simpan kredensial tersebut di file `app.py` dengan format berikut:

    ```
    SPOTIPY_CLIENT_ID=YOUR_CLIENT_ID
    SPOTIPY_CLIENT_SECRET=YOUR_CLIENT_SECRET
    ```

6. **Jalankan aplikasi**:

    ```bash
    python app.py
    ```

Aplikasi akan berjalan di `http://127.0.0.1:5000/`.

## Penggunaan
- Masukkan deskripsi suasana hati kamu di kolom input yang disediakan.
- Sistem akan menganalisis dan memberikan rekomendasi lagu dari Spotify yang sesuai dengan suasana hati kamu.

## Kontribusi
1. Fork repository ini.
2. Buat cabang baru (`git checkout -b feature-branch`).
3. Lakukan perubahan dan commit (`git commit -am 'Add feature'`).
4. Push ke cabang baru (`git push origin feature-branch`).
5. Buat pull request untuk di-review.

## Lisensi
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


