# pages/1_Insights.py
import streamlit as st

st.set_page_config(page_title="AI Insights", page_icon="brain", layout="wide")

# Same premium CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }
    .app-title { font-size: 48px !important; font-weight: 900 !important; color: #6CE0AC !important; text-align: center; }
    .goal-box { background: rgba(255,255,255,0.17); backdrop-filter: blur(14px); border-radius: 25px;
        padding: 32px; box-shadow: 0 14px 40px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.25); text-align: center; }
    .goal-bar { height: 38px; background: rgba(255,255,255,0.22); border-radius: 20px; overflow: hidden; margin: 22px 0; }
    .goal-fill { height: 100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); }
    .rec-red    { background: linear-gradient(135deg, rgba(239,68,68,0.5), rgba(239,68,68,0.2)); border-left: 8px solid #f87171; color: #fee2e2; }
    .rec-orange { background: linear-gradient(135deg, rgba(251,146,60,0.5), rgba(251,146,60,0.2)); border-left: 8px solid #fb923c; color: #fff7ed; }
    .rec-green  { background: linear-gradient(135deg, rgba(34,197,94,0.6), rgba(34,197,94,0.3)); border-left: 8px solid #4ade80; color: white; }
    .rec-celebrate { background: linear-gradient(135deg, #f0e, #8b5cf6, #ec4899); color: white; animation: celebrate 2s infinite; }
    @keyframes celebrate { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .rec-message { font-size: 21px; font-weight: 700; line-height: 1.6; padding: 30px; border-radius: 24px;
        backdrop-filter: blur(14px); box-shadow: 0 12px 40px rgba(0,0,0,0.6); margin-top: 20px; text-align: center; }
    .plan-card { background: rgba(255,255,255,0.15); border-radius: 20px; padding: 24px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: 0.3s; height: 150px; }
    .plan-card:hover { transform: translateY(-8px); }
</style>
""", unsafe_allow_html=True)

# Data from main page
income = st.session_state.get("monthly_income", 85000)
expenses = st.session_state.get("monthly_expenses", 55000)
savings = st.session_state.get("current_savings", 150000)
goal_name = st.session_state.get("goal_name", "Dream House")
goal_amount = st.session_state.get("goal_amount", 5000000)

monthly_save = max(0, income - expenses)

# Emergency Fund
recommended = expenses * 6
emergency_progress = min(100, (savings / recommended * 100) if recommended > 0 else 0)
emergency_remaining = max(0, recommended - savings)
emergency_months = "N/A" if monthly_save <= 0 else max(0, round(emergency_remaining / monthly_save))

# Goal Progress
goal_progress = min(100, (savings / goal_amount * 100) if goal_amount > 0 else 0)
goal_remaining = max(0, goal_amount - savings)
goal_months = "N/A" if monthly_save <= 0 else max(0, round(goal_remaining / monthly_save))

# Recommendations
if emergency_progress >= 100:
    e_color, e_msg = "rec-celebrate", "EMERGENCY FUND COMPLETE!<br><b>Mubarak ho!</b><br>Ab investment pe focus karen"
elif emergency_progress < 50:
    e_color, e_msg = "rec-red", "Emergency fund bohot kam hai!<br><b>Urgent:</b> 20% income save karen<br>Side hustle shuru karen"
elif emergency_progress < 80:
    e_color, e_msg = "rec-orange", "Emergency fund theek hai lekin improve karen<br><b>Action:</b> Extra 10-15% har mahina add karen"
else:
    e_color, e_msg = "rec-green", "Emergency fund qareeb hai!<br><b>Final Push:</b> Bas thoda aur!<br>Shabash!"

if goal_progress >= 100:
    g_color, g_msg = "rec-celebrate", "GOAL ACHIEVED!<br><b>Mubarak ho bhai!</b><br>Naya goal set karen"
elif goal_progress < 50:
    g_color, g_msg = "rec-red", "Goal bohot door hai!<br><b>Action:</b> 15% cut + side income"
elif goal_progress < 90:
    g_color, g_msg = "rec-orange", "Bahut achha!<br>Auto-invest on karen"
else:
    g_color, g_msg = "rec-green", "Goal qareeb hai!<br>Final push de do!"

# Header
st.markdown("<h1 class='app-title'>AI Insights</h1>", unsafe_allow_html=True)

# Emergency Fund First
st.markdown("<h3 style='text-align:center; color:white; margin:50px 0 20px;'>1. Emergency Fund Status</h3>", unsafe_allow_html=True)
st.markdown(f"""
<div class='goal-box'>
    <div style='font-size:26px; font-weight:800; color:white;'>
        Emergency Fund → Recommended: Rs {recommended:,} (6 months)
    </div>
    <div class='goal-bar'><div class='goal-fill' style='width:{emergency_progress}%'></div></div>
    <div style='color:#E0E7FF; font-size:18px; font-weight:600;'>
        {emergency_progress:.1f}% Complete • ETA: {emergency_months} months
    </div>
    <div class='rec-message {e_color}'>{e_msg}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>")

# Goal Section
st.markdown("<h3 style='text-align:center; color:white; margin:50px 0 20px;'>2. Your Goal Progress</h3>", unsafe_allow_html=True)
st.markdown(f"""
<div class='goal-box'>
    <div style='font-size:26px; font-weight:800; color:white;'>
        {goal_name} → Target: Rs {goal_amount:,}
    </div>
    <div class='goal-bar'><div class='goal-fill' style='width:{goal_progress}%'></div></div>
    <div style='color:#E0E7FF; font-size:18px; font-weight:600;'>
        {goal_progress:.1f}% Complete • ETA: {goal_months} months
    </div>
    <div class='rec-message {g_color}'>{g_msg}</div>
</div>
""", unsafe_allow_html=True)

# Personalized Plans (only if goal not achieved)
if goal_progress < 95:
    st.markdown("<h4 style='text-align:center; color:white; margin-top:50px;'>Personalized Plans</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    basic = income * (0.25 if goal_progress < 50 else 0.18 if goal_progress < 80 else 0.12)
    strong = income * (0.40 if goal_progress < 50 else 0.28 if goal_progress < 80 else 0.20)
    with col1:
        st.markdown(f"<div class='plan-card'><b>Basic Plan</b><br>Save Rs {int(basic):,}/month<br><span style='color:#a0d9ff'>Time: {round(goal_remaining/basic) if basic>0 else 'N/A'} months</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='plan-card'><b>Strong Plan</b><br>Save Rs {int(strong):,}/month<br><span style='color:#a0d9ff'>Time: {round(goal_remaining/strong) if strong>0 else 'N/A'} months</span></div>", unsafe_allow_html=True)
