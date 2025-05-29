import streamlit as st
from pathlib import Path
from streamlit_javascript import st_javascript # Tambahkan ini
from user_agents import parse # Tambahkan ini

# --- KONFIGURASI APLIKASI ---
NAMA_FOLDER_MEDIA_UTAMA = "media"
EKSTENSI_GAMBAR_DIDUKUNG = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
EKSTENSI_VIDEO_DIDUKUNG = ('.mp4', '.mov', '.avi', '.mkv')
JUMLAH_KOLOM_GRID_DEFAULT = 3
NAMA_FILE_MUSIK_LATAR = "everything u are.mp3"

# --- MEMUAT TOKEN_MAPPING DARI STREAMLIT SECRETS ---
try:
    # Mengakses tabel 'token_data' dari secrets.
    # st.secrets.token_data akan menjadi objek yang mirip dictionary.
    # Kita konversi ke dictionary Python murni dengan dict().
    TOKEN_MAPPING = dict(st.secrets.token_data) # Perhatikan 'token_data' di sini

    if not TOKEN_MAPPING: # Jika tabel ada tapi isinya kosong
        st.error("Konfigurasi 'token_data' di Streamlit Secrets ditemukan kosong. Harap periksa file .streamlit/secrets.toml atau pengaturan secrets di platform deployment Anda.")
        TOKEN_MAPPING = {} # Fallback penting
except AttributeError:
    # Jika 'token_data' tidak ditemukan sama sekali di st.secrets
    st.error("Konfigurasi 'token_data' tidak ditemukan di Streamlit Secrets. Pastikan tabel [token_data] ada di .streamlit/secrets.toml atau di pengaturan secrets platform deployment.")
    TOKEN_MAPPING = {} # Fallback penting
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat TOKEN_MAPPING dari Streamlit Secrets: {e}")
    TOKEN_MAPPING = {} # Fallback penting

PESAN_UNTUK_TEMAN = {
    "Clea": """
Hai Clea yang paling kusayang,
Apa kabarnya hari ini? Semoga selalu ceria dan bahagia ya, seperti biasanya kamu membawa keceriaan buat aku.
Aku bikin galeri kecil ini khusus buat kamu. Isinya mungkin nggak seberapa, tapi setiap fotonya menyimpan cerita dan kenangan kita yang nggak akan pernah aku lupa.
Semoga kamu suka yaa. Jangan bosen-bosen jadi temen aku! hehe.
Dari aku, yang selalu ada buat kamu.
    """,
    "Kamasa": """
    Hai Kamasa yang hebat!
    Ini adalah sedikit lembaran kenangan yang aku rangkai khusus buat kamu.
    Setiap momen bersamamu itu berharga, dan aku berharap galeri kecil ini bisa jadi pengingat betapa serunya pertemanan kita.
    Jangan pernah berubah ya, tetap jadi Kamasa yang aku kenal. Cheers!
    Sahabatmu.
    """,
    "Meldi": "Pesan untuk Meldi...", "Adinda": "Pesan untuk Adinda...",
    "Farah": "Pesan untuk Farah...", "Gadiza": "Pesan untuk Gadiza...",
    "Arya": "Pesan untuk Arya...", "Andre": "Pesan untuk Andre...",
    "Annisa": "Pesan untuk Annisa...",
    "default": """
Hai Kamu yang Spesial,
Ini adalah sedikit kenangan yang berhasil aku kumpulkan dari momen-momen kita.
Semoga bisa membuatmu tersenyum dan mengenang kembali saat-saat indah itu.
Nikmati ya!
    """
}

# --- FUNGSI BANTU ---
def dapatkan_file_media(path_folder_spesifik):
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

