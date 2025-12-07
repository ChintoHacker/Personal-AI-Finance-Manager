import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# ---------------- Page config ----------------
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")


# ==================== DARK NEON MODE GLOBAL STYLING ====================
st.markdown("""
<style>

body, .stApp {
    background-color: #0a0f1f;
    background-image:
        radial-gradient(circle at top left, #2b0057 0%, transparent 60%),
        radial-gradient(circle at top right, #002f4f 0%, transparent 70%),
        radial-gradient(circle at bottom left, #004f4f 0%, transparent 70%);
    color: #e0e9ff !important;
    font-family: 'Poppins', sans-serif;
}

/* Neon Text */
.neon-title {
    color: #8b5cf6;
    text-shadow: 0 0 12px #8b5cf6, 0 0 22px #8b5cf6;
}

/* Neon Glass Cards */
.neon-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 22px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px #6C2BD980;
    transition: 0.3s ease;
}
.neon-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 35px #8b5cf6aa;
}

/* Fade animation */
.fade {
    animation: fadeIn 1s ease forwards;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)



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

    # Page Title
    st.markdown("<h2 style='text-align:center; color:#6CE0AC; margin-bottom:0;'>AI Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#dbeafe; margin-top:-8px; font-size:17px;'>Your smart emergency readiness overview</p>", unsafe_allow_html=True)

    # Calculations
    required = monthly_expenses * 3
    ideal_required = monthly_expenses * 6
    raw_progress = (current_savings / required * 100) if required > 0 else 0
    progress = min(max(raw_progress, 0), 100)
    months_covered = current_savings / monthly_expenses if monthly_expenses > 0 else 0
    shortfall = max(0, required - current_savings)

    # Gauge Logic + suggestion text (ensure suggestion is always defined)
    if progress < 50:
        gauge_color = "#ef4444"
        text_status = "Low"
        suggestion = "Emergency fund BOHOT kam hai — start saving 20% monthly or create a separate emergency account."
    elif progress < 80:
        gauge_color = "#f59e0b"
        text_status = "Fair"
        suggestion = "Acha progress! Set an auto-transfer to your emergency fund each month."
    else:
        gauge_color = "#10b981"
        text_status = "Good"
        suggestion = "Shabash! Emergency fund nearly/fully complete — keep it isolated for real emergencies."

    angle = progress * 3.6

    # ---------- Gauge Card ----------
    st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-top:18px;">
            <div style="
                width:240px; height:240px; border-radius:50%;
                background: rgba(255,255,255,0.05); padding:18px;
                box-shadow:0 8px 30px rgba(0,0,0,0.45); 
                border:1px solid rgba(255,255,255,0.08);
                backdrop-filter: blur(8px);
            ">
                <div style="
                    width:100%; height:100%; border-radius:50%;
                    background: conic-gradient({gauge_color} {angle}deg, rgba(255,255,255,0.08) {angle}deg);
                    display:flex; justify-content:center; align-items:center;
                ">
                    <div style="
                        width:155px; height:155px; border-radius:50%;
                        background: rgba(0,0,0,0.30);
                        border: 6px solid rgba(255,255,255,0.06);
                        display:flex; flex-direction:column; justify-content:center; align-items:center;
                    ">
                        <div style='color:#bbddff; font-size:13px;'>Emergency Status</div>
                        <div style='color:white; font-size:33px; font-weight:900;'>{progress:.0f}%</div>
                        <div style='color:#d0e8ff; font-size:12px; margin-top:6px;'>{text_status}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- Stats Row ----------
    a, b = st.columns(2)
    a.markdown(f"""
    <div style="background:rgba(255,255,255,0.08); padding:16px; border-radius:14px;
                border:1px solid rgba(255,255,255,0.10); text-align:center;">
        <div style='color:#b6d8ff; font-size:14px;'>Monthly Expenses</div>
        <div style='color:white; font-size:22px; font-weight:800;'>Rs {monthly_expenses:,}</div>
    </div>
    """, unsafe_allow_html=True)

    b.markdown(f"""
    <div style="background:rgba(255,255,255,0.08); padding:16px; border-radius:14px;
                border:1px solid rgba(255,255,255,0.10); text-align:center;">
        <div style='color:#b6d8ff; font-size:14px;'>Months Covered</div>
        <div style='color:white; font-size:22px; font-weight:800;'>{months_covered:.1f} months</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- 3 Info Cards ----------
    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div style="background:rgba(255,255,255,0.07); padding:16px; border-radius:12px; text-align:center;
                border:1px solid rgba(255,255,255,0.10);">
        <div style='color:#c7d2fe; font-size:13px;'>Required (3 months)</div>
        <div style='color:white; font-size:20px; font-weight:800;'>Rs {required:,}</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div style="background:rgba(255,255,255,0.07); padding:16px; border-radius:12px; text-align:center;
                border:1px solid rgba(255,255,255,0.10);">
        <div style='color:#c7d2fe; font-size:13px;'>Ideal (6 months)</div>
        <div style='color:white; font-size:20px; font-weight:800;'>Rs {ideal_required:,}</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div style="background:rgba(255,255,255,0.07); padding:16px; border-radius:12px; text-align:center;
                border:1px solid rgba(255,255,255,0.10);">
        <div style='color:#c7d2fe; font-size:13px;'>Shortfall</div>
        <div style='color:white; font-size:20px; font-weight:800;'>Rs {shortfall:,}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- Suggestion ----------
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.10); padding:16px; border-radius:14px; 
         text-align:center; color:white; font-size:17px; font-weight:700;'>
        {suggestion}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- Quick Insights (more compact & user friendly) ----------
    q1, q2, q3, q4 = st.columns(4)

    q1.markdown(f"""
        <div class='quick-box'>
            <span class='quick-icon'>⚠️</span>
            <span class='quick-title'>Emergency</span>
            <div class='quick-sub'>{text_status} • {progress:.0f}% ready</div>
        </div>
    """, unsafe_allow_html=True)

    q2.markdown(f"""
        <div class='quick-box'>
            <span class='quick-icon'>💰</span>
            <span class='quick-title'>Saving</span>
            <div class='quick-sub'>{'Positive flow' if monthly_income>monthly_expenses else 'Negative flow'}</div>
        </div>
    """, unsafe_allow_html=True)

    q3.markdown(f"""
        <div class='quick-box'>
            <span class='quick-icon'>🎯</span>
            <span class='quick-title'>Goal</span>
            <div class='quick-sub'>{goal_progress:.0f}% complete</div>
        </div>
    """, unsafe_allow_html=True)

    q4.markdown(f"""
        <div class='quick-box'>
            <span class='quick-icon'>📉</span>
            <span class='quick-title'>Debt</span>
            <div class='quick-sub'>{'No debt' if total_debt==0 else f'Rs {total_debt:,}'}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)


# ---------------- PAGE: VISUALS ----------------
# --------------------- IMPROVED VISUALS PAGE (NO HEATMAP + CLEAN + PREMIUM) ---------------------
elif st.session_state["page"] == "visuals":

    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    st.markdown("""
        <h2 class='neon-title' style='text-align:center;'>Visuals Dashboard</h2>
        <p style='text-align:center; margin-top:-10px; color:#dbeafe; font-size:17px;'>
            Clean • Modern • Easy to Understand
        </p>
        <br>
    """, unsafe_allow_html=True)

    # ---------- DATA PREP ----------
    categories = ["Food", "Transport", "Bills", "Shopping", "Other"]
    spending = [
        monthly_expenses * 0.25,
        monthly_expenses * 0.15,
        monthly_expenses * 0.30,
        monthly_expenses * 0.20,
        monthly_expenses * 0.10,
    ]
    df = pd.DataFrame({"Category": categories, "Amount": spending})

    trend_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    df_trend = pd.DataFrame({
        "Month": trend_months,
        "Income": np.random.randint(monthly_income*0.8, monthly_income*1.1, 6),
        "Expenses": np.random.randint(monthly_expenses*0.9, monthly_expenses*1.2, 6)
    })

    # ----------  CARD STYLE ----------
    card = """
        background: rgba(255,255,255,0.06);
        padding: 22px;
        border-radius: 18px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 0 22px rgba(139, 92, 246, 0.35);
        transition: 0.3s;
    """

    # ===================== ROW 1 — PIE CHART =====================
    fig_pie = px.pie(
        df, 
        names="Category", 
        values="Amount",
        color_discrete_sequence=px.colors.sequential.Purples_r
    )
    fig_pie.update_traces(textfont_size=14, pull=0.05)
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        legend=dict(orientation="h", y=-0.25, font=dict(size=14)),
        margin=dict(t=20, b=10)
    )

    st.markdown(f"<div style='{card}' class='fade'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; text-align:center; margin-top:0;'>💠 Spending Breakdown</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div><br>", unsafe_allow_html=True)

    # ===================== ROW 2 — LINE CHART + GAUGE =====================
    col1, col2 = st.columns(2)

    # --- Line Chart (Income vs Expenses) ---
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["Income"],
        mode="lines+markers",
        name="Income",
        line=dict(color="#34d399", width=4),
        marker=dict(size=9)
    ))
    fig_line.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["Expenses"],
        mode="lines+markers",
        name="Expenses",
        line=dict(color="#f87171", width=4),
        marker=dict(size=9)
    ))

    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        font_color="white",
        margin=dict(t=10, b=10, l=0, r=0),
        xaxis=dict(title="Month", gridcolor="#ffffff15"),
        yaxis=dict(title="Amount", gridcolor="#ffffff15")
    )

    with col1:
        st.markdown(f"<div style='{card}' class='fade'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; text-align:center;'>📉 Monthly Trend</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Circular Gauge (Goal Progress) ---
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=goal_progress,
        number={'suffix': "%", "font": {"size": 36}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#a78bfa"},
            "bgcolor": "rgba(255,255,255,0.1)",
            "borderwidth": 2,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 50], "color": "rgba(239,68,68,0.35)"},
                {"range": [50, 80], "color": "rgba(245,158,11,0.35)"},
                {"range": [80, 100], "color": "rgba(52,211,153,0.35)"},
            ],
        }
    ))
    gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)")

    with col2:
        st.markdown(f"<div style='{card}' class='fade'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; text-align:center;'>🎯 Goal Completion</h3>", unsafe_allow_html=True)
        st.plotly_chart(gauge, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ========================= END =========================








