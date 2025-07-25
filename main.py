import streamlit as st
import pandas as pd
import numpy as np

# === PAGE CONFIG ===
st.set_page_config(page_title="SPK Investasi Mahasiswa", layout="wide")

# === BAHASA ===
if 'language' not in st.session_state:
    st.session_state.language = 'id'
lang = st.session_state.language

labels = {
    'id': {
        'title': "📊 Sistem Pendukung Keputusan Investasi Usaha Mahasiswa",
        'manual': "📝 Input Manual",
        'upload': "📁 Upload File",
        'profile': "👤 Profil Usaha",
        'num_usaha': "Jumlah Usaha",
        'save': "💾 Simpan & Tampilkan Hasil",
        'download_template': "⬇️ Unduh Template Kosong (CSV)",
        'upload_prompt': "Unggah file CSV",
        'data_usaha': "📄 Data Usaha Mahasiswa",
        'bobot': "📌 Bobot Kriteria (Metode CRITIC)",
        'hasil': "📈 Hasil Rekomendasi Investasi",
        'download_hasil': "💾 Unduh Hasil",
        'change_lang': "🇬🇧 English",
        'kriteria': ['ROI (%)', 'Modal Awal (Rp)', 'Pendapatan Rata-Rata 3 Bulan (Rp)', 'Aset (Rp)',
                     'Inovasi Produk (1-5)', 'Peluang Pasar (1-5)', 'Tingkat Risiko (1-5)'],
        'nama_usaha': 'Nama Usaha',
        'tambah_profil': "➕ Tambah Profil Usaha",
        'hapus_profil': "🗑️ Hapus Profil",
        'batal': "Batal",
        'status': {
            'sangat_layak': "Sangat Layak",
            'layak': "Layak",
            'cukup_layak': "Cukup Layak",
            'kurang_layak': "Kurang Layak",
            'tidak_layak': "Tidak Layak"
        }
        

    },
    'en': {
        'title': "📊 Decision Support System for Student Business Investment",
        'manual': "📝 Manual Input",
        'upload': "📁 Upload File",
        'profile': "👤 Business Profiles",
        'num_usaha': "Number of Businesses",
        'save': "💾 Save & Show Result",
        'download_template': "⬇️ Download Blank Template (CSV)",
        'upload_prompt': "Upload CSV file",
        'data_usaha': "📄 Student Business Data",
        'bobot': "📌 Criteria Weights (CRITIC Method)",
        'hasil': "📈 Investment Recommendation Result",
        'download_hasil': "💾 Download Result",
        'change_lang': "🇮🇩 Bahasa Indonesia",
        'kriteria': ['ROI (%)', 'Initial Capital (Rp)', 'Avg. 3-Month Revenue (Rp)', 'Assets (Rp)',
                     'Product Innovation (1-5)', 'Market Opportunity (1-5)', 'Risk Level (1-5)'],
        'nama_usaha': 'Business Name',
        'tambah_profil': "➕ Add Business Profile",
        'hapus_profil': "🗑️ Delete Profile",
        'batal': "Cancel",
        'status': {
            'sangat_layak': "Highly Recommended",
            'layak': "Recommended",
            'cukup_layak': "Moderately Recommended",
            'kurang_layak': "Less Recommended",
            'tidak_layak': "Not Recommended"
        }
    }
}

# === Mapping Bahasa untuk Kategori Usaha ===
kategori_mapping = {
    'id': {
        'F&B': 'F&B',
        'Fashion': 'Fashion',
        'Jasa': 'Jasa',
        'Digital': 'Digital',
        'Lainnya': 'Lainnya'
    },
    'en': {
        'F&B': 'F&B',
        'Fashion': 'Fashion',
        'Jasa': 'Services',
        'Digital': 'Digital',
        'Lainnya': 'Others'
    }
}

standard_kriteria = ['ROI (%)', 'Modal Awal (Rp)', 'Pendapatan Rata-Rata 3 Bulan (Rp)',
                     'Aset (Rp)', 'Inovasi Produk (1-5)', 'Peluang Pasar (1-5)', 'Tingkat Risiko (1-5)']

