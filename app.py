# app.py — Final updated by ChatGPT for Hanan
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import math
import pandas as pd

st.set_page_config(page_title="Apka Financial Advisor — Smart", page_icon="💸", layout="wide")

# ===========================
# CSS / Styling
# ===========================
st.markdown(
    """
    <style>
    /* App background & fonts */
    .stApp {
        background: linear-gradient(180deg,#041026 0%, #07122a 100%);
        color: #e6eef8;
        font-family: "Segoe UI", Roboto, sans-serif;
    }

    /* Sidebar (attempt multiple selectors for compatibility) */
    .css-1d391kg, .sidebar .sidebar-content, .stSidebar {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-right: 1px solid rgba(255,255,255,0.03);
        padding: 16px;
        border-radius: 12px;
    }

    /* Header bar */
    .top-header {
      padding:10px 14px; border-radius:10px;
      background: linear-gradient(90deg,#071932,#0b1f36);
      margin-bottom:12px;
    }
    .app-title { font-weight:900; font-size:20px; background: linear-gradient(90deg,#7c3aed,#06b6d4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }

    /* Stat card */
    .stat-card {
      background: rgba(255,255,255,0.02);
      border-radius:12px; padding:14px; text-align:center;
      border: 1px solid rgba(255,255,255,0.03);
      box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }
    .stat-label { color: rgba(230,238,248,0.7); font-size:13px; }
    .stat-value { font-weight:800; font-size:20px; margin-top:6px; }

    /* Goal card */
    .goal-wrap {
      background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      padding:14px; border-radius:12px; border:1px solid rgba(255,255,255,0.03);
    }
    .goal-bar { height:22px; background: rgba(255,255,255,0.03); border-radius:12px; overflow:hidden; }
    .goal-fill { height:100%; background: linear-gradient(90deg,#06b6d4,#7c3aed); transition: width 0.9s; box-shadow: 0 8px 30px rgba(6,182,212,0.08); }

    /* Buttons */
    .glow-btn {
      background: linear-gradient(90deg,#7c3aed,#06b6d4);
      color: white; padding:10px 16px; border-radius:12px; border:none; font-weight:800;
      box-shadow: 0 8px 30px rgba(124,58,237,0.12); cursor:pointer; transition: transform .15s ease, box-shadow .15s ease;
    }
    .glow-btn:hover { transform: translateY(-4px); box-shadow: 0 18px 50px rgba(124,58,237,0.20); }

    .primary-action {
      background: linear-gradient(90deg,#ff7a18,#ffb347);
      box-shadow: 0 10px 40px rgba(255,122,24,0.14);
    }
    .primary-action:hover { box-shadow: 0 20px 70px rgba(255,122,24,0.24); }

    .pdf-btn {
      background: linear-gradient(90deg,#16a34a,#22c55e);
      color:white; padding:10px 16px; border-radius:12px; border:none; font-weight:800;
      box-shadow: 0 8px 30px rgba(34,197,94,0.12);
    }
    .pdf-btn:hover { transform: translateY(-3px); box-shadow: 0 18px 50px rgba(34,197,94,0.24); }

    /* Insight row cards */
    .insight-tile {
      padding:12px; border-radius:10px; margin:6px 6px; background: rgba(255,255,255,0.02); display:flex; align-items:center;
      border: 1px solid rgba(255,255,255,0.03);
      min-height:64px;
    }
    .insight-icon { font-size:20px; width:36px; text-align:center; margin-right:10px; }
    .insight-title { font-weight:700; font-size:14px; }
    .insight-sub { color: rgba(230,238,248,0.7); font-size:13px; margin-top:4px; }

    .insight-warn { border-left:4px solid #fb7185; }
    .insight-good { border-left:4px solid #10b981; }

    .muted { color: rgba(230,238,248,0.65); font-size:13px; }

    @media (max-width:900px) {
      .insight-tile { margin:6px 0; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===========================
# Sidebar: Inputs (USER WANTED ORDER)
# ===========================
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:6px'>Apki Financial Inputs</h2>", unsafe_allow_html=True)

    # 1) Keep monthly income section first
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=1500, step=500, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")

    st.markdown("---")

    # Goal portion at LAST in sidebar (no "amount saved for goal" input)
    goal_name = st.text_input("Goal Name", value="Birthday Present")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=0, value=4000, step=500, format="%d")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Single Analyze / Predict button at end of sidebar (glow, primary)
    if st.button("🔍 Analyze / Predict", key="sidebar_analyze"):
        # store analysis trigger
        st.session_state['analysis_run'] = True
        st.success("Analysis updated ✔")
    else:
        # keep a flag default false if not set
        if 'analysis_run' not in st.session_state:
            st.session_state['analysis_run'] = False

    st.markdown("<div class='muted' style='margin-top:8px'>Click Analyze after changing inputs to refresh suggested actions & metrics.</div>", unsafe_allow_html=True)

# ===========================
# Calculations & Helpers
# ===========================
def safe_div(a, b):
    try:
        return a / b
    except Exception:
        return 0

total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_possible_save = max(0, monthly_income - monthly_expenses)

# Goal progress uses current_savings (user requested)
goal_progress_pct = 0.0
if goal_amount > 0:
    goal_progress_pct = min(100.0, (current_savings / goal_amount) * 100.0)

# Months to goal estimate (if saving all monthly_possible_save to goal)
months_to_goal = math.inf
if monthly_possible_save > 0:
    months_to_goal = round(max(0.0, (goal_amount - current_savings) / monthly_possible_save), 1)

# Emergency fund constants (fixed): 3 months min, 6 months ideal
EMERGENCY_MIN = 3
EMERGENCY_IDEAL = 6
emergency_coverage_months = round(safe_div(current_savings, max(1, monthly_expenses)), 1)
emergency_min_amount = monthly_expenses * EMERGENCY_MIN
emergency_ideal_amount = monthly_expenses * EMERGENCY_IDEAL
emergency_gap_min = max(0, emergency_min_amount - current_savings)
emergency_gap_ideal = max(0, emergency_ideal_amount - current_savings)

# Spending categories (derived)
cat_props = {"Food": 0.30, "Transport": 0.10, "Shopping": 0.20, "Bills": 0.25, "Fun": 0.15}
cat_values = {k: round(monthly_expenses * p) for k, p in cat_props.items()}

# Simple analyze function (called when 'Analyze' clicked)
def run_analysis():
    # generate short suggestions and key metrics
    out = {}
    out['monthly_possible_save'] = monthly_possible_save
    out['goal_progress_pct'] = goal_progress_pct
    out['months_to_goal'] = None if months_to_goal == math.inf else months_to_goal
    out['emergency_coverage_months'] = emergency_coverage_months
    out['emergency_gap_min'] = emergency_gap_min
    out['emergency_gap_ideal'] = emergency_gap_ideal

    # quick actionable suggestions (short)
    tiles = []
    # Emergency tile
    if emergency_coverage_months < EMERGENCY_MIN:
        tiles.append({
            "icon": "⚠",
            "title": f"Emergency: Low",
            "sub": f"{emergency_coverage_months} mo — need Rs {emergency_gap_min:,} to reach {EMERGENCY_MIN}m"
        })
    elif EMERGENCY_MIN <= emergency_coverage_months < EMERGENCY_IDEAL:
        tiles.append({
            "icon": "✅",
            "title": f"Emergency: OK",
            "sub": f"{emergency_coverage_months} mo — aim for {EMERGENCY_IDEAL}m (Rs {emergency_ideal_amount:,})"
        })
    else:
        tiles.append({
            "icon": "🌟",
            "title": f"Emergency: Strong",
            "sub": f"{emergency_coverage_months} mo — consider investing excess"
        })

    # Savings tile
    if monthly_possible_save <= 0:
        tiles.append({"icon": "🛑", "title": "Saving: Negative", "sub": "Expenses ≥ income — reduce non-essential spending"})
    elif monthly_possible_save < 0.2 * monthly_income:
        tiles.append({"icon": "💡", "title": "Saving: Low", "sub": f"Save Rs {monthly_possible_save:,}/mo — aim to increase to 20% of income"})
    else:
        tiles.append({"icon": "🚀", "title": "Saving: Good", "sub": f"Save Rs {monthly_possible_save:,}/mo — split: 50% invest, 30% emergency, 20% goals"})

    # Goal tile
    if goal_progress_pct < 30:
        tiles.append({"icon": "📌", "title": "Goal: Behind", "sub": f"{goal_progress_pct:.0f}% — consider small auto-transfer"})
    else:
        tiles.append({"icon": "🎯", "title": "Goal: On Track", "sub": f"{goal_progress_pct:.0f}% complete"})

    # Debt tile
    if total_debt > 0:
        tiles.append({"icon": "📉", "title": "Debt", "sub": f"Outstanding: Rs {total_debt:,}"})
    else:
        tiles.append({"icon": "🧾", "title": "Debt", "sub": "No debt"})

    out['tiles'] = tiles
    return out

# Run analysis if user pressed Analyze earlier (flag set in sidebar)
if st.session_state.get('analysis_run', False):
    analysis = run_analysis()
else:
    analysis = None

# ===========================
# Header + simple nav
# ===========================
st.markdown(f"""
    <div class="top-header">
      <span class="app-title">Apka Financial Advisor — Smart</span>
      <span style="float:right; color:rgba(230,238,248,0.7); font-size:13px;">{datetime.now().strftime('%d %b %Y')}</span>
    </div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1,1,1], gap="large")
