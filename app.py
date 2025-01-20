import os
import base64
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Memuat .env untuk mendapatkan client ID dan secret
load_dotenv()

app = Flask(__name__)

# Spotify API authentication
client_id = "YOUR_CLIENT_ID"  # Ganti dengan Client ID kamu
client_secret = "YOUR_CLIENT_SECRET"  # Ganti dengan Client Secret kamu
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Fungsi untuk mendapatkan token akses Spotify
def get_spotify_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None

# Fungsi untuk mendeteksi suasana hati berdasarkan input
def detect_mood(user_input):
    mood_keywords = {
    'sedih': ['sedih', 'melankolis', 'putus asa', 'depresi', 'patah hati', 'blues', 'ballad', 'acoustic', 'kecewa', 'perpisahan', 'berduka', 'sakit hati', 'tangisan'],
    'senang': ['senang', 'ceria', 'bahagia', 'gembira', 'positif', 'terinspirasi', 'upbeat', 'disco', 'funk', 'pesta', 'bersemangat', 'fun', 'perayaan'],
    'marah': ['marah', 'kesal', 'frustrasi', 'geram', 'enerjik', 'rock', 'metal', 'punk', 'hardcore', 'kemarahan', 'perjuangan', 'protes'],
    'tenang': ['tenang', 'relaksasi', 'damai', 'mendalam', 'calm', 'indie', 'acoustic', 'jazz', 'meditasi', 'keheningan', 'refleksi'],
    'romantis': ['romantis', 'cinta', 'bucin', 'gombal', 'soft pop', 'indie', 'ballad', 'jazz', 'pasangan', 'keintiman', 'rindu', 'cinta sejati'],
    'energi': ['energi', 'semangat', 'aktif', 'motivasi', 'rock', 'metal', 'punk', 'funk', 'house', 'dynamis', 'intens', 'penuh energi'],
    'nostalgia': ['nostalgia', 'kenangan', 'masa lalu', 'retro', 'oldies', 'pop', 'rock', 'indie', 'kenangan manis', 'rindu masa lalu'],
    'damai': ['damai', 'sejuk', 'ketenangan', 'relaksasi', 'folk', 'jazz', 'indie', 'blues', 'kedamaian', 'keheningan', 'harmonis'],
    'rindu': ['rindu', 'melancholy', 'merindukan', 'terasing', 'ballad', 'pop', 'acoustic', 'sepi', 'perasaan kosong', 'kerinduan'],
    'kebahagiaan': ['bahagia', 'gembira', 'ceria', 'positif', 'reggae', 'electro', 'funk', 'pop', 'meriah', 'senyum', 'kegembiraan', 'momen bahagia'],
    'excited': ['excited', 'teruja', 'gembira', 'semangat', 'enerjik', 'upbeat', 'dance', 'electro', 'perasaan bersemangat', 'menanti-nanti'],
    'bosan': ['bosan', 'jenuh', 'membosankan', 'monoton', 'rutin', 'chill', 'indie', 'relaksasi', 'menunggu', 'lelah', 'tidak ada yang baru'],
    'cemas': ['cemas', 'khawatir', 'gelisah', 'takut', 'stress', 'anxiety', 'ambient', 'kecemasan', 'ketegangan', 'perasaan tidak tenang'],
    'terkejut': ['terkejut', 'shock', 'tercengang', 'stunned', 'surprise', 'dramatic', 'perasaan terkejut', 'kejutan', 'kaget'],
    'penuh_harapan': ['harapan', 'optimis', 'bersemangat', 'percaya diri', 'positif', 'hopeful', 'uplifting', 'kemajuan', 'masa depan', 'tujuan hidup'],
    'bingung': ['bingung', 'ragu', 'kehilangan arah', 'tidak pasti', 'canggung', 'perasaan tidak jelas', 'keraguan', 'pencarian', 'kebingungan'],
    'terpuruk': ['terpuruk', 'down', 'kecewa', 'putus asa', 'frustrasi', 'blues', 'kesedihan mendalam', 'kegagalan', 'kehilangan harapan'],
    'gembira': ['gembira', 'senang', 'ceria', 'bahagia', 'positif', 'upbeat', 'cheerful', 'perasaan ringan', 'hura-hura'],
    'lega': ['lega', 'bebas', 'relieved', 'tenang', 'lega', 'kelegaan', 'damai', 'nyaman', 'lulus', 'terbebas'],
    'malas': ['malas', 'mager', 'rasa malas', 'tidak ingin melakukan apa-apa', 'chill', 'ambient', 'soft pop', 'lelah', 'tidak termotivasi'],
    'frustrasi': ['frustrasi', 'buntu', 'kesal', 'kecewa', 'stress', 'rock', 'hardcore', 'kegagalan', 'jalan buntu', 'kepanikan'],
    'takut': ['takut', 'cemas', 'khawatir', 'perasaan takut', 'gelisah', 'ambient', 'dark', 'ketakutan', 'teror', 'perasaan terancam'],
    'semangat': ['semangat', 'motivasi', 'positif', 'energi', 'aktif', 'enerjik', 'rock', 'punk', 'motivational', 'semangat hidup'],
    'antusias': ['antusias', 'bersemangat', 'excited', 'positif', 'upbeat', 'pop', 'funk', 'perasaan senang', 'menanti-nanti'],
    'terinspirasi': ['terinspirasi', 'bersemangat', 'inspiratif', 'positif', 'uplifting', 'indie', 'acoustic', 'penuh ide', 'motivasi'],
    'curiga': ['curiga', 'waspada', 'takut', 'ragu', 'khawatir', 'dark', 'ambient', 'perasaan mencurigakan', 'keamanan'],
    'haru': ['haru', 'terharu', 'emotional', 'terpukul', 'sentimental', 'ballad', 'pop', 'perasaan mendalam', 'kesedihan manis'],
    'optimis': ['optimis', 'penuh harapan', 'percaya diri', 'positif', 'uplifting', 'indie', 'folk', 'perasaan yakin', 'semangat baru']
}
    
    user_input = user_input.lower()
    for mood, keywords in mood_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return mood
    return 'neutral'

