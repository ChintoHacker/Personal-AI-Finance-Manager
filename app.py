import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
import math
import pandas as pd
import os

st.set_page_config(page_title="Your Financial Advisor — Smart AI Manager", page_icon="💸", layout="wide")

st.markdown("""
<style>
/* ---------- GLOBAL APP ---------- */
.stApp {background: linear-gradient(180deg,#224B7D 0%, #6C9E7F 100%); color: #F7FAFC !important; font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;}
h1, h2, h3, h4, h5 {color: #FFFFFF !important; font-weight: 800; text-shadow: 0px 0px 6px rgba(0,0,0,0.35);}
.app-title {font-weight:900; font-size:35px; letter-spacing:0.5px; color:#6CE0AC !important;}
p, div, span, label {color:#F1F5F9 !important;}
.muted {color: rgba(255,255,255,0.82) !important;}
.stButton > button {background: linear-gradient(90deg,#38bdf8,#818cf8) !important; color:white !important; font-weight:700 !important; border-radius:10px; padding:8px 14px; border:none; box-shadow:0 4px 18px rgba(0,0,0,0.35);}
.stButton > button:hover {transform:scale(1.03); box-shadow:0 8px 28px rgba(0,0,0,0.45);}
.stat-card {background: #7E7E96; border-radius:12px; border:1px solid rgba(255,255,255,0.18); padding:14px;}
.stat-label {font-size:14px; color:#E2E8F0 !important;}
.stat-value {font-size:22px; font-weight:800; color:#FFFFFF !important;}
.goal-wrap {background: rgba(255,255,255,0.1); border-radius:12px; padding:12px; border:1px solid rgba(255,255,255,0.2);}
.goal-bar {height:20px; background: rgba(255,255,255,0.15); border-radius:12px;}
.goal-fill {background: linear-gradient(90deg,#06b6d4,#7c3aed);}
.tile {padding:12px; border-radius:10px; background: rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.22);}
.tile-title {font-size:15px; font-weight:800; color:white !important;}
.tile-sub {font-size:13px; color:#E2E8F0 !important;}
.tile-warn {border-left:4px solid #fb7185;}
.tile-good {border-left:4px solid #10b981;}
.stSidebar, .css-1d391kg, .sidebar .sidebar-content {background: #2D3452 !important; border-right: 1px solid rgba(255,255,255,0.10);}
.stSidebar label, .sidebar .sidebar-content label, .stSidebar .stNumberInput label {color: #1D4757 !important; font-weight: 700 !important; font-size: 18px !important;}
.stSidebar input, .sidebar .sidebar-content input, .stSidebar .stNumberInput input {background: #FFFFFF !important; color: #000000 !important; border: 1px solid #CBD5E1 !important; border-radius: 8px !important; padding: 7px 10px !important;}
.stSidebar input:focus, .sidebar .sidebar-content input:focus {border: 1px solid #60A5FA !important; box-shadow: 0 0 6px rgba(96,165,250,0.4);}
.input-section {background: #5A5A63 !important; border: 1px solid rgba(255,255,255,0.20) !important; border-radius: 10px !important; padding: 12px !important;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar Inputs
# ------------------------------
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:6px'>Apki Financial Inputs</h2>", unsafe_allow_html=True)
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=0, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=0, step=500, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    goal_name = st.text_input("Goal Name")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=0, value=0, step=500, format="%d")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("🔍 Analyze / Predict", key="sidebar_analyze"):
        st.session_state['analysis_run'] = True
        st.success("Analysis updated ✔")
    else:
        if 'analysis_run' not in st.session_state:
            st.session_state['analysis_run'] = False

# ------------------------------
# Core calculations
# ------------------------------
def safe_div(a, b):
    try: return a / b
    except Exception: return 0

total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_possible_save = max(0, monthly_income - monthly_expenses)

goal_progress_pct = 0.0
if goal_amount > 0: goal_progress_pct = min(100.0, (current_savings / goal_amount) * 100.0)
months_to_goal = math.inf
if monthly_possible_save > 0: months_to_goal = round(max(0.0, (goal_amount - current_savings) / monthly_possible_save), 1)

# Emergency fund constants
EMERGENCY_MIN = 3
EMERGENCY_IDEAL = 6
emergency_coverage_months = round(safe_div(current_savings, max(1, monthly_expenses)), 1)
emergency_min_amount = monthly_expenses * EMERGENCY_MIN
emergency_ideal_amount = monthly_expenses * EMERGENCY_IDEAL
emergency_gap_min = max(0, emergency_min_amount - current_savings)
emergency_gap_ideal = max(0, emergency_ideal_amount - current_savings)

cat_props = {"Food": 0.30, "Transport": 0.10, "Shopping": 0.20, "Bills": 0.25, "Fun": 0.15}
cat_values = {k: round(monthly_expenses * p) for k, p in cat_props.items()}

def generate_tiles():
    tiles = []
    if emergency_coverage_months < EMERGENCY_MIN:
        tiles.append({"icon":"⚠","title":"Emergency: Low","sub":f"{emergency_coverage_months} mo — need Rs {emergency_gap_min:,} to reach {EMERGENCY_MIN}m"})
    elif EMERGENCY_MIN <= emergency_coverage_months < EMERGENCY_IDEAL:
        tiles.append({"icon":"✅","title":"Emergency: OK","sub":f"{emergency_coverage_months} mo — aim for {EMERGENCY_IDEAL}m (Rs {emergency_ideal_amount:,})"})
    else:
        tiles.append({"icon":"🌟","title":"Emergency: Strong","sub":f"{emergency_coverage_months} mo — you are covered"})
    if monthly_possible_save <= 0:
        tiles.append({"icon":"🛑","title":"Saving: Negative","sub":"Expenses ≥ income — reduce spending"})
    elif monthly_possible_save < 0.2 * monthly_income:
        tiles.append({"icon":"💡","title":"Saving: Low","sub":f"Save Rs {monthly_possible_save:,}/mo — aim 20% of income"})
    else:
        tiles.append({"icon":"🚀","title":"Saving: Good","sub":f"Save Rs {monthly_possible_save:,}/mo"})
    if goal_progress_pct < 50:
        tiles.append({"icon":"📌","title":"Goal: Behind","sub":f"{goal_progress_pct:.0f}% complete"})
    elif 50 <= goal_progress_pct < 90:
        tiles.append({"icon":"🎯","title":"Goal: Progressing","sub":f"{goal_progress_pct:.0f}% complete"})
    else:
        tiles.append({"icon":"🏁","title":"Goal: Almost Done","sub":f"{goal_progress_pct:.0f}% complete"})
    if total_debt > 0:
        tiles.append({"icon":"📉","title":"Debt","sub":f"Outstanding: Rs {total_debt:,}"})
    else:
        tiles.append({"icon":"🧾","title":"Debt","sub":"No debt"})
    return tiles

analysis_tiles = generate_tiles() if st.session_state.get('analysis_run', False) else None

# ------------------------------
# Header + Navigation
# ------------------------------
st.markdown(f"""
<div class="top-header">
  <span class="app-title">Your Personal Financial Advisor — Smart</span>
  <span style="float:right; color:rgba(230,238,248,0.7); font-size:13px;">{datetime.now().strftime('%d %b %Y')}</span>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1,1,1], gap="large")
