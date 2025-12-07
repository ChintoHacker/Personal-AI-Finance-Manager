import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

# ============================================
#               PAGE STATE
# ============================================
if "page" not in st.session_state:
    st.session_state.page = "overview"

def switch_page(p):
    st.session_state.page = p


# ============================================
#               GLOBAL CSS
# ============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }

    .glow-btn {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        color: white;
        border: none;
        padding: 14px 32px;
        margin: 0 10px;
        border-radius: 50px;
        font-size: 17px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(139,92,246,0.5);
        transition: 0.3s ease;
    }
    .glow-btn:hover { transform: translateY(-4px) scale(1.05); }

    .glow-btn-active {
        background: linear-gradient(45deg, #10b981, #34d399);
        box-shadow: 0 0 25px rgba(16,185,129,0.8);
        color: white;
    }

    .overview-card {
        background: rgba(255,255,255,0.16); backdrop-filter: blur(14px); border-radius: 22px;
        padding: 26px 16px; text-align: center; border: 1.5px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 32px rgba(0,0,0,0.45); height: 155px;
    }

    .meter-box {
        background: rgba(255,255,255,0.18); border-radius: 20px; padding: 25px;
        text-align:center; border:1px solid rgba(255,255,255,0.25);
        box-shadow: 0 8px 25px rgba(0,0,0,0.45);
    }

    .meter-bar {
        height: 40px; background: rgba(255,255,255,0.22); border-radius: 18px;
        overflow: hidden; margin: 15px 0;
    }

    .meter-fill {
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
        transition: 0.6s ease;
    }

    .suggest-red {
        background: rgba(239,68,68,0.4); color:#fee2e2; border-left: 8px solid #ef4444;
        padding:20px; border-radius:18px; font-size:19px; text-align:center;
    }
    .suggest-orange {
        background: rgba(251,146,60,0.4); color:#fff7ed; border-left: 8px solid #fb923c;
        padding:20px; border-radius:18px; font-size:19px; text-align:center;
    }
    .suggest-green {
        background: rgba(34,197,94,0.5); color:white; border-left: 8px solid #22c55e;
        padding:20px; border-radius:18px; font-size:19px; text-align:center;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
#               SIDEBAR INPUT
# ============================================
with st.sidebar:
    st.markdown("<h2 style='color:#6CE0AC; text-align:center;'>Apki Financial Inputs</h2>", unsafe_allow_html=True)

    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000)
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=150000, step=5000)
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000)
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=50000, step=1000)

    if st.button("Update"):
        st.success("Updated!")


# ============================================
#               CALCULATIONS
# ============================================
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)


# ============================================
#         PAGE NAVIGATION BUTTONS
# ============================================
st.markdown("<br>", unsafe_allow_html=True)

colA, colB, colC = st.columns(3)
with colA:
    if st.button("Overview", key="ov", use_container_width=True):
        switch_page("overview")
with colB:
    if st.button("Insights", key="ins", use_container_width=True):
        switch_page("insights")
with colC:
    if st.button("Visuals", key="vis", use_container_width=True):
        switch_page("visuals")


# ============================================
#                PAGE 1 — OVERVIEW
# ============================================
if st.session_state.page == "overview":

    st.markdown("<h1 style='text-align:center; color:#6CE0AC;'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)

    cols = st.columns(5)
    for col, (label, val) in zip(cols, [
        ("Total Amount", total_amount),
        ("Monthly Income", monthly_income),
        ("Monthly Expenses", monthly_expenses),
        ("Total Savings", current_savings),
        ("Net Worth", net_worth)
    ]):
        col.markdown(f"""
        <div class='overview-card'>
            <h4 style='color:white;'>{label}</h4>
            <h2 style='color:white;'>Rs {val:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)



# ============================================
#     PAGE 2 — INSIGHTS (Emergency Fund)
# ============================================
if st.session_state.page == "insights":

    st.markdown("<h1 style='text-align:center; color:#6CE0AC;'>AI Insights</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:white; text-align:center;'>Emergency Fund Status</h3>", unsafe_allow_html=True)

    required_fund = monthly_expenses * 3
    progress = (current_savings / required_fund) * 100 if required_fund > 0 else 0
    progress = min(progress, 100)

    # meter
    st.markdown(f"""
    <div class='meter-box'>
        <h3 style='color:white;'>Required: Rs {required_fund:,}</h3>
        <div class='meter-bar'>
            <div class='meter-fill' style='width:{progress}%'></div>
        </div>
        <h4 style='color:#E0E7FF;'>{progress:.1f}% Ready</h4>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Suggestions
    if progress < 50:
        st.markdown("<div class='suggest-red'>Emergency fund bohot kam hai!<br><b>Action:</b> Thori si savings badhain.</div>", unsafe_allow_html=True)
    elif progress < 80:
        st.markdown("<div class='suggest-orange'>Acha progress!<br><b>Next:</b> Monthly thora aur save karein.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='suggest-green'>Excellent!<br>Emergency fund complete ke qareeb ya complete!</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)



# ============================================
#      PAGE 3 — VISUALS (Existing)
# ============================================
if st.session_state.page == "visuals":

    st.markdown("<h1 style='color:white; text-align:center;'>Financial Overview</h1>", unsafe_allow_html=True)

    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })

    fig = px.bar(chart_data, x="Category", y="Amount",
                 text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
                 color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])

    fig.update_traces(textposition='outside', textfont_size=16)
    fig.update_layout(showlegend=False, height=500)

    st.plotly_chart(fig, use_container_width=True)

