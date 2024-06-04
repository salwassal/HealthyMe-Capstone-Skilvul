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

        # Get user's daily calorie, proteins, and fat needs
        daily_calorie_needs = st.number_input("Enter your daily calorie needs:", min_value=1000, max_value=5000, step=100)
        daily_proteins_needs = st.number_input("Enter your daily proteins needs (grams):", min_value=10, max_value=300, step=10)
        daily_fat_needs = st.number_input("Enter your daily fat needs (grams):", min_value=10, max_value=200, step=10)

        # Function to recommend foods based on user's needs
        def recommend_foods(model, food_df, calorie_needs, proteins_needs, fat_needs, excluded_foods):
            # Predict the cluster for the given needs
            user_cluster = model.predict([[calorie_needs, proteins_needs, fat_needs]])[0]
            
            # Get the foods in the same cluster
            food_df['cluster'] = model.predict(food_df[['calories', 'proteins', 'fat']])
            recommended_foods = food_df[(food_df['cluster'] == user_cluster) & (~food_df['name'].isin(excluded_foods))]
            
            # Filter foods to match the calorie needs closely
            recommended_foods = recommended_foods.iloc[(recommended_foods['calories'] - calorie_needs).abs().argsort()[:1]]
            
            return recommended_foods

        # Calculate needs for each meal
        breakfast_needs = (daily_calorie_needs * 0.25, daily_proteins_needs * 0.25, daily_fat_needs * 0.25)
        lunch_needs = (daily_calorie_needs * 0.30, daily_proteins_needs * 0.30, daily_fat_needs * 0.30)
        snack_needs = (daily_calorie_needs * 0.15, daily_proteins_needs * 0.15, daily_fat_needs * 0.15)
        dinner_needs = (daily_calorie_needs * 0.30, daily_proteins_needs * 0.30, daily_fat_needs * 0.30)

        # Keep track of recommended foods
        excluded_foods = []

        # Recommend foods for each meal
        breakfast_recommendations = recommend_foods(model, food_df, *breakfast_needs, excluded_foods)
        excluded_foods.extend(breakfast_recommendations['name'].tolist())

        lunch_recommendations = recommend_foods(model, food_df, *lunch_needs, excluded_foods)
        excluded_foods.extend(lunch_recommendations['name'].tolist())

        snack_recommendations = recommend_foods(model, food_df, *snack_needs, excluded_foods)
        excluded_foods.extend(snack_recommendations['name'].tolist())

        dinner_recommendations = recommend_foods(model, food_df, *dinner_needs, excluded_foods)
        excluded_foods.extend(dinner_recommendations['name'].tolist())

        # Display the recommended foods
        st.subheader("Recommended Foods for Breakfast:")
        for _, food in breakfast_recommendations.iterrows():
            st.write(f"- {food['name']} ({food['calories']} calories, {food['proteins']}g proteins, {food['fat']}g fat)")

        st.subheader("Recommended Foods for Lunch:")
        for _, food in lunch_recommendations.iterrows():
            st.write(f"- {food['name']} ({food['calories']} calories, {food['proteins']}g proteins, {food['fat']}g fat)")

        st.subheader("Recommended Foods for Snack:")
        for _, food in snack_recommendations.iterrows():
            st.write(f"- {food['name']} ({food['calories']} calories, {food['proteins']}g proteins, {food['fat']}g fat)")

        st.subheader("Recommended Foods for Dinner:")
        for _, food in dinner_recommendations.iterrows():
            st.write(f"- {food['name']} ({food['calories']} calories, {food['proteins']}g proteins, {food['fat']}g fat)")
