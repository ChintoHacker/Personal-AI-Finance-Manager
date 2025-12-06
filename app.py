# app.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import base64
import math

st.set_page_config(page_title="Apka Financial Advisor — Smart", page_icon="💸", layout="wide")

# ===========================
# CSS / Styling
# ===========================
st.markdown("""
<style>
/* Background & app */
.stApp { background: linear-gradient(180deg,#061026 0%, #07122a 100%); color:#e6eef8; }

/* Header */
.app-header {
  position: sticky; top:0; z-index:1000;
  background: linear-gradient(90deg,#071932,#0b1f36);
  padding: 14px 20px; border-bottom: 1px solid rgba(255,255,255,0.03);
  margin-bottom: 18px; border-radius:8px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}
.app-title {
  font-weight:900; font-size:30px;
  background: linear-gradient(90deg,#7c3aed,#06b6d4);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  display:inline-block;
}

/* Nav buttons (we only change nav button colors) */
.top-nav .stButton>button {
  background: linear-gradient(90deg,#7c3aed,#06b6d4);
  color:white; border-radius:12px; padding:10px 18px; font-weight:800;
  box-shadow: 0 8px 30px rgba(99,102,241,0.18);
}
.top-nav .stButton>button:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 40px rgba(99,102,241,0.28);
}

/* Small stat cards */
.stat-card {
  background: rgba(255,255,255,0.02);
  border-radius:12px; padding:14px; text-align:center;
  border: 1px solid rgba(255,255,255,0.03);
}
.stat-label { color: rgba(230,238,248,0.7); font-size:13px; }
.stat-value { font-weight:800; font-size:20px; margin-top:6px; }

/* Goal Progress */
.goal-wrap { background: rgba(255,255,255,0.02); padding:14px; border-radius:12px; border:1px solid rgba(255,255,255,0.03); }
.goal-bar { height:26px; background: rgba(255,255,255,0.03); border-radius:14px; overflow:hidden; }
.goal-fill { height:100%; background: linear-gradient(90deg,#22c55e,#06b6d4); transition: width 0.8s; }

/* insights */
.insight-card { padding:12px; border-radius:10px; margin-bottom:10px; background: rgba(255,255,255,0.02); border-left:6px solid #06b6d4; }
.insight-warning { border-left:6px solid #fb7185; }
.insight-good { border-left:6px solid #10b981; }

/* pdf button bottom */
.pdf-download {
  display:flex; justify-content:center; margin-top:18px; margin-bottom:40px;
}
.pdf-btn {
  background: linear-gradient(90deg,#16a34a,#22c55e); color:white; padding:12px 20px; border-radius:12px; border:none; font-weight:800;
  box-shadow: 0 8px 30px rgba(34,197,94,0.18);
}

/* small muted */
.muted { color: rgba(230,238,248,0.65); font-size:13px; }
.explain { background: rgba(255,255,255,0.02); padding:10px; border-radius:8px; margin-top:8px; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ===========================
# Header + Top nav (buttons colored via CSS)
# ===========================
st.markdown(f"""
<div class="app-header">
  <span class="app-title">Apka Financial Advisor — Smart Dashboard</span>
  <span style="float:right; color:rgba(230,238,248,0.6); font-size:14px;">{datetime.now().strftime('%d %b %Y')}</span>
</div>
""", unsafe_allow_html=True)

# Ensure session state page exists
if "page" not in st.session_state:
    st.session_state.page = "landing"

# top nav using st.columns to preserve button functionality
nav_cols = st.columns([1,1,1], gap="large")
with nav_cols[0]:
    if st.button("🏠 Overview (Landing)"):
        st.session_state.page = "landing"
with nav_cols[1]:
    if st.button("🤖 AI Insights"):
        st.session_state.page = "insights"
with nav_cols[2]:
    if st.button("📈 Visuals"):
        st.session_state.page = "visuals"

# ===========================
# Sidebar - keep for essential inputs only (no spending category inputs)
# ===========================
with st.sidebar:
    st.header("Apki Financial Inputs")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=1500, step=500, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")
    st.markdown("---")
    st.markdown("<div class='muted'>Tip: Click Analyze on top nav after changing inputs to refresh views.</div>", unsafe_allow_html=True)

# ===========================
# Calculations used across pages
# ===========================
total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_possible_save = max(0, monthly_income - monthly_expenses)
goal_purpose = "Birthday Present"  # keep default text if not user-managed; user didn't request goal inputs here
goal_amount = 4000  # small default so goal progress can show similar to your screenshot (adjust as needed)
# If user wants goal editable, later we can add an input — but you didn't request that now.

# Goal progress from provided values (kept as previously designed)
goal_progress = min(100, (current_savings / goal_amount * 100)) if goal_amount > 0 else 0
months_to_goal = round((goal_amount - current_savings) / monthly_possible_save, 1) if monthly_possible_save > 0 else float('inf')
emergency_months = round(current_savings / max(1, monthly_expenses), 1)

# Spending categories: auto-derived from monthly_expenses using sensible defaults (no sidebar inputs)
# defaults (proportions)
cat_props = {
    "Food": 0.30,
    "Transport": 0.10,
    "Shopping": 0.20,
    "Bills": 0.25,
    "Fun": 0.15
}
# adjust so they sum to >1? They sum to 1.0 (0.30+0.10+0.20+0.25+0.15 = 1.0)
cat_values = {k: round(monthly_expenses * p) for k, p in cat_props.items()}

# ===========================
# Helper: personalized suggestions (improved)
# ===========================
def generate_personalized_suggestions():
    suggestions = []
    # Emergency fund
    if emergency_months < 3:
        suggestions.append(("Emergency fund low", f"You have only {emergency_months} months covered. Recommended: build to 3–6 months of expenses. Start by allocating a small part of monthly savings to emergency bucket."))
    else:
        suggestions.append(("Emergency fund healthy", f"You have {emergency_months} months saved — good. Maintain this until 3–6 months is stable."))

    # Debt advice
    if total_debt > 0:
        suggestions.append(("Debt advice", f"You have Rs {total_debt:,} debt. Pay off high-interest debt first. Consider 'debt avalanche' or 'debt snowball' based on behaviour."))
    else:
        suggestions.append(("Debt status", "No debt — excellent. Now prioritize emergency fund and long-term investments."))

    # Savings/investment advice (smart)
    if monthly_possible_save <= 0:
        suggestions.append(("Cashflow alert", "Your expenses are >= income. Review discretionary expenses and aim to create a positive monthly saving amount."))
    elif monthly_possible_save < 0.2 * monthly_income:
        suggestions.append(("Improve savings", f"Your monthly possible saving is Rs {monthly_possible_save:,}. Aim to increase savings to at least 20% of income. Reduce non-essential spending and automate transfers."))
    else:
        suggestions.append(("Good savings habit", f"You can save Rs {monthly_possible_save:,} monthly — consider splitting: 50% investments, 30% emergency/liquid, 20% personal/short-term goals."))

    # Investment suggestions (simple)
    if net_worth > 0 and monthly_possible_save > 0:
        suggestions.append(("Investment idea", "For a balanced approach: small index funds or mutual funds for long-term, fixed deposits for safe portion, and keep a liquid portion for near-term needs."))
    return suggestions

# ===========================
# PAGE: Landing / Dashboard
# ===========================
if st.session_state.page == "landing":
    st.markdown("<h3 style='margin-bottom:6px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

    # top metrics - 5 columns
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        ("Total (Income + Savings)", total_balance),
        ("Income", monthly_income),
        ("Expenses", monthly_expenses),
        ("Savings", current_savings),
        ("Net Worth", net_worth)
    ]
    for col, (label, val) in zip([c1, c2, c3, c4, c5], metrics):
        with col:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">Rs {val:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    # Goal progress (keep stylish)
    st.markdown("<h4 style='margin-top:6px;'>Goal Progress</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="goal-wrap">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="width:70%;">
                    <div style="margin-bottom:8px;"><strong>{goal_purpose}</strong> — Target Rs {goal_amount:,.0f}</div>
                    <div class="goal-bar"><div class="goal-fill" style="width:{goal_progress}%;"></div></div>
                    <div class="muted" style="margin-top:8px;">{goal_progress:.1f}% complete • Rs {current_savings:,.0f} saved</div>
                </div>
                <div style="width:28%; text-align:center;">
                    <div style="font-size:13px; color:rgba(230,238,248,0.7)"><strong>Estimated time</strong></div>
                    <div style="font-size:20px; font-weight:800; margin-top:6px;">{months_to_goal if months_to_goal!=float('inf') else 'N/A'} mo</div>
                    <div class="muted" style="margin-top:6px;">(at current saving pace)</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Smart suggestion block (appears but simplified and styled)
    st.markdown("<h4 style='margin-top:12px;'>Smart Suggestions</h4>", unsafe_allow_html=True)
    suggestions = generate_personalized_suggestions()
    for title, text in suggestions:
        # border color depends on type
        cls = "insight-card"
        if "low" in title.lower() or "alert" in title.lower() or "cashflow" in title.lower():
            cls = "insight-card insight-warning"
        elif "good" in title.lower() or "healthy" in title.lower():
            cls = "insight-card insight-good"
        st.markdown(f"<div class='{cls}'><strong>{title}</strong><div class='muted' style='margin-top:6px'>{text}</div></div>", unsafe_allow_html=True)

# ===========================
# PAGE: AI Insights
# ===========================
elif st.session_state.page == "insights":
    st.header("AI Smart Insights — Actionable & Clear")

    # Emergency Fund section separate and prominent
    st.markdown("<h4>Emergency Fund</h4>", unsafe_allow_html=True)
    emergency_reco = "Recommended: 3–6 months of expenses"
    if emergency_months < 3:
        color_class = "insight-warning"
        status = f"Low: You have {emergency_months} months. {emergency_reco}."
    elif 3 <= emergency_months <= 6:
        color_class = "insight-good"
        status = f"Good: You have {emergency_months} months. Keep it stable."
    else:
        color_class = "insight-good"
        status = f"Excellent: You have {emergency_months} months. Consider investing excess safely."

    st.markdown(f"<div class='insight-card {color_class}'><strong>Emergency Fund</strong><div class='muted' style='margin-top:6px'>{status}</div></div>", unsafe_allow_html=True)

    # General insights - clearer wording and color-coded
    st.markdown("<h4 style='margin-top:12px;'>Other Insights</h4>", unsafe_allow_html=True)
    insights_list = []
    # Cashflow condition
    if monthly_possible_save <= 0:
        insights_list.append(("Cashflow Danger", f"Expenses equal or above income. Monthly possible saving = Rs {monthly_possible_save:,}. Immediate expense review needed."))
    else:
        insights_list.append(("Cashflow Status", f"Monthly possible saving: Rs {monthly_possible_save:,}. Good to automate transfers for saving."))

    if total_debt > 0:
        insights_list.append(("Debt", f"You owe Rs {total_debt:,}. Prioritize high-interest parts first."))
    else:
        insights_list.append(("Debt", "You have no debt — great discipline."))

    # Investment readiness
    if net_worth > 0 and monthly_possible_save > 0:
        insights_list.append(("Investment Readiness", "You are in a position to consider diversified investments: balanced funds, fixed income, and a small equity portion depending on risk tolerance."))
    else:
        insights_list.append(("Investment Readiness", "Stabilize emergency fund & positive cashflow before aggressive investing."))

    for title, text in insights_list:
        cls = "insight-card"
        if "danger" in title.lower() or "cashflow" in title.lower():
            cls = "insight-card insight-warning"
        else:
            cls = "insight-card"
        st.markdown(f"<div class='{cls}'><strong>{title}</strong><div class='muted' style='margin-top:6px'>{text}</div></div>", unsafe_allow_html=True)

    # Keep a nice goal gauge (same as before)
    st.markdown("<h4 style='margin-top:12px;'>Goal Progress</h4>", unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=goal_progress,
        domain={'x':[0,1],'y':[0,1]},
        gauge={'axis':{'range':[0,100]},
               'bar': {'color': "#22c55e"},
               'steps': [{'range':[0,40],'color':'#fb7185'},
                         {'range':[40,70],'color':'#f59e0b'},
                         {'range':[70,100],'color':'#10b981'}]},
        title={'text': f"{goal_purpose} Progress"}
    ))
    gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(gauge, use_container_width=True)

# ===========================
# PAGE: Visuals
# ===========================
elif st.session_state.page == "visuals":
    st.header("Visuals — Trends & Spending")

    # Income vs Expenses (monthly and yearly) - show monthly bars and yearly aggregated
    st.subheader("Income vs Expenses — Monthly")
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    # create example monthly series by repeating the provided monthly values to show a full-year view
    income_series = [monthly_income for _ in months]
    expense_series = [monthly_expenses for _ in months]
    fig_month = go.Figure()
    fig_month.add_trace(go.Bar(x=months, y=income_series, name="Income", marker_color="#06b6d4"))
    fig_month.add_trace(go.Bar(x=months, y=expense_series, name="Expenses", marker_color="#fb7185"))
    fig_month.update_layout(barmode='group', template='plotly_dark', title="Income vs Expenses (Monthly)")
    st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("---")
    # Spending by category (derived automatically)
    st.subheader("Spending by Category (estimated from monthly expenses)")
    labels = list(cat_values.keys())
    values = list(cat_values.values())
    fig_pie = px.pie(values=values, names=labels, hole=0.45, title="Spending Breakdown")
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    # Combined chart: Income / Expenses / Savings
    st.subheader("Combined Snapshot (Recent Trend)")
    months_short = ["-3M","-2M","-1M","Now"]
    incomes = [monthly_income*0.95, monthly_income*0.98, monthly_income*0.99, monthly_income]
    expenses = [monthly_expenses*1.02, monthly_expenses*1.01, monthly_expenses, monthly_expenses]
    savings = [current_savings*0.7, current_savings*0.85, current_savings*0.95, current_savings]
    fig_comb = go.Figure()
    fig_comb.add_trace(go.Scatter(x=months_short, y=incomes, mode="lines+markers", name="Income"))
    fig_comb.add_trace(go.Scatter(x=months_short, y=expenses, mode="lines+markers", name="Expenses"))
    fig_comb.add_trace(go.Scatter(x=months_short, y=savings, mode="lines+markers", name="Savings"))
    fig_comb.update_layout(template="plotly_dark", title="Income / Expenses / Savings (sample recent)")
    st.plotly_chart(fig_comb, use_container_width=True)

    st.markdown("<div class='explain'>Note: Spending categories are estimated proportions of total expenses to help visualize where money goes. You can adjust income/expenses in the sidebar to update these charts.</div>", unsafe_allow_html=True)

# ===========================
# PDF Generation (bottom of every page)
# ===========================
def generate_pdf_bytes():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    # header
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Apka Financial Advisor — Detailed Report", ln=1, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y')}", ln=1)
    pdf.ln(3)

    # 1) Summary
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "1) Quick Summary", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Total (Income + Savings): Rs {total_balance:,.0f}\n"
                   f"Monthly Income: Rs {monthly_income:,.0f}\n"
                   f"Monthly Expenses: Rs {monthly_expenses:,.0f}\n"
                   f"Current Savings: Rs {current_savings:,.0f}\n"
                   f"Net Worth: Rs {net_worth:,.0f}\n")
    pdf.ln(2)

    # 2) Goal progress
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "2) Goal Progress", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Goal: {goal_purpose} — Target Rs {goal_amount:,.0f}\n"
                   f"Progress: {goal_progress:.1f}% ({current_savings:,.0f} saved)\n"
                   f"Estimated months to goal at current saving pace: {months_to_goal if months_to_goal!=float('inf') else 'N/A'}\n")
    pdf.ln(2)

    # 3) Emergency & insights
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "3) Emergency Fund & Insights", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6,
                   f"Emergency fund covers: ~{emergency_months} months of expenses.\n"
                   "Recommendation: Maintain 3–6 months of essential expenses as emergency fund before taking aggressive investment positions.\n\n")
    # Personalized suggestions
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "4) Personalized Suggestions", ln=1)
    pdf.set_font("Arial", "", 10)
    for title, text in generate_personalized_suggestions():
        pdf.multi_cell(0, 6, f"• {title}: {text}")
    pdf.ln(2)

    # 5) Spending breakdown
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 6, "5) Spending Breakdown (estimated)", ln=1)
    pdf.set_font("Arial", "", 10)
    for k, v in cat_values.items():
        pdf.multi_cell(0, 6, f"{k}: Rs {v:,}")
    pdf.ln(4)

    # Footer
    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 5, "This report is informational. For large financial decisions, consult a certified financial advisor. Apka Financial Advisor provides simple, automated suggestions based on provided inputs.")
    out = BytesIO()
    pdf.output(out)
    return out.getvalue()

# produce pdf bytes & download link at bottom
pdf_bytes = generate_pdf_bytes()
b64 = base64.b64encode(pdf_bytes).decode()
st.markdown("---")
st.markdown(f"""
<div class="pdf-download">
  <a href="data:application/pdf;base64,{b64}" download="Apka_Financial_Report_{datetime.now().strftime('%d%m%Y')}.pdf">
    <button class="pdf-btn">📄 Download Detailed PDF Report</button>
  </a>
</div>
""", unsafe_allow_html=True)
