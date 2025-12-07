import streamlit as st
from datetime import datetime
import math

st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="rocket", layout="wide")

# ==============================
# PREMIUM STYLING + RECOMMENDATION BOX
# ==============================
st.markdown("""
<style>
    .stApp { 
        background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); 
        font-family: 'Inter', sans-serif; 
        color: white;
    }
    .app-title { 
        font-size: 42px !important; 
        font-weight: 900 !important; 
        color: #6CE0AC !important; 
        text-align: center;
    }
    
    /* Overview Cards */
    .overview-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 26px 16px;
        text-align: center;
        border: 1.5px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s;
        height: 155px;
    }
    .overview-card:hover { transform: translateY(-10px); }

    .card-label { font-size: 15px; color: #E0E7FF; font-weight: 600; margin-bottom: 10px; }
    .card-value { font-size: 30px; font-weight: 900; color: white; }

    /* Goal Progress */
    .goal-wrap {
        background: rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 28px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        text-align: center;
    }
    .goal-bar { 
        height: 36px; 
        background: rgba(255,255,255,0.2); 
        border-radius: 18px; 
        overflow: hidden; 
        margin: 16px 0; 
    }
    .goal-fill { 
        height: 100%; 
        background: linear-gradient(90deg, #06b6d4, #7c3aed); 
        border-radius: 18px; 
    }

    /* RECOMMENDATION BOX - PREMIUM */
    .recommend-box {
        margin-top: 20px;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        font-size: 17px;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        border: 2px solid;
    }
    .rec-danger {
        background: rgba(251, 113, 133, 0.25);
        border-color: #fb7185;
        color: #ffe4e6;
    }
    .rec-warning {
        background: rgba(251, 187, 113, 0.25);
        border-color: #fbbf24;
        color: #fffbeb;
    }
    .rec-success {
        background: rgba(74, 222, 128, 0.25);
        border-color: #4ade80;
        color: #f0fdf4;
    }

    /* Sidebar */
    .stSidebar { background: #2D3452 !important; }
    .stSidebar label { color: #E0E7FF !important; font-weight: 700; font-size: 17px !important; }
    .input-section { 
        background: rgba(255,255,255,0.1); 
        border-radius: 14px; 
        padding: 20px; 
        margin: 15px 0; 
        border: 1px solid rgba(255,255,255,0.2); 
    }

    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white; border: none; border-radius: 50px;
        padding: 14px; font-weight: 700; width: 100%;
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
        st.success("Analysis Updated!")

# ==============================
# CALCULATIONS
# ==============================
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)

goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))

# ==============================
# HEADER
# ==============================
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:19px; margin-top:-8px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Overview", use_container_width=True):
        st.session_state.page = "overview"
with col2:
    if st.button("AI Insights", use_container_width=True):
        st.session_state.page = "insights"
with col3:
    if st.button("Visuals", use_container_width=True):
        st.session_state.page = "visuals"

if "page" not in st.session_state:
    st.session_state.page = "overview"

# ==============================
# OVERVIEW PAGE WITH SMART RECOMMENDATIONS
# ==============================
if st.session_state.page == "overview":
    st.markdown("<h3 style='text-align:center; color:white; margin:40px 0 20px 0;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

    # 5 Premium Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(f"<div class='overview-card'><div class='card-label'>Total Amount</div><div class='card-value'>Rs {total_amount:,}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='overview-card'><div class='card-label'>Monthly Income</div><div class='card-value'>Rs {monthly_income:,}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='overview-card'><div class='card-label'>Monthly Expenses</div><div class='card-value'>Rs {monthly_expenses:,}</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='overview-card'><div class='card-label'>Total Savings</div><div class='card-value'>Rs {current_savings:,}</div></div>", unsafe_allow_html=True)
    with c5: st.markdown(f"<div class='overview-card'><div class='card-label'>Net Worth</div><div class='card-value'>Rs {net_worth:,}</div></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Goal Progress + Smart Recommendation Box
    st.markdown("<h4 style='color:white; text-align:center; margin-bottom:20px;'>Goal Progress</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='goal-wrap'>
        <div style='font-size:22px; font-weight:700; color:white; margin-bottom:15px;'>
            {goal_name} → Target: Rs {goal_amount:,}
        </div>
        <div class='goal-bar'>
            <div class='goal-fill' style='width:{goal_progress}%'></div>
        </div>
        <div style='display:flex; justify-content:space-between; color:#E0E7FF; font-size:17px; margin-top:12px;'>
            <span><b>{goal_progress:.1f}%</b> Complete</span>
            <span><b>ETA:</b> {months_needed} months</span>
        </div>

        <!-- SMART RECOMMENDATION BOX -->
        <div class='recommend-box {
            "rec-danger" if goal_progress < 50 else 
            "rec-warning" if goal_progress < 90 else 
            "rec-success"
        }'>
            {
                "Warning: Goal bahut peeche hai!<br><b>Karo:</b> Har mahine Rs 10,000 zyada bachaen<br><b>Mat karo:</b> Shopping & dining out" if goal_progress < 50 else
                "Good Progress jaari rakhen!<br><b>Karo:</b> Auto-savings on karen<br><b>Tip:</b> Chhoti luxuries skip karen" if goal_progress < 90 else
                "Success: Goal bohot qareeb hai!<br><b>Next Step:</b> Naya goal set karen<br><b>Congrats!</b>"
            }
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#E0E7FF; font-size:17px; background:rgba(255,255,255,0.1); padding:18px; border-radius:16px;'>Tip: Inputs change karne ke baad sidebar se 'Analyze / Predict' zaroor dabayein!</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")
