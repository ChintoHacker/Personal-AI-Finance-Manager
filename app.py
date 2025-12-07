import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# ---------------- Page config ----------------
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

# ---------------- Styles ----------------
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%); font-family: 'Inter', sans-serif; }
    .app-title { font-size: 42px !important; font-weight: 900 !important; color: #6CE0AC !important; text-align: center; }

    .overview-card {
        background: rgba(255,255,255,0.16); backdrop-filter: blur(14px); border-radius: 22px;
        padding: 26px 16px; text-align: center; border: 1.5px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 32px rgba(0,0,0,0.45); height: 155px; transition: 0.3s;
    }
    .card-label { font-size: 16px; color: #E0E7FF; font-weight: 600; }
    .card-value { font-size: 30px; font-weight: 900; color: white; }

    .goal-box {
        background: rgba(255,255,255,0.17); backdrop-filter: blur(14px); border-radius: 20px;
        padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.12);
        text-align:center;
    }
    .goal-bar { height: 16px; background: rgba(255,255,255,0.12); border-radius: 12px; overflow:hidden; margin:10px auto; width:80%; }
    .goal-fill { height:100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); transition: width 0.6s ease; }

    /* Nav buttons */
    .glow-btn {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        color: white; border: none; padding: 10px 24px; margin: 0 8px;
        border-radius: 999px; font-size:15px; font-weight:700; cursor:pointer;
        box-shadow: 0 6px 18px rgba(139,92,246,0.35);
    }
    .glow-active { background: linear-gradient(45deg,#10b981,#34d399); }

    /* Insights area */
    .insights-wrap { padding:18px; }
    .meter-card { background: rgba(255,255,255,0.04); border-radius:14px; padding:18px; border:1px solid rgba(255,255,255,0.04); box-shadow: 0 8px 24px rgba(0,0,0,0.35); }

    /* Circular gauge */
    .gauge-wrap { display:flex; gap:28px; align-items:center; justify-content:center; flex-wrap:wrap; }
    .gauge {
        width:200px; height:200px; border-radius:50%;
        display:flex; align-items:center; justify-content:center; position:relative;
        box-shadow: 0 12px 30px rgba(0,0,0,0.45);
    }
    .gauge-inner {
        width:140px; height:140px; border-radius:50%;
        background: rgba(0,0,0,0.36); display:flex; align-items:center; justify-content:center; flex-direction:column;
        color:white; font-weight:800; text-align:center; border:6px solid rgba(255,255,255,0.04);
    }
    .gauge-label { font-size:13px; color:#cfe9ff; font-weight:700; }
    .gauge-percent { font-size:28px; margin-top:6px; color:white; font-weight:900; }

    /* Stats boxes */
    .stat-row { display:flex; gap:16px; justify-content:center; margin-top:12px; flex-wrap:wrap; }
    .stat-box { background: rgba(255,255,255,0.06); padding:14px 20px; border-radius:10px; min-width:200px; text-align:center; border:1px solid rgba(255,255,255,0.04); }
    .stat-small { color:#cfe9ff; font-size:13px; }
    .stat-big { color:white; font-size:18px; font-weight:800; margin-top:6px; }

    /* Three info boxes */
    .three-row { display:flex; gap:14px; justify-content:center; margin-top:16px; flex-wrap:wrap; }
    .info-box { background: rgba(124,112,163,0.18); padding:14px; border-radius:10px; min-width:220px; color:white; text-align:left; }
    .info-title { font-size:13px; color:#e6e6ff; margin-bottom:6px; }
    .info-value { font-size:18px; font-weight:800; }

    /* Quick insights */
    .quick-row { display:flex; gap:12px; justify-content:center; margin-top:18px; flex-wrap:nowrap; overflow-x:auto; padding-bottom:6px; }
    .q-card { background: rgba(255,255,255,0.03); border-radius:12px; padding:12px 14px; min-width:220px; display:flex; gap:10px; align-items:flex-start; border:1px solid rgba(255,255,255,0.03); }
    .q-icon { width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; color:white; }
    .q-content { color:#e8f6ff; }
    .q-title { font-weight:800; margin-bottom:4px; }
    .q-sub { font-size:13px; opacity:0.95; }

    /* responsive */
    @media (max-width:900px) {
        .gauge { width:170px; height:170px; }
        .gauge-inner { width:120px; height:120px; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Session state for pages ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "overview"

def set_page(p):
    st.session_state["page"] = p

# ---------------- Sidebar inputs (preserve original) ----------------
with st.sidebar:
    st.markdown("<h2 style='color:#6CE0AC; text-align:center;'>Apki Financial Inputs</h2>", unsafe_allow_html=True)
    st.markdown("<div style='padding:8px;'>", unsafe_allow_html=True)
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

# ---------------- Calculations (preserve) ----------------
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
remaining_goal = max(0, goal_amount - current_savings)

# recommendation (preserve)
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

    basic_time = "N/A" if basic_save <= 0 else round(remaining_goal / basic_save)
    strong_time = "N/A" if strong_save <= 0 else round(remaining_goal / strong_save)

# ---------------- Header + nav ----------------
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:14px; margin-top:-8px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

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

# ---------------- PAGE: OVERVIEW (unchanged) ----------------
if st.session_state["page"] == "overview":
    st.markdown("<h3 style='text-align:center; color:white; margin:14px 0;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
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

    st.markdown("<h3 style='text-align:center; color:white; margin-bottom:18px;'>Goal Progress & Smart Plans</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='goal-box'>
        <div style='font-size:20px; font-weight:800; color:white; margin-bottom:8px;'>{goal_name} → Target: Rs {goal_amount:,}</div>
        <div class='goal-bar'><div class='goal-fill' style='width:{goal_progress}%;'></div></div>
        <div style='color:#E0E7FF; font-size:14px; font-weight:600; margin-top:8px;'>{goal_progress:.1f}% Complete • ETA: {months_needed} months</div>
        <div class='rec-message {rec_color}' style='margin-top:12px;'>{rec_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    if show_plans:
        st.markdown("<h4 style='text-align:center; color:white; margin-top:26px;'>Personalized Savings Plans</h4>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(f"""
            <div class='plan-card'>
                <b>Basic Plan</b><br>
                Save <b>Rs {int(basic_save):,}/month</b><br>
                <span style='color:#a0d9ff; font-size:13px;'>Time: {basic_time} months</span>
            </div>
            """, unsafe_allow_html=True)
        with p2:
            st.markdown(f"""
            <div class='plan-card'>
                <b>Strong Plan</b><br>
                Save <b>Rs {int(strong_save):,}/month</b><br>
                <span style='color:#a0d9ff; font-size:13px;'>Time: {strong_time} months</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # final chart
    st.markdown("<h3 style='text-align:center; color:white;'>Financial Overview</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })
    fig = px.bar(chart_data, x="Category", y="Amount", color="Category",
                 text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
                 color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
    fig.update_traces(textposition='outside', textfont_size=14, textfont_color="white")
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=420,
                      font=dict(color="white", size=14), yaxis=dict(showgrid=False, color="white"), xaxis=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption("© 2025 Your Personal Financial Advisor - Made with love in Pakistan")

# ---------------- PAGE: INSIGHTS (fixed — original summary + gauge below + quick insights) ----------------
elif st.session_state["page"] == "insights":
    st.markdown("<div class='insights-wrap'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#6CE0AC; margin-bottom:6px;'>AI Insights</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#E0E7FF; margin-top:2px;'>Emergency Fund — 3 Months of Expenses</h4>", unsafe_allow_html=True)

    # --- ORIGINAL Emergency summary box (kept intact, simple horizontal fill showing coverage) ---
    required_fund = monthly_expenses * 3
    summary_progress = (current_savings / required_fund) * 100 if required_fund > 0 else 0
    summary_progress_capped = min(max(summary_progress, 0), 100)
    shortfall = max(0, required_fund - current_savings)

    st.markdown(f"""
    <div class='goal-box' style='margin-top:12px;'>
        <div style='font-size:16px; font-weight:800; color:white;'>Emergency Summary</div>
        <div style='font-size:13px; color:#cfe9ff; margin-top:6px;'>Required (3 mo): Rs {required_fund:,} • Current Savings: Rs {current_savings:,}</div>
        <div class='goal-bar' style='margin-top:12px;'><div class='goal-fill' style='width:{summary_progress_capped}%;'></div></div>
        <div style='color:#E0E7FF; font-size:13px; margin-top:8px;'>{summary_progress:.1f}% secured • Shortfall: Rs {shortfall:,}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- New: Separate stylish circular gauge (200px) under the original summary ---
    raw_progress = (current_savings / required_fund) * 100 if required_fund > 0 else 0
    visual_progress = min(max(raw_progress, 0), 100)
    angle_deg = visual_progress * 3.6  # percent -> degrees for conic-gradient
    if raw_progress < 50:
        gauge_color = "#ef4444"
        suggestion_html = "<div style='color:#ffdede; background:rgba(239,68,68,0.08); padding:10px; border-radius:8px; text-align:center; font-weight:700;'>Emergency fund bohot kam hai — start saving 20%/month</div>"
    elif raw_progress < 80:
        gauge_color = "#fb923c"
        suggestion_html = "<div style='color:#fff7ed; background:rgba(251,146,60,0.06); padding:10px; border-radius:8px; text-align:center; font-weight:700;'>Acha progress — set auto-transfer to emergency account</div>"
    else:
        gauge_color = "#10b981"
        suggestion_html = "<div style='color:#e8fff0; background:rgba(16,185,129,0.06); padding:10px; border-radius:8px; text-align:center; font-weight:700;'>Shabash! Emergency fund nearly/fully complete</div>"

    months_covered = current_savings / monthly_expenses if monthly_expenses>0 else 0

    st.markdown(f"""
    <div class='meter-card' style='margin-top:8px;'>
        <div class='gauge-wrap'>
            <div style='min-width:260px; flex:1; display:flex; justify-content:center;'>
                <div class='gauge' style="background: conic-gradient({gauge_color} {angle_deg}deg, rgba(255,255,255,0.06) {angle_deg}deg);">
                    <div class='gauge-inner'>
                        <div class='gauge-label'>Emergency Ready</div>
                        <div class='gauge-percent'>{raw_progress if raw_progress<9999 else 9999:.1f}%</div>
                        <div style='font-size:12px; color:#bfe9ff; margin-top:6px;'>of required</div>
                    </div>
                </div>
            </div>

            <div style='flex:1; min-width:260px; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:8px;'>
                <div style='font-size:14px; color:#cfe9ff; font-weight:700;'>Required Emergency Fund</div>
                <div style='font-size:20px; color:white; font-weight:900;'>Rs {required_fund:,}</div>

                <div class='stat-row' style='margin-top:8px;'>
                    <div class='stat-box'>
                        <div class='stat-small'>Monthly Expenses</div>
                        <div class='stat-big'>Rs {monthly_expenses:,}</div>
                    </div>
                    <div class='stat-box'>
                        <div class='stat-small'>Months Covered</div>
                        <div class='stat-big'>{months_covered:.1f} months</div>
                    </div>
                </div>

                <div style='margin-top:8px; color:#a0d9ff; font-size:13px;'>Current Savings: Rs {current_savings:,} • Shortfall: Rs {shortfall:,}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Three info boxes (Current Coverage, Min Required, Ideal) ---
    current_cov = current_savings / monthly_expenses if monthly_expenses>0 else 0
    min_required = required_fund
    ideal_required = monthly_expenses * 6

    st.markdown(f"""
    <div class='three-row'>
        <div class='info-box'>
            <div class='info-title'>Current Coverage</div>
            <div class='info-value'>{current_cov:.1f} mo</div>
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

    # --- Suggestion line (short) ---
    st.markdown(suggestion_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- QUICK INSIGHTS: 4 cards in one row ---
    saving_status = "Positive" if monthly_income > monthly_expenses else "Negative"
    goal_status = "Behind" if goal_progress < 50 else ("On Track" if goal_progress < 90 else "Nearly/Done")
    debt_status = "No debt" if total_debt <= 0 else f"Rs {total_debt:,}"

    if raw_progress < 50:
        emergency_label = "Emergency: Low"
        emergency_sub = f"{current_cov:.1f} mo — need Rs {shortfall:,} to reach 3m"
    elif raw_progress < 80:
        emergency_label = "Emergency: Fair"
        emergency_sub = "Keep adding monthly transfers"
    else:
        emergency_label = "Emergency: Good"
        emergency_sub = "Nearly/fully covered"

    st.markdown(f"""
    <div class='quick-row'>
        <div class='q-card'>
            <div class='q-icon' style='background:linear-gradient(180deg,#f97316,#ef4444);'>⚠️</div>
            <div class='q-content'>
                <div class='q-title'>{emergency_label}</div>
                <div class='q-sub'>{emergency_sub}</div>
            </div>
        </div>

        <div class='q-card'>
            <div class='q-icon' style='background:linear-gradient(180deg,#10b981,#059669);'>💰</div>
            <div class='q-content'>
                <div class='q-title'>Saving: {saving_status}</div>
                <div class='q-sub'>Income Rs {monthly_income:,} • Exp Rs {monthly_expenses:,}</div>
            </div>
        </div>

        <div class='q-card'>
            <div class='q-icon' style='background:linear-gradient(180deg,#7c3aed,#8b5cf6);'>🎯</div>
            <div class='q-content'>
                <div class='q-title'>Goal: {goal_status}</div>
                <div class='q-sub'>{goal_progress:.0f}% complete</div>
            </div>
        </div>

        <div class='q-card'>
            <div class='q-icon' style='background:linear-gradient(180deg,#0ea5e9,#0284c7);'>📉</div>
            <div class='q-content'>
                <div class='q-title'>Debt</div>
                <div class='q-sub'>{debt_status}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close insights-wrap

# ---------------- PAGE: VISUALS (preserved) ----------------
elif st.session_state["page"] == "visuals":
    st.markdown("<h3 style='text-align:center; color:white;'>Financial Overview</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings", "Investments"],
        "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
    })
    fig = px.bar(chart_data, x="Category", y="Amount", color="Category",
                 text=chart_data["Amount"].apply(lambda x: f"Rs {x:,}"),
                 color_discrete_sequence=["#8b5cf6", "#ef4444", "#10b981", "#f59e0b"])
    fig.update_traces(textposition='outside', textfont_size=16, textfont_color="white")
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=500,
                      font=dict(color="white", size=16), yaxis=dict(showgrid=False, color="white"), xaxis=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
