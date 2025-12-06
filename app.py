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
    
    st.sidebar.image("https://img.icons8.com/fluency/100/money-bag.png", width=100)
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


