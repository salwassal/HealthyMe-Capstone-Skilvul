# Modules
import pyrebase
import streamlit as st
# Nama Tab Browser
st.set_page_config(
    page_title = "HealthyMe Apps", page_icon = "🍽️"
)
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import re 
from streamlit_lottie import st_lottie
import json
import os
# Import File
from kalkulator import KalkulatorKalori
from food_recom import FoodRecom
from tentang_kami import tentangkami

# Menambahkan CSS untuk mengganti background
st.markdown("""
    <style>
     .stApp {
        background-image: url("https://img.freepik.com/free-vector/blurred-white-background-with-shine-effect_1017-33200.jpg?t=st=1717596227~exp=1717599827~hmac=fd818c36fa40c8ee78e1ca882c4ef974970b4cca162b634a0267843fc19e21dc&w=826");
        background-size: cover;
        transition: background 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuration Key
firebaseConfig = {
    'apiKey'        : "AIzaSyB3PB9_Oa6EIbkWTMsxmWuu8ZxLFwREvlQ",
    'authDomain'    : "healtyme-6443f.firebaseapp.com",
    'projectId'     : "healtyme-6443f",
    'databaseURL'   : "https://healtyme-6443f-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket'     : "healtyme-6443f.appspot.com",
    'messagingSenderId' : "985856284247",
    'appId'             : "1:985856284247:web:d328708b2faa65268b7512",
    'measurementId'     : "G-J3Z1ERJZVB"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# Inisialisasi sesi pengguna
if 'user' not in st.session_state:
    st.session_state['user'] = None

def signup(email, password, full_name, phone):
    try:
        # Validasi input email
        if not email:
            st.error("Email tidak boleh kosong!")
            return

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Masukkan email yang valid!")
            return

        # Validasi input password
        if not password:
            st.error("Password tidak boleh kosong!")
            return

        elif len(password) < 6:
            st.error("Password harus memiliki minimal 6 karakter!")
            return

        user = auth.create_user_with_email_and_password(email, password)
        user_id = user['localId']
        # Simpan data diri pengguna di database
        data = {
            "full_name": full_name,
            "phone": phone,
            "email": email
        }
        db.child("users").child(user_id).set(data)
        st.success("Akun berhasil dibuat! Silakan login.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membuat akun: {str(e)}")
        return    

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        if user:
            st.session_state['user'] = {
                'localId': user['localId'],
                'email': email
            }
        st.success("Berhasil login!")
        return user
    except:
        st.error("Email atau password salah.")
        return None

def logout():
    st.session_state['user'] = None
    st.success("Berhasil logout!")

# Fungsi untuk memuat file Lottie
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def show_login_signup():
    # Main Konten Page Login
    st.title("Selamat datang di HealtyME: Teman Sehat Anda!")
    st.write("Temukan kesehatan melalui pola makan yang tepat.")
    st.write("Silakan login untuk mengakses fitur kalkulator BMI dan sistem rekomendasi makanan.")
    
# Menampilkan animasi Lottie
    lottie_path = os.path.join('asset', 'konselor_food.json')
    lottie_animation = load_lottiefile(lottie_path)
    st_lottie(lottie_animation, height=300)
    
    st.write("Kualitas hidup adalah pandangan setiap individu terhadap posisinya dalam kehidupan, salah satunya terkait masalah kesehatan. Menurut WHO, definisi sehat mencakup rumusan secara luas, yaitu keadaan yang sempurna baik fisik, mental maupun sosial, tidak hanya terbebas dari penyakit atau kelemahan/cacat. Menu makanan yang sehat menjadi pilihan bagi siapa saja yang menginginkan perihal diatas. Kriteria menu makanan sehat dan bergizi kerap sekali kita dengar dengan sebutan 4 sehat lima sempurna. Asupan nutrisi dan gizi seimbang setiap makanan beserta nilai gizi esensial tubuh mencakup kandungan vitamin, mineral, karbohidrat, protein, lemak,kalsium, serat dan air dapat membantu tubuh kita menghasilkan cukup energi untuk beraktivitas setiap hari.")
    st.write("Istilah piramida makanan menggambarkan bahwa asupan nutrisi untuk tubuh dapat dikatakan stabil dan sudah memenuhi kebutuhan gizi setiap harinya. Ilustrasi tersebut dapat membantu seseorang tentang gambaran jumlah porsi makan yang sesuai untuk dikonsumsi setiap hari dari masing-masing kelompok makanan. Kadar kandungan makanan tentunya berbeda-beda tiap jenisnya. Oleh karena itu, melalui adanya website berbasis rekomendasi makanan ini diharapkan mampu mendukung gaya hidup sehat sehingga dapat menekan jumlah angka penyakit akibat konsumsi makanan tidak sehat.")

    # Informasi tambahan tentang manfaat menggunakan HealtyME
    st.subheader("Mengapa Memilih HealtyME?")
    st.write("HealtyME dirancang untuk membantu Anda mencapai gaya hidup sehat dengan mudah dan menyenangkan.")

    # Menu di sidebar Page Login
    with st.sidebar:
        st.header("Autentikasi")
        if st.session_state['user'] is None:
            choice = st.radio("Pilih opsi", ["Login", "Signup"])

            if choice == "Signup":
                st.subheader("Buat Akun Baru")
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                full_name = st.text_input("Nama Lengkap", key="signup_full_name")
                phone = st.text_input("Nomor Telepon", key="signup_phone")
                if st.button("Daftar"):
                    signup(email, password, full_name, phone)

            elif choice == "Login":
                st.subheader("Masuk ke Akun")
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                if st.button("Masuk"):
                    user = login(email, password)
                    if user:
                        st.session_state['user'] = user
                        st.rerun()

def sidebar_main_app():
    # Menampilkan informasi pengguna dan konten halaman utama di luar blok sidebar
    user_info = db.child("users").child(st.session_state['user']['localId']).get().val()

    with st.sidebar:
        st.header(f"Selamat datang, {user_info['full_name']} 👋")

        selected = option_menu(None, ["Home", 'BMI Calculator','Rekomendasi Menu','FAQ'], 
            icons=['house', 'calculator','book','question-circle'])
        
        if st.button("Logout"):
            logout()
            st.rerun()
        return selected   
     
# Halaman Utama Setelah Login
def show_main_app():
    selected = sidebar_main_app()

    # Menampilkan informasi pengguna dan konten halaman utama di luar blok sidebar
    user_info = db.child("users").child(st.session_state['user']['localId']).get().val()

    if selected == "Home":
        st.title("Selamat Datang di HealthyMe")
        st.write("Mari memperoleh informasi tentang nutrisi harianmu dan rekomendasi makanan sehat setiap harinya. Ayo buat pilihan makanan sehatmu sendiri melalui saran nutrisi yang telah HealthyMe sediakan.")

        # Membuat DataFrame dari sumber data yang diunggah
        file_path = "nutrition.csv"
        df = pd.read_csv(file_path)

        # Membuat container untuk tabel dan grafik
        with st.container():
            # Tampilkan DataFrame sebagai tabel dengan AgGrid
            st.subheader("Data Nutrisi Makanan Sehat")
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True)  # Mengatur paginasi otomatis
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
            gb.configure_side_bar()  # Menambahkan sidebar untuk fitur pencarian
            gridOptions = gb.build()

            AgGrid(
                df,
                gridOptions=gridOptions,
                enable_enterprise_modules=True,
                update_mode='MODEL_CHANGED',
            
            )

            st.caption("Dataset di atas menunjukkan kandungan kalori, protein, lemak, dan karbohidrat dari berbagai makanan sehat.")

            # Layout grafik dalam satu baris dengan lebar penuh
            st.subheader("Scatter Plot Nutrisi Makanan Sehat")


   
            fig_scatter1 = px.scatter(df, x='calories', y='proteins', color='name',
                                        title='Scatter Plot Kalori vs Protein')
            st.plotly_chart(fig_scatter1, use_container_width=True)

            fig_scatter2 = px.scatter(df, x='calories', y='fat', color='name',
                                        title='Scatter Plot Kalori vs Lemak')
            st.plotly_chart(fig_scatter2, use_container_width=True)


    elif selected == "BMI Calculator":
        KalkulatorKalori().show()

    elif selected == "Rekomendasi Menu":
        FoodRecom().show()

    elif selected == "FAQ":
        tentangkami().show()

# Logika utama untuk menampilkan halaman yang sesuai
if st.session_state['user'] is None:
    show_login_signup()
else:
    show_main_app()
