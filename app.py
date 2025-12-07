import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import math
import pandas as pd
import os

st.set_page_config(page_title="Apka Financial Advisor — Smart", page_icon="💸", layout="wide")

st.markdown("""
<style>

/* ---------- GLOBAL APP ---------- */
.stApp {
    background: linear-gradient(180deg,#224B7D 0%, #6C9E7F 100%);
    color: #F7FAFC !important;
    font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
}

/* ---------- HEADERS ---------- */
h1, h2, h3, h4, h5 {
    color: #FFFFFF !important;
    font-weight: 800;
    text-shadow: 0px 0px 6px rgba(0,0,0,0.35);
}

.app-title {
    font-weight:900;
    font-size:22px;
    letter-spacing:0.5px;
    color:#FFFFFF !important;
}

/* ---------- MAIN TEXT ---------- */
p, div, span, label {
    color:#F1F5F9 !important;  
}

.muted {
    color: rgba(255,255,255,0.82) !important;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    background: linear-gradient(90deg,#38bdf8,#818cf8) !important;
    color:white !important;
    font-weight:700 !important;
    border-radius:10px;
    padding:8px 14px;
    border:none;
    box-shadow:0 4px 18px rgba(0,0,0,0.35);
}

.stButton > button:hover {
    transform:scale(1.03);
    box-shadow:0 8px 28px rgba(0,0,0,0.45);
}

/* ---------- CARDS ---------- */
.stat-card {
    background: rgba(255,255,255,0.08);
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.18);
    padding:14px;
}

.stat-label {
    font-size:14px;
    color:#E2E8F0 !important;
}

.stat-value {
    font-size:22px;
    font-weight:800;
    color:#FFFFFF !important;
}

/* ---------- GOAL BAR ---------- */
.goal-wrap {
    background: rgba(255,255,255,0.1);
    border-radius:12px;
    padding:12px;
    border:1px solid rgba(255,255,255,0.2);
}

.goal-bar {
    height:20px;
    background: rgba(255,255,255,0.15);
    border-radius:12px;
}

.goal-fill {
    background: linear-gradient(90deg,#06b6d4,#7c3aed);
}

/* ---------- TILES ---------- */
.tile {
    padding:12px;
    border-radius:10px;
    background: rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.22);
}

.tile-title {
    font-size:15px;
    font-weight:800;
    color:white !important;
}

.tile-sub {
    font-size:13px;
    color:#E2E8F0 !important;
}

.tile-warn {
    border-left:4px solid #fb7185;
}

.tile-good {
    border-left:4px solid #10b981;
}

/* ---------- SIDEBAR TEXT ONLY (no layout change) ---------- */
.stSidebar, .css-1d391kg, .sidebar-content {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255, 255, 255, 0.15);
}

label, .stNumberInput label {
    color:black !important;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------
# Sidebar: EXACT order requested (no change) — inputs then goal at bottom
# ------------------------------
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:6px'>Apki Financial Inputs</h2>", unsafe_allow_html=True)

    # Input section (kept first)
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=1500, step=500, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    # Goal at bottom of sidebar (no "amount saved for goal")
    goal_name = st.text_input("Goal Name", value="Birthday Present")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=0, value=4000, step=500, format="%d")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Single Analyze / Predict button (glow + contrasting)
    if st.button("🔍 Analyze / Predict", key="sidebar_analyze"):
        st.session_state['analysis_run'] = True
        st.success("Analysis updated ✔")
    else:
        if 'analysis_run' not in st.session_state:
            st.session_state['analysis_run'] = False

    st.markdown("<div class='muted' style='margin-top:8px'>Click Analyze after changing inputs to refresh suggestions & metrics.</div>", unsafe_allow_html=True)

# ------------------------------
# Core calculations & helpers
# ------------------------------
def safe_div(a, b):
    try:
        return a / b
    except Exception:
        return 0

total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_possible_save = max(0, monthly_income - monthly_expenses)

# Goal progress (user requested to use current_savings)
goal_progress_pct = 0.0
if goal_amount > 0:
    goal_progress_pct = min(100.0, (current_savings / goal_amount) * 100.0)

months_to_goal = math.inf
if monthly_possible_save > 0:
    months_to_goal = round(max(0.0, (goal_amount - current_savings) / monthly_possible_save), 1)

# Emergency constants (fixed)
EMERGENCY_MIN = 3
EMERGENCY_IDEAL = 6
emergency_coverage_months = round(safe_div(current_savings, max(1, monthly_expenses)), 1)
emergency_min_amount = monthly_expenses * EMERGENCY_MIN
emergency_ideal_amount = monthly_expenses * EMERGENCY_IDEAL
emergency_gap_min = max(0, emergency_min_amount - current_savings)
emergency_gap_ideal = max(0, emergency_ideal_amount - current_savings)

# Spending categories
cat_props = {"Food": 0.30, "Transport": 0.10, "Shopping": 0.20, "Bills": 0.25, "Fun": 0.15}
cat_values = {k: round(monthly_expenses * p) for k, p in cat_props.items()}

# Analysis generator (short tiles)
def generate_tiles():
    tiles = []
    # Emergency
    if emergency_coverage_months < EMERGENCY_MIN:
        tiles.append({"icon":"⚠","title":"Emergency: Low","sub":f"{emergency_coverage_months} mo — need Rs {emergency_gap_min:,} to reach {EMERGENCY_MIN}m"})
    elif EMERGENCY_MIN <= emergency_coverage_months < EMERGENCY_IDEAL:
        tiles.append({"icon":"✅","title":"Emergency: OK","sub":f"{emergency_coverage_months} mo — aim for {EMERGENCY_IDEAL}m (Rs {emergency_ideal_amount:,})"})
    else:
        tiles.append({"icon":"🌟","title":"Emergency: Strong","sub":f"{emergency_coverage_months} mo — you are covered"})

    # Savings
    if monthly_possible_save <= 0:
        tiles.append({"icon":"🛑","title":"Saving: Negative","sub":"Expenses ≥ income — reduce spending"})
    elif monthly_possible_save < 0.2 * monthly_income:
        tiles.append({"icon":"💡","title":"Saving: Low","sub":f"Save Rs {monthly_possible_save:,}/mo — aim 20% of income"})
    else:
        tiles.append({"icon":"🚀","title":"Saving: Good","sub":f"Save Rs {monthly_possible_save:,}/mo"})

    # Goal short tile
    if goal_progress_pct < 50:
        tiles.append({"icon":"📌","title":"Goal: Behind","sub":f"{goal_progress_pct:.0f}% complete"})
    elif 50 <= goal_progress_pct < 90:
        tiles.append({"icon":"🎯","title":"Goal: Progressing","sub":f"{goal_progress_pct:.0f}% complete"})
    else:
        tiles.append({"icon":"🏁","title":"Goal: Almost Done","sub":f"{goal_progress_pct:.0f}% complete"})

    # Debt
    if total_debt > 0:
        tiles.append({"icon":"📉","title":"Debt","sub":f"Outstanding: Rs {total_debt:,}"})
    else:
        tiles.append({"icon":"🧾","title":"Debt","sub":"No debt"})

    return tiles

# When analysis requested, create updated tiles
analysis_tiles = generate_tiles() if st.session_state.get('analysis_run', False) else None

# ------------------------------
# Header + nav
# ------------------------------
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

# ------------------------------
# PAGE: Landing / Overview
# ------------------------------
if st.session_state.get('page') == 'landing':
    st.markdown("<h3>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

    # Top metric cards
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
    # Goal progress + condition-based suggestions (two short suggestions per state)
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
                  <div class="muted" style="margin-top:8px;">{goal_progress_pct:.1f}% complete • Rs {current_savings:,.0f} used for goal</div>
                </div>
                <div style="width:28%; text-align:center;">
                  <div style="font-size:13px; color:rgba(230,238,248,0.7)"><strong>ETA</strong></div>
                  <div style="font-size:20px; font-weight:800; margin-top:6px;">{months_to_goal if months_to_goal != math.inf else 'N/A'} mo</div>
                  <div class="muted" style="margin-top:6px;">(if monthly savings allocated)</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Condition-based 2 suggestions (short, stylish)
        st.markdown("<h4 style='margin-bottom:6px'>Recommended Actions</h4>", unsafe_allow_html=True)
        suggestions = []
        if goal_progress_pct < 50:
            # compute numbers for suggestion
            # Suggest 1: increase monthly allocation by 20% of monthly_possible_save if possible
            suggested_extra = 0
            if monthly_possible_save > 0:
                suggested_extra = round(monthly_possible_save * 0.2)
            suggestions = [
                {"icon":"💡", "title":"Increase Monthly Allocation", "sub": f"Add ~Rs {suggested_extra:,}/mo to goal"},
                {"icon":"✂️", "title":"Cut Discretionary Spend", "sub": f"Reduce non-essential spend by ~Rs {max(5000, round(monthly_expenses*0.05)):,}/mo"}
            ]
        elif 50 <= goal_progress_pct < 90:
            suggested_extra = 0
            if monthly_possible_save > 0:
                suggested_extra = round(monthly_possible_save * 0.1)
            suggestions = [
                {"icon":"⚡", "title":"Boost Pace Slightly", "sub": f"Add ~Rs {suggested_extra:,}/mo to finish earlier"},
                {"icon":"🔁", "title":"Automate Transfers", "sub": "Set a fixed monthly transfer to your goal"}
            ]
        else:
            suggestions = [
                {"icon":"🎉", "title":"Almost There", "sub": "Great job — keep momentum"},
                {"icon":"📆", "title":"Plan Next", "sub": "Consider your next financial goal"}
            ]

        # Render two suggestion tiles side-by-side
        cols = st.columns(2)
        for col, s in zip(cols, suggestions):
            with col:
                extra = ""
                if "Increase" in s['title'] or "Cut" in s['title']:
                    extra = "tile-warn"
                elif "Almost" in s['title'] or "Boost" in s['title'] or "Automate" in s['title']:
                    extra = "tile-good"
                st.markdown(f"""
                    <div class="tile {extra}">
                      <div class="tile-icon">{s['icon']}</div>
                      <div>
                        <div class="tile-title">{s['title']}</div>
                        <div class="tile-sub">{s['sub']}</div>
                      </div>
                    </div>
                """, unsafe_allow_html=True)

    with right:
        # Compact quick insights (row-wise) — fewer words
        st.markdown("<h4>Quick Insights</h4>", unsafe_allow_html=True)
        # Use analysis_tiles if user ran analyze, else live compute
        quick = analysis_tiles if analysis_tiles is not None else generate_tiles()
        # Show in rows of 2
        rows = [quick[i:i+2] for i in range(0, len(quick), 2)]
        for row in rows:
            cols = st.columns(len(row))
            for col, t in zip(cols, row):
                with col:
                    cls = ""
                    if "Low" in t['title'] or "Negative" in t['title']:
                        cls = "tile-warn"
                    elif "Good" in t['title'] or "OK" in t['title'] or "Strong" in t['title']:
                        cls = "tile-good"
                    st.markdown(f"""
                        <div class="tile {cls}">
                          <div class="tile-icon">{t['icon']}</div>
                          <div>
                            <div class="tile-title">{t['title']}</div>
                            <div class="tile-sub">{t['sub']}</div>
                          </div>
                        </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='muted'>Tip: Click Analyze in sidebar after changing inputs to update recommendations.</div>", unsafe_allow_html=True)

# ------------------------------
# PAGE: AI Insights (Emergency Fund visuals)
# ------------------------------
elif st.session_state.get('page') == 'insights':
    st.header("AI Insights — Emergency Fund")

    # Visual bars comparing current savings to min & ideal
    st.markdown("<h4>Emergency Fund Visual</h4>", unsafe_allow_html=True)
    # Create a small DataFrame for plotting
    df_em = pd.DataFrame({
        "Category": ["You (current savings)", "Minimum (3 mo)", "Ideal (6 mo)"],
        "Amount": [current_savings, emergency_min_amount, emergency_ideal_amount]
    })

    # Bar chart (horizontal) for clear comparison
    fig_em = go.Figure()
    colors = ["#06b6d4", "#fb7185", "#10b981"]
    fig_em.add_trace(go.Bar(
        x=df_em["Amount"],
        y=df_em["Category"],
        orientation='h',
        marker_color=colors
    ))
    fig_em.update_layout(template="plotly_dark", title="Emergency Fund Comparison", xaxis_title="PKR", height=320, margin=dict(l=120))
    st.plotly_chart(fig_em, use_container_width=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Friendly action suggestions (no fractions) — compute months needed if saving a portion of monthly_possible_save
    st.markdown("<h4>Actionable Steps</h4>", unsafe_allow_html=True)
    # If no saving capacity, suggest expense reduction
    if monthly_possible_save <= 0:
        step1 = f"Your monthly savings capacity is 0. Reduce expenses or increase income to build emergency fund."
    else:
        # Plan to reach minimum within a reasonable timeframe (user-friendly)
        months_to_reach_min = math.ceil(emergency_gap_min / monthly_possible_save) if emergency_gap_min > 0 else 0
        months_to_reach_ideal = math.ceil(emergency_gap_ideal / monthly_possible_save) if emergency_gap_ideal > 0 else 0
        step1 = f"To reach minimum (Rs {emergency_min_amount:,}): ~{months_to_reach_min} months at current savings rate (Rs {monthly_possible_save:,}/mo)."
        step1b = f"To reach ideal (Rs {emergency_ideal_amount:,}): ~{months_to_reach_ideal} months."

    # Render two friendly short tiles
    if monthly_possible_save <= 0:
        tiles = [
            {"icon":"🛑", "title":"Build Capacity", "sub": step1},
            {"icon":"✂️", "title":"Cut Spending", "sub":"Start with 1 non-essential subscription cut"}
        ]
    else:
        tiles = [
            {"icon":"⏱️", "title":"Min Target Plan", "sub": step1},
            {"icon":"🎯", "title":"Ideal Target Plan", "sub": step1b}
        ]

    cols = st.columns(2)
    for col, t in zip(cols, tiles):
        with col:
            cls = "tile-good" if "Ideal" in t['title'] or "Min" in t['title'] else ""
            st.markdown(f"""
                <div class="tile {cls}">
                  <div class="tile-icon">{t['icon']}</div>
                  <div>
                    <div class="tile-title">{t['title']}</div>
                    <div class="tile-sub">{t['sub']}</div>
                  </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    # Quick numeric summary
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>Current Coverage</div><div class='stat-value'>{emergency_coverage_months} mo</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>Min Required (3 mo)</div><div class='stat-value'>Rs {emergency_min_amount:,.0f}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>Ideal (6 mo)</div><div class='stat-value'>Rs {emergency_ideal_amount:,.0f}</div></div>", unsafe_allow_html=True)

# ------------------------------
# PAGE: Visuals (charts only, no inputs)
# ------------------------------
elif st.session_state.get('page') == 'visuals':
    st.header("Visuals — Trends & Spending")

    # Prepare a 12-month sample DataFrame
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    df = pd.DataFrame({
        "month": months,
        "income": [monthly_income for _ in months],
        "expenses": [monthly_expenses for _ in months],
    })
    df['savings'] = df['income'] - df['expenses']

    # Income vs Expenses grouped bars with improved look
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['month'], y=df['income'], name="Income", marker_color="#06b6d4"))
    fig.add_trace(go.Bar(x=df['month'], y=df['expenses'], name="Expenses", marker_color="#fb7185"))
    fig.update_layout(template="plotly_dark", barmode='group', title="Income vs Expenses (12 months)", yaxis_title="PKR", height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    # Savings trend: smoother line with markers
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['month'], y=df['savings'], mode="lines+markers", name="Savings", line=dict(width=3, shape='spline')))
    fig2.update_layout(template="plotly_dark", title="Savings Trend (12 months)", yaxis_title="PKR", height=360)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    # Spending pie with donut style
    st.subheader("Spending by Category (estimated)")
    fig_pie = px.pie(values=list(cat_values.values()), names=list(cat_values.keys()), hole=0.45, title="Spending Breakdown")
    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(template="plotly_dark", height=420)
    st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------
# PDF generation (robust, DejaVu support if available)
# ------------------------------
def sanitize_text_for_ascii(s: str) -> str:
    # Replace problematic dashes/quotes
    replacements = {
        "—": "-", "–": "-", "‘": "'", "’": "'", "“": '"', "”": '"'
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s

def build_pdf_bytes():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    # If DejaVuSans.ttf exists in the app directory, register and use it (supports Unicode)
    font_file = "DejaVuSans.ttf"
    use_dejavu = False
    if os.path.exists(font_file):
        try:
            pdf.add_font("DejaVu", "", font_file, uni=True)
            pdf.set_font("DejaVu", size=14)
            use_dejavu = True
        except Exception:
            # fallback if font registration fails
            use_dejavu = False

    if not use_dejavu:
        # use builtin font (latin1) but sanitize text for ASCII/latin1
        pdf.set_font("Arial", size=14)

    # Title
    title = "Apka Financial Advisor - Report"
    if not use_dejavu:
        title = sanitize_text_for_ascii(title)
    pdf.cell(0, 8, title, ln=1, align="C")
    pdf.ln(4)

    # Basic info
    if use_dejavu:
        pdf.set_font("DejaVu", size=11)
    else:
        pdf.set_font("Arial", size=11)

    def write_line(label, value):
        txt = f"{label}: {value}"
        if not use_dejavu:
            txt = sanitize_text_for_ascii(txt)
        pdf.multi_cell(0, 6, txt)

    write_line("Generated", datetime.now().strftime("%d %B %Y"))
    pdf.ln(2)

    # Summary
    pdf.set_font(pdf.font_family, "B", 12)
    pdf.cell(0, 6, "1) Quick Summary", ln=1)
    pdf.set_font(pdf.font_family, size=11)
    write_line("Monthly Income", f"Rs {monthly_income:,.0f}")
    write_line("Monthly Expenses", f"Rs {monthly_expenses:,.0f}")
    write_line("Current Savings", f"Rs {current_savings:,.0f}")
    write_line("Net Worth", f"Rs {net_worth:,.0f}")
    pdf.ln(3)

    # Goal
    pdf.set_font(pdf.font_family, "B", 12)
    pdf.cell(0, 6, "2) Goal", ln=1)
    pdf.set_font(pdf.font_family, size=11)
    write_line("Goal Name", f"{goal_name}")
    write_line("Target Amount", f"Rs {goal_amount:,.0f}")
    write_line("Progress (based on current savings)", f"{goal_progress_pct:.1f}%")
    write_line("Months to target (if all monthly savings applied)", f"{months_to_goal if months_to_goal != math.inf else 'N/A'}")
    pdf.ln(3)

    # Emergency
    pdf.set_font(pdf.font_family, "B", 12)
    pdf.cell(0, 6, "3) Emergency Fund", ln=1)
    pdf.set_font(pdf.font_family, size=11)
    write_line("Current coverage (months)", f"{emergency_coverage_months}")
    write_line("Recommended minimum (3 months)", f"Rs {emergency_min_amount:,.0f}")
    write_line("Recommended ideal (6 months)", f"Rs {emergency_ideal_amount:,.0f}")
    write_line("Gap to minimum", f"Rs {emergency_gap_min:,.0f}")
    pdf.ln(3)

    # Short suggestions — consistent with UI (two short suggestions based on goal progress)
    pdf.set_font(pdf.font_family, "B", 12)
    pdf.cell(0, 6, "4) Short Suggestions", ln=1)
    pdf.set_font(pdf.font_family, size=11)

    # Suggestions for goal progress (same logic as UI)
    if goal_progress_pct < 50:
        suggested_extra = round(monthly_possible_save * 0.2) if monthly_possible_save > 0 else 0
        s1 = f"Add ~Rs {suggested_extra:,}/mo to goal"
        s2 = f"Reduce non-essential spend by ~Rs {max(5000, round(monthly_expenses*0.05)):,}/mo"
    elif 50 <= goal_progress_pct < 90:
        suggested_extra = round(monthly_possible_save * 0.1) if monthly_possible_save > 0 else 0
        s1 = f"Add ~Rs {suggested_extra:,}/mo to finish earlier"
        s2 = "Automate monthly transfers to goal"
    else:
        s1 = "Continue your current plan — you're close"
        s2 = "Plan your next goal"

    write_line("• " + s1, "")
    write_line("• " + s2, "")
    pdf.ln(4)

    # Spending breakdown
    pdf.set_font(pdf.font_family, "B", 12)
    pdf.cell(0, 6, "5) Spending Breakdown (estimated)", ln=1)
    pdf.set_font(pdf.font_family, size=11)
    for k, v in cat_values.items():
        write_line(k, f"Rs {v:,}")

    pdf.ln(6)
    pdf.set_font(pdf.font_family, "I", 9)
    disclaimer = "This report is informational. For major financial decisions, consult a certified advisor."
    if not use_dejavu:
        disclaimer = sanitize_text_for_ascii(disclaimer)
    pdf.multi_cell(0, 5, disclaimer)

    # Return bytes safely
    pdf_str = pdf.output(dest='S')
    if isinstance(pdf_str, str):
        pdf_bytes = pdf_str.encode('latin-1', errors='replace')
    else:
        pdf_bytes = pdf_str
    return pdf_bytes

# PDF download button across pages
st.markdown("---")
try:
    pdf_bytes = build_pdf_bytes()
    st.download_button(
        label="📄 Download Detailed PDF Report",
        data=pdf_bytes,
        file_name=f"Apka_Financial_Report_{datetime.now().strftime('%d%m%Y')}.pdf",
        mime="application/pdf",
        key="download_pdf"
    )
except Exception as e:
    # if PDF build fails, show a friendly error and fallback to a simple text file
    st.error("PDF generation failed — generating a simple text summary instead.")
    summary_text = f"Income: {monthly_income}\nExpenses: {monthly_expenses}\nSavings: {current_savings}\nNet Worth: {net_worth}\n"
    st.download_button("Download summary (txt)", data=summary_text, file_name="summary.txt")

st.markdown("<div class='muted' style='margin-top:8px'>Report includes summary, goal progress, emergency info & short suggestions.</div>", unsafe_allow_html=True)




