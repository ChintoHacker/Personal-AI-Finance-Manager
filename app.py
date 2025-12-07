import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

# ========================= LOGIN =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#6CE0AC;'>Smart Financial Advisor</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.logged_in = True
                st.success("Welcome back!")
                st.rerun()
            else:
                st.error("Wrong credentials")
    st.stop()

# ========================= CSS (FINAL PREMIUM + CELEBRATION) =========================
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }
    .app-title { font-size: 42px !important; font-weight: 900 !important; color: #6CE0AC !important; text-align: center; }
    .overview-card {
        background: rgba(255,255,255,0.16); backdrop-filter: blur(14px); border-radius: 22px;
        padding: 26px 16px; text-align: center; border: 1.5px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 32px rgba(0,0,0,0.45); height: 155px; transition: 0.3s;
    }
    .overview-card:hover { transform: translateY(-10px); }
    .card-label { font-size: 16px; color: #E0E7FF; font-weight: 600; }
    .card-value { font-size: 30px; font-weight: 900; color: white; }
    .goal-box {
        background: rgba(255,255,255,0.17); backdrop-filter: blur(14px); border-radius: 25px;
        padding: 32px; box-shadow: 0 14px 40px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.25);
        text-align: center;
    }
    .goal-bar { height: 38px; background: rgba(255,255,255,0.22); border-radius: 20px; overflow: hidden; margin: 22px 0; }
    .goal-fill { height: 100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); }
    
    /* RECOMMENDATION & CELEBRATION */
    .rec-red    { background: linear-gradient(135deg, rgba(239,68,68,0.5), rgba(239,68,68,0.2)); border-left: 8px solid #f87171; color: #fee2e2; }
    .rec-orange { background: linear-gradient(135deg, rgba(251,146,60,0.5), rgba(251,146,60,0.2)); border-left: 8px solid #fb923c; color: #fff7ed; }
    .rec-green  { background: linear-gradient(135deg, rgba(34,197,94,0.6), rgba(34,197,94,0.3)); border-left: 8px solid #4ade80; color: white; }
    .rec-celebrate { background: linear-gradient(135deg, #f0e, #8b5cf6, #ec4899); color: white; animation: celebrate 2s infinite; }
    @keyframes celebrate { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    
    .rec-message {
        font-size: 21px; font-weight: 700; line-height: 1.6; padding: 30px; border-radius: 24px;
        backdrop-filter: blur(14px); box-shadow: 0 12px 40px rgba(0,0,0,0.6); margin-top: 20px;
        text-align: center;
    }
    .plan-card {
        background: rgba(255,255,255,0.15); border-radius: 20px; padding: 24px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: 0.3s; height: 150px;
    }
    .plan-card:hover { transform: translateY(-8px); }
    .stSidebar { background: #2D3452 !important; }
    .stSidebar label { color: #F1F5F9 !important; font-weight: 700; font-size: 17px !important; }
    .input-section { background: rgba(255,255,255,0.12); border-radius: 18px; padding: 20px; border: 1px solid rgba(255,255,255,0.22); margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# ========================= SIDEBAR =========================
with st.sidebar:
    st.markdown("<h2 style='color:#6CE0AC; text-align:center;'>Apki Financial Inputs</h2>", unsafe_allow_html=True)
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000)
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=150000, step=5000)
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000)
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=50000, step=1000)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    goal_name = st.text_input("Goal Name", value="Dream House")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=1, value=5000000, step=50000)

    if st.button("Analyze / Predict", type="primary", use_container_width=True):
        st.success("Analysis Updated!")

# ========================= CALCULATIONS =========================
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))

remaining = max(0, goal_amount - current_savings)

# ========================= SMART RECOMMENDATION + CELEBRATION =========================
if goal_progress >= 100:
    rec_color = "rec-celebrate"
    rec_msg = "GOAL ACHIEVED!<br><b>Mubarak ho bhai!</b><br>Aap ne kar dikhaya! Ab naya bada goal set karen"
elif goal_progress < 50:
    rec_color = "rec-red"
    rec_msg = "Goal bohot door hai!<br><b>Action:</b> Har cheez se 15% cut karen<br><b>Extra:</b> Side income start karen"
elif goal_progress < 90:
    rec_color = "rec-orange"
    rec_msg = "Bahut achha ja rahe hain!<br><b>Next Level:</b> Auto-invest on karen<br><b>Tip:</b> Budget app use karen"
else:
    rec_color = "rec-green"
    rec_msg = "Goal qareeb hai!<br><b>Final Push:</b> Thodi si zyada saving<br><b>Shabash!</b> Bas thoda aur!"

# ========================= SMART PLANS (Dynamic & Realistic) =========================
show_plans = goal_progress < 95  # Sirf jab tak goal complete na ho

if show_plans:
    if goal_progress < 50:
        basic_save = monthly_income * 0.25
        strong_save = monthly_income * 0.40
    elif goal_progress < 80:
        basic_save = monthly_income * 0.18
        strong_save = monthly_income * 0.28
    else:
        basic_save = monthly_income * 0.12
        strong_save = monthly_income * 0.20

    basic_time = "N/A" if basic_save <= 0 else round(remaining / basic_save)
    strong_time = "N/A" if strong_save <= 0 else round(remaining / strong_save)

# ========================= HEADER =========================
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:19px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

# ========================= OVERVIEW CARDS =========================
st.markdown("<h3 style='text-align:center; color:white; margin:40px 0 30px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
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
        <div class='card-label'>{label}</div>
        <div class='card-value'>Rs {val:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ========================= GOAL SECTION =========================
st.markdown("<h3 style='text-align:center; color:white; margin-bottom:30px;'>Goal Progress & Smart Plans</h3>", unsafe_allow_html=True)

st.markdown(f"""
<div class='goal-box'>
    <div style='font-size:24px; font-weight:800; color:white; margin-bottom:16px;'>
        {goal_name} → Target: Rs {goal_amount:,}
    </div>
    <div class='goal-bar'>
        <div class='goal-fill' style='width:{goal_progress}%'></div>
    </div>
    <div style='color:#E0E7FF; font-size:18px; font-weight:600; margin:16px 0;'>
        {goal_progress:.1f}% Complete • Current ETA: {months_needed} months
    </div>
    <div class='rec-message {rec_color}'>
        {rec_msg}
    </div>
</div>
""", unsafe_allow_html=True)

# ========================= SMART PLANS =========================
if show_plans:
    st.markdown("<h4 style='text-align:center; color:white; margin-top:40px;'>Personalized Savings Plans</h4>", unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(f"""
        <div class='plan-card'>
            <b>Basic Plan</b><br>
            Save <b>Rs {int(basic_save):,}/month</b><br>
            <span style='color:#a0d9ff; font-size:17px;'>Time: {basic_time} months</span>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
        <div class='plan-card'>
            <b>Strong Plan</b><br>
            Save <b>Rs {int(strong_save):,}/month</b><br>
            <span style='color:#a0d9ff; font-size:17px;'>Time: {strong_time} months</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ========================= FINAL CHART (100% CLEAR LABELS) =========================
st.markdown("<h3 style='text-align:center; color:white;'>Financial Overview</h3>", unsafe_allow_html=True)
chart_data = pd.DataFrame({
    "Category": ["Income", "Expenses", "Savings", "Investments"],
    "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
})
fig = px.bar(chart_data, x="Category", y="Amount", color="Category",
             text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
             color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
fig.update_traces(textposition='outside', textfont_size=17, textfont_color="white")
fig.update_layout(
    showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    height=500, font=dict(color="white", size=16),
    yaxis=dict(showgrid=False, title="Amount (PKR)", color="white"),
    xaxis=dict(color="white")
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='text-align:center; background:rgba(255,255,255,0.12); padding:20px; border-radius:18px; color:#E0E7FF; font-size:17px;'>Tip: Inputs change karen? → 'Analyze / Predict' dabana na bhoolen!</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")
