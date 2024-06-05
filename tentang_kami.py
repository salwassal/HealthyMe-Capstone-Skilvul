import streamlit as st
import os

class tentangkami:
    def show(self):
        st.title("Frequently Asked Questions")
        st.write("Hal apa saja yang ingin kamu ketahui tentang HealthyMe?")
        faq = {
            "Apa itu HealthyMe?": "HealthyMe adalah sebuah Aplikasi Website yang memberikan sebuah solusi dengan menyediakan informasi yang akurat tentang gaya hidup sehat untuk meningkatkan kesadaran akan pentingnya pola hidup sehat. Dengan konten yang informatif dan mudah diakses, website ini diharapkan dapat mengubah persepsi bahwa pola hidup sehat adalah hal yang remeh. Tujuan utama dari website ini adalah mendorong perubahan positif dalam perilaku dan kebiasaan sehari-hari agar kesejahteraan jangka panjang dapat dijaga. ",
            "Bagaimana cara mengakses fitur fitur di HealthyMe?": " Anda dapat memilih menu Sign Up  dan mengiputkan Email dan Password. Kemudian, anda bisa memilih menu Sign In untuk masuk dan mengakses fitur fitur yang HealthyMe sediakan.",
            "Fitur apa saja yang disediakan HealthyMe?": "BMI Calculator untuk menghitung Body Mass Index lalu Rekomendasi Makanan untuk Plan kebutuhan kalori/hari",
        }
        for question, answer in faq.items():
            with st.expander(question):
                st.write(answer)
