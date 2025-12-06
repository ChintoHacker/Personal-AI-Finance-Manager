# app.py - Streamlit GUI for Personal AI Finance Manager

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
from reportlab.lib import colors
from datetime import datetime

st.set_page_config(page_title="Personal AI Finance Manager", page_icon="💰", layout="wide")

# Custom theme for beauty
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .sidebar .sidebar-content { background-color: #ffffff; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; }
    .stProgress .st-bo { background-color: #2196F3; }
</style>
""", unsafe_allow_html=True)

# Load and train model (run once)
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

# Sidebar for inputs (Styled)
st.sidebar.title("📊 Enter Your Finance Details")
st.sidebar.markdown("---")
monthly_income = st.sidebar.number_input("Monthly Income (PKR)", min_value=0.0, value=50000.0, step=1000.0, help="Your total monthly earnings")
monthly_expenses = st.sidebar.number_input("Monthly Expenses (PKR)", min_value=0.0, value=30000.0, step=1000.0, help="Total monthly spendings")
current_savings = st.sidebar.number_input("Current Savings (PKR)", min_value=0.0, value=10000.0, step=1000.0, help="Your current saved amount")
debt = st.sidebar.number_input("Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Any loans or debts")
investments = st.sidebar.number_input("Current Investments (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Your investment portfolio value")
age = st.sidebar.number_input("Your Age", min_value=18, max_value=100, value=30, step=1, help="For investment suggestions")

goal_purpose = st.sidebar.text_input("Saving Goal Purpose (e.g., Car)", value="Car", help="What are you saving for?")
goal_amount = st.sidebar.number_input("Goal Amount (PKR)", min_value=0.0, value=100000.0, step=1000.0, help="How much do you need?")

st.sidebar.markdown("---")
if st.sidebar.button("🔍 Analyze My Finances", use_container_width=True):
    results = predict_finance(monthly_income, monthly_expenses, current_savings)
    total_balance = monthly_income - monthly_expenses + current_savings
    net_worth = current_savings + investments - debt
    emergency_needed = monthly_expenses * 6
    emergency_status = "✅ Complete" if current_savings >= emergency_needed else "⚠️ Incomplete"

    # 50/30/20 Rule
    needs = monthly_income * 0.5
    wants = monthly_income * 0.3
    save = monthly_income * 0.2
    savings_progress = min(save / (monthly_income * 0.2), 1.0) if monthly_income > 0 else 0

    # Investment Suggestion
    if age < 30:
        investment_sug = "Aggressive: 80% Stocks, 20% Gold"
    elif age < 45:
        investment_sug = "Balanced: 60% Stocks, 30% Debt, 10% Gold"
    else:
        investment_sug = "Conservative: 40% Stocks, 50% Debt, 10% Gold"

    # Saving Goal (Customized)
    if current_savings > 0:
        current_rate_months = goal_amount / current_savings
        current_rate_years = current_rate_months / 12
        current_sug = f"{current_rate_months:.0f} months (~{current_rate_years:.1f} years)"
    else:
        current_sug = "Infinite - Start saving now!"

    basic_monthly = monthly_income * 0.20
    strong_monthly = monthly_income * 0.30
    basic_months = goal_amount / basic_monthly if basic_monthly > 0 else float('inf')
    strong_months = goal_amount / strong_monthly if strong_monthly > 0 else float('inf')

    # Tabs for organized layout
    tab1, tab2, tab3 = st.tabs(["📈 Predictions & Health", "💡 Insights & Suggestions", "📊 Charts & Visuals"])

    with tab1:
        st.subheader("Prediction Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Balance", f"{total_balance:.2f} PKR")
        col2.metric("Financial Health", results['health'])
        col3.metric("Next Month Savings", f"{results['next_month']:.2f} PKR")
        st.metric("Next 3 Months (Avg)", f"{results['next_3_months']:.2f} PKR")
        st.metric("Next 6 Months (Avg)", f"{results['next_6_months']:.2f} PKR")

    with tab2:
        st.subheader("Net Worth Calculator")
        st.write(f"Net Worth: {net_worth:.2f} PKR (Savings + Investments - Debt)")

        st.subheader("Emergency Fund Status")
        st.write(f"Needed for 6 Months: {emergency_needed:.2f} PKR")
        st.write(f"Status: {emergency_status}")

        st.subheader("50/30/20 Rule Checker")
        st.write(f"Needs (50%): {needs:.2f} PKR")
        st.write(f"Wants (30%): {wants:.2f} PKR")
        st.write(f"Savings (20%): {save:.2f} PKR")
        st.progress(savings_progress)  # Progress bar for savings
        if monthly_income <= 0:
            st.warning("No income entered for progress calculation.")

        st.subheader("Investment Suggestion")
        st.info(investment_sug)

        st.subheader("Saving Goals")
        st.write(f"Goal: {goal_purpose} - Amount: {goal_amount:.2f} PKR")
        st.write(f"Current Rate: {current_sug}")
        st.write(f"Basic (20%): Save {basic_monthly:.2f} PKR/month - {basic_months:.0f} months")
        st.write(f"Strong (30%): Save {strong_monthly:.2f} PKR/month - {strong_months:.0f} months")

    with tab3:
        st.subheader("Income vs Expense Chart")
        fig1, ax1 = plt.subplots(figsize=(6,4))
        ax1.bar(["Income", "Expenses"], [monthly_income, monthly_expenses], color=['#4CAF50', '#F44336'])
        ax1.set_title("Monthly Income vs Expenses")
        ax1.set_ylabel("PKR")
        st.pyplot(fig1)

        st.subheader("Spending by Category Chart")
        categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
        values = [20, 25, 15, 30, 10]  # Dummy data; can make dynamic if needed
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.pie(values, labels=categories, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
        ax2.set_title("Spending by Category")
        st.pyplot(fig2)

        st.subheader("Monthly Finance Trend")
        months = ["Current", "Next", "3 Months", "6 Months"]
        savings_trend = [current_savings, results['next_month'], results['next_3_months'], results['next_6_months']]
        fig3, ax3 = plt.subplots(figsize=(8,4))
        ax3.plot(months, savings_trend, label="Savings", marker='s', color='#2196F3')
        ax3.plot(months, [monthly_income] * 4, label="Income", color='#4CAF50')
        ax3.plot(months, [monthly_expenses] * 4, label="Expenses", color='#F44336')
        ax3.legend()
        ax3.set_title("Finance Trend")
        ax3.set_ylabel("PKR")
        st.pyplot(fig3)

    # PDF Report (Improved & User-Friendly)
    st.subheader("Download Your Report")
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<font size=18>Personal AI Finance Manager Report</font>", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<b>Net Worth:</b> {net_worth:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"<b>Financial Health:</b> {results['health']}", styles['Normal']))
    story.append(Paragraph(f"<b>Total Balance:</b> {total_balance:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"<b>Next Month Savings:</b> {results['next_month']:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"<b>Emergency Fund:</b> {emergency_status} (Needed: {emergency_needed:.2f} PKR)", styles['Normal']))
    story.append(Paragraph(f"<b>50/30/20 Rule:</b> Needs {needs:.2f} | Wants {wants:.2f} | Savings {save:.2f}", styles['Normal']))
    story.append(Paragraph(f"<b>Investment Suggestion:</b> {investment_sug}", styles['Normal']))
    story.append(Paragraph(f"<b>Saving Goal ({goal_purpose}):</b> {goal_amount:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"   Current Rate: {current_sug}", styles['Normal']))
    story.append(Paragraph(f"   Basic (20%): {basic_months:.0f} months", styles['Normal']))
    story.append(Paragraph(f"   Strong (30%): {strong_months:.0f} months", styles['Normal']))
    doc.build(story)
    pdf_buffer.seek(0)
    st.download_button("📄 Download PDF Report", pdf_buffer, "finance_report.pdf", "application/pdf", use_container_width=True)

# Run with: streamlit run app.py