# --- FUNGSI TAMPILAN GALERI KONTEN ---
def tampilkan_konten_media(nama_folder_teman_valid, jumlah_kolom_untuk_tampilan):
    script_dir = Path(__file__).parent.resolve()
    # Bagian debug path di sidebar bisa dipertahankan jika perlu
    # ... (kode debug sidebar Anda) ...

    PATH_FOLDER_TEMAN = script_dir / NAMA_FOLDER_MEDIA_UTAMA / nama_folder_teman_valid
    file_media, status_error = dapatkan_file_media(PATH_FOLDER_TEMAN)

    if status_error == "error_folder_tidak_ditemukan":
        st.error(f"⚠️ Folder media untuk '{nama_folder_teman_valid.capitalize()}' tidak ditemukan!")
        return
    elif status_error == "error_tidak_ada_file_visual":
        st.warning(f"📂 Folder '{nama_folder_teman_valid.capitalize()}' kosong.")
        return
    
    if file_media:
        st.success(f"Menampilkan {len(file_media)} kenangan indah untukmu, {nama_folder_teman_valid.capitalize()}!")
        st.balloons()
        cols_grid = st.columns(jumlah_kolom_untuk_tampilan)
        for i, media_file_path_obj in enumerate(file_media):
            kolom_saat_ini = cols_grid[i % jumlah_kolom_untuk_tampilan]
            nama_file_display = media_file_path_obj.name
            with kolom_saat_ini:
                container = st.container(border=True)
                container.markdown(f"**{nama_file_display}**")
                if media_file_path_obj.suffix.lower() in EKSTENSI_GAMBAR_DIDUKUNG:
                    try:
                        container.image(str(media_file_path_obj), use_container_width=True)
                    except Exception as e:
                        container.error(f"Gagal memuat gambar: {nama_file_display}\nError: {e}")
                elif media_file_path_obj.suffix.lower() in EKSTENSI_VIDEO_DIDUKUNG:
                    try:
                        container.video(str(media_file_path_obj))
                    except Exception as e:
                        container.error(f"Gagal memuat video: {nama_file_display}\nError: {e}")
    else:
        st.info("Tidak ada file media yang ditemukan di folder ini.")

