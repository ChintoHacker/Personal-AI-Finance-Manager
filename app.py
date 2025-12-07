import streamlit as st
from datetime import datetime
import math

st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="rocket", layout="wide")

# ==============================
# STYLING
# ==============================
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }
    .app-title { font-size: 42px !important; font-weight: 900 !important; color: #6CE0AC !important; text-align: center; }

    /* Overview Cards */
    .overview-card {
        background: rgba(255,255,255,0.15); backdrop-filter: blur(12px); border-radius: 20px;
        padding: 26px 16px; text-align: center; border: 1.5px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4); height: 155px; transition: 0.3s;
    }
    .overview-card:hover { transform: translateY(-10px); }
    .card-label { font-size: 15px; color: #E0E7FF; font-weight: 600; }
    .card-value { font-size: 30px; font-weight: 900; color: white; }

    /* Goal Section */
    .goal-box {
        background: rgba(255,255,255,0.15); border-radius: 24px; padding: 32px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
    }
    .goal-bar { height: 38px; background: rgba(255,255,255,0.2); border-radius: 19px; overflow: hidden; margin: 20px 0; }
    .goal-fill { height: 100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); border-radius: 19px; }

    /* Recommendation Card */
    .rec-card {
        margin-top: 24px; padding: 22px; border-radius: 20px; font-size: 18px;
        font-weight: 700; backdrop-filter: blur(10px); box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    }
    .rec-red    { background: rgba(239,68,68,0.25);   border: 2px solid #f87171; color: #fee2e2; }
    .rec-orange { background: rgba(251,146,60,0.25); border: 2px solid #fb923c; color: #fff7ed; }
    .rec-green  { background: rgba(34,197,94,0.25);  border: 2px solid #4ade80; color: #f0fdf4; }

    /* Sidebar */
    .stSidebar { background: #2D3452 !important; }
    .stSidebar label { color: #E0E7FF !important; font-weight: 700; font-size: 17px !important; }
    .input-section { background: rgba(255,255,255,0.1); border-radius: 16px; padding: 20px; margin: 15px 0; border: 1px solid rgba(255,255,255,0.2); }

    .stButton>button { background: linear-gradient(90deg,#0ea5e9,#6366f1); color: white; border: none; border-radius: 50px; padding: 16px; font-weight: 700; width: 100%; }
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
    goal_name = st.text_input("Goal Name", "Dream House")
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
# HEADER + NAVIGATION
# ==============================
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:19px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

# Navigation Buttons
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
# OVERVIEW PAGE (Tera Perfect Wala)
# ==============================
if st.session_state.page == "overview":
    st.markdown("<h3 style='text-align:center; color:white; margin:40px 0 30px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

    # 5 Premium Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        ("Total Amount", total_amount),
        ("Monthly Income", monthly_income),
        ("Monthly Expenses", monthly_expenses),
        ("Total Savings", current_savings),
        ("Net Worth", net_worth)
    ]
    for col, (label, val) in zip([c1,c2,c3,c4,c5], cards):
        col.markdown(f"<div class='overview-card'><div class='card-label'>{label}</div><div class='card-value'>Rs {val:,}</div></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Goal Progress + Beautiful Recommendation Card
    rec_class = "rec-red" if goal_progress < 50 else "rec-orange" if goal_progress < 90 else "rec-green"
    if goal_progress < 50:
        rec_text = "Goal bohot peeche hai!<br><b>Abhi Rs 10,000/month zyada bachaen</b>"
    elif goal_progress < 90:
        rec_text = "Achha progress hai!<br><b>Auto-save on karen aur focus rakhen</b>"
    else:
        rec_text = "Mubarak ho! Goal qareeb hai<br><b>Ab naya goal set karen</b>"

    st.markdown(f"""
    <div class='goal-box'>
        <div style='font-size:24px; font-weight:800; color:white; margin-bottom:16px;'>
            {goal_name} → Target: Rs {goal_amount:,}
        </div>
        <div class='goal-bar'>
            <div class='goal-fill' style='width:{goal_progress}%'></div>
        </div>
        <div style='color:#E0E7FF; font-size:18px; font-weight:600; margin:16px 0;'>
            {goal_progress:.1f}% Complete  •  ETA: {months_needed} months
        </div>

        <div class='rec-card {rec_class}'>
            {rec_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; background:rgba(255,255,255,0.12); padding:20px; border-radius:18px; color:#E0E7FF; font-size:17px;'>Inputs change kiye? → Sidebar se 'Analyze / Predict' zaroor dabayein!</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")
