# app_redesigned.py
# Gorgeous Redesigned Streamlit App for Personal AI Finance Manager
# - Landing page (impressive + interactive)
# - Page 2: Saving Goals, AI Insights, Emergency & Investment (beautiful cards + popups)
# - Page 3: Visualizations (kept as before)
# - Sidebar: colored, upgraded controls with glowing buttons
# Notes: Save this file as app_redesigned.py and run with `streamlit run app_redesigned.py`.

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import altair as alt

st.set_page_config(page_title="Personal AI Finance Manager", page_icon="💠", layout="wide")

# ---------- Custom CSS for Gorgeous Look ----------
st.markdown("""
<style>
:root{--bg:#eaf6ff;--card:#ffffff;--accent:#0b84ff;--accent-2:#00c2a8;--muted:#6c757d}
body { background: var(--bg); }
.block-container { padding: 28px; }
/* Header Glow */
.header-glow{
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight:800;
  color: #04263b;
  font-size:42px;
  text-shadow: 0 6px 20px rgba(11,132,255,0.18), 0 2px 6px rgba(0,0,0,0.06);
}
.header-sub{
  color: #0b4f7a; margin-top: -8px; margin-bottom: 18px;
}
/* Glowing Buttons */
.glow-btn{ display:inline-block; padding:12px 20px; border-radius:12px; color:white; font-weight:600; text-align:center; cursor:pointer; border:none;}
.btn-analyze{ background: linear-gradient(90deg, #007bff, #00c2a8); box-shadow: 0 10px 30px rgba(11,132,255,0.18);}
.btn-report{ background: linear-gradient(90deg, #ff8a00, #ff3d71); box-shadow: 0 10px 30px rgba(255,138,0,0.18);}
.btn-reset{ background: linear-gradient(90deg, #6c757d, #343a40); box-shadow: 0 8px 20px rgba(0,0,0,0.12);}
.glow-btn:hover{ transform: translateY(-4px); filter:brightness(1.03); }
/* Card style */
.stat-card{ background: var(--card); border-radius:14px; padding:18px; box-shadow: 0 6px 20px rgba(5,40,60,0.06); border-left:6px solid rgba(11,132,255,0.14);}
.stat-title{ color:#6c757d; font-size:14px; }
.stat-value{ color:#04263b; font-size:26px; font-weight:700; }
.stat-sub{ color:var(--muted); font-size:12px; margin-top:6px }
/* Sidebar */
section[data-testid="stSidebar"] .css-1d391kg{ background: linear-gradient(180deg,#f2fbff,#e6f5ff); border-radius:8px; padding:18px; }
.sidebar-h{ font-weight:700; color:#04263b }
.small-muted{ color: #6c757d; font-size:13px }
/* Insight card */
.insight{ background: linear-gradient(180deg,#ffffff,#fbfdff); border-radius:12px; padding:18px; box-shadow:0 8px 20px rgba(3,50,75,0.06);}
.invest-popup{ background:linear-gradient(90deg,#fff, #f7fff9); border-radius:10px; padding:14px; }
</style>
""", unsafe_allow_html=True)

# ---------- Helpers: Load / Train Model (cached) ----------
@st.cache_resource
def load_and_train_model(path_csv="personal_finance_tracker_dataset.csv"):
    try:
        df = pd.read_csv(path_csv)
    except FileNotFoundError:
        # Create a tiny synthetic dataset so UI works even without CSV
        dates = pd.date_range(end=pd.Timestamp.today(), periods=24, freq='M')
        df = pd.DataFrame({
            'date': dates,
            'monthly_income': np.random.randint(40000, 120000, size=len(dates)),
            'monthly_expense_total': np.random.randint(20000, 90000, size=len(dates)),
            'actual_savings': np.random.randint(5000, 40000, size=len(dates)),
            'credit_score': np.random.randint(550, 800, size=len(dates))
        })
    df.columns = df.columns.str.strip()
    df['date'] = pd.to_datetime(df['date'])
    df_monthly = df.groupby(pd.Grouper(key='date', freq='ME')).agg({
        'monthly_income': 'mean',
        'monthly_expense_total': 'mean',
        'actual_savings': 'mean',
        'credit_score': 'mean'
    }).reset_index().fillna(0)
    df_monthly = df_monthly.rename(columns={'monthly_income': 'income', 'monthly_expense_total': 'expenses', 'actual_savings': 'savings'})
    df_monthly['extra_spendings'] = np.maximum(0, df_monthly['expenses'] - df_monthly['savings'])
    # We will predict next-month saving only internally (but NOT show the 3/6 averages as user requested)
    df_monthly['savings_next_1'] = df_monthly['savings'].shift(-1)
    df_monthly = df_monthly.dropna()
    X = df_monthly[['income', 'expenses', 'extra_spendings', 'credit_score']]
    Y = df_monthly[['savings_next_1']]
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    X_train, X_test, Y_train, Y_test = train_test_split(Xs, Y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X_train, Y_train.values.ravel())
    return model, scaler

