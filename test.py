import streamlit as st
import os
from pathlib import Path
import base64

# --- KONFIGURASI APLIKASI ---
NAMA_FOLDER_MEDIA_UTAMA = "media"
EKSTENSI_GAMBAR_DIDUKUNG = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
EKSTENSI_VIDEO_DIDUKUNG = ('.mp4', '.mov', '.avi', '.mkv')
JUMLAH_KOLOM_GRID = 3
NAMA_FILE_MUSIK_LATAR = "everything u are.mp3" # Pastikan file ini ada di folder media

TOKEN_MAPPING = {
    "a1b": "clea",
    "7c2": "meldi",
    "k9p": "adinda",
    "z3x": "farah",
    "6xd": "kamasa",
    "7ds": "gadiza",
    "9eh": "arya",
    "0sn": "andre",
    "m5q": "annisa"
}

# --- KONFIGURASI PESAN UNTUK TEMAN ---
# Tambahkan pesan spesifik untuk setiap nama folder teman di sini.
# Kunci dictionary harus sama dengan nilai yang ada di TOKEN_MAPPING.
PESAN_UNTUK_TEMAN = {
    "clea": """
Hai Clea yang paling kusayang,

Apa kabarnya hari ini? Semoga selalu ceria dan bahagia ya, seperti biasanya kamu membawa keceriaan buat aku.
Aku bikin galeri kecil ini khusus buat kamu. Isinya mungkin nggak seberapa, tapi setiap fotonya menyimpan cerita dan kenangan kita yang nggak akan pernah aku lupa.
Semoga kamu suka yaa. Jangan bosen-bosen jadi temen aku! hehe.

Dari aku, yang selalu ada buat kamu.
    """,
    "rand": """
Woy Rand, Bro!

Gimana kabarnya? Sehat kan? Harus sehat dong!
Nih, gw bikinin sesuatu yang simpel tapi semoga berkesan. Kumpulan foto-foto kita dari zaman baheula sampe sekarang.
Liat-liat aja, siapa tau inget lagi momen-momen konyol kita. Jangan lupa traktirannya kalo udah sukses! Hahaha.

Salam hangat,
Sobat lo yang paling keren.
    """,
    "lks": """
Untuk LKS yang Teristimewa,

Mungkin kata-kata tak cukup untuk mengungkapkan betapa berartinya dirimu.
Melalui galeri sederhana ini, aku ingin mengajakmu kembali mengenang setiap tawa, setiap cerita, dan setiap momen yang telah kita ukir bersama.
Semoga ini bisa menjadi pengingat kecil akan indahnya persahabatan kita.
Terima kasih telah menjadi bagian dari perjalananku.

Dengan penuh kasih,
Seseorang yang mengagumimu.
    """,
    "default": """
Hai Kamu yang Spesial,

Ini adalah sedikit kenangan yang berhasil aku kumpulkan dari momen-momen kita.
Semoga bisa membuatmu tersenyum dan mengenang kembali saat-saat indah itu.
Nikmati ya!
    """ # Pesan default jika nama teman tidak ditemukan di atas
}


# --- FUNGSI BANTU ---
def dapatkan_file_media(path_folder_spesifik):
    """Mendeteksi dan mengembalikan daftar file media dari folder, diurutkan."""
    if not isinstance(path_folder_spesifik, Path):
        path_folder_spesifik = Path(path_folder_spesifik)

    if not path_folder_spesifik.is_dir():
        return None, "error_folder_tidak_ditemukan"

    file_media_list = [
        item for item in path_folder_spesifik.iterdir()
        if item.is_file() and (
            item.suffix.lower() in EKSTENSI_GAMBAR_DIDUKUNG or
            item.suffix.lower() in EKSTENSI_VIDEO_DIDUKUNG
        )
    ]

    if not file_media_list:
        return [], "error_tidak_ada_file_visual"

    file_media_list.sort(key=lambda x: x.name, reverse=True)
    return file_media_list, None

def get_audio_b64_and_mimetype(path_file_musik_str):
    """Mengembalikan data audio base64, tipe MIME, dan pesan error jika ada."""
    path_file_musik = Path(path_file_musik_str)
    if not path_file_musik.is_file():
        return None, None, f"File musik '{path_file_musik.name}' tidak ditemukan."
    try:
        with open(path_file_musik, "rb") as f:
            data = f.read()
        b64_audio = base64.b64encode(data).decode()
        file_extension = path_file_musik.suffix.lower()
        
        mime_type_map = {
            ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
        }
        mime_type = mime_type_map.get(file_extension)

        if not mime_type:
            return None, None, f"Tipe file audio '{file_extension}' tidak didukung."
        
        return b64_audio, mime_type, None # Data, MimeType, No Error
    except Exception as e:
        return None, None, f"Gagal memproses file musik: {e}"

