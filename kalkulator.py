import streamlit as st

class KalkulatorKalori:
    def show(self):
        st.title("Pengukuran Kalori")
        berat_badan = st.number_input("Masukkan berat badan Anda (kg)")
        tinggi_badan = st.number_input("Masukkan tinggi badan Anda (cm)")
        usia = st.number_input("Masukkan usia Anda (tahun)")
        jenis_kelamin = st.selectbox("Pilih jenis kelamin", ["Laki-laki", "Perempuan"])

        if st.button("Hitung Kalori"):
            if jenis_kelamin == "Laki-laki":
                bmr = 88.362 + (13.397 * berat_badan) + (4.799 * tinggi_badan) - (5.677 * usia)
            else:
                bmr = 447.593 + (9.247 * berat_badan) + (3.098 * tinggi_badan) - (4.330 * usia)
            
            st.write(f"Kebutuhan kalori harian Anda adalah {bmr:.2f} kkal")