def search_songs_by_mood_and_region(mood):
    access_token = get_spotify_token()
    if not access_token:
        return []

    # Kata kunci genre berdasarkan mood
    mood_genres = {
    'sedih': 'sedih,melankolis,blues,ballad,acoustic,pop,indie,soft pop,slow,tragic,heartbroken,indonesia,pop indonesia,indie indonesia,jazz indonesia,lagu sedih',
    'senang': 'ceria,senang,positif,gembira,pop,disco,funk,house,upbeat,celebration,happy,electro,cheerful,party,indonesia,pop indonesia,semangat,indie indonesia',
    'marah': 'marah,kesal,frustrasi,geram,enerjik,rock,metal,punk,hardcore,grunge,alternative,aggressive,rebellious,indonesia,rock indonesia,punk indonesia',
    'tenang': 'tenang,relaksasi,damai,indie,jazz,acoustic,blues,funk,country,folk,mellow,ambient,cool,calm,soothing,indonesia,jazz indonesia,indie indonesia,lagu tenang',
    'romantis': 'romantis,cinta,soft pop,ballad,jazz,indie,love,soul,slow,dreamy,passionate,heartfelt,indonesia,pop indonesia,indie indonesia,lagu romantis,lagu cinta indonesia',
    'energi': 'energi,semangat,aktif,motivasi,rock,metal,punk,funk,house,electronic,dance,high-energy,powerful,indonesia,musik energi,rock indonesia,funk indonesia',
    'nostalgia': 'nostalgia,retro,oldies,pop,rock,indie,classic,80s,90s,vintage,throwback,sentimental,melancholic,indonesia,lagu nostalgia,pop indonesia,indie indonesia',
    'damai': 'damai,relaksasi,ketenangan,ambient,folk,jazz,indie,blues,calm,mellow,serene,peaceful,relaxed,indonesia,jazz indonesia,indie indonesia,folk indonesia',
    'rindu': 'rindu,melancholy,ballad,acoustic,pop,indie,sad,love,nostalgic,heartfelt,separation,emotional,indonesia,pop indonesia,indie indonesia,lagu rindu',
    'kebahagiaan': 'bahagia,ceria,reggae,electro,funk,pop,disco,upbeat,celebratory,feel-good,happy,vibrant,joyful,indonesia,pop indonesia,indie indonesia',
    'excited': 'excited,semangat,upbeat,enerjik,pop,house,disco,edm,dance,cheerful,festival,electronic,up-tempo,indonesia,pop indonesia,house indonesia',
    'bosan': 'bosan,chill,ambient,lo-fi,soft pop,indie,relaxed,slow,calm,mellow,background,simple,indonesia,lagu santai,indie indonesia,jazz indonesia',
    'cemas': 'Alternative Rock,indie,cemas,stress,bimbang,anxiety,ambient,dark,electronic,experimental,tension,slow,ambient,moody,mystery,indonesia,lagu cemas',
    'terkejut': 'terkejut,shock,stunned,dark,dramatic,suspense,cinematic,techno,experimental,thriller,indonesia,lagu tegang,indie indonesia,rock indonesia',
    'penuh_harapan': 'harapan,optimis,uplifting,indie,folk,acoustic,motivation,positive,hopeful,spiritual,indonesia,lagu harapan,indie indonesia,folk indonesia',
    'bingung': 'bingung,perasaan tidak jelas,soft pop,chill,ambient,indie,lo-fi,experimental,indonesia,lagu bingung,indie indonesia',
    'terpuruk': 'terpuruk,blues,melankolis,pop,acoustic,sad,slow,despair,heartbroken,mournful,indonesia,pop indonesia,indie indonesia,lagu terpuruk',
    'gembira': 'gembira,ceria,positif,cheerful,pop,disco,electronic,house,happy,upbeat,party,dance,indonesia,pop indonesia,indie indonesia',
    'lega': 'lega,relaxed,indie,ambient,funk,soft pop,jazz,lo-fi,easy listening,indonesia,lagu lega,jazz indonesia,indie indonesia',
    'malas': 'malas,chill,ambient,lo-fi,soft pop,indie,easy listening,background,relaxing,indonesia,lagu malas,indie indonesia,jazz indonesia',
    'frustrasi': 'frustrasi,rock,metal,hardcore,punk,grunge,alternative,aggressive,bitter,indonesia,lagu frustasi,rock indonesia,punk indonesia',
    'takut': 'takut,gelap,ambient,dark,cinematic,suspense,horror,mysterious,electronic,indonesia,lagu takut,indie indonesia',
    'semangat': 'semangat,energi,rock,punk,funk,motivation,indie,energetic,workout,high-energy,indonesia,lagu semangat,rock indonesia,funk indonesia',
    'antusias': 'antusias,upbeat,cheerful,electro,pop,indie,energetic,dance,indonesia,lagu antusias,pop indonesia',
    'terinspirasi': 'terinspirasi,positif,uplifting,indie,funk,electronic,acoustic,creative,melodic,indonesia,lagu inspirasi,indie indonesia,folk indonesia',
    'curiga': 'curiga,waspada,misteri,gelap,ambient,dark,electronic,experimental,suspense,indonesia,lagu curiga,indie indonesia',
    'haru': 'haru,emotional,ballad,pop,sentimental,romantic,soft,heartfelt,slow,sweet,indonesia,pop indonesia,indie indonesia,jazz indonesia',
    'optimis': 'optimis,positif,indie,folk,uplifting,motivational,feel-good,cheerful,indonesia,lagu optimis,indie indonesia,folk indonesia'
    }

    # Jika mood tidak dikenali, cari dengan keyword umum
    genre = mood_genres.get(mood.lower(), 'pop indonesia,rock indonesia,indie')

    # Daftar wilayah: 'ID' untuk Indonesia, 'US' untuk Amerika
    regions = ['ID']

    songs = []
    for region in regions:
        url = f'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        params = {
            'q': genre,  # Menggunakan genre untuk mencari lagu
            'type': 'track',  # Mencari lagu (track)
            'limit': 50,  # Mendapatkan 20 lagu per wilayah
            'market': region  # Menentukan wilayah
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            search_results = response.json()['tracks']['items']
            for track in search_results:
                songs.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'url': track['external_urls']['spotify'],
                    'region': region,
                    'image_url': track['album']['images'][0]['url']  # Menyertakan gambar album
                })

    return songs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    mood_input = request.form['mood']
    mood = detect_mood(mood_input)  # Menentukan mood dari input pengguna
    songs = search_songs_by_mood_and_region(mood)

    # Menambahkan keterangan mood
    mood_descriptions = {
    'sedih': 'Nampaknya Anda sedang merasa sedih. Biarkan lagu-lagu melankolis ini menemani Anda, memberikan kenyamanan, dan menghangatkan hati. Saatnya untuk meresapi perasaan Anda dengan alunan musik yang penuh emosi.',
    'senang': 'Hari ini Anda merasa sangat bahagia! Nikmati lagu-lagu ceria dan penuh semangat yang akan membuat setiap detik terasa lebih hidup. Ayo, rayakan kebahagiaan Anda dengan alunan musik yang penuh energi!',
    'marah': 'Lagi marah atau kesal? Saatnya untuk melepaskan amarah dengan lagu-lagu yang keras dan energik. Biarkan musik yang penuh kekuatan ini membantu Anda melepaskan perasaan dan mengembalikan semangat Anda!',
    'tenang': 'Anda sedang berada dalam suasana hati yang tenang dan damai. Nikmati lagu-lagu yang lembut dan menenangkan untuk menciptakan ketenangan dalam diri Anda. Saatnya untuk melepaskan stres dan merasakan kedamaian.',
    'romantis': 'Sedang merasa romantis? Lagu-lagu penuh cinta ini akan menemani perasaan Anda yang lembut dan penuh kasih. Nikmati suasana hati yang penuh dengan keindahan dan kelembutan.',
    'energi': 'Saatnya untuk bangkit dan mengisi ulang semangat Anda! Lagu-lagu penuh energi dan motivasi ini akan memberi dorongan untuk terus maju. Biarkan musik ini membawa Anda untuk melangkah lebih jauh.',
    'nostalgia': 'Perasaan nostalgia datang menghampiri Anda. Mari menikmati lagu-lagu yang membawa kenangan dan memori indah masa lalu. Nikmati perjalanan kembali ke waktu yang telah berlalu.',
    'damai': 'Anda sedang mencari ketenangan? Nikmati lagu-lagu yang menenangkan jiwa dan membawa kedamaian. Saatnya untuk bersantai, menikmati kedamaian batin, dan merasakan ketenangan yang mendalam.',
    'rindu': 'Sedang merindukan seseorang atau sesuatu? Lagu-lagu yang melankolis ini bisa menemani perasaan rindu Anda. Biarkan musik ini berbicara untuk Anda, menyampaikan perasaan yang tak terucapkan.',
    'kebahagiaan': 'Saatnya merayakan kebahagiaan Anda! Nikmati lagu-lagu ceria dan penuh semangat yang akan membuat Anda tersenyum dan menari. Biarkan musik ini mengingatkan Anda betapa indahnya hidup!',
    'excited': 'Perasaan penuh semangat dan antusiasme menyelimuti diri Anda. Lagu-lagu dengan beat yang upbeat dan penuh energi akan membantu Anda merayakan perasaan ini. Ayo, rasakan kegembiraan dan terus bergerak!',
    'bosan': 'Sedang merasa jenuh atau bosan? Nikmati lagu-lagu yang lebih santai dan menenangkan. Musik ini akan menemani Anda dalam momen-momen yang lebih tenang dan penuh relaksasi.',
    'cemas': 'Perasaan cemas dan gelisah bisa terasa sangat berat. Dengarkan musik yang lebih gelap dan penuh ketegangan ini, untuk membantu Anda menyalurkan perasaan dan mencari ketenangan.',
    'terkejut': 'Kejutan datang begitu tiba-tiba, dan perasaan Anda penuh dengan ketegangan. Dengarkan musik yang dramatis dan penuh kejutan untuk mengimbangi perasaan ini dan memberi Anda ruang untuk bernapas.',
    'penuh_harapan': 'Ada harapan dan optimisme di dalam hati Anda. Nikmati musik yang memberi inspirasi, memberi Anda kekuatan untuk menghadapi apa pun yang datang. Biarkan alunan musik ini mengisi hati Anda dengan rasa percaya diri.',
    'bingung': 'Perasaan bingung atau tidak jelas bisa membuat kita merasa kehilangan arah. Nikmati musik yang lebih santai dan penuh eksperimen ini, yang akan membawa ketenangan dan sedikit kejelasan dalam momen yang penuh kebingungannya.',
    'terpuruk': 'Saat Anda merasa terpuruk, biarkan musik melankolis ini menemani Anda. Biarkan perasaan Anda keluar melalui lagu-lagu yang penuh emosi dan memberi ruang untuk penyembuhan.',
    'gembira': 'Anda merasa sangat gembira! Dengarkan lagu-lagu ceria dan penuh keceriaan ini yang akan menambah semangat Anda untuk terus merayakan kebahagiaan. Biarkan musik ini membuat hari Anda semakin berwarna!',
    'lega': 'Rasa lega menyelimuti diri Anda setelah melewati sesuatu yang sulit. Nikmati lagu-lagu yang tenang dan nyaman ini, untuk menenangkan pikiran dan menikmati perasaan lega yang datang.',
    'malas': 'Sedang merasa malas dan ingin beristirahat? Dengarkan musik yang santai dan menenangkan ini untuk menemani momen-momen tanpa beban Anda. Nikmati waktu luang Anda tanpa tekanan.',
    'frustrasi': 'Perasaan frustrasi bisa sangat menekan. Dengarkan musik dengan energi yang keras dan kuat ini untuk melepaskan ketegangan dan mengubah perasaan Anda menjadi sesuatu yang lebih produktif.',
    'takut': 'Saat perasaan takut datang, biarkan musik yang gelap dan penuh ketegangan ini mengiringi Anda. Dengarkan alunan misterius ini untuk menghadapi ketakutan dengan keberanian.',
    'semangat': 'Penuh dengan semangat dan energi! Lagu-lagu energik ini akan memberi Anda dorongan untuk terus maju dan menghadapi tantangan yang ada. Ayo, raih tujuan Anda dengan penuh semangat!',
    'antusias': 'Anda penuh dengan antusiasme dan energi! Nikmati musik dengan beat yang cepat dan penuh semangat untuk terus menjaga perasaan ini. Saatnya untuk mengekspresikan kegembiraan dan kebahagiaan Anda!',
    'terinspirasi': 'Lagu-lagu ini akan menginspirasi Anda untuk terus bergerak maju dan mengejar impian Anda. Nikmati musik yang menenangkan dan memberi motivasi untuk mencapai tujuan Anda.',
    'curiga': 'Perasaan curiga datang dengan ketegangan. Musik yang lebih gelap dan misterius ini bisa membantu Anda meresapi perasaan ini dan memberi ruang untuk pemikiran yang lebih dalam.',
    'haru': 'Lagu-lagu ini akan menemani Anda yang merasa haru. Biarkan alunan melankolis ini membawa Anda ke dalam momen penuh perasaan yang indah dan penuh kenangan.',
    'optimis': 'Rasakan keyakinan dan harapan yang penuh optimisme. Musik yang penuh semangat ini akan mengingatkan Anda untuk terus maju dan percaya pada apa yang akan datang.'
}


    # Jika mood tidak dikenali, beri keterangan umum
    description = mood_descriptions.get(mood, "Coba jelaskan suasana hati Anda, dan kami akan mencarikan lagu yang sesuai!")

    if songs:
        return render_template('index.html', songs=songs, description=description)
    else:
        return render_template('index.html', error="No songs found. Try a different mood!", description=description)
    
@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == '__main__':
    app.run(debug=True)
