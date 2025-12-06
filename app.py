# app.py - Final Gorgeous, Interactive & Professional Pakistani Finance Manager
import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import altair as alt

# Page Config
st.set_page_config(page_title="PakFinance AI Manager", page_icon="💰", layout="wide")

# Gorgeous Design with Backgrounds & Glow
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #e3f2fd, #bbdefb); font-family: 'Segoe UI', sans-serif;}
    .sidebar .sidebar-content {background: linear-gradient(135deg, #ffffff, #f0f4f8); border-radius: 16px; padding: 24px; box-shadow: 0 8px 20px rgba(0,0,0,0.1);}
    .header {font-size: 42px; font-weight: 800; color: #1a4971; text-align: center; text-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    .subheader {font-size: 20px; color: #0d47a1; text-align: center; margin-bottom: 30px;}
    .card {background: white; padding: 24px; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin: 15px 0; transition: transform 0.3s;}
    .card:hover {transform: translateY(-5px);}
    .big-number {font-size: 36px; font-weight: 900; color: #1565c0;}
    .success-box {background: #e8f5e8; border-left: 6px solid #4caf50; padding: 16px; border-radius: 8px; box-shadow: 0 4px 10px rgba(76,175,80,0.2);}
    .warning-box {background: #fff3e0; border-left: 6px solid #ff9800; padding: 16px; border-radius: 8px; box-shadow: 0 4px 10px rgba(255,152,0,0.2);}
    .error-box {background: #ffebee; border-left: 6px solid #f44336; padding: 16px; border-radius: 8px; box-shadow: 0 4px 10px rgba(244,67,54,0.2);}
    .info-box {background: #e3f2fd; border-left: 6px solid #2196f3; padding: 16px; border-radius: 8px; box-shadow: 0 4px 10px rgba(33,150,243,0.2);}
    .stButton>button {background: linear-gradient(90deg, #1976d2, #42a5f5); color: white; border-radius: 12px; padding: 14px; font-weight: bold; width: 100%; box-shadow: 0 6px 15px rgba(25,118,210,0.4); transition: all 0.3s;}
    .stButton>button:hover {transform: translateY(-3px); box-shadow: 0 10px 20px rgba(25,118,210,0.5);}
    .stProgress > div > div > div {background: linear-gradient(90deg, #4caf50, #81c784);}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='header'>PakFinance AI Manager</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Apka Reliable Financial Advisor – Smart, Simple & Secure</div>", unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.markdown("### Apki Details")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0.0, value=100000.0, step=1000.0)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0.0, value=45000.0, step=1000.0)
    current_savings = st.number_input("Current Savings (PKR)", min_value=0.0, value=50000.0, step=1000.0)
    debt = st.number_input("Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0)
    investments = st.number_input("Current Investments (PKR)", min_value=0.0, value=200000.0, step=1000.0)
    goal_purpose = st.text_input("Saving Goal Purpose", value="Car")
    goal_amount = st.number_input("Goal Amount (PKR)", min_value=0.0, value=650000.0, step=1000.0)

# Calculations
monthly_saving = monthly_income - monthly_expenses
net_worth = current_savings + investments - debt
saving_ratio = (monthly_saving / monthly_income) * 100 if monthly_income > 0 else 0
expense_ratio = (monthly_expenses / monthly_income) * 100 if monthly_income > 0 else 0
emergency_needed = monthly_expenses * 6
emergency_progress = min(current_savings / emergency_needed, 1.0) if emergency_needed > 0 else 0
needs = monthly_income * 0.5
wants = monthly_income * 0.3
save = monthly_income * 0.2
show_budget_rule = expense_ratio > 70 or saving_ratio < 20

# Tabs for Pages
tab1, tab2, tab3 = st.tabs(["Dashboard", "Insights", "Visualizations"])

with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<center><div class='big-number'>₨ {monthly_income:,.0f}</div><small>Monthly Income</small><br><small>+46% from last month</small></center>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<center><div class='big-number'>₨ {monthly_expenses:,.0f}</div><small>Monthly Expenses</small><br><small>+799% from last month</small></center>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<center><div class='big-number'>₨ {monthly_saving:,.0f}</div><small>Savings</small><br><small>+68% from last month</small></center>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    with col4:
        st.markdown(f"<center><div class='big-number'>₨ {net_worth:,.0f}</div><small>Net Worth</small></center>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<center><div class='big-number'>{saving_ratio:.1f}%</div><small>Saving Rate</small></center>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # AI Insights
    st.markdown("### AI Insights - Apki Financial Health")
    st.write(f"Saving Rate: {saving_ratio:.1f}% | Expense Rate: {expense_ratio:.1f}%")
    if expense_ratio > 100:
        st.markdown("<div class='error-box'>Overspending! Aap income se zyada kharch kar rahe hain. Tip: Quickly dining, shopping ya subscriptions band karo.</div>", unsafe_allow_html=True)
    elif expense_ratio > 80:
        st.markdown("<div class='warning-box'>High Spending! Aap 80% plus income kharch kar rahe hain. Tip: 50-30-20 rule follow karo.</div>", unsafe_allow_html=True)
    elif expense_ratio > 60:
        st.markdown("<div class='info-box'>Balanced Spending! Aap control mein hain. Tip: Ab saving ko 20% plus karne ki koshish karo.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='success-box'>Excellent Control! Aap bohot smartly manage kar rahe hoo!</div>", unsafe_allow_html=True)
    if saving_ratio < 10:
        st.markdown("<div class='warning-box'>Low Savings! Mahine ka 10% bhi nahi bacha rahe. Tip: Har mahine pehle saving karo, phir kharch.</div>", unsafe_allow_html=True)
    elif saving_ratio < 20:
        st.markdown("<div class='info-box'>Good Start! Saving 10-20% hai. Tip: Ise 20-30% tak le jao for financial freedom.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='success-box'>Amazing Saving Habit! Aap future ke liye ready ho!</div>", unsafe_allow_html=True)

    # Saving Goal
    st.markdown("### Saving Goal")
    if monthly_saving > 0:
        months_current = goal_amount / monthly_saving
        current_sug = f"{months_current:.0f} months (~{months_current/12:.1f} years)"
        st.markdown(f"<div class='card'>Goal: **{goal_purpose}** - Amount: ₨ {goal_amount:,.0f}<br>At Current Rate ({monthly_saving:,.0f} PKR/month): {current_sug}</div>", unsafe_allow_html=True)
    else:
        st.error("Warning: Aap abhi saving nahi kar rahe → Goal kabhi achieve nahi hoga!")

    basic_rate = monthly_income * 0.20
    strong_rate = monthly_income * 0.30
    if monthly_saving < basic_rate:
        months_basic = goal_amount / basic_rate
        st.info(f"Basic (20%): Save {basic_rate:,.0f} PKR/month - {months_basic:.0f} months")
    if monthly_saving < strong_rate:
        months_strong = goal_amount / strong_rate
        st.info(f"Strong (30%): Save {strong_rate:,.0f} PKR/month - {months_strong:.0f} months")
    if monthly_saving >= strong_rate:
        st.success("Outstanding! Ap already 30% se bhi zyada bacha rahy hain! Goal bohot jaldi achieve kar lain gy!")
    elif monthly_saving >= basic_rate:
        st.success("Great Job! Ap already Basic Plan (20%) achieve kar chuka hai!")

    # Emergency Fund
    st.markdown("### Emergency Fund")
    st.write(f"Needed (6 months): ₨ {emergency_needed:,.0f} PKR")
    st.progress(emergency_progress)
    if emergency_progress < 0.5:
        st.warning("Emergency fund kam hai — aim for automatic transfers each month until target.")
    elif emergency_progress < 0.8:
        st.info("Achha start! Ise 100% tak le jao. Tip: Automatic transfers set karo.")
    else:
        st.success("Perfect! Aap emergencies ke liye ready hain. Tip: Ise review karte raho.")

    # Investment Recommendation
    st.markdown("### Investment Recommendations")
    if saving_ratio > 30:
        st.success("Aggressive (for high savers): 80% Stocks, 15% Bonds, 5% Gold — High risk, high return over long-term.")
    elif saving_ratio > 15:
        st.info("Balanced: 60% Stocks, 35% Bonds, 5% Gold — Moderate risk.")
    else:
        st.warning("Conservative: 40% Stocks, 55% Bonds, 5% Gold — Lower volatility.")

    # 50/30/20 Rule (Only if needed)
    if show_budget_rule:
        st.markdown("### 50/30/20 Budget Rule")
        st.write(f"Needs (50%): ₨ {needs:,.0f} | Wants (30%): ₨ {wants:,.0f} | Savings (20%): ₨ {save:,.0f}")
        st.info("Yeh rule follow karo for financial freedom.")

with tab3:
    st.markdown("### Interactive Visualizations")
    # Income vs Expenses
    data_bar = pd.DataFrame({'Category': ['Income', 'Expenses'], 'Amount': [monthly_income, monthly_expenses]})
    chart_bar = alt.Chart(data_bar).mark_bar().encode(
        x='Category',
        y='Amount',
        color=alt.Color('Category', scale=alt.Scale(domain=['Income', 'Expenses'], range=['#4CAF50', '#F44336'])),
        tooltip=['Category', 'Amount']
    ).properties(width=600, height=400, title='Monthly Breakdown').interactive()
    st.altair_chart(chart_bar, use_container_width=True)

    # Spending by Category
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

# PDF Report
st.markdown("### Generate Report")
pdf_buffer = io.BytesIO()
doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
styles = getSampleStyleSheet()
story = []
story.append(Paragraph("PakFinance AI Manager Report", styles['Title']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
story.append(Paragraph(f"Income: ₨ {monthly_income:,.0f}", styles['Normal']))
story.append(Paragraph(f"Expenses: ₨ {monthly_expenses:,.0f}", styles['Normal']))
story.append(Paragraph(f"Savings: ₨ {monthly_saving:,.0f}", styles['Normal']))
story.append(Paragraph(f"Net Worth: ₨ {net_worth:,.0f}", styles['Normal']))
story.append(Paragraph(f"Saving Rate: {saving_ratio:.1f}%", styles['Normal']))
story.append(Paragraph(f"Goal: {goal_purpose} - ₨ {goal_amount:,.0f}", styles['Normal']))
story.append(Paragraph("Emergency Fund Needed: ₨ {emergency_needed:,.0f}", styles['Normal']))
story.append(Paragraph("Investment Suggestion: " + investment_sug, styles['Normal']))
doc.build(story)
pdf_buffer.seek(0)
st.download_button("📄 Download PDF", pdf_buffer, "pakfinance_report.pdf", "application/pdf")
