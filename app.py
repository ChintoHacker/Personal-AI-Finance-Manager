# app.py - Streamlit GUI for Personal AI Finance Manager (Professional & Improved Version)
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

# Professional Custom Theme (Enhanced for Impressive Look)
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
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.5); /* Glow effect */
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 0 20px rgba(0, 123, 255, 0.7); /* Enhanced glow on hover */
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
        transform: translateY(-5px); /* Interactive lift on hover */
    }
    .block-container {
        padding: 25px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .stExpander {
        border: none;
        border-radius: 8px;
        margin-bottom: 15px;
        background-color: #f8f9fc;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .stTab {
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    /* Card-like sections for Insights */
    .insight-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .insight-card:hover {
        transform: translateY(-3px);
    }
</style>
""", unsafe_allow_html=True)

# Add Project Title at the Top
st.title("Personal AI Finance Manager")
st.markdown("Your smart companion for financial planning and predictions.")

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
    credit_score = 650
    extra = max(0, expenses - savings)
    X_new = np.array([[income, expenses, extra, credit_score]])
    X_scaled = scaler.transform(X_new)
    p = model.predict(X_scaled)[0]
    if p[0] > savings * 1.1:
        health = "Excellent"
        health_color = "#28a745"
    elif p[0] < savings * 0.9:
        health = "Poor"
        health_color = "#dc3545"
    else:
        health = "Average"
        health_color = "#ffc107"
    return {
        "next_month": round(p[0], 2),
        "next_3_months": round(p[1], 2),
        "next_6_months": round(p[2], 2),
        "health": health,
        "health_color": health_color
    }

# Sidebar for Inputs (Clean & Professional)
with st.sidebar:
    st.header("Your Financial Details")
    st.markdown("---")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0.0, value=50000.0, step=1000.0, help="Total monthly earnings.")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0.0, value=30000.0, step=1000.0, help="Total monthly spendings.")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0.0, value=10000.0, step=1000.0, help="Current saved amount.")
    debt = st.number_input("Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Loans or debts.")
    investments = st.number_input("Current Investments (PKR)", min_value=0.0, value=0.0, step=1000.0, help="Investment value.")
    age = st.number_input("Your Age", min_value=18, max_value=100, value=30, step=1, help="For suggestions.")
    goal_purpose = st.text_input("Saving Goal Purpose", value="Car", help="e.g., Car, House.")
    goal_amount = st.number_input("Goal Amount (PKR)", min_value=0.0, value=100000.0, step=1000.0, help="Target amount.")
    st.markdown("---")
    analyze_button = st.button("Analyze Finances", use_container_width=True)

if analyze_button:
    results = predict_finance(monthly_income, monthly_expenses, current_savings)
    total_balance = monthly_income - monthly_expenses + current_savings
    net_worth = current_savings + investments - debt
    emergency_needed = monthly_expenses * 6
    emergency_status = "✅ Funded" if current_savings >= emergency_needed else "⚠️ Build Now"
    emergency_progress = min(current_savings / emergency_needed, 1.0) if emergency_needed > 0 else 0
    needs = monthly_income * 0.5
    wants = monthly_income * 0.3
    save = monthly_income * 0.2
    savings_progress = min((current_savings / save) if save > 0 else 0, 1.0)
    if age < 30:
        investment_sug = "Aggressive Portfolio: 80% Stocks, 20% Gold – High growth."
    elif age < 45:
        investment_sug = "Balanced Portfolio: 60% Stocks, 30% Debt, 10% Gold – Steady."
    else:
        investment_sug = "Conservative Portfolio: 40% Stocks, 50% Debt, 10% Gold – Low risk."
    assumed_interest = 0.05 / 12
    if current_savings > 0 and monthly_income > 0:
        basic_monthly = monthly_income * 0.20
        strong_monthly = monthly_income * 0.30
        basic_months = np.log((goal_amount * assumed_interest / basic_monthly) + 1) / np.log(1 + assumed_interest) if basic_monthly > 0 else float('inf')
        strong_months = np.log((goal_amount * assumed_interest / strong_monthly) + 1) / np.log(1 + assumed_interest) if strong_monthly > 0 else float('inf')
        current_rate_months = np.log((goal_amount * assumed_interest / current_savings) + 1) / np.log(1 + assumed_interest)
        current_sug = f"{current_rate_months:.0f} months (5% interest)"
    else:
        current_sug = "Start saving!"
        basic_months = float('inf')
        strong_months = float('inf')

    # Tabs with Clear Labels
    tab1, tab2, tab3 = st.tabs(["Predictions", "Insights", "Visualizations"])

    with tab1:
        st.subheader("Financial Predictions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Balance", f"{total_balance:.2f} PKR")
        with col2:
            st.metric("Financial Health", results['health'], delta_color="normal")
        with col3:
            st.metric("Next Month Savings", f"{results['next_month']:.2f} PKR")
        # Skipped 3 and 6 months avg as per request

    with tab2:
        st.subheader("Key Insights")
        # Improved Design: Card-like sections instead of expanders
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**Net Worth Overview**")
            st.markdown(f"Current Net Worth: {net_worth:.2f} PKR")
            if net_worth < 0:
                st.warning("Negative net worth. Reduce debt.")
            else:
                st.success("Positive net worth!")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**Emergency Fund**")
            st.write(f"Needed: {emergency_needed:.2f} PKR")
            st.write(f"Status: {emergency_status}")
            st.progress(emergency_progress)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**50/30/20 Budget Rule**")
            st.write(f"Needs: {needs:.2f} PKR")
            st.write(f"Wants: {wants:.2f} PKR")
            st.write(f"Savings: {save:.2f} PKR")
            st.progress(savings_progress)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**Investment Recommendations**")
            st.info(investment_sug)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown("**Savings Goal Tracker**")
        st.write(f"Goal: {goal_purpose} – Target: {goal_amount:.2f} PKR")
        st.write(f"Time at Current Rate: {current_sug}")
        st.write(f"Basic (20%): {basic_months:.0f} months")
        st.write(f"Aggressive (30%): {strong_months:.0f} months")
        goal_progress = min(current_savings / goal_amount, 1.0) if goal_amount > 0 else 0
        st.progress(goal_progress)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Interactive Visualizations")
        # 1st Chart: Income vs Expenses (Already good)
        st.markdown("**Income vs Expenses**")
        data_bar = pd.DataFrame({'Category': ['Income', 'Expenses'], 'Amount': [monthly_income, monthly_expenses]})
        chart_bar = alt.Chart(data_bar).mark_bar(size=100).encode(
            x='Category',
            y='Amount',
            color=alt.Color('Category', scale=alt.Scale(domain=['Income', 'Expenses'], range=['#007bff', '#dc3545'])),
            tooltip=['Category', 'Amount']
        ).properties(width=600, height=400, title='Monthly Overview').interactive(bind_y=True)  # Enhanced interactivity
        st.altair_chart(chart_bar, use_container_width=True)

        # Improved 2nd Chart: Spending Breakdown (Donut style with hover effects)
        st.markdown("**Spending Breakdown**")
        categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
        base_values = [0.20, 0.25, 0.15, 0.30, 0.10]
        values = [v * monthly_expenses for v in base_values]
        data_pie = pd.DataFrame({'Category': categories, 'Amount': values})
        chart_pie = alt.Chart(data_pie).mark_arc(innerRadius=80).encode(  # Donut style
            theta='Amount:Q',
            color=alt.Color('Category:N', scale=alt.Scale(scheme='tableau10')),
            tooltip=['Category', 'Amount', alt.Tooltip('Amount:Q', format='.2f')]
        ).properties(width=600, height=400, title='Expense Categories').interactive()
        st.altair_chart(chart_pie, use_container_width=True)

        # Improved 3rd Chart: Finance Trends (Smoother lines, area fill for savings)
        st.markdown("**Finance Trends**")
        months = ["Current", "Next Month", "3 Months", "6 Months"]
        data_trend = pd.DataFrame({
            'Period': months,
            'Savings': [current_savings, results['next_month'], results['next_3_months'], results['next_6_months']],
            'Income': [monthly_income] * 4,
            'Expenses': [monthly_expenses] * 4
        }).melt('Period', var_name='Metric', value_name='Amount')
        chart_line = alt.Chart(data_trend).mark_line(point={'size': 100, 'filled': True}).encode(
            x='Period:O',
            y='Amount:Q',
            color=alt.Color('Metric:N', scale=alt.Scale(scheme='set2')),
            tooltip=['Period', 'Metric', 'Amount'],
            strokeDash=alt.condition(alt.datum.Metric == 'Savings', alt.value([5, 5]), alt.value([0]))  # Dashed for savings
        ).properties(width=800, height=450, title='Projected Trends').interactive()
        # Add area for Savings
        area = alt.Chart(data_trend[data_trend['Metric'] == 'Savings']).mark_area(opacity=0.3).encode(
            x='Period:O',
            y='Amount:Q',
            color='Metric:N'
        )
        st.altair_chart(chart_line + area, use_container_width=True)

    # Generate Report Section
    st.subheader("Generate Report")
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<font size=18>Personal Finance Report</font>", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

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
    st.download_button("Download PDF Report", pdf_buffer, "finance_report.pdf", "application/pdf", use_container_width=True)
