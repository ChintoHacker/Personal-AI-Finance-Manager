# app.py - Streamlit GUI for Personal AI Finance Manager (Professional Version)
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

# Professional Custom Theme (Sleek, Modern, User-Friendly)
st.markdown("""
<style>
    .main { 
        background-color: #f8f9fc; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .sidebar .sidebar-content { 
        background-color: #ffffff; 
        border-right: 1px solid #dee2e6;
        padding: 25px;
        border-radius: 8px;
    }
    .stButton>button { 
        background-color: #007bff; 
        color: white; 
        border-radius: 8px; 
        padding: 12px 24px;
        font-weight: 500;
        transition: background-color 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
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
    }
    .block-container {
        padding: 25px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .stExpander {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .stTab {
        background-color: #f1f3f5;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)

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
    credit_score = 650  # Default; can be made dynamic
    extra = max(0, expenses - savings)
    X_new = np.array([[income, expenses, extra, credit_score]])
    X_scaled = scaler.transform(X_new)
    p = model.predict(X_scaled)[0]
    if p[0] > savings * 1.1:
        health = "Excellent"
        health_color = "#28a745"  # Green
    elif p[0] < savings * 0.9:
        health = "Poor"
        health_color = "#dc3545"  # Red
    else:
        health = "Average"
        health_color = "#ffc107"  # Orange
    return {
        "next_month": round(p[0], 2),
        "next_3_months": round(p[1], 2),
        "next_6_months": round(p[2], 2),
        "health": health,
        "health_color": health_color
    }

# Sidebar for Inputs (Professional, Clean, with Tooltips)
with st.sidebar:
    st.header("📊 Your Financial Details")
    st.markdown("---")
    monthly_income = st.number_input("💼 Monthly Income (PKR)", min_value=0.0, value=50000.0, step=1000.0, help="Enter your total monthly earnings, including salary and any bonuses.")
    monthly_expenses = st.number_input("🛒 Monthly Expenses (PKR)", min_value=0.0, value=30000.0, step=1000.0, help="Sum of all monthly expenditures like rent, utilities, and groceries.")
    current_savings = st.number_input("💰 Current Savings (PKR)", min_value=0.0, value=10000.0, step=1000.0, help="Your current savings balance across all accounts.")
    debt = st.number_input("📉 Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Total outstanding debts, including loans and credit cards.")
    investments = st.number_input("📈 Current Investments (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Current value of your investment portfolio (stocks, funds, etc.).")
    age = st.number_input("👤 Your Age", min_value=18, max_value=100, value=30, step=1, help="Used to provide personalized investment recommendations.")
    goal_purpose = st.text_input("🎯 Saving Goal Purpose", value="Car", help="e.g., 'Buy a House', 'Vacation', or 'Emergency Fund'.")
    goal_amount = st.number_input("🏆 Goal Amount (PKR)", min_value=0.0, value=100000.0, step=1000.0, help="The target amount you aim to save for this goal.")
    st.markdown("---")
    analyze_button = st.button("🔍 Analyze Finances", use_container_width=True)

if analyze_button:
    results = predict_finance(monthly_income, monthly_expenses, current_savings)
    total_balance = monthly_income - monthly_expenses + current_savings
    net_worth = current_savings + investments - debt
    emergency_needed = monthly_expenses * 6
    emergency_status = "✅ Funded" if current_savings >= emergency_needed else "⚠️ Build Now"
    emergency_progress = min(current_savings / emergency_needed, 1.0) if emergency_needed > 0 else 0
    # 50/30/20 Rule
    needs = monthly_income * 0.5
    wants = monthly_income * 0.3
    save = monthly_income * 0.2
    savings_progress = min((current_savings / save) if save > 0 else 0, 1.0)
    # Investment Suggestion
    if age < 30:
        investment_sug = "Aggressive Portfolio: 80% Stocks, 20% Gold – High growth potential."
    elif age < 45:
        investment_sug = "Balanced Portfolio: 60% Stocks, 30% Debt, 10% Gold – Steady returns."
    else:
        investment_sug = "Conservative Portfolio: 40% Stocks, 50% Debt, 10% Gold – Low risk."
    # Saving Goal with Compound Interest
    assumed_interest = 0.05 / 12  # 5% annual
    if current_savings > 0 and monthly_income > 0:
        basic_monthly = monthly_income * 0.20
        strong_monthly = monthly_income * 0.30
        basic_months = np.log((goal_amount * assumed_interest / basic_monthly) + 1) / np.log(1 + assumed_interest) if basic_monthly > 0 else float('inf')
        strong_months = np.log((goal_amount * assumed_interest / strong_monthly) + 1) / np.log(1 + assumed_interest) if strong_monthly > 0 else float('inf')
        current_rate_months = np.log((goal_amount * assumed_interest / current_savings) + 1) / np.log(1 + assumed_interest)
        current_sug = f"{current_rate_months:.0f} months (assuming 5% annual interest)"
    else:
        current_sug = "Begin saving to estimate time!"
        basic_months = float('inf')
        strong_months = float('inf')

    # Interactive Tabs with Icons
    tab1, tab2, tab3 = st.tabs(["📈 Predictions", "💡 Insights", "📊 Visualizations"])

    with tab1:
        st.subheader("Financial Predictions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Balance", f"{total_balance:.2f} PKR")
        with col2:
            st.metric("Financial Health", results['health'], delta_color="normal")
        with col3:
            st.metric("Next Month Savings", f"{results['next_month']:.2f} PKR")
        col4, col5 = st.columns(2)
        with col4:
            st.metric("Avg. Next 3 Months", f"{results['next_3_months']:.2f} PKR")
        with col5:
            st.metric("Avg. Next 6 Months", f"{results['next_6_months']:.2f} PKR")

    with tab2:
        st.subheader("Key Insights")
        with st.expander("Net Worth Overview", expanded=True):
            st.markdown(f"**Current Net Worth:** {net_worth:.2f} PKR")
            if net_worth < 0:
                st.warning("Your net worth is negative. Focus on reducing debt.")
            else:
                st.success("Positive net worth – keep building!")
        with st.expander("Emergency Fund", expanded=True):
            st.write(f"Recommended (6 months expenses): {emergency_needed:.2f} PKR")
            st.write(f"Status: {emergency_status}")
            st.progress(emergency_progress)
        with st.expander("50/30/20 Budget Rule", expanded=True):
            st.write(f"Needs (50%): {needs:.2f} PKR")
            st.write(f"Wants (30%): {wants:.2f} PKR")
            st.write(f"Savings (20%): {save:.2f} PKR")
            st.progress(savings_progress)
        with st.expander("Investment Recommendations", expanded=True):
            st.info(investment_sug)
        with st.expander("Savings Goal Tracker", expanded=True):
            st.write(f"Goal: {goal_purpose} – Target: {goal_amount:.2f} PKR")
            st.write(f"Estimated Time at Current Rate: {current_sug}")
            st.write(f"Basic Savings (20% Income): {basic_months:.0f} months")
            st.write(f"Aggressive Savings (30% Income): {strong_months:.0f} months")
            goal_progress = min(current_savings / goal_amount, 1.0) if goal_amount > 0 else 0
            st.progress(goal_progress)

    with tab3:
        st.subheader("Interactive Visualizations")
        # Interactive Bar Chart
        st.markdown("**Income vs Expenses**")
        data_bar = pd.DataFrame({'Category': ['Income', 'Expenses'], 'Amount': [monthly_income, monthly_expenses]})
        chart_bar = alt.Chart(data_bar).mark_bar().encode(
            x='Category',
            y='Amount',
            color=alt.Color('Category', scale=alt.Scale(domain=['Income', 'Expenses'], range=['#007bff', '#dc3545'])),
            tooltip=['Category', 'Amount']
        ).properties(width='container', height=300, title='Monthly Overview').interactive()
        st.altair_chart(chart_bar, use_container_width=True)

        # Dynamic Pie Chart for Spending (Made more interactive)
        st.markdown("**Spending Breakdown**")
        categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
        base_values = [0.20, 0.25, 0.15, 0.30, 0.10]
        values = [v * monthly_expenses for v in base_values]
        data_pie = pd.DataFrame({'Category': categories, 'Amount': values})
        chart_pie = alt.Chart(data_pie).mark_arc(innerRadius=50).encode(
            theta='Amount:Q',
            color='Category:N',
            tooltip=['Category', 'Amount']
        ).properties(width='container', height=300, title='Expense Categories').interactive()
        st.altair_chart(chart_pie, use_container_width=True)

        # Line Chart for Trends
        st.markdown("**Finance Trends**")
        months = ["Current", "Next Month", "3 Months", "6 Months"]
        data_trend = pd.DataFrame({
            'Period': months,
            'Savings': [current_savings, results['next_month'], results['next_3_months'], results['next_6_months']],
            'Income': [monthly_income] * 4,
            'Expenses': [monthly_expenses] * 4
        }).melt('Period', var_name='Metric', value_name='Amount')
        chart_line = alt.Chart(data_trend).mark_line(point=True).encode(
            x='Period:O',
            y='Amount:Q',
            color='Metric:N',
            tooltip=['Period', 'Metric', 'Amount']
        ).properties(width='container', height=350, title='Projected Trends').interactive()
        st.altair_chart(chart_line, use_container_width=True)

    # Professional PDF Report
    st.subheader("Generate Report")
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<font size=18>Personal Finance Report</font>", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Metrics Table
    data = [
        ['Key Metric', 'Value'],
        ['Net Worth', f"{net_worth:.2f} PKR"],
        ['Financial Health', results['health']],
        ['Total Balance', f"{total_balance:.2f} PKR"],
        ['Next Month Savings', f"{results['next_month']:.2f} PKR"],
        ['Emergency Fund Status', emergency_status],
        ['Investment Advice', investment_sug],
        ['Goal: ' + goal_purpose, f"{goal_amount:.2f} PKR - {current_sug}"]
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    story.append(table)

    # Add Charts to PDF
    img_buffer1 = io.BytesIO()
    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.bar(["Income", "Expenses"], [monthly_income, monthly_expenses], color=['#007bff', '#dc3545'])
    ax1.set_title("Income vs Expenses")
    fig1.savefig(img_buffer1, format='png', bbox_inches='tight')
    img_buffer1.seek(0)
    story.append(Spacer(1, 0.2*inch))
    story.append(Image(img_buffer1, width=4*inch, height=2.5*inch))

    img_buffer2 = io.BytesIO()
    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.pie(values, labels=categories, autopct="%1.1f%%", colors=sns.color_palette("coolwarm"))
    ax2.set_title("Spending Breakdown")
    fig2.savefig(img_buffer2, format='png', bbox_inches='tight')
    img_buffer2.seek(0)
    story.append(Spacer(1, 0.2*inch))
    story.append(Image(img_buffer2, width=4*inch, height=2.5*inch))

    doc.build(story)
    pdf_buffer.seek(0)
    st.download_button("📄 Download PDF Report", pdf_buffer, "finance_report.pdf", "application/pdf", use_container_width=True)

# No balloons or animations for professional look
