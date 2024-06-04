# Modules
import pyrebase
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
# Import File
from kalkulator import KalkulatorKalori
from food_recom import FoodRecom

# Nama Tab Browser
st.set_page_config(
    page_title = "HealthyMe Apps", page_icon = "🍽️"
)

# Menambahkan CSS untuk mengganti background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("D:\KULIAH\MSIB\Skilvul\Learn\Capstone\asset\1.png");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# === Kodebaru P1 ===
# Inisialisasi sesi pengguna
if 'user' not in st.session_state:
    st.session_state['user'] = None
# === Kodebaru P1 ===

def signup(email, password, full_name, phone):
    try:
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
    except:
        st.error("Terjadi kesalahan saat membuat akun. Pastikan email belum terdaftar dan password minimal 6 karakter.")

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

# ==== Kode Baru P1 ===
def show_login_signup():
    # Main Konten Page Login
    st.title("HealtyMe Aplikasi Web")

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
    with st.sidebar:
        st.header("Setelah login ")

        selected = option_menu(None, ["Home", 'BMI Calculator','Rekomendasi Menu', 'Tips','Tentang Kami'], 
            icons=['house', 'calculator','book', 'heart', 'inbox'])
        
        if st.button("Logout"):
            logout()
            st.rerun()
        return selected   
     
# Halaman Utama Setelah Login
def show_main_app():
    selected = sidebar_main_app()

    # Menampilkan informasi pengguna dan konten halaman utama di luar blok sidebar
    user_info = db.child("users").child(st.session_state['user']['localId']).get().val()

    st.write("Selamat datang, ", user_info['full_name'], "👋")

    if selected == "Home":
        st.title("Halaman Utama")
        st.write("Konten untuk Halaman Utama")

    elif selected == "BMI Calculator":
        KalkulatorKalori().show()

    elif selected == "Rekomendasi Menu":
        FoodRecom().show()

# Logika utama untuk menampilkan halaman yang sesuai
if st.session_state['user'] is None:
    show_login_signup()
else:
    show_main_app()