model, scaler = load_and_train_model()

# ---------- Sidebar (Upgraded) ----------
with st.sidebar:
    st.markdown("<div class='sidebar-h'>Personal AI Finance — Controls</div>", unsafe_allow_html=True)
    st.markdown("---")
    monthly_income = st.number_input("Monthly Income (PKR)", min_value=0.0, value=50000.0, step=1000.0)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", min_value=0.0, value=30000.0, step=1000.0)
    current_savings = st.number_input("Current Savings (PKR)", min_value=0.0, value=15000.0, step=1000.0)
    debt = st.number_input("Total Debt (PKR)", min_value=0.0, value=0.0, step=1000.0)
    investments = st.number_input("Current Investments (PKR)", min_value=0.0, value=0.0, step=1000.0)
    st.markdown("---")
    goal_purpose = st.text_input("Saving Goal Purpose", value="Car")
    goal_amount = st.number_input("Goal Amount (PKR)", min_value=0.0, value=100000.0, step=1000.0)
    st.markdown("---")
    # Glowing buttons inside sidebar (styled using markdown + button actions)
    if st.button("🔍 Analyze — Quick", key="sb_analyze"):
        st.session_state['analyze_click'] = True
    if st.button("📄 Download Quick Report", key="sb_report"):
        st.session_state['report_click'] = True
    if st.button("♻️ Reset Inputs", key="sb_reset"):
        # Reset to defaults (simple approach)
        st.experimental_rerun()

# ---------- Main Layout: Top navigation (3 pages) ----------
page = st.radio("", ("Landing Dashboard", "Insights & Goals", "Visualizations"), horizontal=True)

# ---------- Utility calculations ----------
def compute_financials(income, expenses, savings, debt, investments):
    total_balance = income - expenses + savings
    net_worth = savings + investments - debt
    saving_rate = (savings / income) * 100 if income > 0 else 0
    expense_rate = (expenses / income) * 100 if income > 0 else 0
    monthly_saving = income - expenses
    emergency_needed = expenses * 6
    emergency_progress = min(savings / emergency_needed, 1.0) if emergency_needed>0 else 0
    return {
        'total_balance': total_balance,
        'net_worth': net_worth,
        'saving_rate': saving_rate,
        'expense_rate': expense_rate,
        'monthly_saving': monthly_saving,
        'emergency_needed': emergency_needed,
        'emergency_progress': emergency_progress
    }

fin = compute_financials(monthly_income, monthly_expenses, current_savings, debt, investments)

