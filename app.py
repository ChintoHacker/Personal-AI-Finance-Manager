# app.py
import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# ---------------- Page config ----------------
st.set_page_config(page_title="Your Financial Advisor — Smart AI", page_icon="🏆", layout="wide")

# ---------------- Helpers ----------------
def fmt_rs(x):
    try:
        return f"Rs {int(x):,}"
    except Exception:
        return str(x)

# ==================== GLOBAL STYLING + ANIMATIONS (ENHANCED) ====================
st.markdown(
    """
<style>
/* Base app */
:root{
  --glass-bg: rgba(255,255,255,0.03);
  --muted: #98a0b3;
  --accent1: #8b5cf6;
  --accent2: #ec4899;
  --success: #10b981;
  --danger: #ef4444;
}
body, .stApp {
    background: linear-gradient(180deg,#071021 0%, #071a2a 50%, #062531 100%);
    color: #e6eef8 !important;
    font-family: 'Inter', 'Poppins', sans-serif;
}

/* Animated header */
.header-anim {
  font-size: 44px !important;
  font-weight: 900 !important;
  text-align: center;
  color: #7ef0c6 !important;
  letter-spacing: 0.2px;
  text-shadow: 0 6px 26px rgba(0,0,0,0.7), 0 0 18px rgba(142, 99, 255, 0.12);
  background: linear-gradient(90deg, rgba(142,99,255,0.15), rgba(236,72,153,0.08));
  display:inline-block;
  padding:14px 28px;
  border-radius:16px;
  animation: float 4s ease-in-out infinite;
}
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
  100% { transform: translateY(0px); }
}

/* Card glass */
.neon-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 8px 30px rgba(2,6,23,0.6);
    transition: transform .28s ease, box-shadow .28s ease, border .2s ease;
}
.neon-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 22px 60px rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.12);
}

/* subtle fade-in */
.fade {
    animation: fadeIn 0.6s ease both;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Overview cards */
.overview-card {
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}
.card-label { font-size:13px; color:var(--muted); font-weight:700; }
.card-value { font-size:20px; color:#fff; font-weight:900; margin-top:6px; }

/* goal and recommendation */
.goal-box {
    border-radius: 14px;
    padding: 14px;
    border: 1px solid rgba(255,255,255,0.04);
    background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
}
.rec-message {
    border-radius: 12px;
    padding: 14px;
    font-weight: 800;
    color: white;
    margin-top:12px;
    box-shadow: 0 8px 36px rgba(0,0,0,0.45);
}

/* Rounded buttons */
.stButton>button {
    background: linear-gradient(45deg, var(--accent1), var(--accent2)) !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 10px 26px !important;
    font-weight: 800 !important;
    box-shadow: 0 10px 30px rgba(139,92,246,0.16);
    transition: transform .18s ease, box-shadow .18s ease;
}
.stButton>button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 18px 50px rgba(139,92,246,0.22); }

/* Sidebar improvements */
.stSidebar { background: linear-gradient(180deg,#071226,#081625) !important; padding: 16px !important; border-radius: 12px; }
.stSidebar .stNumberInput>div>div>input { color: #ffffff !important; }

/* responsive */
@media (max-width:900px) {
  .header-anim { font-size:28px !important; padding:10px 16px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ========================= SIDEBAR =========================
with st.sidebar:
    st.markdown("<h2 style='color:#7ef0c6; text-align:center;'>Your Financial Inputs</h2>", unsafe_allow_html=True)
    st.markdown("<div style='padding:10px; border-radius:10px;'>", unsafe_allow_html=True)
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=60000, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=150000, step=5000, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=50000, step=1000, format="%d")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#7ef0c6; text-align:center; margin-top:12px;'>Your Goal</h2>", unsafe_allow_html=True)
    goal_name = st.text_input("Goal Name (car 🚙, house 🏡 etc..)", value="My Goal")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=1, value=5000000, step=50000, format="%d")

    if st.button("Analyze / Predict", type="primary"):
        st.success("Analysis Updated!")

# ========================= CALCULATIONS =========================
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)

# compute robust progress and months
goal_progress = 0.0
if goal_amount > 0:
    goal_progress = float(min(100.0, max(0.0, (current_savings / goal_amount * 100))))
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
remaining = max(0, goal_amount - current_savings)

# ========================= SMART RECOMMENDATION + CELEBRATION =========================
if goal_progress >= 100:
    rec_style_bg = "linear-gradient(135deg, #8b5cf6, #ec4899)"
    rec_msg = "🎉 GOAL ACHIEVED! Congrats! Aap ne kar dikhaya! Ab new big goal set karain."
elif goal_progress < 50:
    rec_style_bg = "linear-gradient(135deg, rgba(239,68,68,0.85), rgba(239,68,68,0.35))"
    rec_msg = "⚠️ Goal bohot door hai! Action: Har cheez se 15% cut karen. Extra: Side income start karen."
elif goal_progress < 90:
    rec_style_bg = "linear-gradient(135deg, rgba(251,146,60,0.9), rgba(251,146,60,0.3))"
    rec_msg = "🔧 Bahut achha ja rahe hain! Next Level: Auto-invest on karen. Tip: Budget app use karen."
else:
    rec_style_bg = "linear-gradient(135deg, rgba(34,197,94,0.85), rgba(34,197,94,0.35))"
    rec_msg = "🚀 Goal qareeb hai! Final Push: Thodi si zyada saving — Shabash! Bas thoda aur!"

# ========================= SMART PLANS (Dynamic & Realistic) =========================
show_plans = goal_progress < 95
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

    basic_time = "N/A" if basic_save <= 0 else max(0, round(remaining / basic_save))
    strong_time = "N/A" if strong_save <= 0 else max(0, round(remaining / strong_save))

# ========================= HEADER + NAV =========================
st.markdown(f"<div style='display:flex; justify-content:center; margin-top:8px;'><div class='header-anim'>Your Personal Financial Advisor — Smart AI</div></div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#d8ecff; margin-top:6px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state["page"] = "overview"

# Navigation buttons (same layout)
nav1, nav2, nav3 = st.columns([1,1,1])
with nav1:
    if st.button("Overview"):
        st.session_state["page"] = "overview"
with nav2:
    if st.button("AI Insights"):
        st.session_state["page"] = "insights"
with nav3:
    if st.button("Visuals"):
        st.session_state["page"] = "visuals"

# small nav indicator (visual only)
active = st.session_state["page"]
st.markdown(
    f"""
    <div style="display:flex; justify-content:center; gap:48px; margin-top:8px; margin-bottom:18px;">
      <div style="text-align:center;">
        <div style="font-weight:800; color:{'#fff' if active=='overview' else '#98a0b3'}">Overview</div>
        <div style="height:6px; width:60px; margin-top:6px; border-radius:6px; background:{'#7ef0c6' if active=='overview' else 'transparent'}"></div>
      </div>
      <div style="text-align:center;">
        <div style="font-weight:800; color:{'#fff' if active=='insights' else '#98a0b3'}">AI Insights</div>
        <div style="height:6px; width:60px; margin-top:6px; border-radius:6px; background:{'#f59e0b' if active=='insights' else 'transparent'}"></div>
      </div>
      <div style="text-align:center;">
        <div style="font-weight:800; color:{'#fff' if active=='visuals' else '#98a0b3'}">Visuals</div>
        <div style="height:6px; width:60px; margin-top:6px; border-radius:6px; background:{'#8b5cf6' if active=='visuals' else 'transparent'}"></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- PAGE: OVERVIEW ----------------
if st.session_state["page"] == "overview":
    st.markdown("<h3 style='text-align:center; color:#ffffff; margin:26px 0 10px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
    cols = st.columns(5)
    items = [
        ("Total Amount", total_amount),
        ("Monthly Income", monthly_income),
        ("Monthly Expenses", monthly_expenses),
        ("Total Savings", current_savings),
        ("Net Worth", net_worth)
    ]
    for col, (label, val) in zip(cols, items):
        col.markdown(
            f"""
            <div class='overview-card neon-card fade'>
                <div class='card-label'>{label}</div>
                <div class='card-value'>{fmt_rs(val)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Goal Section
    st.markdown("<h3 style='text-align:center; color:white; margin-bottom:12px;'>Goal Progress & Smart Plans</h3>", unsafe_allow_html=True)
    safe_progress = max(0, min(100, goal_progress))
    st.markdown(
        f"""
        <div class='neon-card goal-box fade'>
            <div style='font-size:20px; font-weight:800; color:white; margin-bottom:10px;'>{goal_name} → Target: {fmt_rs(goal_amount)}</div>
            <div style='height:18px; width:100%; background:rgba(255,255,255,0.03); border-radius:10px; overflow:hidden;'>
                <div style='height:100%; width:{safe_progress}%; background: linear-gradient(90deg, #8b5cf6, #ec4899); transition: width 0.7s cubic-bezier(.2,.9,.3,1);'></div>
            </div>
            <div style='color:#d9efff; font-size:15px; font-weight:700; margin-top:10px;'>{safe_progress:.1f}% Complete • Current ETA: {months_needed} months</div>
            <div style='margin-top:14px; background:{rec_style_bg};' class='rec-message'>{rec_msg}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Smart plans
    if show_plans:
        st.markdown("<h4 style='text-align:center; color:white; margin-top:10px;'>Personalized Savings Plans</h4>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(
                f"""
                <div class='neon-card fade'>
                    <div style='font-weight:900; font-size:16px;'>Basic Plan</div>
                    <div style='font-size:20px; margin-top:6px;'>{fmt_rs(basic_save)}/month</div>
                    <div style='color:#bfe9ff; margin-top:8px;'>Time: {basic_time} months</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with p2:
            st.markdown(
                f"""
                <div class='neon-card fade'>
                    <div style='font-weight:900; font-size:16px;'>Strong Plan</div>
                    <div style='font-size:20px; margin-top:6px;'>{fmt_rs(strong_save)}/month</div>
                    <div style='color:#bfe9ff; margin-top:8px;'>Time: {strong_time} months</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Final Chart - Bar with clear labels/ticks
    st.markdown("<h3 style='text-align:center; color:white;'>Financial Overview</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })
    fig = px.bar(
        chart_data, x="Category", y="Amount", color="Category",
        text=chart_data["Amount"].apply(lambda x: f"{int(x):,}"),
        color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"]
    )
    fig.update_traces(textposition='outside', textfont=dict(size=14, color='#ffffff'))
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=520,
        margin=dict(t=20, b=40, l=40, r=20),
        transition={'duration': 600, 'easing': 'cubic-in-out'},
        font=dict(color="#e8f3ff", size=13)
    )
    fig.update_xaxes(tickfont=dict(size=14, color='#f8fbff'))
    fig.update_yaxes(title_text="Amount (PKR)", tickformat=",", tickfont=dict(size=13, color='#f8fbff'), showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption("© 2025 Your Personal Financial Advisor - Made with Abdul-Hanan in Pakistan")

# ---------------- PAGE: INSIGHTS ----------------
elif st.session_state["page"] == "insights":
    st.markdown("<h2 style='text-align:center; color:#7ef0c6; margin-bottom:0;'>Modern Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#dbeafe; margin-top:-6px; font-size:15px;'>Emergency readiness overview</p>", unsafe_allow_html=True)

    required = monthly_expenses * 3
    ideal_required = monthly_expenses * 6
    raw_progress = (current_savings / required * 100) if required > 0 else 0
    progress = float(min(max(raw_progress, 0), 100))
    months_covered = current_savings / monthly_expenses if monthly_expenses > 0 else 0
    shortfall = max(0, required - current_savings)

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
        suggestion = "Shabash! Emergency fund nearly / fully complete — keep it isolated for real emergencies."

    angle = progress * 3.6

    st.markdown(
        f"""
        <div style='display:flex; justify-content:center; margin-top:18px;'>
            <div style='width:260px; height:260px; border-radius:50%; background:rgba(255,255,255,0.02); padding:18px; box-shadow:0 10px 36px rgba(0,0,0,0.6); border:1px solid rgba(255,255,255,0.04);'>
                <div style='width:100%; height:100%; border-radius:50%; background: conic-gradient({gauge_color} {angle}deg, rgba(255,255,255,0.06) {angle}deg); display:flex; justify-content:center; align-items:center; transition: background 0.6s ease;'>
                    <div style='width:165px; height:165px; border-radius:50%; background: rgba(6,10,20,0.7); border:6px solid rgba(255,255,255,0.03); display:flex; flex-direction:column; justify-content:center; align-items:center;'>
                        <div style='color:#d9f0ff; font-size:13px;'>Emergency Status</div>
                        <div style='color:white; font-size:36px; font-weight:900;'>{progress:.0f}%</div>
                        <div style='color:#bfe9ff; font-size:13px; margin-top:6px;'>{text_status}</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    a, b = st.columns(2)
    a.markdown(
        f"""
        <div class='neon-card fade'>
            <div style='font-size:13px; color:#bfe9ff;'>Monthly Expenses</div>
            <div style='font-weight:900; font-size:22px; margin-top:6px;'>{fmt_rs(monthly_expenses)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    b.markdown(
        f"""
        <div class='neon-card fade'>
            <div style='font-size:13px; color:#bfe9ff;'>Months Covered</div>
            <div style='font-weight:900; font-size:22px; margin-top:6px;'>{months_covered:.1f} months</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f"""
        <div class='neon-card fade'>
            <div style='font-size:13px; color:#c7d2fe;'>Required (3 months)</div>
            <div style='font-weight:900; font-size:18px; margin-top:6px;'>{fmt_rs(required)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c2.markdown(
        f"""
        <div class='neon-card fade'>
            <div style='font-size:13px; color:#c7d2fe;'>Ideal (6 months)</div>
            <div style='font-weight:900; font-size:18px; margin-top:6px;'>{fmt_rs(ideal_required)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c3.markdown(
        f"""
        <div class='neon-card fade'>
            <div style='font-size:13px; color:#c7d2fe;'>Shortfall</div>
            <div style='font-weight:900; font-size:18px; margin-top:6px;'>{fmt_rs(shortfall)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='neon-card fade' style='padding:14px; text-align:center; font-weight:700;'>{suggestion}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    q1.markdown(f"<div class='neon-card quick-box fade'><div style='font-weight:800;'>⚠️ Emergency</div><div style='margin-top:6px;'>{text_status} • {progress:.0f}% ready</div></div>", unsafe_allow_html=True)
    q2.markdown(f"<div class='neon-card quick-box fade'><div style='font-weight:800;'>💰 Saving</div><div style='margin-top:6px;'>{'Positive flow' if monthly_income>monthly_expenses else 'Negative flow'}</div></div>", unsafe_allow_html=True)
    q3.markdown(f"<div class='neon-card quick-box fade'><div style='font-weight:800;'>🎯 Goal</div><div style='margin-top:6px;'>{goal_progress:.0f}% complete</div></div>", unsafe_allow_html=True)
    q4.markdown(f"<div class='neon-card quick-box fade'><div style='font-weight:800;'>📉 Debt</div><div style='margin-top:6px;'>{'No debt' if total_debt==0 else fmt_rs(total_debt)}</div></div>", unsafe_allow_html=True)

# ---------------- PAGE: VISUALS ----------------
elif st.session_state["page"] == "visuals":
    st.markdown("<h2 class='neon-title' style='text-align:center;'>Advanced Financial Visuals</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; margin-top:-6px;'>Breakdowns | Trend | Goal</p>", unsafe_allow_html=True)

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

    # Monthly trend (demo/randomized)
    trend_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    df_trend = pd.DataFrame({
        "Month": trend_months,
        "Income": np.random.randint(int(max(1000, monthly_income*0.8)), int(max(1000, monthly_income*1.1)), 6),
        "Expenses": np.random.randint(int(max(500, monthly_expenses*0.85)), int(max(500, monthly_expenses*1.15)), 6)
    })

    # Pie chart
    fig_pie = px.pie(df, names="Category", values="Amount", hole=0.28,
                     color_discrete_sequence=px.colors.sequential.Purples)
    fig_pie.update_traces(textinfo="percent+label", textposition='inside', textfont=dict(size=13, color='white'))
    fig_pie.update_layout(
        height=420,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", y=-0.12),
        transition={'duration': 600, 'easing': 'cubic-in-out'},
        font=dict(color="#fff")
    )

    st.markdown("<div class='neon-card fade'>", unsafe_allow_html=True)
    st.subheader("💠 Spending Breakdown")
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div><br>", unsafe_allow_html=True)

    # Line chart (trend)
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["Income"],
        mode="lines+markers+text",
        name="Income",
        line=dict(color="#10b981", width=3),
        marker=dict(size=8),
        text=[f"{int(v):,}" for v in df_trend["Income"]],
        textposition="top center",
    ))
    fig_line.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["Expenses"],
        mode="lines+markers+text",
        name="Expenses",
        line=dict(color="#ef4444", width=3),
        marker=dict(size=8),
        text=[f"{int(v):,}" for v in df_trend["Expenses"]],
        textposition="bottom center",
    ))
    fig_line.update_layout(
        height=420,
        margin=dict(t=8, b=24, l=40, r=16),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.02)',
        xaxis=dict(title=None, tickfont=dict(color="#fff", size=12)),
        yaxis=dict(title="Amount (PKR)", tickformat=",", tickfont=dict(color="#fff", size=12)),
        legend=dict(orientation="h", y=-0.15),
        transition={'duration': 600, 'easing': 'cubic-in-out'},
        font=dict(color="#fff")
    )

    a, b = st.columns(2)
    with a:
        st.markdown("<div class='neon-card fade'>", unsafe_allow_html=True)
        st.subheader("📊 Monthly Trend")
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Goal completion gauge (Plotly)
    goal_figure = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=goal_progress,
        title={'text': "Goal Completion", 'font': {'size': 16}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "white"},
            "bar": {"color": "#8b5cf6"},
            "bgcolor": "rgba(255,255,255,0.03)",
            "borderwidth": 0,
        },
        number={'suffix': "%", 'font': {'size': 20}},
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    goal_figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", height=420, margin=dict(t=10,b=10,l=10,r=10))

    with b:
        st.markdown("<div class='neon-card fade'>", unsafe_allow_html=True)
        st.plotly_chart(goal_figure, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ---------------- END ----------------
