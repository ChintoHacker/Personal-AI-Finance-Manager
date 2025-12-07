import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import math

st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="money_with_wings", layout="wide")

# ==============================
# FULL STYLING
# ==============================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%);
        color: #F7FAFC;
        font-family: "Inter", sans-serif;
    }
    .app-title {
        font-size: 38px !important;
        font-weight: 900 !important;
        color: #6CE0AC !important;
        letter-spacing: 0.5px;
    }
    /* Cards */
    .stat-card {
        background: rgba(126,126,150,0.9);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stat-label { font-size: 15px; color: #E0E7FF; }
    .stat-value { font-size: 26px; font-weight: 900; color: white; margin-top: 6px; }

    /* Goal Bar */
    .goal-wrap {
        background: rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    .goal-bar { height: 28px; background: rgba(255,255,255,0.2); border-radius: 14px; overflow: hidden; margin: 12px 0; }
    .goal-fill { height: 100%; background: linear-gradient(90deg, #06b6d4, #7c3aed); border-radius: 14px; }

    /* Tiles */
    .tile {
        background: rgba(255,255,255,0.15);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.25);
        height: 100%;
    }
    .tile-warn { border-left: 6px solid #fb7185; }
    .tile-good { border-left:6px solid #10b981; }
    .tile-title { font-size: 17px; font-weight: 700; color: white; }
    .tile-sub { font-size: 14px; color: #E0E7FF; margin-top: 6px; }

    /* Sidebar */
    .stSidebar {
        background: #2D3452 !important;
    }
    .stSidebar label {
        color: #E0E7FF !important;
        font-weight: 700 !important;
        font-size: 17px !important;
    }
    .input-section {
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 20px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 30px;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .date-badge {
        background: rgba(255,255,255,0.2);
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.3);
        display: inline-block;
    }
    .tip-box {
        background: rgba(255,255,255,0.12);
        padding: 16px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.2);
        font-size: 15px;
        color: #E0E7FF;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================
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
        st.session_state.analyzed = True
        st.success("Analysis Updated")

# ==============================
# CALCULATIONS
# ==============================
total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)

goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
emergency_months = round(current_savings / max(1, monthly_expenses), 1)

# ==============================
# HEADER
# ==============================
col1, col2 = st.columns([5,1])
with col1:
    st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='date-badge'>Today {datetime.now().strftime('%d %b %Y')}</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Nav
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Overview", use_container_width=True): st.session_state.page = "overview"
with c2:
    if st.button("AI Insights", use_container_width=True): st.session_state.page = "insights"
with c3:
    if st.button("Visuals", use_container_width=True): st.session_state.page = "visuals"

if "page" not in st.session_state:
    st.session_state.page = "overview"

# ==============================
# LANDING PAGE (exact order jo tune manga)
# ==============================
if st.session_state.page == "overview":
    st.markdown("<h3>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

    # 1. Cards
    cols = st.columns(5)
    data = [
        ("Total Balance", total_balance),
        ("Monthly Income", monthly_income),
        ("Monthly Expenses", monthly_expenses),
        ("Savings", current_savings),
        ("Net Worth", net_worth)
    ]
    for col, (label, value) in zip(cols, data):
        col.markdown(f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>Rs {value:,}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # 2. Goal Progress
    st.markdown("<h4>Goal Progress</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='goal-wrap'>
        <div style='font-size:19px; font-weight:700; color:white; margin-bottom:10px;'>{goal_name} → Rs {goal_amount:,}</div>
        <div class='goal-bar'><div class='goal-fill' style='width:{goal_progress}%'></div></div>
        <div style='display:flex; justify-content:space-between; color:#E0E7FF; font-size:15px;'>
            <span><b>{goal_progress:.1f}%</b> Complete • Rs {current_savings:,} saved</span>
            <span><b>ETA:</b> {months_needed} months</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Recommended Actions
    st.markdown("<h4>Recommended Actions</h4>", unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
        <div class='tile {"tile-good" if monthly_save >= 0.2*monthly_income else "tile-warn"}'>
            <div class='tile-title'>{"Great Saving!" if monthly_save >= 0.2*monthly_income else "Increase Monthly Saving"}</div>
            <div class='tile-sub'>Currently saving Rs {monthly_save:,}/mo<br><b>Aim for 20% of income</b></div>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class='tile {"tile-good" if total_debt == 0 else "tile-warn"}'>
            <div class='tile-title'>{"Debt Free" if total_debt == 0 else "Clear Debt"}</div>
            <div class='tile-sub'>Outstanding: Rs {total_debt:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. Quick Insights (sabse neeche)
    st.markdown("<h4>Quick Insights</h4>", unsafe_allow_html=True)
    insights = [
        ("Emergency Fund", f"{emergency_months} months", "Good" if emergency_months >= 6 else "Low"),
        ("Savings Rate", f"{(monthly_save/monthly_income*100):.0f}%", "Good" if monthly_save >= 0.2*monthly_income else "Low"),
        ("Goal Progress", f"{goal_progress:.0f}%", "Good" if goal_progress >= 50 else "Behind"),
        ("Debt Status", "No Debt" if total_debt==0 else f"Rs {total_debt:,}", "Good" if total_debt==0 else "Warning")
    ]
    i1,i2,i3,i4 = st.columns(4)
    for col, (title, value, status) in zip([i1,i2,i3,i4], insights):
        cls = "tile-good" if "Good" in status else "tile-warn"
        col.markdown(f"""
        <div class='tile {cls}'>
            <div class='tile-title'>{"Check" if "Good" in status else "Warning"} {title}</div>
            <div class='tile-sub'>{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='tip-box'>Tip: Click 'Analyze / Predict' in sidebar after changing any value to refresh insights!</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Your Personal Financial Advisor - Made with love")
