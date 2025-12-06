# app.py — Final Professional & Beautiful Pakistani Finance Manager
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

# Page Config
st.set_page_config(page_title="PakFinance AI", page_icon="Pakistan Flag", layout="wide")

# Gorgeous Design
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #e3f2fd, #bbdefb); font-family: 'Segoe UI', sans-serif;}
    .header {font-size: 46px; font-weight: 800; color: #1a4971; text-align: center; text-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    .subheader {font-size: 20px; color: #0d47a1; text-align: center; margin-bottom: 30px;}
    .card {background: white; padding: 24px; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin: 15px 0;}
    .big-number {font-size: 36px; font-weight: 900; color: #1565c0;}
    .success-box {background: #e8f5e8; border-left: 6px solid #4caf50; padding: 16px; border-radius: 8px;}
    .warning-box {background: #fff3e0; border-left: 6px solid #ff9800; padding: 16px; border-radius: 8px;}
    .error-box {background: #ffebee; border-left: 6px solid #f44336; padding: 16px; border-radius: 8px;}
    .info-box {background: #e3f2fd; border-left: 6px solid #2196f3; padding: 16px; border-radius: 8px;}
    .stButton>button {background: linear-gradient(90deg, #1976d2, #42a5f5); color: white; border-radius: 12px; padding: 14px; font-weight: bold; width: 100%; box-shadow: 0 6px 15px rgba(25,118,210,0.4);}
    .stButton>button:hover {transform: translateY(-3px); box-shadow: 0 10px 20px rgba(25,118,210,0.5);}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='header'>PakFinance AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Apka Smart Financial Dost — Bilkul Pakistani Style Mein</div>", unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.image("https://flagcdn.com/pk.png", width=80)
    st.markdown("### Your Details")
    monthly_income = st.number_input("Monthly Income (PKR)", 20000, 500000, 80000, 5000)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", 10000, 400000, 45000, 5000)
    current_savings = st.number_input("Current Savings (PKR)", 0, 10000000, 100000, 10000)
    debt = st.number_input("Total Debt (PKR)", 0, 5000000, 0, 5000)
    investments = st.number_input("Current Investments (PKR)", 0, 10000000, 50000, 10000)
    goal_purpose = st.text_input("Saving Goal", "Car")
    goal_amount = st.number_input("Goal Amount (PKR)", 100000, 50000000, 1500000, 50000)

    if st.button("Analyze My Finances"):
        st.success("Analysis Complete!")

# Calculations
monthly_saving = monthly_income - monthly_expenses
net_worth = current_savings + investments - debt
saving_ratio = (monthly_saving / monthly_income) * 100 if monthly_income > 0 else 0
expense_ratio = (monthly_expenses / monthly_income) * 100 if monthly_income > 0 else 0
emergency_needed = monthly_expenses * 6
emergency_progress = min(current_savings / emergency_needed, 1.0) if emergency_needed > 0 else 0

# Main Layout
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='card'><center><div class='big-number'>₨ {monthly_saving:,.0f}</div><small>Monthly Saving</small></center></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card'><center><div class='big-number'>₨ {net_worth:,.0f}</div><small>Net Worth</small></center></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='card'><center><div class='big-number'>{saving_ratio:.1f}%</div><small>Saving Rate</small></center></div>", unsafe_allow_html=True)

# AI Insights
st.markdown("### AI Insights - Apki Financial Health")
st.write(f"**Saving Rate:** {saving_ratio:.1f}% | **Expense Rate:** {expense_ratio:.1f}%")

if expense_ratio > 100:
    st.markdown("<div class='error-box'>Overspending! Aap income se zyada kharch kar rahe hain.</div>", unsafe_allow_html=True)
elif expense_ratio > 80:
    st.markdown("<div class='warning-box'>High Spending! 80%+ income kharch ho raha. 50-30-20 rule follow karo.</div>", unsafe_allow_html=True)
elif expense_ratio > 60:
    st.markdown("<div class='info-box'>Balanced Spending! Ab saving 20%+ karne ki koshish karo.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='success-box'>Excellent Control! Aap bohot smartly manage kar rahe ho!</div>", unsafe_allow_html=True)

if saving_ratio < 10:
    st.markdown("<div class='warning-box'>Low Savings! Mahine ka 10% bhi nahi bacha rahe. Pehle saving karo, phir kharch.</div>", unsafe_allow_html=True)
elif saving_ratio < 20:
    st.markdown("<div class='info-box'>Good Start! 10-20% saving hai. Ise 30% tak le jao.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='success-box'>Amazing Saving Habit! Aap future ke liye ready ho!</div>", unsafe_allow_html=True)

# Saving Goal
st.markdown("### Saving Goal")
if monthly_saving > 0:
    months = goal_amount / monthly_saving
    st.markdown(f"<div class='card'>Goal: **{goal_purpose}** — ₨ {goal_amount:,.0f}<br>At current rate: **{months:.0f} months** (~{months/12:.1f} years)</div>", unsafe_allow_html=True)
    
    basic = monthly_income * 0.20
    strong = monthly_income * 0.30
    if monthly_saving < basic:
        st.info(f"**Basic Plan (20%)**: Save ₨ {basic:,.0f}/month → {goal_amount/basic:.0f} months")
    if monthly_saving < strong:
        st.info(f"**Strong Plan (30%)**: Save ₨ {strong:,.0f}/month → {goal_amount/strong:.0f} months")
    if monthly_saving >= strong:
        st.success("Outstanding! Ap already 30%+ bacha rahe hain! Goal jaldi poora hoga!")
    elif monthly_saving >= basic:
        st.success("Great Job! Ap Basic Plan achieve kar chuke hain!")
else:
    st.error("Aap abhi saving nahi kar rahe — Goal kabhi achieve nahi hoga!")

# Emergency Fund
st.markdown("### Emergency Fund")
st.write(f"Needed (6 months expenses): ₨ {emergency_needed:,.0f}")
st.progress(emergency_progress)
if emergency_progress >= 1:
    st.success("Complete! Aap fully protected hain.")
elif emergency_progress >= 0.7:
    st.info("Almost there! Thodi aur saving karo.")
else:
    st.warning("Emergency fund kam hai — mahine ka 10-20% add karo.")

# Investment Recommendation
st.markdown("### Investment Recommendation")
if saving_ratio > 30:
    st.success("**Aggressive**: 80% Stocks, 20% Gold/Funds — High growth")
elif saving_ratio > 15:
    st.info("**Balanced**: 60% Stocks, 30% Debt, 10% Gold — Steady growth")
else:
    st.warning("**Conservative**: Pehle emergency fund banao, phir low-risk se shuru karo")

# 50/30/20 Rule (Only if needed)
if expense_ratio > 70 or saving_ratio < 20:
    st.markdown("### 50/30/20 Budget Rule")
    needs = monthly_income * 0.5
    wants = monthly_income * 0.3
    save = monthly_income * 0.2
    st.write(f"Needs (50%): ₨ {needs:,.0f} | Wants (30%): ₨ {wants:,.0f} | Savings (20%): ₨ {save:,.0f}")
    st.info("Yeh rule follow karo for financial freedom.")

# PDF Report
def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("PakFinance AI Report", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d %B %Y')}", styles['Normal']))
    story.append(Paragraph(f"Monthly Income: ₨ {monthly_income:,.0f}", styles['Normal']))
    story.append(Paragraph(f"Monthly Saving: ₨ {monthly_saving:,.0f} ({saving_ratio:.1f}%)", styles['Normal']))
    story.append(Paragraph(f"Net Worth: ₨ {net_worth:,.0f}", styles['Normal']))
    story.append(Paragraph(f"Goal: {goal_purpose} — ₨ {goal_amount:,.0f}", styles['Normal']))
    story.append(Paragraph("Keep up the great work!", styles['Normal']))
    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("Download PDF Report"):
    pdf = create_pdf()
    st.download_button("Download Now", pdf, "PakFinance_Report.pdf", "application/pdf")

st.markdown("<br><center>Made with Pakistan for Pakistanis by Grok</center>", unsafe_allow_html=True)
