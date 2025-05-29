import streamlit as st
import os
from pathlib import Path
import base64 # Masih ada, tapi tidak digunakan untuk audio utama sekarang

# --- KONFIGURASI APLIKASI ---
NAMA_FOLDER_MEDIA_UTAMA = "media"
EKSTENSI_GAMBAR_DIDUKUNG = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
EKSTENSI_VIDEO_DIDUKUNG = ('.mp4', '.mov', '.avi', '.mkv')
JUMLAH_KOLOM_GRID = 3
NAMA_FILE_MUSIK_LATAR = "everything u are.mp3"

# TOKEN_MAPPING dengan nilai Kapital (sesuai nama folder aktual Anda di Git)
TOKEN_MAPPING = {
    "a1b": "Clea",
    "7c2": "Meldi",
    "k9p": "Adinda",
    "z3x": "Farah",
    "6xd": "Kamasa",
    "7ds": "Gadiza",
    "9eh": "Arya",
    "0sn": "Andre",
    "m5q": "Annisa"
}

# PESAN_UNTUK_TEMAN dengan key Kapital agar cocok dengan nilai dari TOKEN_MAPPING
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
    "Meldi": "Pesan untuk Meldi...", # Tambahkan pesan sesuai kebutuhan
    "Adinda": "Pesan untuk Adinda...",
    "Farah": "Pesan untuk Farah...",
    "Gadiza": "Pesan untuk Gadiza...",
    "Arya": "Pesan untuk Arya...",
    "Andre": "Pesan untuk Andre...",
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

    file_media_list.sort(key=lambda x: x.name)
    return file_media_list, None

# get_audio_b64_and_mimetype tidak digunakan lagi untuk st.audio, tapi bisa disimpan jika perlu
# def get_audio_b64_and_mimetype(path_file_musik_str): ...