# --- FUNGSI TAMPILAN GALERI KONTEN ---
def tampilkan_konten_media(nama_folder_teman_valid):
    """Menampilkan semua media (gambar/video) dari folder teman yang valid."""
    # st.markdown("---") # Pemisah sebelum konten galeri (dipindah ke atas, setelah pesan surat)
    PATH_FOLDER_TEMAN = Path(NAMA_FOLDER_MEDIA_UTAMA) / nama_folder_teman_valid
    file_media, status_error = dapatkan_file_media(PATH_FOLDER_TEMAN)

    if status_error == "error_folder_tidak_ditemukan":
        st.error(f"⚠️ Folder media untuk '{nama_folder_teman_valid.capitalize()}' (di '{PATH_FOLDER_TEMAN}') tidak ditemukan!")
        st.info(f"Pastikan ada folder bernama '{nama_folder_teman_valid}' di dalam '{NAMA_FOLDER_MEDIA_UTAMA}'.")
        return
    elif status_error == "error_tidak_ada_file_visual":
        st.warning(f"📂 Folder media untuk '{nama_folder_teman_valid.capitalize()}' kosong atau tidak berisi file media yang didukung.")
        st.info("Silakan isi folder tersebut dengan kenangan indah.")
        return
    
    if file_media:
        st.success(f"Menampilkan {len(file_media)} kenangan indah untukmu, {nama_folder_teman_valid.capitalize()}!")
        st.balloons()

        cols_grid = st.columns(JUMLAH_KOLOM_GRID)
        for i, media_file_path in enumerate(file_media):
            kolom_saat_ini = cols_grid[i % JUMLAH_KOLOM_GRID]
            nama_file_display = media_file_path.name
            
            with kolom_saat_ini:
                container = st.container(border=True)
                container.markdown(f"**{nama_file_display}**")
                if media_file_path.suffix.lower() in EKSTENSI_GAMBAR_DIDUKUNG:
                    try:
                        container.image(str(media_file_path.resolve()), use_column_width=True)
                    except Exception as e:
                        container.error(f"Gagal memuat gambar: {nama_file_display}\nError: {e}")
                elif media_file_path.suffix.lower() in EKSTENSI_VIDEO_DIDUKUNG:
                    try:
                        container.video(str(media_file_path.resolve()))
                    except Exception as e:
                        container.error(f"Gagal memuat video: {nama_file_display}\nError: {e}")
    else:
        st.info("Tidak ada file media yang ditemukan di folder ini.")

