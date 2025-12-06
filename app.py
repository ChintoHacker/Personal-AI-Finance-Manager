# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Apka Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Custom CSS for Glow & Style -------------------
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .stButton>button {
        background: linear-gradient(90deg, #1e88e5, #42a5f5);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(30,144,255,0.4);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30,144,255,0.6);
    }
    .title {
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #0d47a1, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .goal-card {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(76,175,80,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ------------------- Title -------------------
st.markdown("<h1 class='title'>Apka Reliable Financial Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555; font-size:18px;'>Smart • Simple • Secure 💙</p>", unsafe_allow_html=True)

# ------------------- Sidebar Inputs -------------------
with st.sidebar:
    st.header("📊 Your Financial Details (PKR)")
    
    monthly_income = st.number_input("Monthly Income", min_value=0.0, value=0.0, step=1000.0)
    monthly_expenses = st.number_input("Monthly Expenses", min_value=0.0, value=0.0, step=1000.0)
    current_savings = st.number_input("Current Savings", min_value=0.0, value=0.0, step=1000.0)
    total_debt = st.number_input("Total Debt", min_value=0.0, value=0.0, step=1000.0)
    current_investments = st.number_input("Current Investments", min_value=0.0, value=0.0, step=1000.0)
    
    st.markdown("---")
    goal_purpose = st.text_input("Saving Goal Purpose", "Birthday Present")
    goal_amount = st.number_input("Goal Amount (PKR)", min_value=0.0, value=4000.0, step=500.0)
    saved_for_goal = st.number_input("Already Saved for Goal", min_value=0.0, value=1500.0, step=100.0)
    
    if st.button("🚀 Analyze & Predict", use_container_width=True):
        st.session_state.analyzed = True
        st.success("Analysis Complete!")

# ------------------- Calculations -------------------
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

if st.session_state.analyzed:
    net_worth = current_savings + current_investments - total_debt
    monthly_saving = monthly_income - monthly_expenses
    saving_rate = (monthly_saving / monthly_income * 100) if monthly_income > 0 else 0
    goal_progress = (saved_for_goal / goal_amount) * 100 if goal_amount > 0 else 0
else:
    net_worth = monthly_saving = saving_rate = goal_progress = 0

# ------------------- Tabs -------------------
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "🤖 AI Insights", "📈 Visualizations"])

# ==================== TAB 1: Dashboard ====================
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>Monthly Income</h3><h2>Rs {monthly_income:,.0f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>Monthly Expenses</h3><h2>Rs {monthly_expenses:,.0f}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>Monthly Savings</h3><h2>Rs {monthly_saving:,.0f}</h2></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"<div class='metric-card'><h3>Net Worth</h3><h2 style='color:#2e7d32;'>Rs {net_worth:,.0f}</h2></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div class='metric-card'><h3>Saving Rate</h3><h2 style='color:#1976d2;'>{ saving_rate:.1f}%</h2></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='metric-card'><h3>Emergency Fund</h3><h2 style='color:#e65100;'>{(monthly_expenses*3):,.0f} Needed</h2></div>", unsafe_allow_html=True)

# ==================== TAB 2: AI Insights ====================
with tab2:
    st.subheader("🎯 Your Savings Goal")
    st.markdown(f"<div class='goal-card'><h3>{goal_purpose}</h3><p>Target: Rs {goal_amount:,.0f} | Saved: Rs {saved_for_goal:,.0f}</p>", unsafe_allow_html=True)
    st.progress(goal_progress / 100)
    st.write(f"**{goal_progress:.1f}%** Complete • {13} days left")

    st.markdown("### 💡 AI Financial Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("💸 You spent **Rs 5,000** on Education this month.")
        st.warning("🍔 Food expenses increased by 42%")
    with col2:
        st.success("✅ You're saving **{:.1f}%** of income – Great job!".format(saving_rate))
        st.info("📈 Consider investing Rs 10,000 in Mutual Funds")

    st.markdown("### 🛡️ Emergency Fund Status")
    months_covered = current_savings / monthly_expenses if monthly_expenses > 0 else 0
    if months_covered >= 6:
        st.success(f"Excellent! You have {months_covered:.1f} months covered.")
    elif months_covered >= 3:
        st.warning(f"Good! You have {months_covered:.1f} months covered.")
    else:
        st.error(f"Build emergency fund! Only {months_covered:.1f} months covered.")

# ==================== TAB 3: Visualizations ====================
with tab3:
    # Spending by Category (Pie Chart)
    categories = ["Food", "Transport", "Education", "Personal Care", "Shopping", "Entertainment"]
    amounts = [8000, 5000, 5000, 3000, 4000, 2000]
    fig_pie = px.pie(values=amounts, names=categories, color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_pie.update_layout(title="Spending by Category")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Income vs Expenses (Bar)
    months = ["Jan", "Feb", "Mar", "Apr"]
    income_data = [80000, 85000, 90000, 95000]
    expense_data = [60000, 62000, 58000, 65000]
    fig_bar = go.Figure(data=[
        go.Bar(name='Income', x=months, y=income_data, marker_color='#42a5f5'),
        go.Bar(name='Expenses', x=months, y=expense_data, marker_color='#ef5350')
    ])
    fig_bar.update_layout(barmode='group', title="Income vs Expenses (Last 4 Months)")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Future Trend Prediction
    future_months = ["Current", "Next Month", "3-Month Avg", "6-Month Avg"]
    predicted_savings = [current_savings, current_savings + monthly_saving*3, current_savings + monthly_saving*9, current_savings + monthly_saving*18]
    fig_line = px.line(x=future_months, y=predicted_savings, markers=True, title="Aapka Future Finance Trend (Predicted)")
    fig_line.update_traces(line=dict(color="#42a5f5", width=4))
    fig_line.add_scatter(x=future_months, y=[monthly_income]*4, mode='lines', name="Income", line=dict(dash='dot'))
    fig_line.add_scatter(x=future_months, y=[monthly_expenses]*4, mode='lines', name="Expenses", line=dict(dash='dash', color='red'))
    st.plotly_chart(fig_line, use_container_width=True)

# ------------------- PDF Export Button -------------------
def create_pdf_report():
    html = f"""
    <h1 style='text-align:center; color:#0d47a1;'>Apka Financial Report - {datetime.now().strftime('%B %Y')}</h1>
    <h2>Summary</h2>
    <p><strong>Monthly Income:</strong> Rs {monthly_income:,.0f}</p>
    <p><strong>Monthly Expenses:</strong> Rs {monthly_expenses:,.0f}</p>
    <p><strong>Net Worth:</strong> Rs {net_worth:,.0f}</p>
    <p><strong>Saving Rate:</strong> {saving_rate:.1f}%</p>
    <h2>Savings Goal: {goal_purpose}</h2>
    <p>Progress: {goal_progress:.1f}%</p>
    """
    return html

if st.button("📄 Download PDF Report"):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Apka Financial Report", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%d %B %Y')}", ln=1)
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, f"Monthly Income: Rs {monthly_income:,.0f}\n"
                         f"Monthly Expenses: Rs {monthly_expenses:,.0f}\n"
                         f"Net Worth: Rs {net_worth:,.0f}\n"
                         f"Saving Rate: {saving_rate:.1f}%\n"
                         f"Goal: {goal_purpose} - {goal_progress:.1f}% Complete")
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="Apka_Finance_Report.pdf">Download Your PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("---")
st.caption("Made with ❤️ by Hacker Boy • Your Personal AI Finance Advisor")
