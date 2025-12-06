import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Apka Financial Advisor", page_icon="💸", layout="wide")

# ========== ADVANCED MODERN CSS ==========
st.markdown("""
<style>
body {background:#0f172a;}
.main {background: linear-gradient(135deg, #0f172a, #020617);}

.glow-btn button {
    background: linear-gradient(45deg, #7c3aed, #3b82f6);
    color: white; border: none; padding: 14px 30px;
    border-radius: 50px; font-weight: bold;
    box-shadow: 0 0 15px rgba(124,58,237,0.8);
    transition: 0.3s ease;
}
.glow-btn button:hover {
    box-shadow: 0 0 40px rgba(124,58,237,1);
    transform: scale(1.08);
}

.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.08);
    transition: .3s ease;
}
.card:hover {transform: translateY(-5px);}

.insight {
    background: linear-gradient(135deg, #1e293b, #020617);
    padding: 20px;
    border-radius: 16px;
    border-left: 6px solid #7c3aed;
    margin-bottom: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

.progress-bar {
    background:#1e293b;
    border-radius: 20px;
    overflow: hidden;
    height: 28px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
}

.progress-fill {
    height:100%;
    background:linear-gradient(90deg,#22c55e,#4ade80);
    box-shadow: 0 0 15px rgba(34,197,94,0.9);
    transition: width 0.8s ease;
}

.pdf-btn {
    background: linear-gradient(45deg,#22c55e,#16a34a);
    color:white;padding:14px;border:none;border-radius:12px;
    font-size:16px;font-weight:bold;cursor:pointer;
    box-shadow:0 0 20px rgba(34,197,94,0.8);
}
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://img.icons8.com/fluency/100/money-bag.png", width=100)
    st.header("Your Data")

    monthly_income = st.number_input("Monthly Income", 0, 1000000, 85000, 5000)
    monthly_expenses = st.number_input("Monthly Expenses", 0, 1000000, 55000, 5000)
    current_savings = st.number_input("Current Savings", 0, 10000000, 150000, 10000)
    total_debt = st.number_input("Total Debt", 0, 5000000, 0, 10000)
    current_investments = st.number_input("Investments", 0, 10000000, 0, 10000)

    goal_purpose = st.text_input("Goal Name", "Car")
    goal_amount = st.number_input("Goal Amount", 1000, 10000000, 500000, 10000)

    st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
    analyze = st.button("Analyze Now")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== CALCULATIONS ==========
total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
saving_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income else 0
goal_progress = min(100, (current_savings / goal_amount * 100)) if goal_amount else 0
months_left = round((goal_amount - current_savings) / max(1, (monthly_income - monthly_expenses)),1)

# ========== TOP NAV ==========
col1,col2,col3 = st.columns(3)
with col1:
    st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
    if st.button("Dashboard"): st.session_state.page="dashboard"
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
    if st.button("AI Insights"): st.session_state.page="insights"
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
    if st.button("Visuals"): st.session_state.page="visuals"
    st.markdown('</div>', unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page="dashboard"

# ========== DASHBOARD ==========
if st.session_state.page=="dashboard":
    st.title("📊 Smart Financial Dashboard")

    a,b,c,d = st.columns(4)
    cards = [
        ("Total Balance", total_balance),
        ("Monthly Income", monthly_income),
        ("Monthly Expenses", monthly_expenses),
        ("Net Worth", net_worth)
    ]
    for col,(title,val) in zip([a,b,c,d],cards):
        with col:
            st.markdown(f"""
            <div class="card">
            <h4>{title}</h4>
            <h2>Rs {val:,.0f}</h2>
            </div>
            """,True)

# ========== AI INSIGHTS ==========
elif st.session_state.page=="insights":
    st.title("🤖 AI Smart Insights")

    insights = [
        f"💡 You save {saving_rate:.1f}% of income — Great job!",
        f"📉 You can reach your goal in approx {months_left} months",
        f"🛡️ Emergency survival: {round(current_savings/max(1,monthly_expenses),1)} months",
        "✅ Your financial stability is improving"
    ]

    for msg in insights:
        st.markdown(f'<div class="insight">{msg}</div>',True)

    st.subheader("🎯 Goal Progress")
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width:{goal_progress}%"></div>
    </div>
    <h3>{goal_progress:.1f}% — Rs {current_savings:,.0f} / Rs {goal_amount:,.0f}</h3>
    """,True)

# ========== VISUAL PAGE (IMPROVED) ==========
elif st.session_state.page=="visuals":
    st.title("📈 Smart Visuals")

    # Improved Bar Chart
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Income", x=["Jan","Feb","Mar","Apr"], y=[80000,85000,90000,95000]))
    fig.add_trace(go.Bar(name="Expenses", x=["Jan","Feb","Mar","Apr"], y=[60000,62000,65000,68000]))
    fig.update_layout(barmode="group", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Improved Line Chart
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=["Now","+1M","+3M","+6M"], y=[150000,180000,220000,300000], mode="lines+markers"))
    fig2.update_layout(template="plotly_dark", title="Savings Growth Prediction")
    st.plotly_chart(fig2, use_container_width=True)

# ========== PERFECT PDF EXPORT ==========
if st.sidebar.button("📄 Download Smart PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",20)
    pdf.cell(0,10,"Smart Financial Report",ln=1,align="C")

    pdf.set_font("Arial","",12)
    pdf.cell(0,10,f"Generated: {datetime.now().strftime('%d %B %Y')}",ln=1)

    pdf.ln(5)
    pdf.cell(0,10,f"Total Balance: Rs {total_balance:,.0f}",ln=1)
    pdf.cell(0,10,f"Income: Rs {monthly_income:,.0f}",ln=1)
    pdf.cell(0,10,f"Expenses: Rs {monthly_expenses:,.0f}",ln=1)
    pdf.cell(0,10,f"Savings: Rs {current_savings:,.0f}",ln=1)
    pdf.cell(0,10,f"Net Worth: Rs {net_worth:,.0f}",ln=1)
    pdf.ln(5)
    pdf.cell(0,10,f"Goal: {goal_purpose}",ln=1)
    pdf.cell(0,10,f"Progress: {goal_progress:.1f}%",ln=1)

    buf = BytesIO()
    pdf.output(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()

    st.sidebar.markdown(
        f'<a href="data:application/pdf;base64,{b64}" download="Smart_Report.pdf">'
        f'<button class="pdf-btn">✅ Download PDF Now</button></a>',
        unsafe_allow_html=True
    )
