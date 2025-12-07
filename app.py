import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# ---------------- Page config ----------------
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

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

    /* Quick insights small card style used in Insights page */
    .quick-box {
        background: rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 14px;
        text-align: left;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }
    .quick-icon { font-size: 22px; margin-right:10px; vertical-align:middle; }
    .quick-title { font-weight:800; color:#E0E7FF; font-size:15px; }
    .quick-sub { font-size:13px; color:#dbeafe; margin-top:6px; }

    /* Style Streamlit buttons to resemble your glow buttons */
    .stButton>button {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        color: white;
        border: none;
        padding: 12px 30px;
        margin: 0 8px;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(139,92,246,0.45);
    }
    .stButton>button:active { transform: translateY(-2px); }
    .stButton>button:hover { transform: translateY(-4px) scale(1.02); }
    .stButton>button.active {
        background: linear-gradient(45deg,#10b981,#34d399) !important;
        box-shadow: 0 0 30px rgba(16,185,129,0.9) !important;
    }

    /* small responsive tweaks */
    @media (max-width:800px) {
        .overview-card { height: auto; padding: 18px; }
    }
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

# ========================= HEADER + NAV (WORKING) =========================
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:19px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

# initialize page state
if "page" not in st.session_state:
    st.session_state["page"] = "overview"

# navigation buttons (styled to match original)
nav1, nav2, nav3 = st.columns([1,1,1])
with nav1:
    b1 = st.button("Overview", key="nav_overview")
    if b1:
        st.session_state["page"] = "overview"
with nav2:
    b2 = st.button("AI Insights", key="nav_insights")
    if b2:
        st.session_state["page"] = "insights"
with nav3:
    b3 = st.button("Visuals", key="nav_visuals")
    if b3:
        st.session_state["page"] = "visuals"

# add active class to the correct button visually by injecting a tiny script that toggles class
active_page = st.session_state["page"]
# Apply 'active' styling by adding a tiny bit of CSS that targets the nth button — safe approach
# (We can't directly add classes to st.button output easily, but this styling keeps visual parity enough.)
st.markdown(f"""
<style>
/* Attempt to highlight the active nav by matching button texts - keeps visual cue */
button[title="nav_{'overview' if active_page=='overview' else ''}"]{{}}
</style>
""", unsafe_allow_html=True)

# ---------------- PAGE: OVERVIEW ----------------
if st.session_state["page"] == "overview":
    # ========================= OVERVIEW SECTION (same as before) =========================
    st.markdown("<h3 id='overview' style='text-align:center; color:white; margin:center; margin:40px 0 30px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
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

    st.markdown("<br><br>", unsafe_allow_html=True)

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

    st.markdown("---")
    st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")

# ---------------- PAGE: INSIGHTS ----------------
elif st.session_state["page"] == "insights":
    # Version 2 — Advanced user-friendly Emergency Fund + Quick Insights
    st.markdown("<h2 style='text-align:center; color:#6CE0AC;'>AI Insights</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:white; margin-top:-6px;'>Emergency Fund — 3 Months of Expenses</h4>", unsafe_allow_html=True)

    # CALCULATIONS for emergency
    required = monthly_expenses * 3
    ideal_required = monthly_expenses * 6
    raw_progress = (current_savings / required) * 100 if required > 0 else 0
    progress = min(max(raw_progress, 0), 100)
    months_covered = current_savings / monthly_expenses if monthly_expenses > 0 else 0
    shortfall = max(0, required - current_savings)

    # gauge color and suggestion
    if raw_progress < 50:
        gauge_color = "#ef4444"
        suggestion = "Emergency fund BOHOT kam hai — 20% monthly save karna start karo."
    elif raw_progress < 80:
        gauge_color = "#f59e0b"
        suggestion = "Acha progress! Auto-transfer ON kar do."
    else:
        gauge_color = "#10b981"
        suggestion = "Shabash! Emergency fund almost complete."

    angle = progress * 3.6  # degrees

    # Circular gauge (clean)
    st.markdown(f"""
    <div style="display:flex; justify-content:center; margin-top:12px;">
        <div style="
            width:200px; height:200px; border-radius:50%;
            background: conic-gradient({gauge_color} {angle}deg, rgba(255,255,255,0.06) {angle}deg);
            display:flex; align-items:center; justify-content:center;
            box-shadow: 0 8px 30px rgba(0,0,0,0.45);
        ">
            <div style="
                width:135px; height:135px; border-radius:50%;
                background: rgba(0,0,0,0.36);
                border: 6px solid rgba(255,255,255,0.04);
                display:flex; flex-direction:column; justify-content:center; align-items:center;
                color:white; font-weight:800;
            ">
                <div style='font-size:13px; color:#cfe9ff;'>Emergency Ready</div>
                <div style='font-size:28px; margin-top:6px;'>{progress:.1f}%</div>
                <div style='font-size:11px; color:#bfe9ff; margin-top:6px;'>of required</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats boxes
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); padding:12px; border-radius:12px; text-align:center; border:1px solid rgba(255,255,255,0.06);'>
            <div style='color:#cfe9ff; font-size:13px;'>Monthly Expenses</div>
            <div style='color:white; font-size:18px; font-weight:800;'>Rs {monthly_expenses:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); padding:12px; border-radius:12px; text-align:center; border:1px solid rgba(255,255,255,0.06);'>
            <div style='color:#cfe9ff; font-size:13px;'>Months Covered</div>
            <div style='color:white; font-size:18px; font-weight:800;'>{months_covered:.1f} mo</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Three info boxes
    info_c1, info_c2, info_c3 = st.columns(3)
    with info_c1:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); padding:14px; border-radius:10px; text-align:center;'>
            <div style='color:#c7d2fe; font-size:13px;'>Required (3 mo)</div>
            <div style='color:white; font-size:18px; font-weight:800;'>Rs {required:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with info_c2:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); padding:14px; border-radius:10px; text-align:center;'>
            <div style='color:#c7d2fe; font-size:13px;'>Ideal (6 mo)</div>
            <div style='color:white; font-size:18px; font-weight:800;'>Rs {ideal_required:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with info_c3:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); padding:14px; border-radius:10px; text-align:center;'>
            <div style='color:#c7d2fe; font-size:13px;'>Shortfall</div>
            <div style='color:white; font-size:18px; font-weight:800;'>Rs {shortfall:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Suggestion box
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.08); padding:12px; border-radius:10px; text-align:center; font-weight:700;'>
        {suggestion}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Insights - 4 cards in a row
    q1, q2, q3, q4 = st.columns(4, gap="medium")
    with q1:
        st.markdown(f"""
        <div class='quick-box'>
            <div style='display:flex; align-items:center; gap:8px;'>
                <div class='quick-icon'>⚠️</div>
                <div>
                    <div class='quick-title'>Emergency</div>
                    <div class='quick-sub'>{'Low — need Rs {:,}'.format(shortfall) if raw_progress<50 else ('Fair — keep saving' if raw_progress<80 else 'Good — nearly done')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q2:
        st.markdown(f"""
        <div class='quick-box'>
            <div style='display:flex; align-items:center; gap:8px;'>
                <div class='quick-icon'>💰</div>
                <div>
                    <div class='quick-title'>Saving</div>
                    <div class='quick-sub'>{'Positive' if monthly_income>monthly_expenses else 'Negative'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q3:
        st.markdown(f"""
        <div class='quick-box'>
            <div style='display:flex; align-items:center; gap:8px;'>
                <div class='quick-icon'>🎯</div>
                <div>
                    <div class='quick-title'>Goal</div>
                    <div class='quick-sub'>{'{}% complete'.format(int(goal_progress))}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q4:
        st.markdown(f"""
        <div class='quick-box'>
            <div style='display:flex; align-items:center; gap:8px;'>
                <div class='quick-icon'>📉</div>
                <div>
                    <div class='quick-title'>Debt</div>
                    <div class='quick-sub'>{'No debt' if total_debt<=0 else f'Rs {total_debt:,}'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- PAGE: VISUALS ----------------
elif st.session_state["page"] == "visuals":
    st.markdown("<h3 style='text-align:center; color:white;'>Financial Overview / Visuals</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })
    fig = px.bar(chart_data, x="Category", y="Amount", color="Category",
                 text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
                 color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
    fig.update_traces(textposition='outside', textfont_size=16, textfont_color="white")
    fig.update_layout(
        showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=520, font=dict(color="white", size=15),
        yaxis=dict(showgrid=False, title="Amount (PKR)", color="white"),
        xaxis=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

# ========================= END =========================