# --- BAGIAN UTAMA APLIKASI ---
def main():
    st.set_page_config(page_title="Kenangan Kita Bersama", layout="wide")

    query_params = st.query_params

    if 'app_step' not in st.session_state:
        st.session_state.app_step = "splash_screen"
    if 'nama_folder_teman_valid' not in st.session_state:
        st.session_state.nama_folder_teman_valid = None
    if 'audio_js_injected' not in st.session_state:
        st.session_state.audio_js_injected = False

    if st.session_state.app_step == "splash_screen":
        st.session_state.audio_js_injected = False
        token_dari_url_list = query_params.get("l", [])
        token_dari_url = token_dari_url_list if token_dari_url_list else None # Ambil elemen pertama jika ada

        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("<br>"*8, unsafe_allow_html=True)
            # CSS untuk tombol bisa disederhanakan atau dipindah ke fungsi/variabel terpisah jika kompleks
            st.markdown("""
            <style>
                div.stButton > button {
                    display: block;
                    width: 100%;
                    padding: 1rem 1.5rem;
                    font-size: 1.25rem;
                    font-weight: bold;
                    color: white;
                    background: linear-gradient(to right, #ff7e5f, #feb47b);
                    border: none;
                    border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                div.stButton > button:hover {
                    background: linear-gradient(to right, #feb47b, #ff7e5f);
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
                    transform: translateY(-2px);
                }
                div.stButton > button:active {
                    transform: translateY(0);
                    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                }
            </style>
            """, unsafe_allow_html=True)

            if st.button("SIAP KAH GUSYY? ✨", key="tombol_siap_splash"):
                if token_dari_url and token_dari_url in TOKEN_MAPPING:
                    st.session_state.nama_folder_teman_valid = TOKEN_MAPPING[token_dari_url]
                    st.session_state.app_step = "show_gallery_and_play_music"
                    st.rerun()
                else:
                    if token_dari_url:
                        st.error(f"🚫 LINK '{token_dari_url}' SALAH!")
                    else:
                        st.error("🚫 UDAH GAUSA KEPO AH")

            st.markdown("<br>"*8, unsafe_allow_html=True)
            if not token_dari_url:
                st.info("NYARI APA SI??")

    elif st.session_state.app_step == "show_gallery_and_play_music":
        nama_folder_teman = st.session_state.nama_folder_teman_valid

        if not nama_folder_teman:
            st.error("Terjadi kesalahan: Sesi token tidak valid. Silakan kembali ke halaman awal dan gunakan URL yang benar.")
            st.session_state.app_step = "splash_screen"
            if st.button("Kembali ke Halaman Awal"):
                st.rerun()
            return

        nama_teman_display = nama_folder_teman.capitalize()
        st.title(f"💌 Sebuah Pesan & Galeri untuk {nama_teman_display} 🎞️")
        # st.markdown(f"_Momen-momen indah bersamamu, {nama_teman_display}!_") # Subtitle bisa diintegrasikan ke pesan

        # --- MULAI BAGIAN PESAN SURAT ---
        pesan_spesifik = PESAN_UNTUK_TEMAN.get(nama_folder_teman, PESAN_UNTUK_TEMAN["default"])
        
        st.markdown(
            f"""
            <div style="
                border: 1px solid #e0e0e0; 
                border-radius: 8px; 
                padding: 20px 25px; 
                margin-bottom: 25px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: left; /* Membuat teks di dalam surat rata kiri */
            ">
                <h4 style="margin-top:0; margin-bottom:10px; ">Untukmu, {nama_teman_display}...</h4>
                <hr style="border-top: 1px solid #eee; margin-bottom: 15px;">
                <p style="white-space: pre-wrap; line-height: 1.6; ">{pesan_spesifik}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---") # Garis pemisah sebelum bar musik
        # --- AKHIR BAGIAN PESAN SURAT ---

        if not st.session_state.audio_js_injected:
            path_musik_str = str(Path(NAMA_FOLDER_MEDIA_UTAMA) / NAMA_FILE_MUSIK_LATAR)
            audio_b64, audio_mime_type, audio_error = get_audio_b64_and_mimetype(path_musik_str)

            if audio_error:
                st.warning(f"Tidak dapat menyiapkan musik latar: {audio_error}")
            elif audio_b64 and audio_mime_type:
                start_time_seconds = 0 

                js_code = f"""
                    <div id="audioPlayerDiv" style="width: 100%; text-align: center; margin-bottom: 15px; margin-top: 10px;">
                    </div>
                    <script>
                        if (!document.getElementById('customAudioPlayer')) {{
                            const audioData = "data:{audio_mime_type};base64,{audio_b64}";
                            const audioContainer = document.getElementById('audioPlayerDiv');
                            const audioElement = document.createElement('audio');
                            audioElement.id = 'customAudioPlayer';
                            audioElement.src = audioData;
                            audioElement.controls = true; 
                            audioElement.loop = true;   
                            audioElement.style.width = "80%"; 

                            audioContainer.appendChild(audioElement);

                            audioElement.onloadedmetadata = function() {{
                                audioElement.currentTime = {start_time_seconds};
                                console.log("Audio metadata loaded. currentTime set to {start_time_seconds} seconds.");
                                const playPromise = audioElement.play();
                                if (playPromise !== undefined) {{
                                    playPromise.then(_ => {{
                                        console.log("Audio playback started from {start_time_seconds}s for {nama_folder_teman}.");
                                    }}).catch(error => {{
                                        console.error("Playback from specific time failed for {nama_folder_teman}:", error);
                                    }});
                                }}
                            }};
                        }}
                    </script>
                """
                st.components.v1.html(js_code, height=65) # Sesuaikan tinggi jika perlu
            st.session_state.audio_js_injected = True
        
        # st.markdown("---") # Pemisah setelah musik, sebelum galeri
        tampilkan_konten_media(nama_folder_teman)

    else:
        st.warning("Halaman tidak ditemukan atau terjadi kesalahan alur aplikasi.")
        st.session_state.app_step = "splash_screen"
        if st.button("Kembali ke Halaman Awal"):
            st.rerun()

if __name__ == "__main__":
    main()