# === STYLING ===
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #EAF4FF;
        border-right: 1px solid #D0E3F1;
    }
    div.stButton > button {
        width: 100%;
        background-color: #2196F3;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.6em 1.2em;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0b7dda;
    }
    .stDownloadButton button {
        width: 100%;
        background-color: #00BFFF;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        margin-bottom: 10px;
    }
    .dataframe th {
        background-color: #F0F8FF;
    }
    .dataframe td {
        text-align: center;
        padding: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# === SIDEBAR ===
st.sidebar.title("SPK Investasi Mahasiswa" if lang == 'id' else "Decision Support System")
manual_click = st.sidebar.button(labels[lang]['manual'], key="btn_manual")
upload_click = st.sidebar.button(labels[lang]['upload'], key="btn_upload")
profile_click = st.sidebar.button(labels[lang]['profile'], key="btn_profile")
with st.sidebar:
    st.markdown("---")
    if st.button(labels[lang]['change_lang']):
        st.session_state.language = 'en' if lang == 'id' else 'id'
        st.rerun()

if 'input_method' not in st.session_state:
    st.session_state.input_method = "Manual"
if manual_click:
    st.session_state.input_method = "Manual"
if upload_click:
    st.session_state.input_method = "Upload"
if profile_click:
    st.session_state.input_method = "Profile"
input_method = st.session_state.input_method

# === FUNGSI ===
def calculate_critic(data, cost_indices=[]):
    data_normalized = data.copy()
    for i, col in enumerate(data.columns):
        if i in cost_indices:
            data_normalized[col] = data[col].min() / data[col]
        else:
            data_normalized[col] = data[col] / data[col].max()
    std_dev = data_normalized.std()
    corr_matrix = data_normalized.corr()
    conflict = 1 - corr_matrix.abs()
    info = std_dev * conflict.sum()
    weights = info / info.sum()
    return weights, data_normalized

def calculate_codas(data_normalized, weights):
    weighted_data = data_normalized * weights.values
    ideal_solution = weighted_data.min()
    euclidean = np.sqrt(((weighted_data - ideal_solution) ** 2).sum(axis=1))
    taxicab = np.abs(weighted_data - ideal_solution).sum(axis=1)
    score = euclidean + taxicab
    return (score - score.min()) / (score.max() - score.min())

def get_status_and_recommendation(score, modal_awal):
    stts = labels[lang]['status']
    if score >= 0.81:
        return stts['sangat_layak'], modal_awal * 0.60
    elif score >= 0.61:
        return stts['layak'], modal_awal * 0.45
    elif score >= 0.41:
        return stts['cukup_layak'], modal_awal * 0.30
    elif score >= 0.21:
        return stts['kurang_layak'], modal_awal * 0.15
    else:
        return stts['tidak_layak'], 0.0

# === MAIN ===
st.title(labels[lang]['title'])
df_usaha = None

import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="spk_investasi"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Koneksi ke database gagal: {err}")
        return None


def load_profiles_from_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profil_usaha")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)

def insert_profile(nama, deskripsi, kategori):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO profil_usaha (nama_usaha, deskripsi, kategori) VALUES (%s, %s, %s)",
                       (nama, deskripsi, kategori))
        conn.commit()
    except Exception as e:
        st.error(f"Gagal menyimpan ke database: {e}")
    finally:
        conn.close()

