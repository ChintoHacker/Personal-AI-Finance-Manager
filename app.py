import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime

st.set_page_config(page_title="Personal AI Finance Manager", page_icon="💰", layout="wide")

# Load and train model (run once on startup)
@st.cache_resource
def load_and_train_model():
    df = pd.read_csv("personal_finance_tracker_dataset.csv")
    df.columns = df.columns.str.strip()
    df['date'] = pd.to_datetime(df['date'])

    df_monthly = df.groupby(pd.Grouper(key='date', freq='M')).agg({
        'monthly_income': 'mean',
        'monthly_expense_total': 'mean',
        'actual_savings': 'mean',
        'credit_score': 'mean'
    }).reset_index()

    df_monthly = df_monthly.rename(columns={
        'monthly_income': 'income',
        'monthly_expense_total': 'expenses',
        'actual_savings': 'savings'
    }).fillna(0)

    df_monthly["extra_spendings"] = np.maximum(0, df_monthly["expenses"] - df_monthly["savings"])

    df_monthly["savings_next_1"] = df_monthly["savings"].shift(-1)
    df_monthly["savings_next_3"] = df_monthly["savings"].rolling(3).mean().shift(-1)
    df_monthly["savings_next_6"] = df_monthly["savings"].rolling(6).mean().shift(-1)

    df_monthly = df_monthly.dropna()

    X = df_monthly[["income", "expenses", "extra_spendings", "credit_score"]]

    Y = df_monthly[["savings_next_1", "savings_next_3", "savings_next_6"]]

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    X_train, X_test, Y_train, Y_test = train_test_split(Xs, Y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, Y_train)

    joblib.dump(model, "finance_model.joblib")
    joblib.dump(scaler, "scaler.joblib")

    return model, scaler

model, scaler = load_and_train_model()

def predict_finance(income, expenses, savings):
    credit_score = 650
    extra = max(0, expenses - savings)

    X_new = np.array([[income, expenses, extra, credit_score]])
    X_scaled = scaler.transform(X_new)

    p = model.predict(X_scaled)[0]

    if p[0] > savings:
        health = "Excellent"
    elif p[0] < 0:
        health = "Poor"
    else:
        health = "Average"

    return {
        "next_month": round(p[0], 2),
        "next_3_months": round(p[1], 2),
        "next_6_months": round(p[2], 2),
        "health": health
    }

# Sidebar for inputs
st.sidebar.title("Enter Your Details")
monthly_income = st.sidebar.number_input("Monthly Income (PKR)", min_value=0.0, value=50000.0)
monthly_expenses = st.sidebar.number_input("Monthly Expenses (PKR)", min_value=0.0, value=30000.0)
current_savings = st.sidebar.number_input("Current Savings (PKR)", min_value=0.0, value=10000.0)
debt = st.sidebar.number_input("Total Debt (PKR)", min_value=0.0, value=0.0)
investments = st.sidebar.number_input("Current Investments (PKR)", min_value=0.0, value=0.0)
age = st.sidebar.number_input("Your Age", min_value=18, max_value=100, value=30)
retirement_age = st.sidebar.number_input("Retirement Age", min_value=age, max_value=100, value=60)

goal_purpose = st.sidebar.text_input("Saving Goal Purpose (e.g., Car)", value="Car")
goal_amount = st.sidebar.number_input("Goal Amount (PKR)", min_value=0.0, value=100000.0)

# Main page
st.title("Personal AI Finance Manager")

