import streamlit as st
from datetime import datetime
import math
import time
import plotly.express as px

# ------------------------- PAGE CONFIG -------------------------
st.set_page_config(
    page_title="Smart Financial Advisor",
    page_icon="💸",
    layout="wide"
)

# ------------------------- LOGIN SYSTEM -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ------------------------- DARK/LIGHT MODE -------------------------
theme = st.sidebar.selectbox("Theme Mode", ["Dark", "Light"])

if theme == "Dark":
    bg_color = "linear-gradient(180deg, #224B7D 0%, #6C9E7F 100%)"
    text_color = "white"
else:
    bg_color = "#f5f5f5"
    text_color = "black"

# ------------------------- CSS FIX + ANIMATIONS -------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}
    .fade-in {{
        animation: fadeIn 1.3s ease-in-out;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .rec-card {{
        border-radius: 18px;
        padding: 18px;
        font-size: 18px;
        font-weight: 700;
        color: white;
        margin-top: 15px;
        animation: fadeIn 1s ease-in-out;
    }}
    .rec-red    {{ background:#dc2626; }}
    .rec-orange {{ background:#f97316; }}
    .rec-green  {{ background:#16a34a; }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------- SIDEBAR INPUTS -------------------------
with st.sidebar:
    st.header("📌 Your Financial Inputs")

    monthly_income = st.number_input("Monthly Income (PKR)", 0, value=85000)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", 0, value=55000)
    current_savings = st.number_input("Current Savings (PKR)", 0, value=150000)
    total_debt = st.number_input("Total Debt (PKR)", 0, value=0)
    current_investments = st.number_input("Current Investments (PKR)", 0, value=50000)

    st.markdown("---")
    goal_name = st.text_input("Goal Name", "Dream House")
    goal_amount = st.number_input("Goal Target (PKR)", 1, value=5000000)

    if st.button("Analyze / Predict"):
        st.success("Updated ✔")

# ------------------------- CALCULATIONS -------------------------
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100, (current_savings / goal_amount) * 100)
eta_months = (
    "N/A" if monthly_save == 0 else round((goal_amount - current_savings) / monthly_save)
)

# ------------------------- HEADER -------------------------
st.markdown("<h1 class='fade-in' style='text-align:center;'>💸 Smart Financial Advisor</h1>", unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align:center; font-size:17px;'>{datetime.now().strftime('%d %B %Y')}</p>",
    unsafe_allow_html=True
)

# ------------------------- OVERVIEW CARDS -------------------------
st.subheader("📊 Overview — Quick Snapshot")

c1, c2, c3, c4, c5 = st.columns(5)

cards = [
    ("Total Amount", total_amount),
    ("Monthly Income", monthly_income),
    ("Expenses", monthly_expenses),
    ("Savings", current_savings),
    ("Net Worth", net_worth)
]

for col, (label, val) in zip([c1,c2,c3,c4,c5], cards):
    col.markdown(
        f"""
        <div class='fade-in' style="
            background:rgba(255,255,255,0.18);
            border-radius:14px;
            padding:18px;
            text-align:center;
            color:white;">
            <h4>{label}</h4>
            <h2>Rs {val:,}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------- RECOMMENDATIONS -------------------------
if goal_progress < 50:
    rec_class = "rec-red"
    rec_msg = "Goal bohot peeche hai — Monthly savings increase karein."
    rec_msg2 = "Kam az kam Rs 10,000 extra save karna start karein."
elif goal_progress < 90:
    rec_class = "rec-orange"
    rec_msg = "Progress theek hai — Bas consistency rakhein."
    rec_msg2 = "Auto-save enable karna helpful hoga."
else:
    rec_class = "rec-green"
    rec_msg = "Aap goal ke bohot qareeb hain — Shabash!"
    rec_msg2 = "Next financial goal set karein."

st.markdown(
    f"""
    <div class="rec-card {rec_class}">
        {rec_msg}<br>{rec_msg2}
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------- GOAL PROGRESS -------------------------
st.subheader(f"🎯 Goal Progress — {goal_name}")

st.progress(goal_progress / 100)

st.write(
    f"**{goal_progress:.1f}%** complete • **ETA:** {eta_months} months"
)

# ------------------------- CHARTS -------------------------
st.subheader("📈 Financial Growth Chart")

chart_data = {
    "Category": ["Income", "Expenses", "Savings", "Investments"],
    "Amount": [monthly_income, monthly_expenses, current_savings, current_investments]
}

fig = px.bar(chart_data, x="Category", y="Amount", title="Financial Overview", text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# ------------------------- FOOTER -------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2025 Smart Financial Advisor • Made with ❤️ in Pakistan 🇵🇰")
