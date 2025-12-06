# app.py - Final Professional, Interactive & Gorgeous Version
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import altair as alt  # For interactive charts

st.set_page_config(page_title="Personal AI Finance Manager", page_icon="💰", layout="wide")

# Gorgeous Custom Theme (Impressive, Interactive, Beautiful)
st.markdown("""
<style>
    /* Main Page Background */
    .main { 
        background-color: #e9f7ff;  /* Soft blue for main page */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Sidebar Background & Design */
    .sidebar .sidebar-content { 
        background-color: #f0f4f8;  /* Light gray-blue for sidebar */
        border-right: 1px solid #dee2e6;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    /* Glow Buttons */
    .stButton>button { 
        background-color: #007bff; 
        color: white; 
        border-radius: 8px; 
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.5); /* Glow effect */
        width: 100%;
        margin-bottom: 10px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 0 20px rgba(0, 123, 255, 0.7); /* Enhanced glow */
        transform: scale(1.05); /* Interactive scale */
    }
    .stProgress > div > div > div > div {
        background-color: #28a745;
    }
    h1, h2, h3, h4 {
        color: #212529;
        font-weight: 600;
    }
    .stMetric {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .stMetric:hover {
        transform: translateY(-5px); /* Interactive lift */
    }
    .block-container {
        padding: 25px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .insight-card {
        background-color: #f8f9fc;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .insight-card:hover {
        transform: translateY(-3px);
    }
    /* Tab Styles */
    .stTab {
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Landing Page (Impressive & Interactive)
st.title("Personal AI Finance Manager")
st.markdown("### Empowering Your Financial Future with AI Insights")
st.markdown("Track, Predict, and Optimize Your Finances – Simple, Smart, Secure.")

# Load and train model (run once)
@st.cache_resource
def load_and_train_model():
    df = pd.read_csv("personal_finance_tracker_dataset.csv")
    df.columns = df.columns.str.strip()
    df['date'] = pd.to_datetime(df['date'])
    df_monthly = df.groupby(pd.Grouper(key='date', freq='ME')).agg({
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
    credit_score = 650  # Default
    extra = max(0, expenses - savings)
    X_new = np.array([[income, expenses, extra, credit_score]])
    X_scaled = scaler.transform(X_new)
    p = model.predict(X_scaled)[0]
    return {
        "next_3_months": round(p[1], 2),
        "next_6_months": round(p[2], 2)
    }

# Sidebar for Inputs (No Age, Customized Buttons)
with st.sidebar:
    st.header("Your Financial Details")
    st.markdown("---")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0.0, value=50000.0, step=1000.0, help="Your total monthly earnings.")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0.0, value=30000.0, step=1000.0, help="Sum of all monthly spendings.")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0.0, value=10000.0, step=1000.0, help="Your current saved amount.")
    debt = st.number_input("Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Any loans or debts.")
    investments = st.number_input("Current Investments (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Your investment portfolio value.")
    goal_purpose = st.text_input("Saving Goal Purpose (e.g., Car)", value="Car", help="What are you saving for?")
    goal_amount = st.number_input("Goal Amount (PKR)", min_value=0.0, value=100000.0, step=1000.0, help="How much do you need?")
    st.markdown("---")
    analyze_button = st.button("🔍 Analyze Finances", use_container_width=True)

if analyze_button:
    results = predict_finance(monthly_income, monthly_expenses, current_savings)
    total_balance = monthly_income - monthly_expenses + current_savings
    net_worth = current_savings + investments - debt
    emergency_needed = monthly_expenses * 6
    emergency_status = "✅ Complete" if current_savings >= emergency_needed else "⚠️ Incomplete"
    emergency_progress = min(current_savings / emergency_needed, 1.0) if emergency_needed > 0 else 0
    # 50/30/20 Rule
    needs = monthly_income * 0.5
    wants = monthly_income * 0.3
    save = monthly_income * 0.2
    savings_progress = min((current_savings / save) if save > 0 else 0, 1.0)
    # AI Insights (New Section)
    saving_ratio = (current_savings / monthly_income) * 100 if monthly_income > 0 else 0
    expense_ratio = (monthly_expenses / monthly_income) * 100 if monthly_income > 0 else 0
    # Investment Suggestion (Based on User Inputs - No Age)
    saving_rate = monthly_saving = monthly_income - monthly_expenses
    if saving_rate > monthly_income * 0.3:
        investment_sug = "Aggressive: 80% Stocks, 20% Gold. Aap bohot achhi saving kar rahe hain – high-growth options try karo!"
    elif saving_rate > monthly_income * 0.1:
        investment_sug = "Balanced: 60% Stocks, 30% Debt, 10% Gold. Aap stable hain – mix of growth and safety best rahega."
    else:
        investment_sug = "Conservative: 40% Stocks, 50% Debt, 10% Gold. Pehle saving badhao – low-risk options se shuru karo."
    # Saving Goal (Upgraded)
    current_monthly_saving = monthly_saving  # Use realistic monthly saving
    if current_monthly_saving > 0:
        months_current = goal_amount / current_monthly_saving
        current_sug = f"{months_current:.0f} months (~{months_current/12:.1f} years)"
    else:
        current_sug = "Warning: Aap abhi saving nahi kar rahe → Goal kabhi achieve nahi hoga!"
        months_current = float('inf')
    basic_rate = monthly_income * 0.20
    strong_rate = monthly_income * 0.30
    if current_monthly_saving < basic_rate:
        months_basic = goal_amount / basic_rate
        basic_sug = f"Save: {basic_rate:,.0f} PKR/month → {months_basic:.0f} months (~{months_basic/12:.1f} years)"
    else:
        basic_sug = ""
    if current_monthly_saving < strong_rate:
        months_strong = goal_amount / strong_rate
        strong_sug = f"Save: {strong_rate:,.0f} PKR/month → {months_strong:.0f} months (~{months_strong/12:.1f} years)"
    else:
        strong_sug = ""
    if current_monthly_saving >= strong_rate:
        praise_sug = "Outstanding! Ap already 30% se bhi zyada bacha rahy hain! Apna goal bohot jaldi achieve kar lain gy! Keep it up!"
    elif current_monthly_saving >= basic_rate:
        praise_sug = "Great Job! Ap already Basic Plan (20%) achieve kar chuka hai! Strong Plan ki taraf jain, aur bhi jaldi goal poora ho jayega!"
    else:
        praise_sug = ""
    # Show 50/30/20 only if needed (expense >60% or saving <20%)
    show_budget_rule = expense_ratio > 60 or saving_ratio < 20

    # Tabs with Clear Labels
    tab1, tab2, tab3 = st.tabs(["Predictions", "Insights", "Visualizations"])

    with tab1:
        st.subheader("Financial Predictions")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Balance", f"{total_balance:.2f} PKR")
            st.metric("Net Worth", f"{net_worth:.2f} PKR")
        with col2:
            st.metric("Avg. Next 3 Months Savings", f"{results['next_3_months']:.2f} PKR")
            st.metric("Avg. Next 6 Months Savings", f"{results['next_6_months']:.2f} PKR")

    with tab2:
        st.subheader("AI Insights - User Financial Health")
        st.write(f"Saving Rate: {saving_ratio:.1f}%   |   Expense Rate: {expense_ratio:.1f}%")
        if expense_ratio > 100:
            st.error("Overspending! Aap income se zyada kharch kar rahe hain. Tip: Quickly dining, shopping ya subscriptions band karo.")
        elif expense_ratio > 80:
            st.warning("High Spending! Aap 80% plus income kharch kar rahe hain. Tip: 50-30-20 rule follow karo (50% needs, 30% wants, 20% savings)")
        elif expense_ratio > 60:
            st.info("Balanced Spending! Aap control mein hain. Tip: Ab saving ko 20% plus karne ki koshish karo.")
        else:
            st.success("Excellent Control! Aap bohot smartly manage kar rahe hoo!")
        if saving_ratio < 10:
            st.warning("Low Savings! Mahine ka 10% bhi nahi bacha rahe. Tip: Har mahine pehle saving karo, phir kharch.")
        elif saving_ratio < 20:
            st.info("Good Start! Saving 10-20% hai. Tip: Ise 20-30% tak le jao for financial freedom.")
        else:
            st.success("Amazing Saving Habit! Aap future ke liye ready ho!")

        st.subheader("Saving Goal")
        st.write(f"Goal: {goal_purpose} - Amount: {goal_amount:.2f} PKR")
        st.write(f"At Your Current Rate ({current_monthly_saving:,.0f} PKR/month): {current_sug}")
        st.write("Recommended Plans")
        if basic_sug:
            st.info(basic_sug)
        if strong_sug:
            st.info(strong_sug)
        if praise_sug:
            st.success(praise_sug)

        st.subheader("Emergency Fund Status (Improved)")
        st.write(f"Needed for 6 Months: {emergency_needed:.2f} PKR")
        st.write(f"Status: {emergency_status}")
        st.progress(emergency_progress)
        if emergency_progress < 0.5:
            st.warning("Emergency fund kam hai! Mahine ka 10-20% add karo. Tip: High-interest saving account use karo.")
        elif emergency_progress < 0.8:
            st.info("Achha start! Ise 100% tak le jao. Tip: Automatic transfers set karo.")
        else:
            st.success("Perfect! Aap emergencies ke liye ready hain. Tip: Ise review karte raho inflation ke hisaab se.")

        st.subheader("Investment Recommendations (Customized)")
        st.info(investment_sug)

        if show_budget_rule:
            st.subheader("50/30/20 Budget Rule (Only Shown When Needed)")
            st.write(f"Needs (50%): {needs:.2f} PKR")
            st.write(f"Wants (30%): {wants:.2f} PKR")
            st.write(f"Savings (20%): {save:.2f} PKR")
            st.progress(savings_progress)
            if savings_progress < 0.5:
                st.warning("Tip: Expenses kam karo taake savings badhe. Start with tracking apps.")
            else:
                st.info("Tip: Yeh rule follow karte raho for long-term stability.")

    with tab3:
        st.subheader("Interactive Visualizations")
        # Income vs Expenses
        st.markdown("**Income vs Expenses**")
        data_bar = pd.DataFrame({'Category': ['Income', 'Expenses'], 'Amount': [monthly_income, monthly_expenses]})
        chart_bar = alt.Chart(data_bar).mark_bar().encode(
            x='Category',
            y='Amount',
            color=alt.Color('Category', scale=alt.Scale(domain=['Income', 'Expenses'], range=['#4CAF50', '#F44336'])),
            tooltip=['Category', 'Amount']
        ).properties(width=600, height=400, title='Monthly Breakdown').interactive()
        st.altair_chart(chart_bar, use_container_width=True)

        # Spending by Category (Pie)
        st.markdown("**Spending by Category**")
        categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
        values = [monthly_expenses * 0.2, monthly_expenses * 0.25, monthly_expenses * 0.15, monthly_expenses * 0.3, monthly_expenses * 0.1]
        data_pie = pd.DataFrame({'Category': categories, 'Amount': values})
        chart_pie = alt.Chart(data_pie).mark_arc().encode(
            theta='Amount:Q',
            color='Category:N',
            tooltip=['Category', 'Amount']
        ).properties(width=600, height=400, title='Expense Distribution').interactive()
        st.altair_chart(chart_pie, use_container_width=True)

        # Finance Trend
        st.markdown("**Finance Trend**")
        months = ["Current", "Next 3 Months", "Next 6 Months"]
        data_trend = pd.DataFrame({
            'Month': months,
            'Savings': [current_savings, results['next_3_months'], results['next_6_months']],
            'Income': [monthly_income] * 3,
            'Expenses': [monthly_expenses] * 3
        }).melt('Month', var_name='Type', value_name='Amount')
        chart_line = alt.Chart(data_trend).mark_line(point=True).encode(
            x='Month:O',
            y='Amount:Q',
            color='Type:N',
            tooltip=['Month', 'Type', 'Amount']
        ).properties(width=800, height=400, title='Trend Over Time').interactive()
        st.altair_chart(chart_line, use_container_width=True)

    # PDF Report (Clear & Simple)
    st.subheader("Generate Report")
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Personal AI Finance Manager Report", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Paragraph(f"Income: {monthly_income:.2f} PKR | Expenses: {monthly_expenses:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"Net Worth: {net_worth:.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"AI Insights: Saving Rate {saving_ratio:.1f}% | Expense Rate {expense_ratio:.1f}%", styles['Normal']))
    story.append(Paragraph("Saving Goal: " + goal_purpose + f" - {goal_amount:.2f} PKR", styles['Normal']))
    story.append(Paragraph("Time Needed: " + current_sug, styles['Normal']))
    story.append(Paragraph("Emergency Fund: Needed {emergency_needed:.2f} PKR - Status: " + emergency_status, styles['Normal']))
    story.append(Paragraph("Investment Suggestion: " + investment_sug, styles['Normal']))
    if show_budget_rule:
        story.append(Paragraph("50/30/20 Rule: Needs {needs:.2f} | Wants {wants:.2f} | Savings {save:.2f}", styles['Normal']))
    doc.build(story)
    pdf_buffer.seek(0)
    st.download_button("📄 Download PDF Report", pdf_buffer, "finance_report.pdf", "application/pdf", use_container_width=True)
