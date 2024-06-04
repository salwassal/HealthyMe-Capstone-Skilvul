import streamlit as st

class KalkulatorKalori:
    def show(self):
        # Fungsi untuk menghitung BMI
        def calculate_bmi(weight, height):
            height_m = height / 100
            return weight / (height_m ** 2)
        
        # Fungsi untuk menentukan kategori BMI
        def determine_bmi_category(bmi):
            if bmi < 18.5:
                return "Kurus (Kurang Berat Badan)"
            elif 18.5 <= bmi < 24.9:
                return "Normal (Berat Badan Ideal)"
            elif 25 <= bmi < 29.9:
                return "Berlebih Berat Badan"
            elif 30 <= bmi < 34.9:
                return "Obesitas Tingkat 1"
            elif 35 <= bmi < 39.9:
                return "Obesitas Tingkat 2 (Berisiko Tinggi)"
            else:
                return "Obesitas Tingkat 3 (Sangat Berisiko)"

        # Fungsi untuk menghitung berat badan ideal menggunakan Metode Devine
        def calculate_ideal_weight_devine(gender, height):
            height_in = height / 2.54
            if gender == 'Pria':
                return 50 + 2.3 * (height_in - 60)
            else:
                return 45.5 + 2.3 * (height_in - 60)

        # Fungsi untuk menghitung BMR menggunakan berat badan ideal
        def calculate_bmr_mifflin(gender, weight, height, age):
            if gender == 'Pria':
                return (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                return (10 * weight) + (6.25 * height) - (5 * age) - 161

        # Fungsi untuk menghitung TDEE berdasarkan BMR dan tingkat aktivitas
        def calculate_tdee(bmr, activity_level):
            if activity_level == 'Sangat tidak aktif':
                return bmr * 1.2
            elif activity_level == 'Ringan aktif':
                return bmr * 1.375
            elif activity_level == 'Sedang aktif':
                return bmr * 1.55
            elif activity_level == 'Sangat aktif':
                return bmr * 1.725
            else:
                return bmr * 1.9
            
        # Fungsi untuk menentukan distribusi makronutrien
        def calculate_macros(tdee, goal):
            if goal == 'Menurunkan Berat Badan':
                tdee -= 500
            elif goal == 'Menambah Berat Badan':
                tdee += 500

            carbs = 0.5 * tdee / 4  # 4 kalori per gram karbohidrat, 0.5  ratio makronutrien
            protein = 0.3 * tdee / 4  # 4 kalori per gram protein, 0.3  ratio makronutrien
            fat = 0.2 * tdee / 9  # 9 kalori per gram lemak, 0.2  ratio makronutrien

            return tdee, carbs, protein, fat

        st.title("Kalkulator Kebutuhan Kalori dan Makronutrien Harian")

        gender = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"])
        weight = st.number_input("Berat Badan (kg)", min_value=0.0, format="%.2f")
        height = st.number_input("Tinggi Badan (cm)", min_value=0.0, format="%.2f")
        age = st.number_input("Usia (tahun)", min_value=0, format="%d")
        activity_level = st.selectbox("Tingkat Aktivitas", ["Sangat tidak aktif", "Ringan aktif", "Sedang aktif", "Sangat aktif", "Ekstrem aktif"])
        goal = st.selectbox("Tujuan", ["Menurunkan Berat Badan", "Mempertahankan Berat Badan", "Menambah Berat Badan"])


        if st.button("Hitung"):
            # Hitung BMI
            bmi = calculate_bmi(weight, height)
            bmi_category = determine_bmi_category(bmi)

            # Hitung berat badan ideal menggunakan Metode Devine
            ideal_weight = calculate_ideal_weight_devine(gender, height)
            
            # Hitung BMR menggunakan berat badan ideal
            bmr = calculate_bmr_mifflin(gender, ideal_weight, height, age)
            
            # Hitung TDEE berdasarkan BMR dan tingkat aktivitas
            tdee = calculate_tdee(bmr, activity_level)
            
            # Hitung distribusi makronutrien dan kalori harian
            adjusted_tdee, carbs, protein, fat = calculate_macros(tdee, goal)
            
            st.subheader("Hasil Perhitungan Nutrisi Harian")
            st.write(f"BMI: {bmi:.2f} (Kategori: {bmi_category})")
            st.write(f"Berat Badan Ideal (Metode Devine): {ideal_weight:.2f} kg")
            st.write(f"BMR (menggunakan berat badan ideal): {bmr:.2f} kalori/hari")
            st.write(f"TDEE (Total Kebutuhan Kalori Harian): {tdee:.2f} kalori/hari")
            st.write(f"Kebutuhan Kalori Harian (disesuaikan dengan tujuan): {adjusted_tdee:.2f} kalori/hari")
            st.write(f"Karbohidrat: {carbs:.2f} gram/hari")
            st.write(f"Protein: {protein:.2f} gram/hari")
            st.write(f"Lemak: {fat:.2f} gram/hari")