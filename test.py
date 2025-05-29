import streamlit as st
import os
from pathlib import Path
import base64

# --- KONFIGURASI APLIKASI --- (Salin dari kode Anda)
NAMA_FOLDER_MEDIA_UTAMA = "media"
EKSTENSI_GAMBAR_DIDUKUNG = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
EKSTENSI_VIDEO_DIDUKUNG = ('.mp4', '.mov', '.avi', '.mkv')
JUMLAH_KOLOM_GRID = 3
NAMA_FILE_MUSIK_LATAR = "everything u are.mp3"

TOKEN_MAPPING = {
    "a1b": "Clea",  # Ubah dari "clea"
    "7c2": "Meldi", # Ubah dari "meldi"
    "k9p": "Adinda",# Ubah dari "adinda"
    "z3x": "Farah", # Ubah dari "farah"
    "6xd": "Kamasa",# Ubah dari "kamasa"
    "7ds": "Gadiza",# Ubah dari "gadiza"
    "9eh": "Arya",  # Ubah dari "arya"
    "0sn": "Andre", # Ubah dari "andre"
    "m5q": "Annisa" # Ubah dari "annisa"
}

PESAN_UNTUK_TEMAN = {
    "clea": """
Hai Clea yang paling kusayang,

Apa kabarnya hari ini? Semoga selalu ceria dan bahagia ya, seperti biasanya kamu membawa keceriaan buat aku.
Aku bikin galeri kecil ini khusus buat kamu. Isinya mungkin nggak seberapa, tapi setiap fotonya menyimpan cerita dan kenangan kita yang nggak akan pernah aku lupa.
Semoga kamu suka yaa. Jangan bosen-bosen jadi temen aku! hehe.

Dari aku, yang selalu ada buat kamu.
    """,
    "kamasa": """
    Hai Kamasa!

    Ini pesan khusus untukmu. Semoga harimu menyenangkan!
    Cek galeri ini ya!
    """,
    # Tambahkan pesan lain sesuai TOKEN_MAPPING atau gunakan default
    "default": """
Hai Kamu yang Spesial,

Ini adalah sedikit kenangan yang berhasil aku kumpulkan dari momen-momen kita.
Semoga bisa membuatmu tersenyum dan mengenang kembali saat-saat indah itu.
Nikmati ya!
    """
}
# --- FUNGSI BANTU --- (Salin dari kode Anda)
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

# --- FUNGSI TAMPILAN GALERI KONTEN --- (Salin dari kode Anda)
def tampilkan_konten_media(nama_folder_teman_valid):
    """Menampilkan semua media (gambar/video) dari folder teman yang valid."""
    
    # --- AWAL KODE DEBUG PATH DETAIL ---
    # Pastikan NAMA_FOLDER_MEDIA_UTAMA sudah didefinisikan secara global atau di-pass ke fungsi ini
    # Untuk contoh ini, saya asumsikan NAMA_FOLDER_MEDIA_UTAMA adalah variabel global
    
    script_dir = Path(__file__).parent.resolve() # Direktori tempat script .py Anda berada
    with st.sidebar:
        st.markdown("---")
        st.subheader(f"🔧 Debug Path untuk: '{nama_folder_teman_valid}'")
        st.write(f"Direktori script: `{script_dir}`")
        st.write(f"Nama folder media utama (konfigurasi): `{NAMA_FOLDER_MEDIA_UTAMA}`")

        # Path absolut yang coba dibangun ke folder media utama
        abs_path_media_utama = script_dir / NAMA_FOLDER_MEDIA_UTAMA
        st.write(f"Path absolut target ke folder media utama: `{abs_path_media_utama}`")

        # Path absolut yang coba dibangun ke folder teman spesifik
        abs_path_folder_teman = abs_path_media_utama / nama_folder_teman_valid
        st.write(f"Path absolut target ke folder teman: `{abs_path_folder_teman}`")

        st.markdown("**Pengecekan Eksistensi Folder:**")
        if abs_path_media_utama.exists() and abs_path_media_utama.is_dir():
            st.success(f"✅ Folder media utama ('{NAMA_FOLDER_MEDIA_UTAMA}') DITEMUKAN di `{abs_path_media_utama}`.")
            try:
                st.write(f"Isi dari '{abs_path_media_utama}': `{os.listdir(abs_path_media_utama)}`")
                
                # Sekarang cek subfolder teman
                if abs_path_folder_teman.exists() and abs_path_folder_teman.is_dir():
                    st.success(f"✅ Folder teman ('{nama_folder_teman_valid}') DITEMUKAN di `{abs_path_folder_teman}`.")
                    try:
                        st.write(f"Isi dari '{abs_path_folder_teman}': `{os.listdir(abs_path_folder_teman)}`")
                    except Exception as e:
                        st.error(f"⚠️ Gagal membaca isi folder teman '{nama_folder_teman_valid}': {e}")
                else:
                    st.error(f"❌ Folder teman ('{nama_folder_teman_valid}') TIDAK DITEMUKAN di `{abs_path_folder_teman}`.")
            except Exception as e:
                st.error(f"⚠️ Gagal membaca isi folder media utama: {e}")
        else:
            st.error(f"❌ Folder media utama ('{NAMA_FOLDER_MEDIA_UTAMA}') TIDAK DITEMUKAN atau bukan direktori di `{abs_path_media_utama}`.")
        st.markdown("---")
    # --- AKHIR KODE DEBUG PATH DETAIL ---
    
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

