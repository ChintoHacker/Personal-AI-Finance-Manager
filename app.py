# app.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import base64

st.set_page_config(page_title="Apka Financial Advisor — Smart", page_icon="💸", layout="wide")

# -------------------- STYLES --------------------
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {background: linear-gradient(180deg,#071024 0%, #06192b 100%); color:#e6eef8}

    /* Header */
    .app-header {
        position: sticky; top: 0; z-index:1000;
        background: linear-gradient(90deg,#0b1220, #0f172a);
        border-bottom: 1px solid rgba(255,255,255,0.04);
        padding: 14px; border-radius: 8px; margin-bottom: 18px;
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
    }
    .app-title {font-size:28px; font-weight:800; background:linear-gradient(90deg,#7c3aed,#06b6d4);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; display:inline-block;}

    /* Cards */
    .stat-card {
        background: rgba(255,255,255,0.03); padding:18px; border-radius:14px; text-align:center;
        border:1px solid rgba(255,255,255,0.03);
    }
    .stat-num {font-size:22px; font-weight:800;}

    /* Glowing button */
    .glow {
        background: linear-gradient(90deg,#7c3aed,#3b82f6); color:white;
        padding:10px 18px; border-radius:12px; border:none; font-weight:700;
        box-shadow: 0 6px 30px rgba(59,130,246,0.28);
        cursor:pointer;
    }

    /* Insight card */
    .insight-card {
        border-radius:14px; padding:14px; margin-bottom:12px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-left: 6px solid #06b6d4;
    }

    /* Goal progress custom */
    .goal-wrap {background: rgba(255,255,255,0.02); padding:16px; border-radius:12px; border:1px solid rgba(255,255,255,0.03);}
    .goal-bar {height:26px; background: rgba(255,255,255,0.03); border-radius:14px; overflow:hidden;}
    .goal-fill {height:100%; background: linear-gradient(90deg,#22c55e,#06b6d4); transition: width .8s;}
    .muted {color: rgba(230,238,248,0.6); font-size:13px;}

    .explain {background: rgba(255,255,255,0.02); padding:12px; border-radius:8px; font-size:13px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HEADER (fixed) --------------------
st.markdown(
    f"""<div class="app-header">
            <span class="app-title">Apka Financial Advisor — Smart Dashboard</span>
            <span style="float:right; color:rgba(230,238,248,0.6); font-size:14px;">Generated: {datetime.now().strftime('%d %b %Y')}</span>
        </div>""",
    unsafe_allow_html=True,
)

# -------------------- SIDEBAR FOR USER INPUTS --------------------
with st.sidebar:
    st.header("Apki Financial Inputs")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0, value=85000, step=1000, format="%d")
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0, value=55000, step=1000, format="%d")
    current_savings = st.number_input("Current Savings (PKR)", min_value=0, value=1500, step=500, format="%d")
    total_debt = st.number_input("Total Debt (PKR)", min_value=0, value=0, step=1000, format="%d")
    current_investments = st.number_input("Current Investments (PKR)", min_value=0, value=0, step=1000, format="%d")

    st.subheader("Goal (optional)")
    goal_purpose = st.text_input("Goal Name", value="Birthday Present")
    goal_amount = st.number_input("Goal Target (PKR)", min_value=1000, value=4000, step=500, format="%d")

    st.subheader("Spending - Categories (for visuals)")
    # default category values (editable)
    food = st.number_input("Food (PKR)", min_value=0, value=18000, step=500)
    transport = st.number_input("Transport (PKR)", min_value=0, value=5000, step=500)
    shopping = st.number_input("Shopping (PKR)", min_value=0, value=12000, step=500)
    bills = st.number_input("Bills (PKR)", min_value=0, value=6000, step=500)
    fun = st.number_input("Fun (PKR)", min_value=0, value=3000, step=500)

    if st.button("Analyze Now", key="sidebar_analyze"):
        st.success("Inputs updated — scroll the pages to see insights & visuals!")

# -------------------- CALCULATIONS --------------------
total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
saving_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
goal_progress = min(100, (current_savings / goal_amount * 100)) if goal_amount > 0 else 0
monthly_possible_save = max(0, monthly_income - monthly_expenses)
months_to_goal = round((goal_amount - current_savings) / monthly_possible_save, 1) if monthly_possible_save > 0 else float('inf')
emergency_months = round(current_savings / max(1, monthly_expenses), 1)

# simple recommendation logic
def recommendation_summary():
    lines = []
    if total_debt > 0:
        lines.append("🔴 You have outstanding debt — prioritize paying high-interest debt first.")
    if emergency_months < 3:
        lines.append(f"⚠️ Emergency fund low ({emergency_months} months). Aim for 3–6 months of expenses.")
    if net_worth < 0:
        lines.append("🔻 Net worth negative — avoid risky investments until debt reduces.")
    else:
        lines.append("✅ Net worth positive — consider diversified investments.")
    # suggested allocation (simple rules)
    if saving_rate >= 30:
        lines.append("Suggestion: Good saving habit. Consider 40% long-term investments, 30% short-term, 30% liquid.")
    elif saving_rate >= 20:
        lines.append("Suggestion: Decent saving. Aim to increase to 30% — move 10% extra towards investments.")
    else:
        lines.append("Suggestion: Saving rate low. Try to raise savings to at least 20% of income.")
    return lines

# -------------------- NAVIGATION PAGES --------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

# top nav simplified
nav_col1, nav_col2, nav_col3 = st.columns([1,1,1])
with nav_col1:
    if st.button("🏠 Overview (Landing)"):
        st.session_state.page = "landing"
with nav_col2:
    if st.button("🤖 AI Insights"):
        st.session_state.page = "insights"
with nav_col3:
    if st.button("📈 Visuals"):
        st.session_state.page = "visuals"

# -------------------- PAGE 1: LANDING / DASHBOARD --------------------
if st.session_state.page == "landing":
    st.markdown("<h3 style='margin-bottom:6px;'>Overview — Quick Snapshot</h3>", unsafe_allow_html=True)

    # top metrics
    metrics_cols = st.columns(5)
    metrics = [
        ("Total", total_balance, "Apka available total (Income + Savings)"),
        ("Income", monthly_income, "Monthly income"),
        ("Expenses", monthly_expenses, "Monthly expenses"),
        ("Savings", current_savings, "Current saved amount"),
        ("Net Worth", net_worth, "Assets minus liabilities")
    ]
    for col, (label, value, desc) in zip(metrics_cols, metrics):
        with col:
            st.markdown(f"""
                <div class="stat-card">
                    <div style='color:rgba(230,238,248,0.8); font-size:13px; margin-bottom:6px'>{label}</div>
                    <div class="stat-num">Rs {value:,.0f}</div>
                    <div class="muted" style="margin-top:6px;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    # saving ratio and small explanation
    st.markdown(f"""
        <div class="explain">
            <strong>Saving Rate:</strong> You save <strong>{saving_rate:.1f}%</strong> of your income monthly.
            <br><span class="muted">Tip: Aim for 20%+ as a baseline. 30%+ is excellent.</span>
        </div>
    """, unsafe_allow_html=True)

    # Goal progress stylish
    st.markdown("<h4 style='margin-top:16px;'>Goal Progress</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="goal-wrap">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="width:68%;">
                    <div style="margin-bottom:8px;"><strong>{goal_purpose}</strong> — Target Rs {goal_amount:,.0f}</div>
                    <div class="goal-bar"><div class="goal-fill" style="width:{goal_progress}%;"></div></div>
                    <div style="margin-top:8px;" class="muted">{goal_progress:.1f}% complete • Rs {current_savings:,.0f} saved</div>
                </div>
                <div style="width:30%; text-align:center;">
                    <!-- mini gauge using plotly below (rendered as image) -->
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # show recommendation plans only if saving_rate < 39% OR goal_progress < 40%
    show_plans = (saving_rate < 39) or (goal_progress < 40)
    if show_plans:
        st.markdown("<h4 style='margin-top:18px;'>——————————————————————————————————————————————————<br>&nbsp;&nbsp;RECOMMENDED PLANS<br>——————————————————————————————————————————————————</h4>", unsafe_allow_html=True)
        # compute plan amounts
        basic_pct = 0.20
        strong_pct = 0.30
        basic_save = int(monthly_income * basic_pct)
        strong_save = int(monthly_income * strong_pct)
        basic_months = round((goal_amount - current_savings) / max(1, basic_save), 1) if basic_save>0 else float('inf')
        strong_months = round((goal_amount - current_savings) / max(1, strong_save), 1) if strong_save>0 else float('inf')

        st.markdown(f"""
            <div class="insight-card">
                <strong>Basic Plan (20% of income)</strong><br>
                Save: Rs {basic_save:,} / month → {basic_months} months (~{round(basic_months/12,2)} years)
                <br><br>
                <strong>Strong Plan (30% of income)</strong><br>
                Save: Rs {strong_save:,} / month → {strong_months} months (~{round(strong_months/12,2)} years)
            </div>
            """, unsafe_allow_html=True)

    # short personalized recommendation summary
    st.markdown("<h4 style='margin-top:14px;'>Personalized Suggestions</h4>", unsafe_allow_html=True)
    for line in recommendation_summary():
        st.markdown(f"<div class='insight-card'>{line}</div>", unsafe_allow_html=True)

# -------------------- PAGE 2: AI INSIGHTS (improved colours & clarity) --------------------
elif st.session_state.page == "insights":
    st.header("AI Smart Insights — Clear & Actionable")
    # nicer color palette via badges and explicit text
    insights = []
    # Insight rules
    if saving_rate < 20:
        insights.append(("Low Savings Rate", f"You're saving only {saving_rate:.1f}% — try to increase to 20% minimum."))
    else:
        insights.append(("Good Savings Rate", f"You're saving {saving_rate:.1f}% — keep it up! Try to slowly increase to 30% for faster goals."))

    if emergency_months < 3:
        insights.append(("Emergency Fund Alert", f"Emergency fund covers {emergency_months} months. Build to 3–6 months."))
    else:
        insights.append(("Emergency Fund Healthy", f"You have {emergency_months} months — good cushion."))

    if total_debt > 0:
        insights.append(("Debt Warning", f"You have Rs {total_debt:,} debt. Prioritize high-interest portions first."))
    else:
        insights.append(("Debt Status", "No debt — excellent discipline."))

    # show insights with clear colored left border (simple & not ugly)
    for title, text in insights:
        # choose border color based on title severity
        color = "#f97316" if "Alert" in title or "Low" in title or "Warning" in title else "#06b6d4"
        st.markdown(f"""
            <div style="border-left:6px solid {color}; padding:12px; border-radius:10px; margin-bottom:10px; background: rgba(255,255,255,0.02);">
                <strong>{title}</strong><br><span class="muted">{text}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h4 style='margin-top:12px;'>Goal Progress — Visual Gauge</h4>", unsafe_allow_html=True)
    # Use plotly gauge for better visual (small)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=goal_progress,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#22c55e"},
            'steps': [
                {'range': [0, 40], 'color': "#fb7185"},
                {'range': [40, 70], 'color': "#f59e0b"},
                {'range': [70, 100], 'color': "#10b981"}
            ]
        },
        title={'text': f"{goal_purpose} Progress"}
    ))
    gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(gauge, use_container_width=True)

    st.markdown("<div class='explain'><strong>Note:</strong> Goal progress is based on Current Savings vs Goal Target. If you want a monthly plan to reach the goal faster, use the Recommended Plans on the Overview page.</div>", unsafe_allow_html=True)

# -------------------- PAGE 3: VISUALS --------------------
elif st.session_state.page == "visuals":
    st.header("Smart Visuals — Spending & Trends")

    # Spending by category (pie)
    cat_labels = ["Food", "Transport", "Shopping", "Bills", "Fun"]
    cat_values = [food, transport, shopping, bills, fun]
    fig_pie = px.pie(values=cat_values, names=cat_labels, title="Spending by Category", hole=0.4)
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    # savings/income/expense trend (sample simple time series using current numbers)
    st.markdown("### Income / Expenses / Savings Snapshot (sample trend)")
    fig_line = go.Figure()
    # create pseudo-history using the given current values (for demonstration)
    months = ["-3M", "-2M", "-1M", "Now"]
    incomes = [monthly_income*0.9, monthly_income*0.95, monthly_income, monthly_income]
    expenses = [monthly_expenses*1.05, monthly_expenses*1.02, monthly_expenses, monthly_expenses]
    savings_line = [current_savings*0.7, current_savings*0.85, current_savings*0.95, current_savings]

    fig_line.add_trace(go.Scatter(x=months, y=incomes, mode="lines+markers", name="Income"))
    fig_line.add_trace(go.Scatter(x=months, y=expenses, mode="lines+markers", name="Expenses"))
    fig_line.add_trace(go.Scatter(x=months, y=savings_line, mode="lines+markers", name="Savings"))
    fig_line.update_layout(template="plotly_dark", title="Recent Trend (sample)")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("<div class='explain'>These visuals are dynamic — change category amounts in the sidebar to update the pie and trend.</div>", unsafe_allow_html=True)

# -------------------- PDF GENERATION (bottom of every page) --------------------
def generate_pdf_bytes():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "Smart Financial Report — Apka Financial Advisor", ln=1, align="C")
    pdf.ln(4)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(20, 20, 28)
    pdf.multi_cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y')}")
    pdf.ln(4)

    # Summary section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "1) Quick Summary", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6,
                   f"Total (Income + Savings): Rs {total_balance:,.0f}\n"
                   f"Monthly Income: Rs {monthly_income:,.0f}\n"
                   f"Monthly Expenses: Rs {monthly_expenses:,.0f}\n"
                   f"Current Savings: Rs {current_savings:,.0f}\n"
                   f"Net Worth: Rs {net_worth:,.0f}\n"
                   f"Saving Rate: {saving_rate:.1f}%\n")
    pdf.ln(2)

    # Goal & plans
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "2) Goal & Recommended Plans", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6,
                   f"Goal: {goal_purpose} — Target Rs {goal_amount:,.0f}\n"
                   f"Progress: {goal_progress:.1f}% (Rs {current_savings:,.0f} saved)\n"
                   f"Estimated months to goal at current saving pace: {months_to_goal if months_to_goal!=float('inf') else 'N/A'}\n\n"
                   "Recommended Plans (based on your income):\n"
                   f"• Basic Plan (20% of income): Save Rs {int(monthly_income*0.20):,}/month — months to goal: {round((goal_amount-current_savings)/max(1,int(monthly_income*0.20)),1) if int(monthly_income*0.20)>0 else 'N/A'}\n"
                   f"• Strong Plan (30% of income): Save Rs {int(monthly_income*0.30):,}/month — months to goal: {round((goal_amount-current_savings)/max(1,int(monthly_income*0.30)),1) if int(monthly_income*0.30)>0 else 'N/A'}\n")
    pdf.ln(2)

    # Insights explanation
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "3) Insights & Explanation", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6,
                   "This section gives action-oriented suggestions. Read each item and act:\n"
                   "- If you have debt, pay high-interest portions first (credit card, personal loans).\n"
                   "- Build emergency fund = 3–6 months of expenses before aggressive investing.\n"
                   "- Aim saving rate 20%+ as baseline. 30%+ accelerates goals.\n"
                   "- Diversify investments (mix of low-cost index funds, fixed deposits, and a small portion for higher-return instruments if risk-appropriate).\n")
    pdf.ln(2)

    # Spending breakdown
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "4) Spending Breakdown (categories)", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6,
                   f"Food: Rs {food:,}\nTransport: Rs {transport:,}\nShopping: Rs {shopping:,}\nBills: Rs {bills:,}\nFun: Rs {fun:,}\n")
    pdf.ln(4)

    # Footer note
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(90, 90, 100)
    pdf.multi_cell(0, 5, "Report created by Apka Financial Advisor — simple recommendations. This is informational; for large investments or debts consult a licensed financial advisor.")
    # output bytes
    out = BytesIO()
    pdf.output(out)
    return out.getvalue()

# place download link at bottom of page (visible regardless of current nav)
st.markdown("---")
pdf_bytes = generate_pdf_bytes()
b64 = base64.b64encode(pdf_bytes).decode()
st.markdown(
    f'<div style="text-align:center; margin:14px 0;">'
    f'<a href="data:application/pdf;base64,{b64}" download="Apka_Financial_Report_{datetime.now().strftime("%d%m%Y")}.pdf">'
    f'<button class="glow">📄 Download Detailed PDF Report</button></a></div>',
    unsafe_allow_html=True
)