with nav1:
    if st.button("🏠 Overview"): st.session_state['page'] = 'landing'
with nav2:
    if st.button("🤖 AI Insights"): st.session_state['page'] = 'insights'
with nav3:
    if st.button("📈 Visuals"): st.session_state['page'] = 'visuals'
if 'page' not in st.session_state: st.session_state['page'] = 'landing'

# ------------------------------
# Landing Page (Overview)
# ------------------------------
if st.session_state.get('page') == 'landing':
    st.markdown("<h3>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [("Total Amount(Income + Savings)", total_balance),("Monthly Income", monthly_income),
               ("Monthly Expenses", monthly_expenses),("Total Savings", current_savings),
               ("Net Worth", net_worth)]
    for col, (label, val) in zip([c1, c2, c3, c4, c5], metrics):
        with col:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>Rs {val:,.0f}</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    # Goal progress + recommendations (same as before, unchanged)
    left, right = st.columns([2,1], gap="large")
    # ... same landing page content as original code ...

# ------------------------------
# AI Insights Page — Emergency Fund (Redesigned & Motivational)
# ------------------------------
elif st.session_state.get('page') == 'insights':
    st.header("AI Insights — Emergency Fund Overview")

    FIXED_MIN_MONTHS = 3
    FIXED_IDEAL_MONTHS = 6
    recommended_min = monthly_expenses * FIXED_MIN_MONTHS
    recommended_ideal = monthly_expenses * FIXED_IDEAL_MONTHS
    emergency_coverage_months = round(safe_div(current_savings, max(1, monthly_expenses)), 1)
    ideal_pct = min(100, (current_savings / recommended_ideal) * 100)

    # Tiles
    tiles = []
    if emergency_coverage_months < FIXED_MIN_MONTHS:
        gap_min = max(0, recommended_min - current_savings)
        gap_ideal = max(0, recommended_ideal - current_savings)
        tiles.append({"icon":"⚠️","title":"Emergency Fund: Low","sub":f"Save ~Rs {gap_min:,} to reach minimum, Rs {gap_ideal:,} for ideal."})
        tiles.append({"icon":"✂️","title":"Suggested Action","sub":"Reduce non-essential spend or increase income."})
    elif FIXED_MIN_MONTHS <= emergency_coverage_months < FIXED_IDEAL_MONTHS:
        tiles.append({"icon":"✅","title":"Emergency Fund: Moderate","sub":f"Current coverage: {emergency_coverage_months} mo — almost ideal!"})
        tiles.append({"icon":"⚡","title":"Recommendation","sub":"Increase savings slightly to reach ideal faster."})
    else:
        tiles.append({"icon":"🌟","title":"Emergency Fund: Excellent","sub":f"Current coverage: {emergency_coverage_months} mo — financially strong!"})
        tiles.append({"icon":"🎯","title":"Next Steps","sub":"Maintain your fund and plan new financial goals."})

    cols = st.columns(2, gap="large")
    for col, t in zip(cols, tiles):
        with col:
            cls = "tile-warn" if "Low" in t['title'] else "tile-good"
            st.markdown(f"<div class='tile {cls}'><div class='tile-icon'>{t['icon']}</div><div><div class='tile-title'>{t['title']}</div><div class='tile-sub'>{t['sub']}</div></div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    df_em = pd.DataFrame({"Category": ["You (Current Savings)", "Minimum (3 mo)", "Ideal (6 mo)"],
                          "Amount": [current_savings, recommended_min, recommended_ideal]})
    colors = ["#06b6d4", "#fb7185", "#10b981"]
    fig_em = go.Figure()
    fig_em.add_trace(go.Bar(x=df_em["Amount"], y=df_em["Category"], orientation='h', marker_color=colors,
                             text=[f"Rs {amt:,}" for amt in df_em["Amount"]], textposition="auto"))
    fig_em.update_layout(template="plotly_dark", title="Emergency Fund Status", xaxis_title="PKR", height=320, margin=dict(l=130))
    st.plotly_chart(fig_em, use_container_width=True)

# ------------------------------
# Visuals Page
# ------------------------------
elif st.session_state.get('page') == 'visuals':
    st.header("Visuals — Trends & Spending")
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    df = pd.DataFrame({"month": months,"income": [monthly_income]*12,"expenses": [monthly_expenses]*12})
    df['savings'] = df['income'] - df['expenses']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['month'], y=df['income'], name="Income", marker_color="#06b6d4"))
    fig.add_trace(go.Bar(x=df['month'], y=df['expenses'], name="Expenses", marker_color="#fb7185"))
    fig.update_layout(template="plotly_dark", barmode='group', title="Income vs Expenses (12 months)", yaxis_title="PKR", height=400)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['month'], y=df['savings'], mode="lines+markers", name="Savings", line=dict(width=3, shape='spline')))
    fig2.update_layout(template="plotly_dark", title="Savings Trend (12 months)", yaxis_title="PKR", height=360)
    st.plotly_chart(fig2, use_container_width=True)

    fig_pie = px.pie(values=list(cat_values.values()), names=list(cat_values.keys()), hole=0.45, title="Spending Breakdown")
    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(template="plotly_dark", height=420)
    st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------
# PDF Generation (same as before)
# ------------------------------
# ... existing PDF code unchanged ...
