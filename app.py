# app.py - Streamlit GUI for Personal AI Finance Manager (Improved Version)
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
import altair as alt  # Added for interactive charts

st.set_page_config(page_title="Personal AI Finance Manager", page_icon="💰", layout="wide")

# Enhanced Custom Theme for Gorgeousness
st.markdown("""
<style>
    .main { 
        background-color: #f0f2f6; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sidebar .sidebar-content { 
        background-color: #ffffff; 
        border-right: 1px solid #e0e0e0;
        padding: 20px;
    }
    .stButton>button { 
        background-color: #4CAF50; 
        color: white; 
        border-radius: 12px; 
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stProgress .st-bo { 
        background-color: #2196F3; 
    }
    h1, h2, h3 {
        color: #333333;
        font-weight: 600;
    }
    .stMetric {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        background-color: #ffffff;
    }
    .block-container {
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load and train model (run once)
@st.cache_resource
def load_and_train_model():
    df = pd.read_csv("personal_finance_tracker_dataset.csv")
    df.columns = df.columns.str.strip()
    df['date'] = pd.to_datetime(df['date'])
    df_monthly = df.groupby(pd.Grouper(key='date', freq='ME')).agg({  # Updated to 'ME' to avoid deprecation warning
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
    credit_score = 650  # Default; can make dynamic later
    extra = max(0, expenses - savings)
    X_new = np.array([[income, expenses, extra, credit_score]])
    X_scaled = scaler.transform(X_new)
    p = model.predict(X_scaled)[0]
    if p[0] > savings * 1.1:  # Improved threshold for health
        health = "Excellent"
        health_color = "green"
    elif p[0] < savings * 0.9:
        health = "Poor"
        health_color = "red"
    else:
        health = "Average"
        health_color = "orange"
    return {
        "next_month": round(p[0], 2),
        "next_3_months": round(p[1], 2),
        "next_6_months": round(p[2], 2),
        "health": health,
        "health_color": health_color
    }

# Sidebar for inputs (Styled with Emojis and Better Layout)
st.sidebar.title("📊 Enter Your Finance Details")
st.sidebar.markdown("---")
monthly_income = st.sidebar.number_input("💼 Monthly Income (PKR)", min_value=0.0, value=50000.0, step=1000.0, help="Your total monthly earnings including salary and bonuses")
monthly_expenses = st.sidebar.number_input("🛒 Monthly Expenses (PKR)", min_value=0.0, value=30000.0, step=1000.0, help="Sum of all your monthly spendings like rent, food, etc.")
current_savings = st.sidebar.number_input("💰 Current Savings (PKR)", min_value=0.0, value=10000.0, step=1000.0, help="Your current balance in savings accounts")
debt = st.sidebar.number_input("📉 Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Outstanding loans, credit card debts, etc.")
investments = st.sidebar.number_input("📈 Current Investments (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Value of stocks, mutual funds, etc.")
age = st.sidebar.number_input("👤 Your Age", min_value=18, max_value=100, value=30, step=1, help="Helps tailor investment advice")
goal_purpose = st.sidebar.text_input("🎯 Saving Goal Purpose (e.g., Car)", value="Car", help="What are you saving for? E.g., House, Vacation")
goal_amount = st.sidebar.number_input("🏆 Goal Amount (PKR)", min_value=0.0, value=100000.0, step=1000.0, help="Target amount for your goal")
st.sidebar.markdown("---")
if st.sidebar.button("🔍 Analyze My Finances", use_container_width=True):
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
    # Investment Suggestion with more details
    if age < 30:
        investment_sug = "Aggressive: 80% Stocks, 20% Gold. Focus on high-growth options."
    elif age < 45:
        investment_sug = "Balanced: 60% Stocks, 30% Debt, 10% Gold. Mix of growth and stability."
    else:
        investment_sug = "Conservative: 40% Stocks, 50% Debt, 10% Gold. Prioritize capital preservation."
    # Saving Goal (Improved with interest assumption)
    assumed_interest = 0.05 / 12  # 5% annual interest monthly
    if current_savings > 0 and monthly_income > 0:
        basic_monthly = monthly_income * 0.20
        strong_monthly = monthly_income * 0.30
        basic_months = np.log((goal_amount * assumed_interest / basic_monthly) + 1) / np.log(1 + assumed_interest) if basic_monthly > 0 else float('inf')
        strong_months = np.log((goal_amount * assumed_interest / strong_monthly) + 1) / np.log(1 + assumed_interest) if strong_monthly > 0 else float('inf')
        current_rate_months = np.log((goal_amount * assumed_interest / current_savings) + 1) / np.log(1 + assumed_interest)
        current_sug = f"{current_rate_months:.0f} months (with 5% interest)"
    else:
        current_sug = "Start saving to calculate!"
        basic_months = float('inf')
        strong_months = float('inf')
    # Tabs for organized layout with icons
    tab1, tab2, tab3 = st.tabs(["📈 Predictions & Health", "💡 Insights & Suggestions", "📊 Charts & Visuals"])
    with tab1:
        st.subheader("Prediction Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Balance", f"{total_balance:.2f} PKR", delta=None)
        with col2:
            delta_color = "normal" if results['health'] == "Average" else ("normal" if results['health'] == "Excellent" else "inverse")
            st.metric("Financial Health", results['health'], delta_color=delta_color)
        with col3:
            st.metric("Next Month Savings", f"{results['next_month']:.2f} PKR")
        col4, col5 = st.columns(2)
        with col4:
            st.metric("Next 3 Months (Avg)", f"{results['next_3_months']:.2f} PKR")
        with col5:
            st.metric("Next 6 Months (Avg)", f"{results['next_6_months']:.2f} PKR")
    with tab2:
        st.expander("Net Worth Calculator", expanded=True).markdown(f"**Net Worth:** {net_worth:.2f} PKR (Savings + Investments - Debt)")
        expander_emergency = st.expander("Emergency Fund Status", expanded=True)
        with expander_emergency:
            st.write(f"Needed for 6 Months: {emergency_needed:.2f} PKR")
            st.write(f"Status: {emergency_status}")
            st.progress(emergency_progress)
            if emergency_progress < 1:
                st.warning("Build your emergency fund!")
        expander_rule = st.expander("50/30/20 Rule Checker", expanded=True)
        with expander_rule:
            st.write(f"Needs (50%): {needs:.2f} PKR")
            st.write(f"Wants (30%): {wants:.2f} PKR")
            st.write(f"Savings (20%): {save:.2f} PKR")
            st.progress(savings_progress)
            if savings_progress < 0.5:
                st.info("Tip: Aim to save at least 20% of income.")
        expander_invest = st.expander("Investment Suggestion", expanded=True)
        with expander_invest:
            st.info(investment_sug)
        expander_goal = st.expander("Saving Goals", expanded=True)
        with expander_goal:
            st.write(f"Goal: {goal_purpose} - Amount: {goal_amount:.2f} PKR")
            st.write(f"Current Rate: {current_sug}")
            st.write(f"Basic (20%): Save {monthly_income * 0.20:.2f} PKR/month - {basic_months:.0f} months")
            st.write(f"Strong (30%): Save {monthly_income * 0.30:.2f} PKR/month - {strong_months:.0f} months")
            goal_progress = min(current_savings / goal_amount, 1.0) if goal_amount > 0 else 0
            st.progress(goal_progress)
    with tab3:
        st.subheader("Income vs Expenses (Interactive Bar Chart)")
        data_bar = pd.DataFrame({
            'Category': ['Income', 'Expenses'],
            'Amount': [monthly_income, monthly_expenses]
        })
        chart_bar = alt.Chart(data_bar).mark_bar().encode(
            x='Category',
            y='Amount',
            color=alt.Color('Category', scale=alt.Scale(domain=['Income', 'Expenses'], range=['#4CAF50', '#F44336'])),
            tooltip=['Category', 'Amount']
        ).properties(width=600, height=400, title='Monthly Income vs Expenses')
        st.altair_chart(chart_bar, use_container_width=True)

        st.subheader("Spending by Category (Pie Chart)")
        # Made slightly dynamic based on expenses
        categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
        base_values = [0.20, 0.25, 0.15, 0.30, 0.10]
        values = [v * monthly_expenses for v in base_values]
        data_pie = pd.DataFrame({'Category': categories, 'Percentage': values})
        chart_pie = alt.Chart(data_pie).mark_arc().encode(
            theta='Percentage:Q',
            color='Category:N',
            tooltip=['Category', 'Percentage']
        ).properties(width=400, height=400, title='Spending by Category').interactive()
        st.altair_chart(chart_pie, use_container_width=True)

        st.subheader("Finance Trend Over Time (Line Chart)")
        months = ["Current", "Next Month", "Next 3 Months", "Next 6 Months"]
        data_trend = pd.DataFrame({
            'Month': months,
            'Savings': [current_savings, results['next_month'], results['next_3_months'], results['next_6_months']],
            'Income': [monthly_income] * 4,
            'Expenses': [monthly_expenses] * 4
        }).melt('Month', var_name='Type', value_name='Amount')
        chart_line = alt.Chart(data_trend).mark_line(point=True).encode(
            x='Month:O',
            y='Amount:Q',
            color='Type:N',
            tooltip=['Month', 'Type', 'Amount']
        ).properties(width=800, height=400, title='Finance Trend').interactive()
        st.altair_chart(chart_line, use_container_width=True)

        # New Chart: Goal Progress
        st.subheader("Saving Goal Progress")
        goal_progress = min(current_savings / goal_amount, 1.0) if goal_amount > 0 else 0
        st.progress(goal_progress)
        st.write(f"Progress towards {goal_purpose}: {goal_progress * 100:.1f}%")

    # Enhanced PDF Report with Table and Charts
    st.subheader("Download Your Report")
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<font size=18>Personal AI Finance Manager Report</font>", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Add Table for Key Metrics
    data = [
        ['Metric', 'Value'],
        ['Net Worth', f"{net_worth:.2f} PKR"],
        ['Financial Health', results['health']],
        ['Total Balance', f"{total_balance:.2f} PKR"],
        ['Next Month Savings', f"{results['next_month']:.2f} PKR"],
        ['Emergency Fund', f"{emergency_status} (Needed: {emergency_needed:.2f} PKR)"],
        ['50/30/20 Rule', f"Needs {needs:.2f} | Wants {wants:.2f} | Savings {save:.2f}"],
        ['Investment Suggestion', investment_sug],
        ['Saving Goal', f"{goal_purpose}: {goal_amount:.2f} PKR"],
        ['Current Rate', current_sug],
        ['Basic (20%)', f"{basic_months:.0f} months"],
        ['Strong (30%)', f"{strong_months:.0f} months"]
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(table)

    # Add Charts as Images
    # Income vs Expenses
    img_buffer1 = io.BytesIO()
    plt.figure(figsize=(6,4))
    plt.bar(["Income", "Expenses"], [monthly_income, monthly_expenses], color=['#4CAF50', '#F44336'])
    plt.title("Income vs Expenses")
    plt.ylabel("PKR")
    plt.savefig(img_buffer1, format='png')
    img_buffer1.seek(0)
    story.append(Spacer(1, 0.2*inch))
    story.append(Image(img_buffer1, width=4*inch, height=3*inch))

    # Spending Pie
    img_buffer2 = io.BytesIO()
    plt.figure(figsize=(6,4))
    plt.pie(values, labels=categories, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
    plt.title("Spending by Category")
    plt.savefig(img_buffer2, format='png')
    img_buffer2.seek(0)
    story.append(Spacer(1, 0.2*inch))
    story.append(Image(img_buffer2, width=4*inch, height=3*inch))

    doc.build(story)
    pdf_buffer.seek(0)
    st.download_button("📄 Download PDF Report", pdf_buffer, "finance_report.pdf", "application/pdf", use_container_width=True)

# Fun Animation on Load
st.balloons()
