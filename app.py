# Modules
import pyrebase
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import re 
# Import File
from kalkulator import KalkulatorKalori
from food_recom import FoodRecom

# Nama Tab Browser
st.set_page_config(
    page_title = "HealthyMe Apps", page_icon = "🍽️"
)

# # Menambahkan CSS untuk mengganti background
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-image: url("https://img.freepik.com/free-photo/delicious-breakfast-meal-composition_23-2148878838.jpg?t=st=1717472687~exp=1717476287~hmac=330df9123e31cbe475ce88a634794f92795ac3c20b650f0ef87f8ac23da9975f&w=1060");
#         background-size: cover;
#         transition: background 0.5s ease;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

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
    # except:
    #     st.error("Terjadi kesalahan saat membuat akun. Pastikan email belum terdaftar dan password minimal 6 karakter.")


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
    st.title("Selamat datang di HealtyME: Teman Sehat Anda!")
    st.write("Temukan kesehatan melalui pola makan yang tepat.")
    st.write("Silakan login untuk mengakses fitur kalkulator BMI dan sistem rekomendasi makanan.")

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
    with st.sidebar:
        st.header("Setelah login ")

        selected = option_menu(None, ["Home", 'BMI Calculator','Rekomendasi Menu'], 
            icons=['house', 'calculator','book'])
        
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
    st.divider()

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