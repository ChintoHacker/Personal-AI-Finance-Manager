import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# ========================= PAGE CONFIG =========================
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="rocket", layout="wide")

# ========================= LOGIN SYSTEM =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#6CE0AC;'>Smart Financial Advisor</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Login Required</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "123":  # Change kar lena apna pasandida
                st.session_state.logged_in = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Wrong username or password")
    st.stop()

# ========================= THEME TOGGLE =========================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def switch_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# ========================= CSS (Tera Original Premium Design + Theme Support) =========================
dark_css = """
background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%);
color: white;
"""
light_css = """
background: #f8fafc;
color: #1e293b;
"""

st.markdown(f"""
<style>
    .stApp {{ {dark_css if st.session_state.theme == "dark" else light_css} font-family: 'Inter', sans-serif; }}
    .app-title {{ font-size: 42px !important; font-weight: 900 !important; color: #6CE0AC !important; text-align: center; }}
    .overview-card {{
        background: rgba(255,255,255,0.16); backdrop-filter: blur(14px); border-radius: 22px;
        padding: 26px 16px; text-align: center; border: 1.5px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 32px rgba(0,0,0,0.45); height: 155px; transition: 0.3s;
    }}
    .overview-card:hover {{ transform: translateY(-10px); }}
    .card-label {{ font-size: 16px; color: {'#E0E7FF' if st.session_state.theme=='dark' else '#64748b'}; font-weight: 600; }}
    .card-value {{ font-size: 30px; font-weight: 900; color: white; }}
    .goal-box {{
        background: rgba(255,255,255,0.17); backdrop-filter: blur(14px); border-radius: 25px;
        padding: 32px; box-shadow: 0 14px 40px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.25);
        text-align: center; animation: fadeIn 1s ease;
    }}
    @keyframes fadeIn {{ from {{opacity:0; transform:translateY(20px)}} to {{opacity:1; transform:translateY(0)}} }}
    .goal-bar {{ height: 38px; background: rgba(255,255,255,0.22); border-radius: 20px; overflow: hidden; margin: 20px 0; }}
    .goal-fill {{ height: 100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); transition: width 1.5s ease; }}
    .rec-red    {{ background: linear-gradient(135deg, rgba(239,68,68,0.35), rgba(239,68,68,0.15)); border-left: 6px solid #f87171; }}
    .rec-orange {{ background: linear-gradient(135deg, rgba(251,146,60,0.35), rgba(251,146,60,0.15)); border-left: 6px solid #fb923c; }}
    .rec-green  {{ background: linear-gradient(135deg, rgba(34,197,94,0.35), rgba(34,197,94,0.15)); border-left: 6px solid #4ade80; }}
    .rec-message {{
        font-size: 19px; font-weight: 700; line-height: 1.6; padding: 24px; border-radius: 20px;
        backdrop-filter: blur(12px); box-shadow: 0 10px 34px rgba(0,0,0,0.55); color: white; margin-top: 20px;
    }}
    .stSidebar {{ background: #2D3452 !important; }}
    .stSidebar label {{ color: #F1F5F9 !important; font-weight: 700; font-size: 17px !important; }}
    .input-section {{ background: rgba(255,255,255,0.12); border-radius: 18px; padding: 20px; border: 1px solid rgba(255,255,255,0.22); margin: 10px 0; }}
    .stButton>button {{ background: linear-gradient(90deg,#0ea5e9,#6366f1); color: white; border-radius: 50px; padding: 16px; font-weight: 700; width: 100%; border: none; }}
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

    st.markdown("---")
    st.button("Toggle Theme", on_click=switch_theme, use_container_width=True)
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ========================= CALCULATIONS =========================
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))

# ========================= RECOMMENDATION =========================
if goal_progress < 50:
    rec_color = "rec-red"
    rec_msg = "Goal bohot peeche hai!<br><b>Abhi Rs 10,000/month zyada bachaen</b>"
elif goal_progress < 90:
    rec_color = "rec-orange"
    rec_msg = "Achha progress hai!<br><b>Auto-save on karen aur focus rakhen</b>"
else:
    rec_color = "rec-green"
    rec_msg = "Mubarak ho! Goal qareeb hai<br><b>Ab naya goal set karen</b>"

# ========================= HEADER =========================
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:19px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

# ========================= OVERVIEW CARDS =========================
st.markdown("<h3 style='text-align:center; color:white; margin:40px 0 30px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

cols = st.columns(5)
cards = [("Total Amount", total_amount), ("Monthly Income", monthly_income),
         ("Monthly Expenses", monthly_expenses), ("Total Savings", current_savings), ("Net Worth", net_worth)]

for col, (label, val) in zip(cols, cards):
    col.markdown(f"""
    <div class='overview-card'>
        <div class='card-label'>{label}</div>
        <div class='card-value'>Rs {val:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ========================= GOAL + RECOMMENDATION (100% FIXED) =========================
st.markdown(f"""
<div class='goal-box'>
    <div style='font-size:24px; font-weight:800; color:white; margin-bottom:16px;'>
        {goal_name} → Target: Rs {goal_amount:,}
    </div>
    <div class='goal-bar'>
        <div class='goal-fill' style='width:{goal_progress}%'></div>
    </div>
    <div style='color:#E0E7FF; font-size:18px; font-weight:600; margin:16px 0;'>
        {goal_progress:.1f}% Complete • ETA: {months_needed} months
    </div>
    <div class='rec-message {rec_color}'>
        {rec_msg}
    </div>
</div>
""", unsafe_allow_html=True)

# ========================= CHARTS =========================
st.markdown("<h3 style='text-align:center; color:white; margin-top:50px;'>Financial Overview Chart</h3>", unsafe_allow_html=True)
chart_data = pd.DataFrame({
    "Category": ["Income", "Expenses", "Savings", "Investments"],
    "Amount (PKR)": [monthly_income, monthly_expenses, current_savings, current_investments]
})
fig = px.bar(chart_data, x="Category", y="Amount (PKR)", color="Category", text_auto=True,
             color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; background:rgba(255,255,255,0.12); padding:20px; border-radius:18px; color:#E0E7FF; font-size:17px;'>Inputs change karne ke baad 'Analyze / Predict' zaroor dabana!</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")
