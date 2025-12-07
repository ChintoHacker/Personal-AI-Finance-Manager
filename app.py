import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# ----------------- Page config -----------------
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

# ----------------- Styles (original + new) -----------------
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }

    .app-title { font-size: 42px !important; font-weight: 900 !important; color: #6CE0AC !important; text-align: center; }
    .overview-card {
        background: rgba(255,255,255,0.16); backdrop-filter: blur(14px); border-radius: 22px;
        padding: 26px 16px; text-align: center; border: 1.5px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 32px rgba(0,0,0,0.45); height: 155px; transition: 0.3s;
    }
    .overview-card:hover { transform: translateY(-8px); }
    .card-label { font-size: 16px; color: #E0E7FF; font-weight: 600; }
    .card-value { font-size: 30px; font-weight: 900; color: white; }

    .goal-box {
        background: rgba(255,255,255,0.17); backdrop-filter: blur(14px); border-radius: 25px;
        padding: 32px; box-shadow: 0 14px 40px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.25);
        text-align: center;
    }
    .goal-bar { height: 38px; background: rgba(255,255,255,0.22); border-radius: 20px; overflow: hidden; margin: 22px 0; }
    .goal-fill { height: 100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); }

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

    /* Navigation buttons */
    .glow-btn {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        color: white;
        border: none;
        padding: 12px 30px;
        margin: 0 8px;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(139,92,246,0.5);
    }
    .glow-btn:hover { transform: translateY(-4px); }
    .glow-active { background: linear-gradient(45deg,#10b981,#34d399); }

    /* Insights styles */
    .insights-section { margin: 18px 0 30px; }
    .meter-card {
        background: rgba(255,255,255,0.06); border-radius: 14px; padding: 20px;
        border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    }

    /* Circular gauge using conic gradient */
    .gauge-wrap { display:flex; align-items:center; gap:28px; justify-content:center; flex-wrap:wrap; }
    .gauge {
        width: 200px; height: 200px; border-radius: 50%;
        display:flex; align-items:center; justify-content:center;
        background: conic-gradient(#ef4444 0deg, rgba(255,255,255,0.06) 0deg); /* will override inline */
        position:relative;
        box-shadow: 0 8px 30px rgba(0,0,0,0.45);
    }
    .gauge-inner {
        width: 140px; height:140px; border-radius:50%;
        background: rgba(0,0,0,0.35);
        display:flex; align-items:center; justify-content:center; flex-direction:column;
        color:white; font-weight:800; font-size:16px;
        border: 6px solid rgba(255,255,255,0.06);
    }
    .gauge-label { font-size:13px; color:#cfe9ff; font-weight:700; }
    .gauge-percent { font-size:28px; margin-top:4px; color:white; font-weight:900; }

    /* Stats boxes (Expenses & Months Covered) */
    .stat-row { display:flex; gap:18px; justify-content:center; margin-top:12px; flex-wrap:wrap; }
    .stat-box {
        background: rgba(255,255,255,0.06); padding:18px 26px; border-radius:12px;
        min-width:220px; text-align:center; border:1px solid rgba(255,255,255,0.06);
    }
    .stat-small { color:#cfe9ff; font-size:13px; }
    .stat-big { color:white; font-size:20px; font-weight:800; margin-top:6px; }

    /* Three info boxes */
    .three-row { display:flex; gap:18px; justify-content:center; margin-top:18px; flex-wrap:wrap; }
    .info-box {
        background: rgba(124, 112, 163, 0.22); padding:18px; border-radius:12px; min-width:240px;
        color:white; text-align:left; box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }
    .info-title { font-size:13px; color:#e6e6ff; margin-bottom:6px; }
    .info-value { font-size:20px; font-weight:800; }

    /* Quick insights row - 4 cards in one row */
    .quick-row { display:flex; gap:16px; justify-content:center; margin-top:20px; flex-wrap:nowrap; overflow-x:auto; padding-bottom:6px; }
    .q-card {
        background: rgba(255,255,255,0.04); border-radius:12px; padding:16px 18px; min-width:210px;
        display:flex; gap:10px; align-items:flex-start; border:1px solid rgba(255,255,255,0.04);
    }
    .q-icon {
        width:40px; height:40px; border-radius:10px; background:rgba(255,255,255,0.06);
        display:flex; align-items:center; justify-content:center; font-size:18px; color:white;
    }
    .q-content { color:#e8f6ff; }
    .q-title { font-weight:800; margin-bottom:4px; }
    .q-sub { font-size:13px; opacity:0.9; }

    /* Responsive tweak for super small screens */
    @media (max-width:800px) {
        .quick-row { gap:10px; }
        .gauge { width:170px; height:170px; }
        .gauge-inner { width:120px; height:120px; }
    }
</style>
""", unsafe_allow_html=True)


# ----------------- Session state for page -----------------
if "page" not in st.session_state:
    st.session_state["page"] = "overview"

def set_page(p):
    st.session_state["page"] = p

# ----------------- Sidebar inputs (preserve original) -----------------
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

# ----------------- Calculations (preserve originals) -----------------
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
remaining = max(0, goal_amount - current_savings)

# recommendation messages (preserve)
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

# smart plans (preserve)
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

# ----------------- Header & nav buttons -----------------
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:14px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

nav_c1, nav_c2, nav_c3 = st.columns([1,1,1])
with nav_c1:
    if st.button("Overview", key="nav_overview"):
        set_page("overview")
with nav_c2:
    if st.button("AI Insights", key="nav_insights"):
        set_page("insights")
with nav_c3:
    if st.button("Visuals", key="nav_visuals"):
        set_page("visuals")

st.markdown("<hr style='border:1px solid rgba(255,255,255,0.06)'>", unsafe_allow_html=True)

# ----------------- PAGE: OVERVIEW (preserved) -----------------
if st.session_state["page"] == "overview":
    st.markdown("<h3 id='overview' style='text-align:center; color:white; margin:center; margin:20px 0 10px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
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

    st.markdown("<h3 style='text-align:center; color:white; margin-bottom:20px;'>Goal Progress & Smart Plans</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='goal-box'>
        <div style='font-size:24px; font-weight:800; color:white; margin-bottom:12px;'>
            {goal_name} → Target: Rs {goal_amount:,}
        </div>
        <div class='goal-bar'>
            <div class='goal-fill' style='width:{goal_progress}%'></div>
        </div>
        <div style='color:#E0E7FF; font-size:16px; font-weight:600; margin:12px 0;'>
            {goal_progress:.1f}% Complete • Current ETA: {months_needed} months
        </div>
        <div class='rec-message {rec_color}'>
            {rec_msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_plans:
        st.markdown("<h4 style='text-align:center; color:white; margin-top:30px;'>Personalized Savings Plans</h4>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(f"""
            <div class='plan-card'>
                <b>Basic Plan</b><br>
                Save <b>Rs {int(basic_save):,}/month</b><br>
                <span style='color:#a0d9ff; font-size:15px;'>Time: {basic_time} months</span>
            </div>
            """, unsafe_allow_html=True)
        with p2:
            st.markdown(f"""
            <div class='plan-card'>
                <b>Strong Plan</b><br>
                Save <b>Rs {int(strong_save):,}/month</b><br>
                <span style='color:#a0d9ff; font-size:15px;'>Time: {strong_time} months</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center; color:white;'>Financial Overview</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })
    fig = px.bar(chart_data, x="Category", y="Amount", color="Category",
                 text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
                 color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
    fig.update_traces(textposition='outside', textfont_size=14, textfont_color="white")
    fig.update_layout(
        showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=420, font=dict(color="white", size=14),
        yaxis=dict(showgrid=False, title="Amount (PKR)", color="white"),
        xaxis=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")

# ----------------- PAGE: INSIGHTS (new enhanced page) -----------------
elif st.session_state["page"] == "insights":
    st.markdown("<div class='insights-section'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#6CE0AC; margin-bottom:6px;'>AI Insights</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#E0E7FF; margin-top:2px;'>Emergency Fund — 3 Months of Expenses</h4>", unsafe_allow_html=True)

    # Emergency fund calculations
    required_fund = monthly_expenses * 3
    raw_progress = (current_savings / required_fund) * 100 if required_fund > 0 else 0
    visual_progress = min(max(raw_progress, 0), 100)  # capped 0..100 for gauge display
    # choose color based on thresholds
    if raw_progress < 50:
        gauge_color = "#ef4444"   # red
        suggestion_html = "<div class='sugg-weak'>Emergency fund bohot kam hai — <b>Action:</b> Har mahine minimum 20% alag rakhna. Side-income ya expense cut consider karein.</div>"
    elif raw_progress < 80:
        gauge_color = "#fb923c"   # orange
        suggestion_html = "<div class='sugg-mid'>Acha progress — <b>Next:</b> Auto-transfer aur consistency rakhein.</div>"
    else:
        gauge_color = "#10b981"   # green
        suggestion_html = "<div class='sugg-good'>Shabash! Emergency fund accha hai — <b>Tip:</b> Fund ko isolated rakhein.</div>"

    # Render gauge + stats
    # Build inline conic-gradient style for exact degrees
    angle_deg = visual_progress * 3.6  # percent -> degrees
    remaining_shortfall = max(0, required_fund - current_savings)
    months_covered = current_savings / monthly_expenses if monthly_expenses > 0 else 0

    st.markdown(f"""
    <div class='meter-card'>
        <div class='gauge-wrap'>
            <div style='flex:1; min-width:220px;'>
                <div style='display:flex; justify-content:center;'>
                    <div class='gauge' style="background: conic-gradient({gauge_color} {angle_deg}deg, rgba(255,255,255,0.06) {angle_deg}deg);">
                        <div class='gauge-inner'>
                            <div class='gauge-label'>Emergency Ready</div>
                            <div class='gauge-percent'>{raw_progress if raw_progress < 9999 else 9999:.1f}%</div>
                            <div style='font-size:12px; color:#bfe9ff; margin-top:6px;'>of required</div>
                        </div>
                    </div>
                </div>
            </div>

            <div style='flex:1; min-width:300px;'>
                <div style='display:flex; flex-direction:column; gap:10px; align-items:center;'>
                    <div style='font-size:14px; color:#cfe9ff; font-weight:700;'>Required Emergency Fund</div>
                    <div style='font-size:20px; color:white; font-weight:900;'>Rs {required_fund:,}</div>

                    <div class='stat-row' style='margin-top:12px;'>
                        <div class='stat-box'>
                            <div class='stat-small'>Monthly Expenses</div>
                            <div class='stat-big'>Rs {monthly_expenses:,}</div>
                        </div>
                        <div class='stat-box'>
                            <div class='stat-small'>Months Covered</div>
                            <div class='stat-big'>{months_covered:.1f} months</div>
                        </div>
                    </div>

                    <div style='margin-top:10px; width:100%; display:flex; justify-content:center;'>
                        <div style='color:#a0d9ff; font-size:13px;'>Current Savings: Rs {current_savings:,} &nbsp;•&nbsp; Shortfall: Rs {remaining_shortfall:,}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Three info boxes row
    current_coverage_months = current_savings / monthly_expenses if monthly_expenses > 0 else 0
    min_required = required_fund
    ideal_required = monthly_expenses * 6

    st.markdown(f"""
    <div class='three-row'>
        <div class='info-box'>
            <div class='info-title'>Current Coverage</div>
            <div class='info-value'>{current_coverage_months:.1f} mo</div>
        </div>
        <div class='info-box'>
            <div class='info-title'>Min Required (3 mo)</div>
            <div class='info-value'>Rs {min_required:,}</div>
        </div>
        <div class='info-box'>
            <div class='info-title'>Ideal (6 mo)</div>
            <div class='info-value'>Rs {ideal_required:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Suggestion (short)
    st.markdown(suggestion_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # QUICK INSIGHTS ROW - 4 cards in one row (icons chosen for best fit)
    # Emergency (⚠️), Saving (💰), Goal (🎯), Debt (📉)
    # Short statuses derived from inputs
    saving_status = "Positive" if monthly_income > monthly_expenses else "Negative"
    goal_pct = goal_progress
    debt_status = "No debt" if total_debt <= 0 else f"Rs {total_debt:,}"

    # Emergency short text
    if raw_progress < 50:
        emergency_text = "Low — need Rs {:,} to reach 3m".format(remaining_shortfall)
        emergency_label = "Emergency: Low"
    elif raw_progress < 80:
        emergency_text = "Fair — keep building"
        emergency_label = "Emergency: Fair"
    else:
        emergency_text = "Good — nearly/fully covered"
        emergency_label = "Emergency: Good"

    st.markdown(f"""
    <div class='quick-row'>
        <div class='q-card'>
            <div class='q-icon' style='background: linear-gradient(180deg,#f97316,#ef4444);'>⚠️</div>
            <div class='q-content'>
                <div class='q-title'>{emergency_label}</div>
                <div class='q-sub'>{emergency_text}</div>
            </div>
        </div>

        <div class='q-card'>
            <div class='q-icon' style='background: linear-gradient(180deg,#10b981,#059669);'>💰</div>
            <div class='q-content'>
                <div class='q-title'>Saving: {saving_status}</div>
                <div class='q-sub'>Income: Rs {monthly_income:,} • Expenses: Rs {monthly_expenses:,}</div>
            </div>
        </div>

        <div class='q-card'>
            <div class='q-icon' style='background: linear-gradient(180deg,#7c3aed,#8b5cf6);'>🎯</div>
            <div class='q-content'>
                <div class='q-title'>Goal: { "Behind" if goal_pct < 50 else ("On Track" if goal_pct < 90 else "Near/Done") }</div>
                <div class='q-sub'>{goal_pct:.0f}% complete</div>
            </div>
        </div>

        <div class='q-card'>
            <div class='q-icon' style='background: linear-gradient(180deg,#0ea5e9,#0284c7);'>📉</div>
            <div class='q-content'>
                <div class='q-title'>Debt</div>
                <div class='q-sub'>{debt_status}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

# ----------------- PAGE: VISUALS (preserved) -----------------
elif st.session_state["page"] == "visuals":
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
    st.markdown("<br><br>", unsafe_allow_html=True)

# ----------------- End -----------------
