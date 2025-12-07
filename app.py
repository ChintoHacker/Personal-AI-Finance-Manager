import streamlit as st
from datetime import datetime
import math
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ---------------- page config ----------------
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

# ---------------- CSS: Premium Glass Theme + Animations ----------------
st.markdown(
    """
    <style>
    /* ---------- Base & layout ---------- */
    .stApp { background: linear-gradient(180deg, #0f172a 0%, #0f2a4a 50%, #134e4a 100%); color: #E6F0FF; font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
    .app-title { font-size: 40px !important; font-weight: 900 !important; color: #7EE7C7 !important; text-align: center; margin-bottom: 4px; }
    .sub-title { text-align:center; color: rgba(230,240,255,0.8); margin-top:-8px; margin-bottom: 22px; font-size:15px; }

    /* ---------- Cards / Glass ---------- */
    .glass {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
        backdrop-filter: blur(8px) saturate(140%);
        transition: transform 0.28s ease, box-shadow 0.28s ease;
    }
    .glass:hover { transform: translateY(-6px); box-shadow: 0 18px 50px rgba(2,6,23,0.7); }

    .metric-label { color: rgba(230,240,255,0.85); font-weight:700; font-size:14px; }
    .metric-value { color:white; font-weight:900; font-size:26px; margin-top:6px; }

    /* ---------- Goal Box ---------- */
    .goal-box { border-radius:22px; padding:24px; margin-top:12px; }
    .goal-bar { height:28px; background: rgba(255,255,255,0.06); border-radius:999px; overflow:hidden; }
    .goal-fill { height:100%; background: linear-gradient(90deg,#7c3aed,#06b6d4); box-shadow: 0 6px 24px rgba(108,49,255,0.12); transition: width 0.9s ease; }

    /* ---------- Navigation Buttons ---------- */
    .nav-wrap { text-align:center; margin: 18px 0 30px 0; }
    .nav-btn {
        display:inline-block; padding:12px 30px; margin:0 10px; border-radius:999px; font-weight:800;
        border: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
        color: #F8FAFF; cursor:pointer; box-shadow: 0 8px 30px rgba(2,6,23,0.55);
        transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
    }
    .nav-btn:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 18px 50px rgba(2,6,23,0.65); }
    .nav-btn.active { background: linear-gradient(90deg,#06b6d4,#7c3aed); color: white; box-shadow: 0 18px 60px rgba(7,89,133,0.28); }

    /* ---------- Insight: Gauge & tiles ---------- */
    .insight-wrap { display:flex; gap:18px; align-items:center; justify-content:space-between; flex-wrap:wrap; }
    .gauge-card { width:360px; min-width:300px; text-align:center; padding:18px; border-radius:16px; }
    .tile { padding:16px; border-radius:14px; min-width:220px; max-width:420px; }
    .tile .title { font-weight:800; font-size:16px; color:white; margin-bottom:6px; }
    .tile .sub { color: rgba(230,240,255,0.82); font-size:14px; }

    /* color variants */
    .tile-warning { background: linear-gradient(180deg, rgba(251,146,60,0.12), rgba(251,146,60,0.02)); border-left:6px solid #fb923c; }
    .tile-ok { background: linear-gradient(180deg, rgba(34,197,94,0.08), rgba(34,197,94,0.02)); border-left:6px solid #34d399; }
    .tile-critical { background: linear-gradient(180deg, rgba(239,68,68,0.08), rgba(239,68,68,0.02)); border-left:6px solid #fb7185; }
    .tile-celebrate { background: linear-gradient(90deg,#8b5cf6,#ec4899); color:white; border-left:6px solid rgba(255,255,255,0.12); box-shadow: 0 12px 38px rgba(139,92,246,0.12); }

    /* pulse for healthy */
    .pulse { animation: pulse 2.4s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }

    /* small helper */
    .muted { color: rgba(230,240,255,0.7); font-size:13px; }
    .center { text-align:center; }
    @media (max-width:900px) {
        .insight-wrap { flex-direction:column; align-items:center; }
        .gauge-card { width:100%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Sidebar Inputs ----------------
with st.sidebar:
    st.markdown("<h2 style='color:#7EE7C7; text-align:center;'>Apki Financial Inputs</h2>", unsafe_allow_html=True)
    st.markdown("<div style='padding:10px; border-radius:12px; background: rgba(255,255,255,0.02);'>", unsafe_allow_html=True)
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000)
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=150000, step=5000)
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000)
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=50000, step=1000)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    goal_name = st.text_input("Goal Name", value="Dream House")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=1, value=5000000, step=50000)
    if st.button("Analyze / Predict", type="primary"):
        st.session_state['analyzed'] = True
        st.success("Analysis Updated!")

# ---------------- Navigation state ----------------
if 'page' not in st.session_state:
    st.session_state['page'] = 'overview'

# top nav (styled)
nav1, nav2, nav3 = st.columns([1,1,1], gap="large")
with nav1:
    if st.button("Overview"):
        st.session_state['page'] = 'overview'
with nav2:
    if st.button("AI Insights"):
        st.session_state['page'] = 'insights'
with nav3:
    if st.button("Visuals"):
        st.session_state['page'] = 'visuals'

# ---------------- calculations (unchanged) ----------------
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
remaining = max(0, goal_amount - current_savings)

# recommendation messaging (kept simple & motivational)
if goal_progress >= 100:
    rec_color = "tile-celebrate"
    rec_msg = "GOAL ACHIEVED — Mubarak! 🎉 Keep building new wins."
elif goal_progress < 50:
    rec_color = "tile-critical"
    rec_msg = "Goal is far — start small changes & steady automation."
elif goal_progress < 90:
    rec_color = "tile-warning"
    rec_msg = "Good progress — automate transfers & tighten budget a bit."
else:
    rec_color = "tile-ok"
    rec_msg = "Almost there — final push and you'll hit it!"

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
    basic_time = "N/A" if basic_save <= 0 else round(remaining / basic_save)
    strong_time = "N/A" if strong_save <= 0 else round(remaining / strong_save)

# ---------------- Overview Page ----------------
if st.session_state['page'] == 'overview':
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    st.markdown("<div class='app-title'>Your Personal Financial Advisor — Smart</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-title'>Today • {datetime.now().strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    cols = st.columns(5, gap="large")
    labels_vals = [
        ("Total Amount", total_amount),
        ("Monthly Income", monthly_income),
        ("Monthly Expenses", monthly_expenses),
        ("Total Savings", current_savings),
        ("Net Worth", net_worth),
    ]
    for col, (label, val) in zip(cols, labels_vals):
        col.markdown("<div class='glass'>", unsafe_allow_html=True)
        col.markdown(f"<div class='metric-label'>{label}</div>", unsafe_allow_html=True)
        col.markdown(f"<div class='metric-value'>Rs {val:,}</div>", unsafe_allow_html=True)
        col.markdown("</div>", unsafe_allow_html=True)

    # goal box
    st.markdown("<div style='margin-top:26px'/>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='glass goal-box'>
            <div style='font-weight:900; font-size:20px; color:white;'>{goal_name} — Target: Rs {goal_amount:,}</div>
            <div style='height:12px'></div>
            <div class='goal-bar' aria-hidden='true'><div class='goal-fill' style='width:{goal_progress}%;'></div></div>
            <div style='margin-top:12px; color:rgba(230,240,255,0.9); font-weight:700;'>{goal_progress:.1f}% complete • ETA: {months_needed} months</div>
            <div style='margin-top:16px;' class='tile {rec_color}'>
                <div style='font-weight:800; font-size:15px; color:inherit'>{rec_msg}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if show_plans:
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        p1, p2 = st.columns(2, gap="large")
        p1.markdown(f"<div class='glass plan-card'><div style='font-weight:900; font-size:18px;'>Basic Plan</div><div class='muted' style='margin-top:8px;'>Save Rs {int(basic_save):,}/mo</div><div style='margin-top:10px; font-weight:800;'>Est: {basic_time} months</div></div>", unsafe_allow_html=True)
        p2.markdown(f"<div class='glass plan-card'><div style='font-weight:900; font-size:18px;'>Strong Plan</div><div class='muted' style='margin-top:8px;'>Save Rs {int(strong_save):,}/mo</div><div style='margin-top:10px; font-weight:800;'>Est: {strong_time} months</div></div>", unsafe_allow_html=True)

# ---------------- AI INSIGHTS Page (REDESIGNED) ----------------
elif st.session_state['page'] == 'insights':
    st.markdown("<div class='center'><div class='app-title'>AI Insights</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Smart Emergency Fund — quick, clear & motivational</div>", unsafe_allow_html=True)

    # emergency values
    EM_MIN = 3
    EM_IDEAL = 6
    coverage_months = round(current_savings / max(1, monthly_expenses), 1)
    min_amount = monthly_expenses * EM_MIN
    ideal_amount = monthly_expenses * EM_IDEAL
    gap_min = max(0, min_amount - current_savings)
    gap_ideal = max(0, ideal_amount - current_savings)
    coverage_pct_of_ideal = min(100, (current_savings / ideal_amount) * 100) if ideal_amount > 0 else 0

    # left: gauge card, right: tiles and chart
    st.markdown("<div class='insight-wrap'>", unsafe_allow_html=True)

    # -------- Gauge card (Plotly Indicator) --------
    gauge_col, right_col = st.columns([1,1], gap="large")
    with gauge_col:
        card_html = "<div class='glass gauge-card'>"
        card_html += f"<div style='font-weight:900; font-size:18px; margin-bottom:8px;'>Emergency Coverage</div>"
        card_html += f"<div style='color:rgba(230,240,255,0.9); margin-bottom:6px;'>You have <b>Rs {current_savings:,}</b> saved</div>"
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)

        # plotly gauge (indicator)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=coverage_pct_of_ideal,
            number={'suffix': "%", 'font': {'size': 20}},
            delta={'reference': 100, 'relative': False, 'position': "top", 'font': {'size': 12}},
            gauge={
                'axis': {'range': [0, 100], 'tickmode': 'array', 'tickvals':[0,25,50,75,100]},
                'bar': {'color': "#7c3aed"},
                'steps': [
                    {'range': [0,33], 'color': "rgba(239,68,68,0.12)"},
                    {'range': [33,66], 'color': "rgba(251,146,60,0.10)"},
                    {'range': [66,100], 'color': "rgba(34,197,94,0.08)"},
                ],
                'threshold': {'line': {'color': "#06b6d4", 'width': 3}, 'thickness': 0.8, 'value': min(100, coverage_pct_of_ideal)}
            },
            title={'text': "Progress toward 6 months", 'font': {'size': 12}}
        ))
        fig_g.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=20,b=10,l=20,r=20))
        st.plotly_chart(fig_g, use_container_width=True)

    with right_col:
        # recommendation tiles based on coverage
        if coverage_months < EM_MIN:
            tile1_cls = "tile-critical"
            tile1_title = "⚠ Emergency Fund: LOW"
            tile1_sub = f"{coverage_months} months — Save Rs {gap_min:,} to reach 3 mo, Rs {gap_ideal:,} for 6 mo."
            tile2_cls = "tile-warning"
            tile2_title = "First Steps"
            tile2_sub = "Pause non-essentials, automate small transfer, and build habit."
        elif coverage_months < EM_IDEAL:
            tile1_cls = "tile-warning pulse"
            tile1_title = "✅ Emergency Fund: Moderate"
            tile1_sub = f"{coverage_months} months — you're close. Add Rs {gap_ideal:,} for ideal."
            tile2_cls = "tile-ok"
            tile2_title = "Quick Wins"
            tile2_sub = "Redirect bonuses, reduce 1 subscription, automate transfers."
        else:
            tile1_cls = "tile-celebrate pulse"
            tile1_title = "🌟 Emergency Fund: EXCELLENT"
            tile1_sub = f"{coverage_months} months — great job! Maintain & diversify."
            tile2_cls = "tile-ok"
            tile2_title = "Next Moves"
            tile2_sub = "Invest excess, plan goals, consider long-term safety net."

        # render two stacked tiles + small action row
        st.markdown(f"<div class='tile {tile1_cls} glass'><div class='title'>{tile1_title}</div><div class='sub'>{tile1_sub}</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tile {tile2_cls} glass'><div class='title'>{tile2_title}</div><div class='sub'>{tile2_sub}</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # end insight-wrap

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ---------------- Horizontal comparison chart (current vs 3mo vs 6mo) ----------------
    df_em = pd.DataFrame({
        "Category": ["Current Savings", "Minimum (3 mo)", "Ideal (6 mo)"],
        "Amount": [current_savings, min_amount, ideal_amount],
    })
    fig_bar = px.bar(df_em, x="Amount", y="Category", orientation='h',
                     text=df_em["Amount"].apply(lambda x: f"Rs {x:,}"),
                     color="Category",
                     color_discrete_sequence=["#06b6d4", "#fb7185", "#10b981"])
    fig_bar.update_traces(textposition="inside", insidetextanchor="middle", textfont=dict(size=13, color="white"))
    fig_bar.update_layout(template="plotly_dark", height=300, margin=dict(l=140), showlegend=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------- Short action row ----------------
    a1, a2, a3 = st.columns([1,1,1], gap="large")
    a1.markdown(f"<div class='glass tile tile-warning center'><div style='font-weight:800'>Build Habit</div><div class='muted'>Start Rs {max(5000, int(monthly_save*0.1)):,}/mo</div></div>", unsafe_allow_html=True)
    a2.markdown(f"<div class='glass tile tile-ok center'><div style='font-weight:800'>Automatic Transfer</div><div class='muted'>Schedule small weekly transfer</div></div>", unsafe_allow_html=True)
    a3.markdown(f"<div class='glass tile tile-ok center'><div style='font-weight:800'>Celebrate Wins</div><div class='muted'>If >6 mo — diversify & invest</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='muted center'>Tip: Use the 'Analyze / Predict' button in sidebar after making changes to update values.</div>", unsafe_allow_html=True)

# ---------------- Visuals page (kept attractive) ----------------
elif st.session_state['page'] == 'visuals':
    st.markdown("<div class='center'><div class='app-title'>Financial Visuals</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Clear charts for decisions</div>", unsafe_allow_html=True)

    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })
    fig = px.bar(chart_data, x="Category", y="Amount", color="Category",
                 text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
                 color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
    fig.update_traces(textposition='outside', textfont_size=14)
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=520,
                      font=dict(color="white", size=14), yaxis=dict(showgrid=False, title="Amount (PKR)", color="white"), xaxis=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Footer ----------------
st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.06); margin-top:22px;'>", unsafe_allow_html=True)
st.caption("© 2025 Your Personal Financial Advisor — Made with care in Pakistan")