if st.sidebar.button("Analyze & Predict"):
    results = predict_finance(monthly_income, monthly_expenses, current_savings)
    total_balance = monthly_income - monthly_expenses + current_savings
    net_worth = current_savings + investments - debt
    emergency_needed = monthly_expenses * 6
    emergency_status = "Complete" if current_savings >= emergency_needed else "Incomplete"

    # 50/30/20 Rule
    needs = monthly_income * 0.5
    wants = monthly_income * 0.3
    save = monthly_income * 0.2

    # Investment Suggestion
    if age < 30:
        investment_sug = "Aggressive: 80% Stocks, 20% Gold"
    elif age < 45:
        investment_sug = "Balanced: 60% Stocks, 30% Debt, 10% Gold"
    else:
        investment_sug = "Conservative: 40% Stocks, 50% Debt, 10% Gold"

    # Saving Goal
    current_rate_months = goal_amount / current_savings if current_savings > 0 else float('inf')
    basic_monthly = monthly_income * 0.20
    strong_monthly = monthly_income * 0.30
    basic_months = goal_amount / basic_monthly if basic_monthly > 0 else float('inf')
    strong_months = goal_amount / strong_monthly if strong_monthly > 0 else float('inf')

    st.subheader("Prediction Results")
    st.write(f"Total Balance: {total_balance:.2f} PKR")
    st.write(f"Financial Health: {results['health']}")
    st.write(f"Next Month Savings: {results['next_month']:.2f} PKR")
    st.write(f"Next 3 Months (Avg): {results['next_3_months']:.2f} PKR")
    st.write(f"Next 6 Months (Avg): {results['next_6_months']:.2f} PKR")

    st.subheader("Net Worth Calculator")
    st.write(f"Net Worth: {net_worth:.2f} PKR (Savings + Investments - Debt)")

    st.subheader("Emergency Fund Status")
    st.write(f"Needed for 6 Months: {emergency_needed:.2f} PKR")
    st.write(f"Status: {emergency_status}")

    st.subheader("50/30/20 Rule Checker")
    st.write(f"Needs (50%): {needs:.2f} PKR")
    st.write(f"Wants (30%): {wants:.2f} PKR")
    st.write(f"Savings (20%): {save:.2f} PKR")
    # Simple progress bar
    st.progress(save / (monthly_income * 0.2)) if monthly_income > 0 else st.write("No income entered")

    st.subheader("Investment Suggestion")
    st.write(investment_sug)

    st.subheader("Saving Goals")
    st.write(f"Goal: {goal_purpose} - Amount: {goal_amount:.2f} PKR")
    st.write(f"Current Rate: {current_rate_months:.0f} months")
    st.write(f"Basic (20%): Save {basic_monthly:.2f} PKR/month - {basic_months:.0f} months")
    st.write(f"Strong (30%): Save {strong_monthly:.2f} PKR/month - {strong_months:.0f} months")

    # Charts (from original)
    st.subheader("Income vs Expense Chart")
    fig1, ax1 = plt.subplots()
    ax1.bar(["Income", "Expenses"], [monthly_income, monthly_expenses])
    st.pyplot(fig1)

    st.subheader("Spending by Category Chart")
    categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
    values = [20, 25, 15, 30, 10]  # Dummy, replace with real if needed
    fig2, ax2 = plt.subplots()
    ax2.pie(values, labels=categories, autopct="%1.1f%%")
    st.pyplot(fig2)

    st.subheader("Monthly Finance Trend")
    months = ["Current", "Next", "3 Months", "6 Months"]
    savings_trend = [current_savings, results['next_month'], results['next_3_months'], results['next_6_months']]
    fig3, ax3 = plt.subplots()
    ax3.plot(months, savings_trend, label="Savings", marker='s')
    ax3.plot(months, [monthly_income] * 4, label="Income")
    ax3.plot(months, [monthly_expenses] * 4, label="Expenses")
    ax3.legend()
    st.pyplot(fig3)

    # Generate PDF Report
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Personal AI Finance Manager Report", styles['Title']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Paragraph(f"Net Worth: {net_worth:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"Financial Health: {results['health']}", styles['Normal']))
    # Add more details as needed
    doc.build(story)
    pdf_buffer.seek(0)
    st.download_button("Download PDF Report", pdf_buffer, "finance_report.pdf", "application/pdf")