with nav1:
    if st.button("🏠 Overview"):
        st.session_state['page'] = 'landing'
with nav2:
    if st.button("🤖 AI Insights"):
        st.session_state['page'] = 'insights'
with nav3:
    if st.button("📈 Visuals"):
        st.session_state['page'] = 'visuals'
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'

# ===========================
# PAGE: Overview / Landing
# ===========================
if st.session_state.get('page') == 'landing':
    st.markdown("<h3>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
    # top metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        ("Total (Income + Savings)", total_balance),
        ("Income", monthly_income),
        ("Expenses", monthly_expenses),
        ("Savings", current_savings),
        ("Net Worth", net_worth),
    ]
    for col, (label, val) in zip([c1, c2, c3, c4, c5], metrics):
        with col:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>Rs {val:,.0f}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    # Goal progress (modified, no analyze button)
    left, right = st.columns([2,1], gap="large")
    with left:
        st.markdown("<h4>Goal Progress</h4>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="goal-wrap">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="width:68%;">
                  <div style="margin-bottom:8px;"><strong>{goal_name}</strong> — Target Rs {goal_amount:,.0f}</div>
                  <div class="goal-bar"><div class="goal-fill" style="width:{goal_progress_pct:.1f}%;"></div></div>
                  <div class="muted" style="margin-top:8px;">{goal_progress_pct:.1f}% complete • Rs {current_savings:,.0f} saved (savings used for goal)</div>
                </div>
                <div style="width:28%; text-align:center;">
                  <div style="font-size:13px; color:rgba(230,238,248,0.7)"><strong>ETA</strong></div>
                  <div style="font-size:20px; font-weight:800; margin-top:6px;">{months_to_goal if months_to_goal != math.inf else 'N/A'} mo</div>
                  <div class="muted" style="margin-top:6px;">(if monthly savings allocated)</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    with right:
        # show compact quick cards (if analysis run show analysis tiles else show computed quick metrics)
        st.markdown("<h4>Quick Insights</h4>", unsafe_allow_html=True)
        if analysis:
            tiles = analysis['tiles']
        else:
            # compute small set based on live numbers
            tiles = []
            # emergency quick
            if emergency_coverage_months < EMERGENCY_MIN:
                tiles.append({"icon":"⚠", "title":"Emergency: Low", "sub":f"{emergency_coverage_months} mo"})
            else:
                tiles.append({"icon":"✅", "title":"Emergency", "sub":f"{emergency_coverage_months} mo"})
            # saving quick
            if monthly_possible_save <= 0:
                tiles.append({"icon":"🛑","title":"Saving", "sub":"No positive savings"})
            else:
                tiles.append({"icon":"💰","title":"Saving", "sub":f"Rs {monthly_possible_save:,}/mo"})
            # debt quick
            if total_debt > 0:
                tiles.append({"icon":"📉","title":"Debt", "sub":f"Rs {total_debt:,}"})
            else:
                tiles.append({"icon":"🧾","title":"Debt", "sub":"No debt"})

        # render tiles row-wise (two columns)
        cols_count = 2
        rows = [tiles[i:i+cols_count] for i in range(0, len(tiles), cols_count)]
        for row in rows:
            cols = st.columns(len(row))
            for col, tile in zip(cols, row):
                with col:
                    extra_class = ""
                    if "Low" in tile['title'] or "Negative" in tile.get('sub',''):
                        extra_class = "insight-warn"
                    elif "Good" in tile.get('title','') or "✅" in tile.get('icon',''):
                        extra_class = "insight-good"
                    st.markdown(
                        f"""
                        <div class="insight-tile {extra_class}">
                          <div class="insight-icon">{tile['icon']}</div>
                          <div>
                            <div class="insight-title">{tile['title']}</div>
                            <div class="insight-sub">{tile['sub']}</div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='muted'>Tip: update values in sidebar and press Analyze once to refresh suggestions above.</div>", unsafe_allow_html=True)

# ===========================
# PAGE: AI Insights (Emergency focus)
# ===========================
elif st.session_state.get('page') == 'insights':
    st.header("AI Smart Insights — Emergency & Actions")

    # Emergency fund card (constant recommendation, not user input)
    if emergency_coverage_months < EMERGENCY_MIN:
        cls = "insight-tile insight-warn"
        status = f"You have {emergency_coverage_months} months. Minimum needed: Rs {emergency_min_amount:,.0f} (3 months)."
        action = f"Need Rs {emergency_gap_min:,.0f} more. Try saving Rs {max(1, round(emergency_gap_min / max(1, monthly_possible_save)))} months at current savings rate."
    elif EMERGENCY_MIN <= emergency_coverage_months < EMERGENCY_IDEAL:
        cls = "insight-tile insight-good"
        status = f"{emergency_coverage_months} months covered. Ideal: {EMERGENCY_IDEAL} months (Rs {emergency_ideal_amount:,.0f})."
        action = f"Gap to ideal: Rs {emergency_gap_ideal:,.0f}."
    else:
        cls = "insight-tile"
        status = f"{emergency_coverage_months} months covered — strong position."
        action = "Consider investing surplus conservatively."

    st.markdown(f"<div class='{cls}'><div class='insight-icon'>🚨</div><div><div class='insight-title'>Emergency Fund</div><div class='insight-sub'>{status}</div><div class='insight-sub' style='margin-top:6px'>{action}</div></div></div>", unsafe_allow_html=True)

    st.markdown("---")
    # Short action tiles row (use analysis if available)
    st.markdown("<h4>Actions</h4>", unsafe_allow_html=True)
    if analysis:
        tiles = analysis['tiles']
    else:
        # fallback small set:
        tiles = [
            {"icon":"💡","title":"Increase Savings","sub":"Automate Rs 10% transfer to emergency"},
            {"icon":"📈","title":"Invest Small","sub":"Start SIP once emergency >=3m"},
            {"icon":"🧾","title":"Debt Plan","sub":"Prioritize high-interest loans"}
        ]
    cols = st.columns(len(tiles))
    for col, tile in zip(cols, tiles):
        with col:
            st.markdown(f"<div class='insight-tile'><div class='insight-icon'>{tile['icon']}</div><div><div class='insight-title'>{tile['title']}</div><div class='insight-sub'>{tile['sub']}</div></div></div>", unsafe_allow_html=True)

    st.markdown("---")
    # Quick summary stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>Emergency Coverage</div><div class='stat-value'>{emergency_coverage_months} mo</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>Suggested Min</div><div class='stat-value'>Rs {emergency_min_amount:,.0f}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>Suggested Ideal</div><div class='stat-value'>Rs {emergency_ideal_amount:,.0f}</div></div>", unsafe_allow_html=True)

# ===========================
# PAGE: Visuals (no input controls here)
# ===========================
elif st.session_state.get('page') == 'visuals':
    st.header("Visuals — Trends & Spending")

    # Construct a 12-month sample series based on current inputs
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    df = pd.DataFrame({
        "month": months,
        "income": [monthly_income for _ in months],
        "expenses": [monthly_expenses for _ in months],
    })
    df['savings'] = df['income'] - df['expenses']

    # Income vs Expense bar
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['month'], y=df['income'], name="Income", marker_color="#06b6d4"))
    fig.add_trace(go.Bar(x=df['month'], y=df['expenses'], name="Expenses", marker_color="#fb7185"))
    fig.update_layout(template="plotly_dark", barmode='group', title="Income vs Expenses (12 months)", yaxis_title="PKR")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    # Savings trend line
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['month'], y=df['savings'], mode="lines+markers", name="Savings"))
    fig2.update_layout(template="plotly_dark", title="Savings Trend (12 months)", yaxis_title="PKR")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    # Spending pie
    st.subheader("Spending by Category (estimated)")
    fig_pie = px.pie(values=list(cat_values.values()), names=list(cat_values.keys()), hole=0.4, title="Spending Breakdown")
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# ===========================
# PDF Generation: build bytes & download button (fixed)
# ===========================
def build_pdf_bytes():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Apka Financial Advisor — Report", ln=1, align="C")
    pdf.ln(4)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y')}", ln=1)
    pdf.ln(4)

    # Summary
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "1) Quick Summary", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Monthly Income: Rs {monthly_income:,.0f}\n"
                   f"Monthly Expenses: Rs {monthly_expenses:,.0f}\n"
                   f"Current Savings: Rs {current_savings:,.0f}\n"
                   f"Net Worth: Rs {net_worth:,.0f}\n")
    pdf.ln(3)

    # Goal
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "2) Goal", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"Goal: {goal_name}\nTarget: Rs {goal_amount:,.0f}\nProgress (based on current savings): {goal_progress_pct:.1f}%\nEstimated months to target (if all monthly savings applied): {months_to_goal if months_to_goal != math.inf else 'N/A'}\n")
    pdf.ln(3)

    # Emergency
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "3) Emergency Fund", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Current coverage: ~{emergency_coverage_months} months of expenses.\n"
                   f"Recommended minimum: {EMERGENCY_MIN} months (Rs {emergency_min_amount:,.0f}).\n"
                   f"Recommended ideal: {EMERGENCY_IDEAL} months (Rs {emergency_ideal_amount:,.0f}).\n"
                   f"Gap to minimum: Rs {emergency_gap_min:,.0f}\n")
    pdf.ln(3)

    # Suggestions (short)
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "4) Suggestions (short)", ln=1)
    pdf.set_font("Arial", "", 10)
    # use analysis if available else create minimal suggestions
    if analysis:
        tiles = analysis['tiles']
        for t in tiles:
            pdf.multi_cell(0, 6, f"• {t['title']}: {t['sub']}")
    else:
        pdf.multi_cell(0, 6, "• Build emergency to 3–6 months. • Increase monthly savings. • Prioritize high-interest debt.")
    pdf.ln(4)

    # Spending breakdown
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "5) Spending Breakdown (estimated)", ln=1)
    pdf.set_font("Arial", "", 10)
    for k, v in cat_values.items():
        pdf.multi_cell(0, 6, f"{k}: Rs {v:,}")
    pdf.ln(6)

    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 5, "This report is informational. For large decisions, consult a certified financial advisor.")

    # get bytes reliably
    pdf_str = pdf.output(dest='S')
    if isinstance(pdf_str, str):
        pdf_bytes = pdf_str.encode('latin-1')
    else:
        pdf_bytes = pdf_str
    return pdf_bytes

# PDF download UI (bottom, across pages)
st.markdown("---")
pdf_bytes = build_pdf_bytes()
st.download_button(
    label="📄 Download Detailed PDF Report",
    data=pdf_bytes,
    file_name=f"Apka_Financial_Report_{datetime.now().strftime('%d%m%Y')}.pdf",
    mime="application/pdf",
    key="download_pdf"
)
st.markdown("<div class='muted' style='margin-top:8px'>Report contains summary, goal, emergency info & short suggestions.</div>", unsafe_allow_html=True)