def delete_profile(profile_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profil_usaha WHERE id = %s", (profile_id,))
    conn.commit()
    conn.close()

# === Halaman Profil Usaha ===
if input_method == "Profile":
    st.subheader(labels[lang]['profile'])

    # Inisialisasi popup
    if 'show_add_popup' not in st.session_state:
        st.session_state.show_add_popup = False

    # Tombol tambah (trigger popup)
    if st.button(labels[lang]['tambah_profil']):
        st.session_state.show_add_popup = True

    # Popup Form Tambah Profil
    if st.session_state.show_add_popup:
        st.markdown("### Tambah Profil Usaha" if lang == 'id' else "### Add Business Profile")
        with st.form("popup_add_profile"):
            nama_usaha = st.text_input("Nama Usaha" if lang == 'id' else "Business Name")
            deskripsi = st.text_area("Deskripsi" if lang == 'id' else "Description")
            kategori = st.selectbox("Kategori" if lang == 'id' else "Category", options=["F&B", "Fashion", "Jasa", "Digital", "Lainnya"])
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button(labels[lang]['tambah_profil'])
            with col2:
                cancel = st.form_submit_button(labels[lang]['batal'])

            if submitted and nama_usaha:
                insert_profile(nama_usaha, deskripsi, kategori)
                st.session_state.show_add_popup = False
                st.success("Profil usaha ditambahkan!")
                st.rerun()
            if cancel:
                st.session_state.show_add_popup = False
                st.rerun()

    # Load dan tampilkan profil dalam bentuk tabel
    st.markdown("### Daftar Profil Usaha" if lang == 'id' else "### List of Business Profiles")
    df_profiles = load_profiles_from_db()
    # Terjemahkan kategori sesuai bahasa
    df_profiles['kategori'] = df_profiles['kategori'].map(kategori_mapping[lang])


    if not df_profiles.empty:
        df_show = df_profiles[['id', 'nama_usaha', 'deskripsi', 'kategori']].rename(columns={
            'id': 'ID',
            'nama_usaha': 'Nama Usaha' if lang == 'id' else 'Business Name',
            'deskripsi': 'Deskripsi' if lang == 'id' else 'Description',
            'kategori': 'Kategori' if lang == 'id' else 'Category'
        })

        st.dataframe(df_show, use_container_width=True)

        selected_id = st.selectbox(
            "📌 Pilih ID untuk dihapus:" if lang == 'id' else "📌 Select ID to delete:",
            df_profiles['id'],
            format_func=lambda x: f"{x} - {df_profiles.loc[df_profiles['id'] == x, 'nama_usaha'].values[0]}"
        )
        if st.button(labels[lang]['hapus_profil']):
            delete_profile(selected_id)
            st.success("Profil berhasil dihapus!")
            st.rerun()
    else:
        st.info("Belum ada profil usaha." if lang == 'id' else "No business profiles yet.")

# === Halaman Input Manual ===
elif input_method == "Manual":
    st.subheader(labels[lang]['manual'])
    num = st.number_input(labels[lang]['num_usaha'], min_value=1, max_value=20, step=1)
    default_data = pd.DataFrame({
        labels[lang]['nama_usaha']: [f"Business {i+1}" if lang == 'en' else f"Usaha {i+1}" for i in range(num)],
        **{col: [0.0]*num for col in labels[lang]['kriteria']}
    })
    df_input = st.data_editor(default_data, use_container_width=True, num_rows="dynamic")
    if st.button(labels[lang]['save'], key="process_manual"):
        df_usaha = df_input.copy()

# === Halaman Upload File ===
elif input_method == "Upload":
    st.subheader(labels[lang]['upload'])
    template_df = pd.DataFrame({
        labels[lang]['nama_usaha']: [""],
        **{col: [0.0] for col in labels[lang]['kriteria']}
    })
    template_csv = template_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=labels[lang]['download_template'],
        data=template_csv,
        file_name='template_input_usaha.csv',
        mime='text/csv'
    )
    uploaded_file = st.file_uploader(labels[lang]['upload_prompt'], type=["csv"])
    if uploaded_file is not None:
        try:
            df_usaha = pd.read_csv(uploaded_file)
            missing = set(labels[lang]['kriteria']) - set(df_usaha.columns)
            if missing:
                st.error("❌ Kolom berikut tidak ditemukan: " + ", ".join(missing))
                df_usaha = None
            else:
                st.success("✅ Data berhasil dimuat!" if lang == 'id' else "✅ File loaded successfully!")
        except Exception as e:
            st.error(f"Gagal membaca file: {e}" if lang == 'id' else f"Failed to read file: {e}")

# === Perhitungan CRITIC & CODAS ===
if df_usaha is not None:
    st.subheader(labels[lang]['data_usaha'])
    st.dataframe(df_usaha.reset_index(drop=True), use_container_width=True)

    col_map = dict(zip(labels[lang]['kriteria'], standard_kriteria))
    df_kriteria = df_usaha.rename(columns=col_map)[standard_kriteria].apply(pd.to_numeric, errors='coerce').fillna(0)

    weights, data_normalized = calculate_critic(df_kriteria, cost_indices=[1, 6])

    st.subheader(labels[lang]['bobot'])
    st.write(weights)

    df_usaha['Skor CODAS'] = calculate_codas(data_normalized, weights)
    df_usaha['Peringkat'] = df_usaha['Skor CODAS'].rank(ascending=False, method='min').astype(int)
    df_usaha['Status Kelayakan'], df_usaha['Rekomendasi Investasi (Rp)'] = zip(
        *[get_status_and_recommendation(score, modal) for score, modal in zip(df_usaha['Skor CODAS'], df_kriteria['Modal Awal (Rp)'])])

    st.subheader(labels[lang]['hasil'])
    df_usaha[labels[lang]['nama_usaha']] = df_usaha[labels[lang]['nama_usaha']].fillna("-")
    df_output = df_usaha[['Peringkat', labels[lang]['nama_usaha'], 'Skor CODAS', 'Status Kelayakan', 'Rekomendasi Investasi (Rp)']]
    df_output = df_output.sort_values(by='Peringkat').reset_index(drop=True)

    st.dataframe(
        df_output.style.format({
            "Skor CODAS": "{:.4f}",
            "Rekomendasi Investasi (Rp)": "Rp {:,.0f}"
        }).set_properties(**{'text-align': 'center'}).set_properties(
            subset=[labels[lang]['nama_usaha']], **{'text-align': 'left'}),
        use_container_width=True
    )

    csv = df_output.to_csv(index=False)
    st.download_button(labels[lang]['download_hasil'], data=csv, file_name="hasil_investasi.csv", mime="text/csv")