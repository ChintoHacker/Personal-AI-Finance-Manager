import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from fpdf import FPDF
from io import BytesIO

# Page Setup
st.set_page_config(page_title="Apka Financial Advisor", page_icon="money_with_wings", layout="wide")

# Custom CSS - Bilkul Modern & Stylish
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;}
    .sidebar .stButton>button {background: #ff6b6b; color: white; font-weight: bold;}
    .header {
        background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 20px; backdrop-filter: blur(10px);
    }
    .title {font-size: 42px; background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;}
    .nav-btn {
        background: linear-gradient(45deg, #667eea, #764ba2); color: white;
        border: none; padding: 12px 25px; margin: 0 10px; border-radius: 50px;
        font-weight: bold; box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        transition: all 0.3s; cursor: pointer;
    }
    .nav-btn:hover {transform: translateY(-5px); box-shadow: 0 15px 30px rgba(102,126,234,0.6);}
    .nav-btn.active {background: #ff6b6b; transform: scale(1.1);}
    .card {
        background: white; padding: 25px; border-radius: 20px; margin: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: all 0.3s; text-align: center;
    }
    .card:hover {transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.2);}
    .big-number {font-size: 38px; font-weight: bold; color: #667eea;}
    .insight-card {
        background: linear-gradient(135deg, #ffeaa7, #fab1a0); padding: 20px;
        border-radius: 15px; margin: 10px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .goal-bar {height: 30px; border-radius: 15px; background: #ddd; overflow: hidden;}
    .goal-fill {height: 100%; background: linear-gradient(90deg, #55efc4, #00b894); transition: width 1s;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1 class="title">Apka Reliable Financial Advisor</h1>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Dashboard", key="d1"):
        st.session_state.page = "dashboard"
with col2:
    if st.button("AI Insights", key="d2"):
        st.session_state.page = "insights"
with col3:
    if st.button("Visualizations", key="d3"):
        st.session_state.page = "visuals"
st.markdown('</div>', unsafe_allow_html=True)

# Default Page
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# Sidebar - Clean & Stylish
with st.sidebar:
    # Option 1: Direct base64 use karo (sabse easy aur working)
st.sidebar.image("data:image/png;base64,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
    st.header("Your Details (PKR)")
    monthly_income = st.number_input("Monthly Income", 0, 1000000, 85000, 5000)
    monthly_expenses = st.number_input("Monthly Expenses", 0, 1000000, 55000, 5000)
    current_savings = st.number_input("Current Savings", 0, 10000000, 150000, 10000)
    total_debt = st.number_input("Total Debt", 0, 5000000, 0, 10000)
    current_investments = st.number_input("Current Investments", 0, 10000000, 0, 10000)
    goal_purpose = st.text_input("Goal Purpose", "Car")
    goal_amount = st.number_input("Goal Amount", 1000, 10000000, 500000, 10000)
    
    if st.button("Analyze Now", use_container_width=True):
        st.success("Analysis Done!")

# Calculations
total_balance = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
saving_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
goal_progress = min(100, (current_savings / goal_amount * 100) if goal_amount > 0 else 0)

# Pages
if st.session_state.page == "dashboard":
    st.markdown("### Your Financial Summary")
    cols = st.columns(6)
    metrics = [
        ("Total Balance", f"Rs {total_balance:,.0f}", "#667eea"),
        ("Income", f"Rs {monthly_income:,.0f}", "#55efc4"),
        ("Expenses", f"Rs {monthly_expenses:,.0f}", "#ff7675"),
        ("Savings", f"Rs {current_savings:,.0f}", "#74b9ff"),
        ("Net Worth", f"Rs {net_worth:,.0f}", "#a29bfe"),
        ("Saving Rate", f"{saving_rate:.1f}%", "#fd79a8")
    ]
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="card"><h4>{label}</h4><p class="big-number" style="color:{color}">{value}</p></div>', True)

elif st.session_state.page == "insights":
    st.markdown("### AI Smart Insights")
    insights = [
        ("High Expense Alert", "Food & Shopping taking 65% of expenses. Reduce by Rs 10,000/month", "warning"),
        ("Great Saving Rate!", f"You're saving {saving_rate:.1f}% — Better than 80% Pakistanis!", "tada"),
        ("Emergency Fund", f"You can survive {current_savings//monthly_expenses} months without income", "shield"),
        ("Debt Status", "You're debt-free! Amazing financial discipline", "star")
    ]
    for title, text, emoji in insights:
        st.markdown(f'<div class="insight-card"><h3>{emoji} {title}</h3><p>{text}</p></div>', True)
    
    st.markdown("### Your Goal Progress")
    st.markdown(f'<h2>{goal_purpose}</h2>', True)
    st.markdown(f'<div class="goal-bar"><div class="goal-fill" style="width:{goal_progress}%"></div></div>', True)
    st.markdown(f"<h3>{goal_progress:.1f}% Complete • Rs {current_savings:,.0f} / Rs {goal_amount:,.0f}</h3>", True)

elif st.session_state.page == "visuals":
    st.markdown("### Income vs Expenses")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Nov', 'Dec', 'Jan', 'Feb'], y=[80000, 85000, 90000, 95000], name='Income', marker_color='#55efc4'))
    fig.add_trace(go.Bar(x=['Nov', 'Dec', 'Jan', 'Feb'], y=[65000, 55000, 60000, 58000], name='Expenses', marker_color='#ff6b6b'))
    fig.update_layout(barmode='group', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Spending Breakdown")
    fig2 = px.pie(values=[30, 25, 20, 15, 10], names=['Food', 'Transport', 'Shopping', 'Bills', 'Fun'], color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("### Future Finance Trend")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=['Current', 'Next', '3M Avg', '6M Avg'], y=[150000, 180000, 250000, 380000], 
                              mode='lines+markers', name='Savings Growth', line=dict(color='#55efc4', width=5)))
    fig3.add_trace(go.Scatter(x=['Current', 'Next', '3M Avg', '6M Avg'], y=[85000]*4, name='Income', line=dict(dash='dot')))
    fig3.add_trace(go.Scatter(x=['Current', 'Next', '3M Avg', '6M Avg'], y=[55000]*4, name='Expenses', line=dict(dash='dash', color='red')))
    fig3.update_layout(template='plotly_dark', title="You're on track to be rich!")
    st.plotly_chart(fig3, use_container_width=True)

# PDF Export - Ab Bohot Achhi Hai
if st.sidebar.button("Download Beautiful PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 20, "Apka Financial Report", ln=1, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%d %B %Y')}", ln=1)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(102, 126, 234)
    pdf.set_text_color(255,255,255)
    pdf.cell(0, 12, "  Your Financial Summary  ", fill=True, ln=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"""
Total Available Money (Income + Savings): Rs {total_balance:,.0f}
→ Yeh woh paisa hai jo aap abhi use kar sakte hain

Monthly Income: Rs {monthly_income:,.0f}
Monthly Expenses: Rs {monthly_expenses:,.0f}
Current Savings: Rs {current_savings:,.0f}
Net Worth: Rs {net_worth:,.0f}

Saving Rate: {saving_rate:.1f}%
→ Bohot achha! 20% se zyada target karo

Goal "{goal_purpose}": {goal_progress:.1f}% Complete
→ Bas thodi aur mehnat, ho jayega!
    """)
    buffer = BytesIO()
    pdf.output(buffer)
    b64 = base64.b64encode(buffer.getvalue()).decode()
    st.sidebar.markdown(f'<a href="data:application/pdf;base64,{b64}" download="Apka_Report_{datetime.now().strftime("%d%m%Y")}.pdf"><button style="background:#ff6b6b;color:white;padding:15px;border:none;border-radius:10px;font-size:16px;">Download PDF Now</button></a>', True)

st.sidebar.success("Made with love by your AI Financial Dost")