# --- FUNGSI TAMPILAN GALERI KONTEN ---
def tampilkan_konten_media(nama_folder_teman_valid):
    script_dir = Path(__file__).parent.resolve()
    # Debug path konten di sidebar bisa dipertahankan jika masih perlu
    with st.sidebar:
        st.markdown("---")
        st.subheader(f"🔧 Debug Path Konten untuk: '{nama_folder_teman_valid}'")
        abs_path_media_utama = script_dir / NAMA_FOLDER_MEDIA_UTAMA
        abs_path_folder_teman = abs_path_media_utama / nama_folder_teman_valid
        st.write(f"Path target ke folder teman: `{abs_path_folder_teman}`")
        if abs_path_folder_teman.exists() and abs_path_folder_teman.is_dir():
            st.success(f"✅ Folder teman ('{nama_folder_teman_valid}') DITEMUKAN.")
            try:
                st.write(f"Isi (awal): `{os.listdir(abs_path_folder_teman)[:5]}`")
            except Exception: pass
        else:
            st.error(f"❌ Folder teman ('{nama_folder_teman_valid}') TIDAK DITEMUKAN di `{abs_path_folder_teman}`.")
        st.markdown("---")

    PATH_FOLDER_TEMAN = script_dir / NAMA_FOLDER_MEDIA_UTAMA / nama_folder_teman_valid
    file_media, status_error = dapatkan_file_media(PATH_FOLDER_TEMAN)

    if status_error == "error_folder_tidak_ditemukan":
        st.error(f"⚠️ Folder media untuk '{nama_folder_teman_valid.capitalize()}' (di '{PATH_FOLDER_TEMAN}') tidak ditemukan!")
        st.info(f"Pastikan ada folder bernama '{nama_folder_teman_valid}' (sesuai kapitalisasi di TOKEN_MAPPING) di dalam '{NAMA_FOLDER_MEDIA_UTAMA}'. Periksa juga Git Anda.")
        return
    elif status_error == "error_tidak_ada_file_visual":
        st.warning(f"📂 Folder '{nama_folder_teman_valid.capitalize()}' kosong atau tidak berisi file media (gambar/video).")
        return
    
    if file_media:
        st.success(f"Menampilkan {len(file_media)} kenangan indah untukmu, {nama_folder_teman_valid.capitalize()}!")
        st.balloons()

        cols_grid = st.columns(JUMLAH_KOLOM_GRID)
        for i, media_file_path_obj in enumerate(file_media):
            kolom_saat_ini = cols_grid[i % JUMLAH_KOLOM_GRID]
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

    query_params = st.query_params
    script_dir = Path(__file__).parent.resolve()

    with st.sidebar:
        st.subheader("🔧 Debug Info: Query Params")
        token_l_value_raw = query_params.get("l")
        token_L_value_raw = query_params.get("L")
        actual_token_l = token_l_value_raw[0] if isinstance(token_l_value_raw, list) and token_l_value_raw else token_l_value_raw
        actual_token_L = token_L_value_raw[0] if isinstance(token_L_value_raw, list) and token_L_value_raw else token_L_value_raw
        st.write(f"Dari 'l': `{actual_token_l}`, Dari 'L': `{actual_token_L}`")

        raw_token_from_url = actual_token_L if actual_token_L is not None else actual_token_l
        token_untuk_lookup = raw_token_from_url.lower() if raw_token_from_url else None
        
        st.subheader("🔧 Token Diproses")
        st.write(f"Token mentah URL: `{raw_token_from_url}`")
        st.write(f"Token lookup (lowercase): `{token_untuk_lookup}`")


    if 'app_step' not in st.session_state:
        st.session_state.app_step = "splash_screen"
    if 'nama_folder_teman_valid' not in st.session_state:
        st.session_state.nama_folder_teman_valid = None
    # Hapus state lama untuk JS player, ganti dengan state untuk st.audio jika perlu
    if 'audio_player_rendered' not in st.session_state:
        st.session_state.audio_player_rendered = False


    if st.session_state.app_step == "splash_screen":
        st.session_state.audio_player_rendered = False # Reset saat kembali ke splash
        
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("<br>"*8, unsafe_allow_html=True)
            st.markdown("""
            <style>
                div.stButton > button {
                    display: block; width: 100%; padding: 1rem 1.5rem;
                    font-size: 1.25rem; font-weight: bold; color: white;
                    background: linear-gradient(to right, #ff7e5f, #feb47b);
                    border: none; border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    transition: all 0.3s ease; cursor: pointer;
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
                # Pastikan TOKEN_MAPPING keys adalah lowercase untuk dicocokkan dengan token_untuk_lookup
                # Contoh: "6xd" (lowercase) di TOKEN_MAPPING.keys()
                if token_untuk_lookup and token_untuk_lookup in TOKEN_MAPPING:
                    st.session_state.nama_folder_teman_valid = TOKEN_MAPPING[token_untuk_lookup] # Mendapat "Kamasa", dll.
                    st.session_state.app_step = "show_gallery_and_play_music"
                    st.rerun()
                else:
                    if raw_token_from_url:
                        st.error(f"🚫 LINK dengan kode '{raw_token_from_url}' SALAH atau TIDAK VALID!")
                        st.info("Pastikan kode di URL adalah salah satu dari: " + ", ".join(TOKEN_MAPPING.keys()))
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

        nama_teman_display = nama_folder_teman # Sudah dikapitalisasi dari TOKEN_MAPPING
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

        # --- MENGGUNAKAN st.audio() UNTUK MUSIK LATAR ---
        if not st.session_state.audio_player_rendered:
            path_musik_str = str(script_dir / NAMA_FOLDER_MEDIA_UTAMA / NAMA_FILE_MUSIK_LATAR)
            st.write(f"PY: Mencoba memuat musik untuk st.audio dari: `{path_musik_str}`")

            try:
                with open(path_musik_str, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                # Menampilkan audio player standar Streamlit
                st.audio(audio_bytes, format='audio/mpeg', start_time=0, autoplay=True)
                st.success("PY: Audio player `st.audio` seharusnya tampil. Coba putar manual.")
                
                st.session_state.audio_player_rendered = True
            except FileNotFoundError:
                st.error(f"PY: File musik '{NAMA_FILE_MUSIK_LATAR}' TIDAK DITEMUKAN di `{path_musik_str}`. Pastikan file ada di server deploy dan path sudah benar.")
                st.session_state.audio_player_rendered = True # Tetap set agar tidak coba ulang terus
            except Exception as e:
                st.error(f"PY: Gagal memuat musik dengan st.audio: {e}")
                st.session_state.audio_player_rendered = True # Tetap set
        
        tampilkan_konten_media(nama_folder_teman)

    else:
        st.warning("Halaman tidak ditemukan.")
        st.session_state.app_step = "splash_screen"
        if st.button("Kembali"): st.rerun()

if __name__ == "__main__":
    main()