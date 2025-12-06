# app.py - Streamlit GUI for Personal AI Finance Manager
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Personal AI Finance Manager", page_icon="💰", layout="wide")

# Load the pre-trained model and scaler (assume they are saved from the notebook)
try:
    model = joblib.load("finance_model.joblib")
    scaler = joblib.load("scaler.joblib")
except FileNotFoundError:
    st.error("Model files not found. Please run the notebook to train and save the model.")
    st.stop()

# Sidebar for user inputs
st.sidebar.title("Enter Your Details")
monthly_income = st.sidebar.number_input("Monthly Income (PKR)", min_value=0.0, value=50000.0)
monthly_expenses = st.sidebar.number_input("Monthly Expenses (PKR)", min_value=0.0, value=30000.0)
current_savings = st.sidebar.number_input("Current Savings (PKR)", min_value=0.0, value=10000.0)
credit_score = st.sidebar.number_input("Credit Score", min_value=300, max_value=850, value=650)

if st.sidebar.button("Predict"):
    # Prepare input for prediction
    extra_spendings = max(0, monthly_expenses - current_savings)
    input_data = np.array([[monthly_income, monthly_expenses, extra_spendings, credit_score]])
    input_scaled = scaler.transform(input_data)
    predictions = model.predict(input_scaled)[0]

    st.title("Finance Predictions")
    st.write(f"Next Month Savings: {predictions[0]:.2f} PKR")
    st.write(f"Next 3 Months Avg Savings: {predictions[1]:.2f} PKR")
    st.write(f"Next 6 Months Avg Savings: {predictions[2]:.2f} PKR")