# --- BAGIAN UTAMA APLIKASI ---
def main():
    st.set_page_config(page_title="Kenangan Kita Bersama", layout="wide")
    
    css_lengkap = """
        <style>
            /* Sembunyikan elemen UI Streamlit default */
            #MainMenu {visibility: hidden;}
            div[data-testid="stMainMenu"] {visibility: hidden;}
            
            footer {visibility: hidden;}
            
            header[data-testid="stHeader"] {visibility: hidden;} /* Untuk Streamlit versi lama */
            div[data-testid="stHeader"] {visibility: hidden;} /* Untuk Streamlit versi lebih baru */

            /* Menghilangkan padding atas yang biasanya dibuat oleh header yang disembunyikan */
            .main .block-container { 
                padding-top: 1rem; 
                padding-bottom: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            /* CSS Tombol Splash Screen */
            div.stButton > button {
                display: block;
                width: 100%;
                padding: 1rem 1.5rem;
                font-size: 1.25rem;
                font-weight: bold;
                color: white;
                background: linear-gradient(to right, #ff7e5f, #feb47b); /* Warna Gradasi Orange-Peach */
                border: none;
                border-radius: 12px; /* Sedikit lebih bulat */
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease-in-out;
                cursor: pointer;
            }
            div.stButton > button:hover {
                background: linear-gradient(to right, #feb47b, #ff7e5f); /* Gradasi dibalik saat hover */
                box-shadow: 0 7px 20px rgba(0, 0, 0, 0.3);
                transform: translateY(-3px); /* Efek mengangkat sedikit */
            }
            div.stButton > button:active {
                transform: translateY(0);
                box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            }

        </style>
    """
    st.markdown(css_lengkap, unsafe_allow_html=True)

    # --- Deteksi Tipe Perangkat (PC atau Bukan) ---
    if 'device_type_determined' not in st.session_state:
        st.session_state.device_type_determined = False
        st.session_state.is_session_pc = True # Default sementara ke PC

    if not st.session_state.device_type_determined:
        # `st_javascript` akan mengembalikan None pada run pertama, 
        # lalu user agent string pada run kedua (setelah JS di client tereksekusi)
        ua_string = st_javascript("window.navigator.userAgent;")
        
        if ua_string: # Jika ua_string sudah didapatkan (bukan None)
            user_agent = parse(ua_string)
            st.session_state.is_session_pc = user_agent.is_pc
            st.session_state.device_type_determined = True
            # st.sidebar.info(f"UA: {ua_string[:30]}...") # Untuk debug
            # st.sidebar.info(f"Deteksi Perangkat: {'PC' if st.session_state.is_session_pc else 'Non-PC'}") # Untuk debug
            st.rerun() # Penting untuk me-render ulang dengan state yang benar
        # else:
            # Saat ua_string masih None (pada run pertama sebelum JS kembali),
            # aplikasi akan berjalan dengan default is_session_pc = True.
            # st.rerun() di atas akan memastikan ini segera dikoreksi.
            # Anda bisa menampilkan pesan "Mendeteksi tipe perangkat..." di sini jika mau.
            # st.info("Mendeteksi tipe perangkat...")


    query_params = st.query_params
    script_dir = Path(__file__).parent.resolve()

    # ... (kode debug query params Anda di sidebar bisa tetap di sini) ...

    if 'app_step' not in st.session_state:
        st.session_state.app_step = "splash_screen"
    if 'nama_folder_teman_valid' not in st.session_state:
        st.session_state.nama_folder_teman_valid = None
    if 'audio_player_rendered' not in st.session_state:
        st.session_state.audio_player_rendered = False

    if st.session_state.app_step == "splash_screen":
        st.session_state.audio_player_rendered = False
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("<br>"*8, unsafe_allow_html=True)
            # ... (kode CSS tombol Anda) ...
            st.markdown("""
            <style> 
                /* ... CSS Anda ... */ 
            </style>
            """, unsafe_allow_html=True)

            # Mendapatkan token dari URL (logika Anda sudah benar)
            token_l_value_raw = query_params.get("l")
            token_L_value_raw = query_params.get("L")
            actual_token_l = token_l_value_raw[0] if isinstance(token_l_value_raw, list) and token_l_value_raw else token_l_value_raw
            actual_token_L = token_L_value_raw[0] if isinstance(token_L_value_raw, list) and token_L_value_raw else token_L_value_raw
            raw_token_from_url = actual_token_L if actual_token_L is not None else actual_token_l
            token_untuk_lookup = raw_token_from_url.lower() if raw_token_from_url else None

            if st.button("SIAP KAH GUSYY? ✨ *penceten rek", key="tombol_siap_splash"):
                if token_untuk_lookup and token_untuk_lookup in TOKEN_MAPPING:
                    st.session_state.nama_folder_teman_valid = TOKEN_MAPPING[token_untuk_lookup]
                    st.session_state.app_step = "show_gallery_and_play_music"
                    st.rerun()
                else:
                    # ... (logika error token Anda) ...
                    if raw_token_from_url:
                        st.error(f"🚫 LINK dengan kode '{raw_token_from_url}' SALAH atau TIDAK VALID!")
                    else:
                        st.error("🚫 UDAH GAUSA KEPO AH. URL butuh kode token.")
            
            st.markdown("<br>"*8, unsafe_allow_html=True)
            if not raw_token_from_url:
                st.info("NYARI APA SI?? (Tips: URL-nya kurang kode token)")


    elif st.session_state.app_step == "show_gallery_and_play_music":
        nama_folder_teman = st.session_state.nama_folder_teman_valid
        if not nama_folder_teman:
            st.error("Sesi token tidak valid. Kembali ke halaman awal.")
            st.session_state.app_step = "splash_screen"
            if st.button("Kembali"): st.rerun()
            return

        nama_teman_display = nama_folder_teman
        st.title(f"💌 Pesan & Galeri untuk {nama_teman_display} 🎞️")
        
        # Ambil pesan berdasarkan nama_folder_teman ("Kamasa", "Clea", dll.)
        pesan_spesifik = PESAN_UNTUK_TEMAN.get(nama_folder_teman, PESAN_UNTUK_TEMAN["default"])
        # Pastikan CSS pesan Anda sudah benar di sini
        st.markdown(
            f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px 25px; 
                        margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: left;">
                <h4 style="margin-top:0; margin-bottom:10px; ">Untukmu, {nama_teman_display}...</h4>
                <hr style="border-top: 1px solid #eee; margin-bottom: 15px;">
                <p style="white-space: pre-wrap; line-height: 1.6; ">{pesan_spesifik}</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("---") # Pemisah sebelum audio

        if not st.session_state.audio_player_rendered:
            path_musik_str = str(script_dir / NAMA_FOLDER_MEDIA_UTAMA / NAMA_FILE_MUSIK_LATAR)
            try:
                with open(path_musik_str, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mpeg', start_time=0, autoplay=True, loop=True)
                st.session_state.audio_player_rendered = True
            except FileNotFoundError:
                st.error(f"PY: File musik '{NAMA_FILE_MUSIK_LATAR}' TIDAK DITEMUKAN.")
                st.session_state.audio_player_rendered = True
            except Exception as e:
                st.error(f"PY: Gagal memuat musik: {e}")
                st.session_state.audio_player_rendered = True
        
        # --- Penentuan Jumlah Kolom Berdasarkan Deteksi Perangkat ---
        is_pc = st.session_state.get('is_session_pc', True) # Ambil dari session_state, default ke True (PC)
        
        if is_pc:
            jumlah_kolom_galeri = JUMLAH_KOLOM_GRID_DEFAULT
            # st.sidebar.info(f"Layout: PC ({jumlah_kolom_galeri} kolom)") # Untuk debug
        else:
            jumlah_kolom_galeri = 1
            # st.sidebar.info(f"Layout: Non-PC ({jumlah_kolom_galeri} kolom)") # Untuk debug
        

        tampilkan_konten_media(nama_folder_teman, jumlah_kolom_galeri)

    else:
        st.warning("Halaman tidak ditemukan.")
        st.session_state.app_step = "splash_screen"
        if st.button("Kembali"): st.rerun()

if __name__ == "__main__":
    main()