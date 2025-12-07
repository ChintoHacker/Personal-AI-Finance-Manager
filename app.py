import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# ----------------- Page config -----------------
st.set_page_config(page_title="Your Financial Advisor — Smart", page_icon="trophy", layout="wide")

# ----------------- Preserve original CSS + additions for meter/navigation -----------------
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

    /* Glow nav buttons */
    .glow-nav { text-align:center; margin:30px 0; }
    .glow-btn {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        color: white;
        border: none;
        padding: 12px 30px;
        margin: 0 10px;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.6), 0 0 40px rgba(236, 72, 153, 0.4);
        transition: all 0.3s ease;
    }
    .glow-btn.active {
        background: linear-gradient(45deg, #10b981, #34d399);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.9);
    }

    /* Emergency meter styles */
    .meter-box {
        background: rgba(255,255,255,0.16); backdrop-filter: blur(10px); border-radius: 18px;
        padding: 22px; border: 1px solid rgba(255,255,255,0.25); box-shadow: 0 10px 30px rgba(0,0,0,0.45);
        text-align:center;
    }
    .meter-bar { height: 36px; background: rgba(255,255,255,0.10); border-radius: 18px; overflow:hidden; margin:14px 0; }
    .meter-fill { height:100%; background: linear-gradient(90deg, #8b5cf6, #ec4899); transition: width 0.8s ease; }
    .sugg-weak { background: rgba(239,68,68,0.25); color:#fff; padding:14px; border-radius:12px; font-weight:700; }
    .sugg-mid  { background: rgba(251,146,60,0.22); color:#fff; padding:14px; border-radius:12px; font-weight:700; }
    .sugg-good { background: rgba(34,197,94,0.22); color:#fff; padding:14px; border-radius:12px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ----------------- Session state for page navigation -----------------
if "page" not in st.session_state:
    st.session_state["page"] = "overview"

def set_page(p):
    st.session_state["page"] = p

# ----------------- SIDEBAR (keep exactly like original) -----------------
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

# ----------------- CALCULATIONS (preserve original logic) -----------------
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100.0, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)
months_needed = "N/A" if monthly_save <= 0 else max(0, round((goal_amount - current_savings) / monthly_save))
remaining = max(0, goal_amount - current_savings)

# RECOMMENDATION logic (preserve)
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

# SMART PLANS (preserve original)
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

# ----------------- Header + Nav Buttons (glow) -----------------
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:14px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

# Nav buttons row (use st.columns to align)
nav_c1, nav_c2, nav_c3 = st.columns([1,1,1])
with nav_c1:
    btn_label = "Overview"
    if st.button(btn_label, key="nav_overview"):
        set_page("overview")
with nav_c2:
    btn_label = "AI Insights"
    if st.button(btn_label, key="nav_insights"):
        set_page("insights")
with nav_c3:
    btn_label = "Visuals"
    if st.button(btn_label, key="nav_visuals"):
        set_page("visuals")

st.markdown("<hr style='border:1px solid rgba(255,255,255,0.08)'>", unsafe_allow_html=True)

# ----------------- PAGE: OVERVIEW (original content preserved) -----------------
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

    # Goal Section (original)
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

    # Final Chart (preserve)
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

# ----------------- PAGE: INSIGHTS (NEW separate page with Emergency Fund meter) -----------------
elif st.session_state["page"] == "insights":
    st.markdown("<h2 style='text-align:center; color:#6CE0AC; margin-bottom:4px;'>AI Insights</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#E0E7FF; margin-top:2px;'>Emergency Fund — 3 Months of Expenses</h4>", unsafe_allow_html=True)

    # Calculation for emergency fund (3 months)
    required_fund = monthly_expenses * 3
    # progress can be >100 if savings > required, but meter should cap visually at 100%
    raw_progress = (current_savings / required_fund) * 100 if required_fund > 0 else 0
    visual_progress = min(max(raw_progress, 0), 100)  # 0..100 for CSS width

    # Render meter card
    st.markdown(f"""
    <div class='meter-box'>
        <div style='font-size:18px; color:#E0E7FF; font-weight:700;'>Required Emergency Fund</div>
        <div style='font-size:22px; color:white; margin-top:6px; font-weight:800;'>Rs {required_fund:,}</div>
        <div class='meter-bar' role='progressbar' aria-valuenow='{raw_progress:.1f}' aria-valuemin='0' aria-valuemax='100'>
            <div class='meter-fill' style='width:{visual_progress}%;'></div>
        </div>
        <div style='color:#E0E7FF; font-size:15px; margin-top:6px; font-weight:600;'>{min(raw_progress, 9999):.1f}% of required fund secured</div>
        <div style='color:#a0d9ff; font-size:13px; margin-top:6px;'>Current Savings: Rs {current_savings:,}  •  Shortfall: Rs {max(0, required_fund - current_savings):,}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Show tailored suggestion based on thresholds (<50, <80, >=80/100)
    if raw_progress < 50:
        st.markdown("<div class='sugg-weak'>Emergency fund bohot kam hai — <b>Action:</b> Har mahine minimum 20% alag rakhna. Side-income ya expense cut consider karein.</div>", unsafe_allow_html=True)
    elif raw_progress < 80:
        st.markdown("<div class='sugg-mid'>Acha chal raha hai — <b>Next:</b> Thoda aur consistency. Auto-transfer to emergency account set karein.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='sugg-good'>Shabash! Emergency fund accha hai — <b>Tip:</b> Is fund ko isolated rakhein aur investments me risk na lein.</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Compact extra info (short & minimal)
    st.markdown("""
    <div style='display:flex; gap:12px;'>
        <div style='flex:1; background:rgba(255,255,255,0.06); padding:14px; border-radius:12px; text-align:center;'>
            <div style='font-size:13px; color:#E0E7FF;'>Monthly Expenses</div>
            <div style='font-size:18px; color:white; font-weight:800;'>Rs {0:,}</div>
        </div>
        <div style='flex:1; background:rgba(255,255,255,0.06); padding:14px; border-radius:12px; text-align:center;'>
            <div style='font-size:13px; color:#E0E7FF;'>Months Covered</div>
            <div style='font-size:18px; color:white; font-weight:800;'>{1:.1f} months</div>
        </div>
    </div>
    """.format(monthly_expenses, current_savings / monthly_expenses if monthly_expenses>0 else 0), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

# ----------------- PAGE: VISUALS (preserve original final chart) -----------------
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