# --- BAGIAN UTAMA APLIKASI (MODIFIKASI) ---
def main():
    st.set_page_config(page_title="Kenangan Kita Bersama", layout="wide")

    query_params = st.query_params
    
    

    # --- DEBUG CODE START ---
    with st.sidebar: # Menampilkan debug info di sidebar
        st.subheader("🔧 Debug Info: Query Params")
        st.write("Isi `st.query_params` mentah:")
        st.write(query_params)

        # Mencoba mengambil 'l' (lowercase)
        token_l_value_raw = query_params.get("l")
        st.write(f"Nilai mentah untuk key 'l': `{token_l_value_raw}` (Tipe: `{type(token_l_value_raw).__name__}`)")

        # Mencoba mengambil 'L' (uppercase)
        token_L_value_raw = query_params.get("L")
        st.write(f"Nilai mentah untuk key 'L': `{token_L_value_raw}` (Tipe: `{type(token_L_value_raw).__name__}`)")

        # Memproses nilai token (ambil elemen pertama jika list)
        actual_token_l = None
        if isinstance(token_l_value_raw, list):
            if token_l_value_raw: actual_token_l = token_l_value_raw[0]
        else:
            actual_token_l = token_l_value_raw

        actual_token_L = None
        if isinstance(token_L_value_raw, list):
            if token_L_value_raw: actual_token_L = token_L_value_raw[0]
        else:
            actual_token_L = token_L_value_raw
        
        st.write(f"Nilai terproses dari 'l': `{actual_token_l}`")
        st.write(f"Nilai terproses dari 'L': `{actual_token_L}`")
    # --- DEBUG CODE END ---

    if 'app_step' not in st.session_state:
        st.session_state.app_step = "splash_screen"
    if 'nama_folder_teman_valid' not in st.session_state:
        st.session_state.nama_folder_teman_valid = None
    if 'audio_js_injected' not in st.session_state:
        st.session_state.audio_js_injected = False

    if st.session_state.app_step == "splash_screen":
        st.session_state.audio_js_injected = False
        
        # --- LOGIKA PENGAMBILAN TOKEN YANG DIPERBAIKI ---
        raw_token_from_url = None
        if actual_token_L is not None: # Prioritaskan 'L' jika ada (sesuai pengamatan di deploy)
            raw_token_from_url = actual_token_L
            with st.sidebar: st.info("Menggunakan token dari key 'L'.")
        elif actual_token_l is not None: # Jika 'L' tidak ada, coba 'l'
            raw_token_from_url = actual_token_l
            with st.sidebar: st.info("Menggunakan token dari key 'l'.")
        else:
            with st.sidebar: st.warning("Token tidak ditemukan di URL (baik 'l' maupun 'L').")

        token_untuk_lookup = None
        if raw_token_from_url:
            token_untuk_lookup = raw_token_from_url.lower() # Konversi ke lowercase untuk pencocokan
        
        with st.sidebar:
            st.subheader("🔧 Token Diproses")
            st.write(f"Token mentah dari URL: `{raw_token_from_url if raw_token_from_url else 'Tidak Ada'}`")
            st.write(f"Token untuk lookup (lowercase): `{token_untuk_lookup if token_untuk_lookup else 'Tidak Ada'}`")
        # --- AKHIR LOGIKA PENGAMBILAN TOKEN ---

        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("<br>"*8, unsafe_allow_html=True)
            st.markdown("""
            <style>
                div.stButton > button { /* CSS Tombol Anda */ } 
            </style>
            """, unsafe_allow_html=True) # Pastikan CSS Anda ada di sini atau pindahkan

            if st.button("SIAP KAH GUSYY? ✨", key="tombol_siap_splash"):
                if token_untuk_lookup and token_untuk_lookup in TOKEN_MAPPING:
                    st.session_state.nama_folder_teman_valid = TOKEN_MAPPING[token_untuk_lookup]
                    st.session_state.app_step = "show_gallery_and_play_music"
                    st.rerun()
                else:
                    if raw_token_from_url: # Token ada tapi tidak valid
                        st.error(f"🚫 LINK dengan kode '{raw_token_from_url}' SALAH atau TIDAK VALID!")
                        st.info("Pastikan kode di URL (setelah `?l=` atau `?L=`) adalah salah satu dari yang ini (tidak case-sensitive): " + ", ".join(TOKEN_MAPPING.keys()))
                    else: # Tidak ada token sama sekali di URL
                        st.error("🚫 UDAH GAUSA KEPO AH")
                        st.info("Kamu butuh kode spesial di URL untuk masuk. Contoh: `?l=kodekamu` atau `?L=kodekamu`")
            
            st.markdown("<br>"*8, unsafe_allow_html=True)
            if not raw_token_from_url: # Jika tidak ada token mentah sama sekali
                st.info("NYARI APA SI?? (Tips: URL-nya sepertinya kurang kode token, coba tambahkan `?l=kode` atau `?L=kode` di akhir URL)")

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
        
        pesan_spesifik = PESAN_UNTUK_TEMAN.get(nama_folder_teman, PESAN_UNTUK_TEMAN["default"])
        st.markdown(
            f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px 25px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: left;">
                <h4 style="margin-top:0; margin-bottom:10px; ">Untukmu, {nama_teman_display}...</h4>
                <hr style="border-top: 1px solid #eee; margin-bottom: 15px;">
                <p style="white-space: pre-wrap; line-height: 1.6; ">{pesan_spesifik}</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("---")

        if not st.session_state.audio_js_injected:
            path_musik_str = str(Path(NAMA_FOLDER_MEDIA_UTAMA) / NAMA_FILE_MUSIK_LATAR)
            audio_b64, audio_mime_type, audio_error = get_audio_b64_and_mimetype(path_musik_str)
            
            # --- DEBUG AUDIO START ---
            with st.sidebar:
                st.markdown("---") # Pemisah tambahan di sidebar
                st.subheader("🎵 Debug Info Audio")
                st.write(f"Path musik yang dicoba: `{path_musik_str}`")
                st.write(f"Error saat memproses audio: `{audio_error}`")
                st.write(f"MIME Type terdeteksi: `{audio_mime_type}`")
                if audio_b64:
                    st.write(f"Panjang data Audio B64: {len(audio_b64)}")
                else:
                    st.write("Data Audio B64: Kosong/Tidak ada")
                st.markdown("---") # Pemisah tambahan di sidebar
            # --- DEBUG AUDIO END ---

            if audio_error:
                st.warning(f"Tidak dapat menyiapkan musik latar: {audio_error}")
            elif audio_b64 and audio_mime_type:
                start_time_seconds = 0 
                js_code = f"""
                    <div id="audioPlayerDiv" style="width: 100%; text-align: center; margin-bottom: 15px; margin-top: 10px;"></div>
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
                st.components.v1.html(js_code, height=65)
            st.session_state.audio_js_injected = True
        
        tampilkan_konten_media(nama_folder_teman)

    else:
        st.warning("Halaman tidak ditemukan atau terjadi kesalahan alur aplikasi.")
        st.session_state.app_step = "splash_screen"
        if st.button("Kembali ke Halaman Awal"):
            st.rerun()

if __name__ == "__main__":
    main()