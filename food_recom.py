import streamlit as st
import pickle
import pandas as pd
from sklearn.cluster import KMeans


class FoodRecom:
    def show(self):
        st.title("Rekomendasi Makanan")
        
        # Load the saved model
        with open('CP_kmeans.pkl', 'rb') as f:
            model = pickle.load(f)

        # Baca dataset
        food_df = pd.read_csv('nutrition.csv')

        # Dapatkan kebutuhan kalori, protein, dan karbohidrat harian user
        daily_calorie_needs = st.number_input("Masukkan kebutuhan kalori harian Anda:", min_value=1000, max_value=5000, step=100)
        daily_proteins_needs = st.number_input("Masukkan kebutuhan protein harian Anda (gram):", min_value=10, max_value=300, step=10)
        daily_carbs_needs = st.number_input("Masukkan kebutuhan karbohidrat harian Anda (gram):", min_value=50, max_value=500, step=10)


        if st.button("Generate Menu Makanan"):
            # Fungsi untuk merekomendasikan makanan berdasarkan kebutuhan user
            def recommend_foods(model, food_df, calorie_needs, proteins_needs, carbs_needs, excluded_foods):
                # Prediksi cluster untuk kebutuhan yang diberikan
                user_cluster = model.predict([[calorie_needs, proteins_needs, carbs_needs]])[0]
                
                # Dapatkan makanan dalam cluster yang sama
                food_df['cluster'] = model.predict(food_df[['calories', 'proteins', 'carbohydrate']])
                recommended_foods = food_df[(food_df['cluster'] == user_cluster) & (~food_df['name'].isin(excluded_foods))]
                
                # Filter makanan untuk mencocokkan kebutuhan kalori, protein, karbo dengan lebih dekat
                recommended_foods = recommended_foods.iloc[(recommended_foods[['calories', 'proteins', 'carbohydrate']] - [calorie_needs, proteins_needs, carbs_needs]).abs().sum(axis=1).argsort()[:5]]
                
                return recommended_foods

            # Hitung kebutuhan untuk setiap kali makan
            breakfast_needs = (daily_calorie_needs * 0.25, daily_proteins_needs * 0.25, daily_carbs_needs * 0.25)
            lunch_needs = (daily_calorie_needs * 0.30, daily_proteins_needs * 0.30, daily_carbs_needs * 0.30)
            snack_needs = (daily_calorie_needs * 0.15, daily_proteins_needs * 0.15, daily_carbs_needs * 0.15)
            dinner_needs = (daily_calorie_needs * 0.30, daily_proteins_needs * 0.30, daily_carbs_needs * 0.30)

            # Melacak makanan yang sudah direkomendasikan
            excluded_foods = []

            # Rekomendasikan makanan untuk setiap kali makan
            breakfast_recommendations = recommend_foods(model, food_df, *breakfast_needs, excluded_foods)
            excluded_foods.extend(breakfast_recommendations['name'].tolist())

            lunch_recommendations = recommend_foods(model, food_df, *lunch_needs, excluded_foods)
            excluded_foods.extend(lunch_recommendations['name'].tolist())

            snack_recommendations = recommend_foods(model, food_df, *snack_needs, excluded_foods)
            excluded_foods.extend(snack_recommendations['name'].tolist())

            dinner_recommendations = recommend_foods(model, food_df, *dinner_needs, excluded_foods)
            excluded_foods.extend(dinner_recommendations['name'].tolist())

            # Tampilkan makanan yang direkomendasikan
            st.subheader("Makanan yang Direkomendasikan untuk Sarapan:")
            for _, food in breakfast_recommendations.iterrows():
                st.write(f"- {food['name']} ({food['calories']} kalori, {food['proteins']}g protein, {food['carbohydrate']}g karbohidrat)")

            st.subheader("Makanan yang Direkomendasikan untuk Makan Siang:")
            for _, food in lunch_recommendations.iterrows():
                st.write(f"- {food['name']} ({food['calories']} kalori, {food['proteins']}g protein, {food['carbohydrate']}g karbohidrat)")

            st.subheader("Makanan yang Direkomendasikan untuk Snack:")
            for _, food in snack_recommendations.iterrows():
                st.write(f"- {food['name']} ({food['calories']} kalori, {food['proteins']}g protein, {food['carbohydrate']}g karbohidrat)")

            st.subheader("Makanan yang Direkomendasikan untuk Makan Malam:")
            for _, food in dinner_recommendations.iterrows():
                st.write(f"- {food['name']} ({food['calories']} kalori, {food['proteins']}g protein, {food['carbohydrate']}g karbohidrat)")
