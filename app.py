# app.py (UPGRADED by ChatGPT)
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import pandas as pd
import math

st.set_page_config(page_title="Apka Financial Advisor — Smart", page_icon="💸", layout="wide")

# ===========================
# Custom CSS (UI overhaul)
# ===========================
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(180deg,#041026 0%, #07122a 100%);
        color: #e6eef8;
        font-family: "Segoe UI", Roboto, sans-serif;
    }

    /* Sidebar style */
    .css-1d391kg {  /* Streamlit sidebar container class may vary across versions */
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-right: 1px solid rgba(255,255,255,0.03);
        padding: 18px;
        border-radius: 12px;
    }
    /* Fallback: also try to style .sidebar for other versions */
    .sidebar .sidebar-content { background: transparent; }

    /* Card style */
    .stat-card {
      background: rgba(255,255,255,0.02);
      border-radius:12px; padding:14px; text-align:center;
      border: 1px solid rgba(255,255,255,0.03);
    }
    .stat-label { color: rgba(230,238,248,0.7); font-size:13px; }
    .stat-value { font-weight:800; font-size:20px; margin-top:6px; }

    /* Goal progress */
    .goal-wrap {
      background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      padding:16px; border-radius:12px; border:1px solid rgba(255,255,255,0.03);
      box-shadow: 0 6px 20px rgba(2,6,23,0.6);
    }
    .goal-bar { height:26px; background: rgba(255,255,255,0.03); border-radius:14px; overflow:hidden; }
    .goal-fill { height:100%; background: linear-gradient(90deg,#7c3aed,#06b6d4); transition: width 0.9s; box-shadow: 0 6px 24px rgba(99,102,241,0.12); }

    /* Buttons (a common class used for HTML buttons) */
    .glow-btn {
      background: linear-gradient(90deg,#7c3aed,#06b6d4);
      color: white; padding:10px 18px; border-radius:12px; border:none; font-weight:800;
      box-shadow: 0 8px 30px rgba(124,58,237,0.12); cursor:pointer;
      transition: transform .15s ease, box-shadow .15s ease;
    }
    .glow-btn:hover { transform: translateY(-4px); box-shadow: 0 18px 50px rgba(124,58,237,0.20); }

    /* Primary action (analyze/predict) - extra glow */
    .primary-action {
      background: linear-gradient(90deg,#ff7a18,#ffb347);
      box-shadow: 0 10px 40px rgba(255,122,24,0.18);
    }
    .primary-action:hover { box-shadow: 0 20px 70px rgba(255,122,24,0.28); }

    /* PDF button */
    .pdf-btn {
      background: linear-gradient(90deg,#16a34a,#22c55e);
      color:white; padding:12px 20px; border-radius:12px; border:none; font-weight:800;
      box-shadow: 0 8px 30px rgba(34,197,94,0.18);
    }
    .pdf-btn:hover { transform: translateY(-3px); box-shadow: 0 18px 50px rgba(34,197,94,0.25); }

    /* Insight cards */
    .insight-card { padding:12px; border-radius:10px; margin-bottom:10px; background: rgba(255,255,255,0.02); border-left:6px solid #06b6d4; }
    .insight-warning { border-left:6px solid #fb7185; }
    .insight-good { border-left:6px solid #10b981; }

    /* muted small text */
    .muted { color: rgba(230,238,248,0.65); font-size:13px; }

    /* Responsive tweaks for columns */
    @media (max-width: 900px) {
      .stApp .css-1d391kg { padding: 10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Sidebar (enhanced)
# ---------------------------
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:6px'>Apki Financial Inputs</h2>", unsafe_allow_html=True)
    # Goals: user-managed
    goal_name = st.text_input("Goal Name", value="Birthday Present")
    goal_amount = st.number_input("Goal Target Amount (PKR)", min_value=0, value=4000, step=500, format="%d")
    goal_saved = st.number_input("Amount already saved for goal (PKR)", min_value=0, value=1500, step=100, format="%d")

    st.markdown("---")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=1500, step=500, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")
    st.markdown("---")

    st.markdown("<div class='muted'>Tip: Click the Analyze button (on the page) after changing inputs to refresh views.</div>", unsafe_allow_html=True)

# ===========================
# Core calculations & helpers
# ===========================
def safe_div(a, b):
    try:
        return a / b
    except Exception:
        return 0

total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_possible_save = max(0, monthly_income - monthly_expenses)

# Goal progress logic (user-provided)
goal_progress_pct = 0.0
if goal_amount > 0:
    goal_progress_pct = min(100.0, (goal_saved / goal_amount) * 100.0)
months_to_goal = math.inf
if monthly_possible_save > 0:
    months_to_goal = round(max(0.0, (goal_amount - goal_saved) / monthly_possible_save), 1)

# Emergency fund recommendations & auto-aim
emergency_months_current = round(safe_div(current_savings, max(1, monthly_expenses)), 1)
emergency_reco_min = 3
emergency_reco_max = 6
# Offer a suggested target: choose recommended months depending on current coverage
recommended_months = emergency_reco_min if emergency_months_current < emergency_reco_min else emergency_reco_max if emergency_months_current < emergency_reco_max else emergency_reco_max
# allow user to select recommended aim (auto-select but editable)
emergency_aim_months = st.sidebar.selectbox("Emergency target (months)", options=[3, 6], index=0 if recommended_months==3 else 1, help="Choose 3 months (minimum) or 6 months (ideal)")
emergency_target_amount = monthly_expenses * emergency_aim_months
emergency_amount_needed = max(0, emergency_target_amount - current_savings)

# Spending categories (derived)
cat_props = {"Food": 0.30, "Transport": 0.10, "Shopping": 0.20, "Bills": 0.25, "Fun": 0.15}
cat_values = {k: round(monthly_expenses * p) for k, p in cat_props.items()}

# Personalized suggestions (improved)
def generate_personalized_suggestions():
    suggestions = []
    # Emergency fund
    if emergency_months_current < 3:
        suggestions.append(("Emergency fund low", f"You have only {emergency_months_current} months covered. Recommended target: {emergency_aim_months} months ≈ Rs {emergency_target_amount:,.0f}. You need Rs {emergency_amount_needed:,.0f} more. Start by moving a small fixed amount every month to a liquid account."))
    elif 3 <= emergency_months_current <= 6:
        suggestions.append(("Emergency fund OK", f"You have {emergency_months_current} months saved — good. Aim to reach {emergency_aim_months} months if possible."))
    else:
        suggestions.append(("Emergency fund strong", f"You have {emergency_months_current} months saved — excellent. Consider investing surplus conservatively."))

    # Debt
    if total_debt > 0:
        suggestions.append(("Debt strategy", f"You owe Rs {total_debt:,}. Prioritize high-interest loans. Consider putting extra savings towards highest-rate debt."))
    else:
        suggestions.append(("Debt free", "No debt — good. Prioritize emergency fund & long-term investments."))

    # Cashflow
    if monthly_possible_save <= 0:
        suggestions.append(("Cashflow alert", "Expenses are >= income. Immediate review of discretionary expenses needed to avoid negative savings."))
    elif monthly_possible_save < 0.2 * monthly_income:
        suggestions.append(("Savings improvement", f"Your monthly possible saving is Rs {monthly_possible_save:,.0f}. Aim to push it to at least 20% of income. Consider automated transfers."))
    else:
        suggestions.append(("Savings healthy", f"You can save Rs {monthly_possible_save:,.0f} monthly. Consider 50% long-term, 30% emergency/liquid, 20% personal short-term goals."))

    # Goal advice
    if goal_progress_pct < 30:
        suggestions.append(("Goal ramp-up", f"Goal '{goal_name}' progress is {goal_progress_pct:.1f}%. Consider allocating a portion of monthly savings for this target."))
    else:
        suggestions.append(("Goal on track", f"Goal '{goal_name}' is {goal_progress_pct:.1f}% complete. Keep momentum."))

    # Investment suggestion
    if net_worth > 0 and monthly_possible_save > 0:
        suggestions.append(("Investment idea", "If you have >3 months emergency coverage, consider diversified funds (index/mutual) for long-term growth while keeping safe portion in deposits."))
    return suggestions

# ===========================
# Top header + nav (simple)
# ===========================
st.markdown(
    f"""
    <div style="padding:10px 14px; border-radius:10px; background: linear-gradient(90deg,#071932,#0b1f36); margin-bottom:12px;">
      <span style="font-weight:900; font-size:22px; background: linear-gradient(90deg,#7c3aed,#06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Apka Financial Advisor — Smart Dashboard</span>
      <span style="float:right; color:rgba(230,238,248,0.7); font-size:13px;">{datetime.now().strftime('%d %b %Y')}</span>
    </div>
    """, unsafe_allow_html=True)

# Top navigation using columns
nav_col1, nav_col2, nav_col3 = st.columns([1,1,1], gap="large")
with nav_col1:
    if st.button("🏠 Overview"):
        st.session_state['page'] = "landing"
with nav_col2:
    if st.button("🤖 AI Insights"):
        st.session_state['page'] = "insights"
with nav_col3:
    if st.button("📈 Visuals"):
        st.session_state['page'] = "visuals"

# Default page
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# ANALYZE / PREDICT action (we place it once per page where needed)
def analyze_action():
    # basic "prediction": months to reach goal and suggested allocation
    result = {}
    result['months_to_goal'] = months_to_goal if months_to_goal != math.inf else None
    # A simple projection: if user invests a portion of monthly savings into goal
    result['save_rate_pct'] = 0.2 if monthly_possible_save > 0 else 0.0
    result['monthly_allocation_recommendation'] = round(monthly_possible_save * result['save_rate_pct'])
    return result

# ===========================
# PAGE: Landing / Overview
# ===========================
if st.session_state.get("page") == "landing":
    st.markdown("<h3 style='margin-bottom:6px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)
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
            st.markdown(f"""<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-value">Rs {val:,.0f}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    # Goal section
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
                  <div class="muted" style="margin-top:8px;">{goal_progress_pct:.1f}% complete • Rs {goal_saved:,.0f} saved</div>
                </div>
                <div style="width:28%; text-align:center;">
                  <div style="font-size:13px; color:rgba(230,238,248,0.7)"><strong>ETA</strong></div>
                  <div style="font-size:20px; font-weight:800; margin-top:6px;">{months_to_goal if months_to_goal!=math.inf else 'N/A'} mo</div>
                  <div class="muted" style="margin-top:6px;">(at current saving pace)</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        # Analyze / Predict button (styled HTML button, do action using st.session_state flag)
        if st.button("🔍 Analyze / Predict", key="analyze_top"):
            st.session_state['last_analysis'] = analyze_action()
            st.success("Analysis complete — suggestions updated below.")
    with right:
        # Quick suggestions small
        st.markdown("<h4 style='margin-bottom:6px;'>Quick Insights</h4>", unsafe_allow_html=True)
        quick = []
        if monthly_possible_save <= 0:
            quick.append(("Cashflow", f"Monthly possible saving: Rs {monthly_possible_save:,.0f} — review expenses."))
        else:
            quick.append(("Saving", f"Monthly possible saving: Rs {monthly_possible_save:,.0f}."))
        if total_debt > 0:
            quick.append(("Debt", f"Rs {total_debt:,} owed."))
        else:
            quick.append(("Debt", "No debt."))
        for title, text in quick:
            st.markdown(f"<div class='insight-card'><strong>{title}</strong><div class='muted' style='margin-top:6px'>{text}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    # Smart Suggestions (improved)
    st.markdown("<h4>Smart Suggestions</h4>", unsafe_allow_html=True)
    suggestions = generate_personalized_suggestions()
    for title, text in suggestions:
        cls = "insight-card"
        if "low" in title.lower() or "alert" in title.lower() or "danger" in title.lower():
            cls = "insight-card insight-warning"
        elif "good" in title.lower() or "strong" in title.lower():
            cls = "insight-card insight-good"
        st.markdown(f"<div class='{cls}'><strong>{title}</strong><div class='muted' style='margin-top:6px'>{text}</div></div>", unsafe_allow_html=True)

# ===========================
# PAGE: AI Insights
# ===========================
elif st.session_state.get("page") == "insights":
    st.header("AI Smart Insights — Actionable & Clear")

    # Emergency Fund prominent
    st.markdown("<h4>Emergency Fund</h4>", unsafe_allow_html=True)
    if emergency_months_current < 3:
        color_cls = "insight-card insight-warning"
        status = f"Low: You have {emergency_months_current} months. Recommended target: {emergency_aim_months} months (Rs {emergency_target_amount:,.0f}). You need Rs {emergency_amount_needed:,.0f} more."
    elif 3 <= emergency_months_current <= 6:
        color_cls = "insight-card insight-good"
        status = f"Good: You have {emergency_months_current} months. Recommended target: {emergency_aim_months} months (Rs {emergency_target_amount:,.0f})."
    else:
        color_cls = "insight-card insight-good"
        status = f"Excellent: You have {emergency_months_current} months. You could direct excess to investments."

    st.markdown(f"<div class='{color_cls}'><strong>Emergency Fund</strong><div class='muted' style='margin-top:6px'>{status}</div></div>", unsafe_allow_html=True)

    st.markdown("<h4 style='margin-top:12px;'>Deep Insights</h4>", unsafe_allow_html=True)
    insights = generate_personalized_suggestions()
    for t, m in insights:
        cls = "insight-card"
        if "alert" in t.lower() or "danger" in t.lower() or "low" in t.lower():
            cls = "insight-card insight-warning"
        elif "good" in t.lower() or "strong" in t.lower():
            cls = "insight-card insight-good"
        st.markdown(f"<div class='{cls}'><strong>{t}</strong><div class='muted' style='margin-top:6px'>{m}</div></div>", unsafe_allow_html=True)

    # Gauge for goal progress
    st.markdown("<h4 style='margin-top:12px;'>Goal Gauge</h4>", unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=goal_progress_pct,
        gauge={'axis': {'range': [0,100]},
               'bar': {'color': "#06b6d4"},
               'steps':[{'range':[0,40],'color':'#fb7185'},{'range':[40,70],'color':'#f59e0b'},{'range':[70,100],'color':'#10b981'}]},
        title={'text': f"{goal_name} Progress"}
    ))
    gauge.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(gauge, use_container_width=True)

# ===========================
# PAGE: Visuals
# ===========================
elif st.session_state.get("page") == "visuals":
    st.header("Visuals — Trends & Spending")

    # Month & Year selectors
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    current_year = datetime.now().year
    years = [current_year-1, current_year]
    sel_month = st.selectbox("Select month", options=months, index=datetime.now().month-1)
    sel_year = st.selectbox("Select year", options=years, index=len(years)-1)
    st.markdown("<div class='muted'>Showing income vs expenses for selected month & a 12-month view below</div>", unsafe_allow_html=True)

    # Create monthly series for a full-year display (sample replication)
    df_year = pd.DataFrame({
        "month": months,
        "income": [monthly_income for _ in months],
        "expenses": [monthly_expenses for _ in months],
        "savings": [max(0, monthly_income - monthly_expenses) for _ in months]
    })

    # Income vs Expense for selected month (highlight)
    sel_idx = months.index(sel_month)
    fig_single = go.Figure()
    fig_single.add_trace(go.Bar(x=[sel_month], y=[monthly_income], name="Income", marker_color="#06b6d4"))
    fig_single.add_trace(go.Bar(x=[sel_month], y=[monthly_expenses], name="Expenses", marker_color="#fb7185"))
    fig_single.update_layout(template="plotly_dark", title=f"Income vs Expenses — {sel_month} {sel_year}", yaxis_title="PKR")
    st.plotly_chart(fig_single, use_container_width=True)

    st.markdown("---")
    # Full year grouped bar
    fig_year = go.Figure()
    fig_year.add_trace(go.Bar(x=df_year["month"], y=df_year["income"], name="Income", marker_color="#06b6d4"))
    fig_year.add_trace(go.Bar(x=df_year["month"], y=df_year["expenses"], name="Expenses", marker_color="#fb7185"))
    fig_year.add_trace(go.Scatter(x=df_year["month"], y=df_year["savings"], mode="lines+markers", name="Savings", line=dict(width=3)))
    fig_year.update_layout(barmode='group', template='plotly_dark', title=f"Income / Expenses / Savings — {sel_year}", yaxis_title="PKR")
    st.plotly_chart(fig_year, use_container_width=True)

    st.markdown("---")
    # Spending pie
    st.subheader("Spending by Category (estimated)")
    fig_pie = px.pie(values=list(cat_values.values()), names=list(cat_values.keys()), hole=0.4, title="Estimated Spending Breakdown")
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# ===========================
# PDF Generation (fixed + download button)
# ===========================
def build_pdf_bytes():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Apka Financial Advisor — Detailed Report", ln=1, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y')}", ln=1)
    pdf.ln(4)

    # Summary
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "1) Quick Summary", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Total (Income + Savings): Rs {total_balance:,.0f}\n"
                   f"Monthly Income: Rs {monthly_income:,.0f}\n"
                   f"Monthly Expenses: Rs {monthly_expenses:,.0f}\n"
                   f"Current Savings: Rs {current_savings:,.0f}\n"
                   f"Net Worth: Rs {net_worth:,.0f}\n")
    pdf.ln(3)

    # Goal
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "2) Goal", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Goal: {goal_name}\nTarget: Rs {goal_amount:,.0f}\nSaved: Rs {goal_saved:,.0f}\nProgress: {goal_progress_pct:.1f}%\n"
                   f"Months to goal (at current pace): {months_to_goal if months_to_goal!=math.inf else 'N/A'}\n")
    pdf.ln(3)

    # Emergency
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "3) Emergency Fund", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Current coverage: ~{emergency_months_current} months of expenses.\n"
                   f"Recommended target: {emergency_aim_months} months ≈ Rs {emergency_target_amount:,.0f}\n"
                   f"Amount needed to reach target: Rs {emergency_amount_needed:,.0f}\n")
    pdf.ln(3)

    # Suggestions
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "4) Suggestions", ln=1)
    pdf.set_font("Arial", "", 10)
    for t, m in generate_personalized_suggestions():
        pdf.multi_cell(0, 6, f"• {t}: {m}")
    pdf.ln(3)

    # Spending breakdown
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "5) Spending Breakdown (estimated)", ln=1)
    pdf.set_font("Arial", "", 10)
    for k, v in cat_values.items():
        pdf.multi_cell(0, 6, f"{k}: Rs {v:,}")
    pdf.ln(6)

    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 5, "This report is informational. For large decisions consult a certified financial advisor.")
    # Return bytes using dest='S' which returns PDF as string
    pdf_bytes_str = pdf.output(dest='S')
    # FPDF uses latin-1 encoding for output string, convert to bytes
    if isinstance(pdf_bytes_str, str):
        pdf_bytes = pdf_bytes_str.encode('latin-1')
    else:
        # already bytes-like
        pdf_bytes = pdf_bytes_str
    return pdf_bytes

# Render PDF download UI at bottom across all pages
st.markdown("---")
pdf_bytes = build_pdf_bytes()
# Download button with nice label
st.download_button(
    label="📄 Download Detailed PDF Report",
    data=pdf_bytes,
    file_name=f"Apka_Financial_Report_{datetime.now().strftime('%d%m%Y')}.pdf",
    mime="application/pdf",
    key="download_pdf"
)

# Small footer
st.markdown("<div class='muted' style='margin-top:10px'>Report generated from user inputs. Update inputs and click Analyze for new recommendations.</div>", unsafe_allow_html=True)