# ---------- Page 1: Gorgeous Landing Dashboard ----------
if page == "Landing Dashboard":
    # Header
    st.markdown("<div class='header-glow'>💠 Personal AI Finance Manager</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>A beautiful, interactive quick view of your finances</div>", unsafe_allow_html=True)

    # Three big glowing buttons
    c1, c2, c3 = st.columns([3,3,2])
    with c1:
        if st.button("Analyze Finances", key="main_analyze"):
            st.session_state['analyze_click'] = True
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with c2:
        if st.button("Generate Report", key="main_report"):
            st.session_state['report_click'] = True
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with c3:
        if st.button("Reset", key="main_reset"):
            st.experimental_rerun()

    st.write("---")

    # Final Predictions Section (Gorgeous Cards, Only the requested KPIs)
    st.markdown("<div style='display:flex;gap:18px'>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-title'>Total Balance</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-value'>{fin['total_balance']:,.2f} PKR</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-sub'>Income - Expenses + Savings</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with k2:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-title'>Net Worth</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-value'>{fin['net_worth']:,.2f} PKR</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-sub'>Savings + Investments - Debt</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with k3:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-title'>Monthly Saving</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-value'>{fin['monthly_saving']:,.2f} PKR</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-sub'>Income - Expenses</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with k4:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-title'>Savings Ratio</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-value'>{fin['saving_rate']:.2f}%</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-sub'>Current Savings / Income</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<div class='insight'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin:6px 0 10px 0'>Final Predictions</h3>", unsafe_allow_html=True)
    st.write("KPI summary: Only essential numbers shown here for a clean quick decision-making view.")
    st.markdown("</div>", unsafe_allow_html=True)

    # If user clicked analyze via any button, show a short modal-like expander with tips
    if st.session_state.get('analyze_click'):
        with st.expander("🔔 Pro Tips & Next Steps (Interactive)", expanded=True):
            st.write("- Automate savings with standing instructions to reach goals faster.")
            st.write("- Revisit budget categories monthly and move 10% of 'wants' to 'savings' when possible.")
            st.write("- Consider a high-yield savings account for emergency funds.")

