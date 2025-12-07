import streamlit as st
from datetime import datetime
import math

st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="money_with_wings", layout="wide")

# ==============================
# PREMIUM STYLING
# ==============================
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }
    .app-title { font-size: 40px !important; font-weight: 900 !important; color: #6CE0AC !important; }
    
    /* SUPER PREMIUM CARDS */
    .overview-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 24px 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .overview-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
    }
    .card-label {
        font-size: 15px;
        color: #E0E7FF;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .card-value {
        font-size: 28px;
        font-weight: 900;
        color: white;
        letter-spacing: 0.5px;
    }

    /* Goal & Other Sections */
    .goal-wrap, .tile, .input-section, .tip-box { 
        background: rgba(255,255,255,0.12); 
        border-radius: 16px; 
        padding: 20px; 
        border: 1px solid rgba(255,255,255,0.2); 
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    .goal-bar { height: 30px; background: rgba(255,255,255,0.2); border-radius: 15px; overflow: hidden; margin: 12px 0; }
    .goal-fill { height: 100%; background: linear-gradient(90deg, #06b6d4, #7c3aed); border-radius: 15px; }
    .tile-warn { border-left: 6px solid #fb7185; }
    .tile-good { border-left: 6px solid #10b981; }

    /* Sidebar */
    .stSidebar { background: #2D3452 !important; }
    .stSidebar label { color: #E0E7FF !important; font-weight: 700; font-size: 17px !important; }
    .input-section { margin: 10px 0; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white; border: none; border-radius: 50px;
        padding: 14px; font-weight: 700; box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { transform: translateY(-4px); }
</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR (same as before)
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
    goal_name = st.text_input("Goal Name", "Dream House")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=1, value=5000000, step=50000)

    if st.button("Analyze / Predict", type="primary", use_container_width=True):
        st.success("Analysis Updated")

# ==============================
# CALCULATIONS
# ==============================
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
emergency_months = round(current_savings / max(1, monthly_expenses), 1)

# ==============================
# HEADER
# ==============================
col1, col2 = st.columns([4,1])
with col1:
    st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='background:rgba(255,255,255,0.2); padding:12px 20px; border-radius:30px; text-align:center; font-weight:600;'>Today {datetime.now().strftime('%d %b %Y')}</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Nav
c1, c2, c3 = st.columns(3)
with c1: if st.button("Overview", use_container_width=True): st.session_state.page = "overview"
with c2: if st.button("AI Insights", use_container_width=True): st.session_state.page = "insights"
with c3: if st.button("Visuals", use_container_width=True): st.session_state.page = "visuals"
if "page" not in st.session_state:
    st.session_state.page = "overview"

# ==============================
# MAIN PAGE - ONLY OVERVIEW IMPROVED
# ==============================
if st.session_state.page == "overview":
    st.markdown("<h3 style='text-align:center; color:#fff;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 5 PREMIUM CARDS - YEH WAHI HAI JO TU CHAHTA THA
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class='overview-card'>
            <div class='card-label'>Total Amount</div>
            <div class='card-value'>Rs {total_amount:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='overview-card'>
            <div class='card-label'>Monthly Income</div>
            <div class='card-value'>Rs {monthly_income:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='overview-card'>
            <div class='card-label'>Monthly Expenses</div>
            <div class='card-value'>Rs {monthly_expenses:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='overview-card'>
            <div class='card-label'>Total Savings</div>
            <div class='card-value'>Rs {current_savings:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class='overview-card'>
            <div class='card-label'>Net Worth</div>
            <div class='card-value'>Rs {net_worth:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Baki sab same rahega (Goal, Actions, Insights)
    st.markdown("<h4>Goal Progress</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='goal-wrap'>
        <div style='font-size:20px; font-weight:700; color:white;'>{goal_name} → Rs {goal_amount:,}</div>
        <div class='goal-bar'><div class='goal-fill' style='width:{goal_progress}%'></div></div>
        <div style='display:flex; justify-content:space-between; color:#E0E7FF;'>
            <span><b>{goal_progress:.1f}%</b> Complete</span>
            <span><b>ETA:</b> {months_needed} months</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h4>Recommended Actions & Quick Insights</h4>", unsafe_allow_html=True)
    # (Yahan tu apne tiles daal sakta hai agar chahiye to bol dena)

    st.markdown("---")
    st.markdown("<div style='text-align:center; padding:20px; color:#E0E7FF;'>Tip: Click 'Analyze / Predict' after updating inputs!</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Your Personal Financial Advisor - Made with passion")
