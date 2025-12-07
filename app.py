# app.py (FINAL - Updated exactly as requested)
# Changes: removed empty top bar in Visuals, improved text visibility across UI and charts,
# moved section titles into their neon boxes, fixed Risk Score calculation and logic,
# improved PDF layout to be professional and user-friendly. No other behavior changed.
import streamlit as st
from datetime import datetime
import math
import plotly.express as px
import pandas as pd

# Small imports used in visuals/insights and PDF
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ---------------- Page config ----------------
st.set_page_config(page_title="Your Financial Advisor — Smart AI", page_icon="trophy", layout="wide")

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
    st.markdown("<h2 style='color:#6CE0AC; text-align:center;'>Your Financial Inputs</h2>", unsafe_allow_html=True)
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)

    # ---------- IMPORTANT: removed meaningful autofill by setting defaults to 0 ----------
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=0, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=0, step=5000, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#6CE0AC; text-align:center;'>Your Goal</h2>", unsafe_allow_html=True)
    goal_name = st.text_input("Goal Name(car 🚙, house 🏡 etc..)", value="")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=0, value=0, step=50000, format="%d")

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
    rec_msg = "GOAL ACHIEVED!<br><b>Congrats!</b><br>Aap ne kar dikhaya! Ab new big goal set karain"
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
st.markdown("<h1 class='app-title'>Your Personal Financial Advisor — Smart AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#E0E7FF; font-size:22px; margin-top:-10px;'>Today {datetime.now().strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

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
            {goal_name if goal_name else 'Unnamed Goal'} → Target: Rs {goal_amount:,}
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
    # ensure text and axis labels are obvious on gradient
    fig.update_traces(textposition='outside', textfont_size=16, textfont_color="white")
    fig.update_layout(
        showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=520, font=dict(color="white", size=14),
        yaxis=dict(showgrid=False, title="Amount (PKR)", color="white"),
        xaxis=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- PDF Export Button (improved layout) ----------
    def create_professional_pdf():
        # Professional white-page PDF created via PIL (Option A) - improved layout
        W, H = 1240, 1754  # A4-like tall canvas
        margin = 60
        img = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(img)

        # Attempt to use a nicer font if available; fallback to default
        try:
            header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
            section_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
            normal_font = ImageFont.truetype("DejaVuSans.ttf", 18)
            mono_font = ImageFont.truetype("DejaVuSans.ttf", 16)
        except Exception:
            header_font = ImageFont.load_default()
            section_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            mono_font = ImageFont.load_default()

        y = margin
        draw.text((margin, y), "Your Personal Financial Advisor — Report", fill="black", font=header_font)
        y += 56
        draw.text((margin, y), f"Generated: {datetime.now().strftime('%d %B %Y')}", fill="black", font=mono_font)
        y += 28

        # Draw Overview box
        box_x = margin
        box_w = W - 2 * margin
        box_h = 220
        draw.rectangle((box_x, y, box_x + box_w, y + box_h), outline=(0,0,0), width=1, fill=(245,245,245))
        inner_x = box_x + 18
        inner_y = y + 14
        draw.text((inner_x, inner_y), "Overview", fill="black", font=section_font)
        inner_y += 32
        overview_lines = [
            f"Monthly Income: Rs {monthly_income:,}",
            f"Monthly Expenses: Rs {monthly_expenses:,}",
            f"Monthly Savings (Income-Expenses): Rs {monthly_save:,}",
            f"Current Savings: Rs {current_savings:,}",
            f"Total Investments: Rs {current_investments:,}",
            f"Total Debt: Rs {total_debt:,}",
            f"Net Worth: Rs {net_worth:,}"
        ]
        for line in overview_lines:
            draw.text((inner_x, inner_y), line, fill="black", font=mono_font)
            inner_y += 24
        y += box_h + 20

        # Goal box
        box_h = 160
        draw.rectangle((box_x, y, box_x + box_w, y + box_h), outline=(0,0,0), width=1, fill=(245,245,245))
        inner_x = box_x + 18
        inner_y = y + 14
        draw.text((inner_x, inner_y), "Goal & Progress", fill="black", font=section_font)
        inner_y += 30
        draw.text((inner_x, inner_y), f"Goal: {goal_name if goal_name else 'Unnamed Goal'}", fill="black", font=mono_font)
        inner_y += 22
        draw.text((inner_x, inner_y), f"Target: Rs {goal_amount:,} • Progress: {goal_progress:.1f}%", fill="black", font=mono_font)
        inner_y += 22
        draw.text((inner_x, inner_y), f"Remaining: Rs {remaining:,}", fill="black", font=mono_font)
        y += box_h + 20

        # Recommendation & Plans box
        box_h = 160
        draw.rectangle((box_x, y, box_x + box_w, y + box_h), outline=(0,0,0), width=1, fill=(245,245,245))
        inner_x = box_x + 18
        inner_y = y + 14
        draw.text((inner_x, inner_y), "Recommendation & Plans", fill="black", font=section_font)
        inner_y += 30
        rec_text = rec_msg.replace("<br>", " ").replace("<b>", "").replace("</b>", "")
        # wrap rec_text into multiple lines
        max_chars = 80
        for i in range(0, len(rec_text), max_chars):
            draw.text((inner_x, inner_y), rec_text[i:i+max_chars], fill="black", font=mono_font)
            inner_y += 20
        inner_y += 6
        if show_plans:
            draw.text((inner_x, inner_y), f"Basic Plan: Rs {int(basic_save):,}/month • Time: {basic_time} months", fill="black", font=mono_font)
            inner_y += 20
            draw.text((inner_x, inner_y), f"Strong Plan: Rs {int(strong_save):,}/month • Time: {strong_time} months", fill="black", font=mono_font)
        y += box_h + 20

        # Risk + Category breakdown box
        box_h = 210
        draw.rectangle((box_x, y, box_x + box_w, y + box_h), outline=(0,0,0), width=1, fill=(245,245,245))
        inner_x = box_x + 18
        inner_y = y + 14
        draw.text((inner_x, inner_y), "Risk & Categories", fill="black", font=section_font)
        inner_y += 30

        # Risk calculation (repeat in report to be explicit)
        # compute stable risk for pdf
        try:
            debt_norm = total_debt / (total_debt + current_savings + 1) if (total_debt + current_savings) > 0 else 0
            expense_norm = monthly_expenses / (monthly_income + 1) if monthly_income > 0 else 0
            risk_score_pdf = int(min(max((debt_norm * 0.6 + expense_norm * 0.4) * 100, 0), 100))
        except Exception:
            risk_score_pdf = 50
        risk_level_pdf = "Low" if risk_score_pdf < 30 else ("Moderate" if risk_score_pdf < 65 else "High")
        draw.text((inner_x, inner_y), f"Risk Score: {risk_score_pdf}/100 • {risk_level_pdf}", fill="black", font=mono_font)
        inner_y += 28
        draw.text((inner_x, inner_y), "Top spending categories:", fill="black", font=mono_font)
        inner_y += 22
        # category breakdown
        cats = ["Food", "Transport", "Bills", "Shopping", "Other"]
        if monthly_expenses <= 0:
            amounts = [0,0,0,0,0]
        else:
            amounts = [monthly_expenses * 0.25, monthly_expenses * 0.15, monthly_expenses * 0.30, monthly_expenses * 0.20, monthly_expenses * 0.10]
        for c, a in zip(cats, amounts):
            draw.text((inner_x+8, inner_y), f"{c}: Rs {int(a):,}", fill="black", font=mono_font)
            inner_y += 20

        # Footer
        draw.line((margin, H - 120, W - margin, H - 120), fill=(0,0,0), width=1)
        draw.text((margin, H - 100), "© 2025 Your Personal Financial Advisor - Made with Abdul-Hanan in Pakistan", fill="black", font=mono_font)

        buf = BytesIO()
        # Save as PDF (PIL can save image as a single-page PDF)
        img.save(buf, format="PDF", resolution=100.0)
        buf.seek(0)
        return buf

    pdf_buf = None
    if st.button("Export PDF Report (Professional)"):
        try:
            pdf_buf = create_professional_pdf()
            st.success("PDF Generated — click Download below.")
            st.download_button("Download Financial Report (PDF)", data=pdf_buf, file_name="financial_report.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")

    st.markdown("---")
    st.caption("© 2025 Your Personal Financial Advisor - Made with Abdul-Hanan in Pakistan")

# ---------------- PAGE: INSIGHTS ----------------
elif st.session_state["page"] == "insights":

    # Page Title
    st.markdown("<h2 style='text-align:center; color:#6CE0AC; margin-bottom:0;'>Modern Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#dbeafe; margin-top:-8px; font-size:17px;'>Emergency readiness overview</p>", unsafe_allow_html=True)

    # Calculations
    required = monthly_expenses * 3
    ideal_required = monthly_expenses * 6
    raw_progress = (current_savings / required * 100) if required > 0 else 0
    progress = min(max(raw_progress, 0), 100)
    months_covered = (current_savings / monthly_expenses) if monthly_expenses > 0 else 0
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
        suggestion = "Shabash! Emergency fund nearly / fully complete — keep it isolated for real emergencies."

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

    # ---------- NEW: Risk Level Score (fixed & improved logic) ----------
    # compute normalized, explainable risk
    try:
        debt_norm = total_debt / (total_debt + current_savings + 1) if (total_debt + current_savings) > 0 else 0
        expense_norm = monthly_expenses / (monthly_income + 1) if monthly_income > 0 else 0
        risk_score = int(min(max((debt_norm * 0.6 + expense_norm * 0.4) * 100, 0), 100))
    except Exception:
        risk_score = 50

    risk_level = "Low" if risk_score < 30 else ("Moderate" if risk_score < 65 else "High")

    st.markdown(f"""
        <div style='background:rgba(255,255,255,0.06); padding:18px; border-radius:12px; 
             border:1px solid rgba(255,255,255,0.08); display:flex; align-items:center;'>
            <div style='flex:1;'>
                <div style='font-size:15px; color:#c7d2fe; font-weight:800;'>Risk Level Score</div>
                <div style='font-size:28px; color:white; font-weight:900;'>{risk_score}/100 • {risk_level}</div>
                <div style='color:#dbeafe; margin-top:8px;'>This score considers debt, net worth and monthly flow. A higher score means more financial stress.</div>
            </div>
            <div style='width:180px; text-align:center;'>
                <div style='background:rgba(255,255,255,0.08); padding:10px; border-radius:8px;'>
                    <div style='font-size:13px; color:#c7d2fe;'>Quick Advice</div>
                    <div style='color:white; font-weight:700; margin-top:6px;'>
                        { 'Focus on saving & debt paydown' if risk_score>=50 else 'Keep up the good work' }
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- PAGE: VISUALS ----------------
elif st.session_state["page"] == "visuals":

    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    st.markdown("<h2 class='neon-title' style='text-align:center;'>Advanced Financial Visuals</h2>", unsafe_allow_html=True)
    # removed empty decorative top bar per your request (Option A)
    st.markdown("<p style='text-align:center; margin-top:-10px;'>Breakdowns | Trend | Goal </p>", unsafe_allow_html=True)

    # ---------- DATA PREP ----------
    categories = ["Food", "Transport", "Bills", "Shopping", "Other"]
    # ensure spending distribution is meaningful even when monthly_expenses == 0
    if monthly_expenses <= 0:
        spending = [0, 0, 0, 0, 0]
    else:
        spending = [
            monthly_expenses * 0.25,
            monthly_expenses * 0.15,
            monthly_expenses * 0.30,
            monthly_expenses * 0.20,
            monthly_expenses * 0.10,
        ]
    df = pd.DataFrame({"Category": categories, "Amount": spending})

    # Monthly trend (use deterministic fallback when monthly values are zero)
    trend_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    if monthly_income == 0:
        incomes = np.zeros(6, dtype=int)
    else:
        incomes = np.random.randint(int(monthly_income*0.8), int(monthly_income*1.1)+1, 6)
    if monthly_expenses == 0:
        expenses_arr = np.zeros(6, dtype=int)
    else:
        expenses_arr = np.random.randint(int(monthly_expenses*0.9), int(monthly_expenses*1.2)+1, 6)

    df_trend = pd.DataFrame({
        "Month": trend_months,
        "Income": incomes,
        "Expenses": expenses_arr
    })

    # Heatmap Data
    heatmap_data = np.random.randint(2000, 9000, (6, 5))

    # ---------- ROW: Top Info Boxes (Income & Expenses) ----------
    top1, top2, top3 = st.columns([1,1,2])
    top1.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); padding:18px; border-radius:12px; text-align:center; border:1px solid rgba(255,255,255,0.08);">
            <div style='color:#c7d2fe; font-size:14px; font-weight:800;'>Income</div>
            <div style='color:white; font-size:26px; font-weight:900;'>Rs {monthly_income:,}</div>
            <div style='color:#dbeafe; font-size:12px; margin-top:6px;'>Monthly</div>
        </div>
    """, unsafe_allow_html=True)

    top2.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); padding:18px; border-radius:12px; text-align:center; border:1px solid rgba(255,255,255,0.08);">
            <div style='color:#c7d2fe; font-size:14px; font-weight:800;'>Expenses</div>
            <div style='color:white; font-size:26px; font-weight:900;'>Rs {monthly_expenses:,}</div>
            <div style='color:#dbeafe; font-size:12px; margin-top:6px;'>Monthly</div>
        </div>
    """, unsafe_allow_html=True)

    top3.markdown(f"""
        <div style="background:rgba(255,255,255,0.04); padding:18px; border-radius:12px; text-align:left; border:1px solid rgba(255,255,255,0.06);">
            <div style='color:#c7d2fe; font-size:14px; font-weight:800;'>Note</div>
            <div style='color:white; font-size:13px; margin-top:6px;'>These cards reflect current monthly totals — enter values in the sidebar to update charts below.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- ROW 1: Pie Chart (Animated) - title INSIDE card ----------
    fig_pie = px.pie(df, names="Category", values="Amount",
                     color_discrete_sequence=px.colors.sequential.Purples)
    # show label + percent clearly and ensure texts are white
    fig_pie.update_traces(textinfo="label+percent", pull=0.08, textposition="outside")
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend=dict(orientation="h", y=-0.15)
    )

    st.markdown("<div class='neon-card fade'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; align-items:center; margin-bottom:6px;'><div style=""" + "'font-size:18px; font-weight:800; color:#c7d2fe; margin-right:10px;'" + "">💠</div><div style='font-size:20px; font-weight:800; color:white;'>Spending Breakdown</div></div>", unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div><br>", unsafe_allow_html=True)

    # ---------- ROW 2: Line Chart (Animated Smooth Curve) & Gauge (titles INSIDE cards) ----------
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["Income"],
        mode="lines+markers+text",
        name="Income",
        text=[f"Rs {int(v):,}" for v in df_trend["Income"]],
        textposition="top center",
        line=dict(color="#10b981", width=4),
    ))
    fig_line.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["Expenses"],
        mode="lines+markers+text",
        name="Expenses",
        text=[f"Rs {int(v):,}" for v in df_trend["Expenses"]],
        textposition="bottom center",
        line=dict(color="#ef4444", width=4),
    ))
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        font_color="white",
        xaxis_title=None,
        yaxis_title="Amount (PKR)",
        yaxis=dict(color="white"),
        xaxis=dict(color="white")
    )

    a, b = st.columns(2)

    with a:
        st.markdown("<div class='neon-card fade'>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex; align-items:center; margin-bottom:6px;'><div style=""" + "'font-size:18px; font-weight:800; color:#c7d2fe; margin-right:10px;'" + "">📈</div><div style='font-size:20px; font-weight:800; color:white;'>Monthly Trend</div></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- ROW 2 (Right): Circular Gauge (title inside card) ----------
    goal_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=goal_progress,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#8b5cf6"},
            "bgcolor": "rgba(255,255,255,0.07)",
            "borderwidth": 2,
            "bordercolor": "white",
        },
        number={'suffix': "%"},
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    goal_figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")

    with b:
        st.markdown("<div class='neon-card fade'>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex; align-items:center; margin-bottom:6px;'><div style=""" + "'font-size:18px; font-weight:800; color:#c7d2fe; margin-right:10px;'" + "">🎯</div><div style='font-size:20px; font-weight:800; color:white;'>Goal Completion</div></div>", unsafe_allow_html=True)
        st.plotly_chart(goal_figure, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- PDF Export for Visuals: improved layout ----------
    def create_quick_visuals_pdf():
        # A short PDF capturing main visuals summary (improved formatting)
        W, H = 1240, 1754
        margin = 60
        img = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(img)
        try:
            header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            mono_font = ImageFont.truetype("DejaVuSans.ttf", 18)
        except Exception:
            header_font = ImageFont.load_default()
            mono_font = ImageFont.load_default()

        y = margin
        draw.text((margin, y), "Visuals Snapshot — Financial Report", fill="black", font=header_font)
        y += 56
        draw.text((margin, y), f"Income: Rs {monthly_income:,} • Expenses: Rs {monthly_expenses:,}", fill="black", font=mono_font)
        y += 30
        draw.text((margin, y), f"Top categories (Amounts):", fill="black", font=mono_font)
        y += 26
        for idx, row in df.iterrows():
            draw.text((margin+18, y), f"{row['Category']}: Rs {int(row['Amount']):,}", fill="black", font=mono_font)
            y += 22

        # Add small risk line
        y += 8
        draw.text((margin, y), f"Risk Score: {risk_score}/100 • {risk_level}", fill="black", font=mono_font)

        buf = BytesIO()
        img.save(buf, format="PDF", resolution=100.0)
        buf.seek(0)
        return buf

    if st.button("Export Quick Visuals PDF"):
        try:
            buf = create_quick_visuals_pdf()
            st.success("Visuals PDF ready.")
            st.download_button("Download Visuals Snapshot (PDF)", data=buf, file_name="visuals_snapshot.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"PDF export failed: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

# ========================= END =========================