# ---------- Page 2: Insights & Goals (Beautiful cards + popups) ----------
elif page == "Insights & Goals":
    st.markdown("<div class='header-glow'>Insights & Smart Goals</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>Gorgeous cards, interactive insight boxes and improved investment suggestions</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2,1])

    with col_left:
        # Saving Goal Card
        st.markdown("<div class='insight'>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='margin-bottom:6px'>🎯 Saving Goal — {goal_purpose}</h4>", unsafe_allow_html=True)
        st.write(f"Goal Target: {goal_amount:,.0f} PKR")
        if fin['monthly_saving'] > 0:
            months_needed = goal_amount / fin['monthly_saving']
            st.markdown(f"<b>At current monthly saving ({fin['monthly_saving']:,.0f} PKR):</b> ~ {months_needed:.0f} months (~{months_needed/12:.1f} years)", unsafe_allow_html=True)
        else:
            st.error("You are not saving monthly. Increase income or reduce expenses to start progress.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # AI Insight Card (Redesigned + colorful)
        st.markdown("<div class='insight'>", unsafe_allow_html=True)
        st.markdown("<h4>🤖 AI Insights</h4>", unsafe_allow_html=True)
        st.write(f"Savings Ratio: **{fin['saving_rate']:.1f}%** — Expense Ratio: **{fin['expense_rate']:.1f}%**")
        # Better looking suggestion boxes
        if fin['expense_rate'] > 80:
            st.warning("High Spending! Aap 80%+ income kharch kar rahe ho. Consider trimming wants and subscriptions.")
        elif fin['expense_rate'] > 60:
            st.info("Balanced but improve savings — try pushing savings to 20%+")
        else:
            st.success("Great — good control on expenses!")
        # Fancy small interactive popup for deeper suggestions
        if st.button("Show detailed AI suggestions", key="ai_popup"):
            with st.modal("AI Suggestions"):
                st.markdown("<div style='padding:8px;'>", unsafe_allow_html=True)
                st.write("**Personalized Suggestions:**")
                st.write("1. Setup auto-transfer to savings every payday.")
                st.write("2. Use 30-day rules: freeze one non-essential spending for a month and track results.")
                st.write("3. Consider index funds for long-term investments if you can consistently save.")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Emergency Fund Card
        st.markdown("<div class='insight'>", unsafe_allow_html=True)
        st.markdown("<h4>🛟 Emergency Fund</h4>", unsafe_allow_html=True)
        st.write(f"Needed (6 months): {fin['emergency_needed']:,.0f} PKR")
        st.write(f"Progress: {current_savings:,.0f} / {fin['emergency_needed']:,.0f}")
        st.progress(fin['emergency_progress'])
        if fin['emergency_progress'] < 0.5:
            st.warning("Emergency fund kam hai — aim for automatic transfers each month until target.")
        else:
            st.success("Good progress on emergency fund — keep reviewing yearly.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Investment Recommendation (Upgraded & popup)
        st.markdown("<div class='insight'>", unsafe_allow_html=True)
        st.markdown("<h4>💼 Investment Recommendations</h4>", unsafe_allow_html=True)
        # Use friendly buckets
        saving_rate_percent = fin['monthly_saving'] / monthly_income if monthly_income>0 else 0
        if saving_rate_percent > 0.3:
            st.success("Aggressive Profile")
            st.write("Recommendation: Consider a growth-heavy portfolio — e.g., equity index funds, small allocation to international funds and gold.")
        elif saving_rate_percent > 0.1:
            st.info("Balanced Profile")
            st.write("Recommendation: Balanced mix — equities + bonds + small gold allocation.")
        else:
            st.warning("Conservative / Starting Profile")
            st.write("Recommendation: Build emergency fund first. Then start with low-cost bond funds and small equity SIPs.")

        # Pop-up deep-dive (modal) for portfolio examples
        if st.button("See sample portfolios & risks", key="invest_popup"):
            with st.modal("Sample Portfolios & Risk"):
                st.markdown("<div class='invest-popup'>", unsafe_allow_html=True)
                st.write("**Aggressive (for high savers):** 80% Stocks, 15% Bonds, 5% Gold — High risk, high return over long-term.")
                st.write("**Balanced:** 60% Stocks, 35% Bonds, 5% Gold — Moderate risk.")
                st.write("**Conservative:** 40% Stocks, 55% Bonds, 5% Gold — Lower volatility.")
                st.write("")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Page 3: Visualizations (unchanged logic but nice look) ----------
else:
    st.markdown("<div class='header-glow'>Interactive Visualizations</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>Charts to help you understand income, expenses and trend</div>", unsafe_allow_html=True)

    # Income vs Expenses bar
    data_bar = pd.DataFrame({'Category': ['Income', 'Expenses'], 'Amount': [monthly_income, monthly_expenses]})
    chart_bar = alt.Chart(data_bar).mark_bar().encode(
        x='Category', y='Amount', tooltip=['Category', 'Amount']
    ).properties(width=600, height=350, title='Monthly Income vs Expenses')
    st.altair_chart(chart_bar, use_container_width=True)

    # Expense distribution (synthetic categories)
    categories = ["Food", "Bills", "Travel", "Shopping", "Health"]
    vals = [monthly_expenses*0.2, monthly_expenses*0.25, monthly_expenses*0.15, monthly_expenses*0.3, monthly_expenses*0.1]
    data_pie = pd.DataFrame({'Category': categories, 'Amount': vals})
    chart_pie = alt.Chart(data_pie).mark_arc().encode(theta='Amount:Q', color='Category:N', tooltip=['Category','Amount']).properties(width=600, height=350, title='Expense Distribution')
    st.altair_chart(chart_pie, use_container_width=True)

    # Trend placeholder
    data_trend = pd.DataFrame({
        'Month': ['Now','1 Month','2 Months','3 Months'],
        'Savings': [current_savings, current_savings + fin['monthly_saving'], current_savings + fin['monthly_saving']*2, current_savings + fin['monthly_saving']*3]
    })
    chart_line = alt.Chart(data_trend).mark_line(point=True).encode(x='Month', y='Savings').properties(width=800, height=350, title='Savings Trend (Projection)')
    st.altair_chart(chart_line, use_container_width=True)

# ---------- PDF Report Generation (neat & clean) ----------
if st.session_state.get('report_click'):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Personal AI Finance Manager — Quick Report", styles['Title']))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Paragraph(f"Income: {monthly_income:,.2f} PKR | Expenses: {monthly_expenses:,.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"Net Worth: {fin['net_worth']:,.2f} PKR", styles['Normal']))
    story.append(Paragraph(f"Savings Ratio: {fin['saving_rate']:.2f}% | Expense Ratio: {fin['expense_rate']:.2f}%", styles['Normal']))
    story.append(Paragraph(f"Goal: {goal_purpose} — {goal_amount:,.2f} PKR", styles['Normal']))
    story.append(Paragraph("\nRecommendations:", styles['Heading3']))
    story.append(Paragraph("1. Automate savings. 2. Build emergency fund to 6 months. 3. Start conservative investments if you have <20% savings rate.", styles['Normal']))
    doc.build(story)
    pdf_buffer.seek(0)
    st.download_button("Download Full Report", pdf_buffer, file_name="finance_quick_report.pdf", mime="application/pdf")
    st.session_state['report_click'] = False

# End of file
