import streamlit as st
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import requests

# -------------------------------------------------------------------------
#  LOTTIE LOADER (Simple function to load animations)
# -------------------------------------------------------------------------
def load_lottie(url):
    try:
        return requests.get(url).json()
    except:
        return None

# -------------------------------------------------------------------------
#  PAGE CONFIG
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Your Financial Advisor — Smart AI",
    page_icon="💸",
    layout="wide"
)

# -------------------------------------------------------------------------
#  FULL PREMIUM NEON + ANIMATED GRADIENT UI
# -------------------------------------------------------------------------
st.markdown("""
<style>

/* Global Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700;900&display=swap');

html, body, .stApp {
    font-family: 'Poppins', sans-serif;
}

/* 🔥 Animated Background */
.stApp {
    background: linear-gradient(135deg, #0f0029, #001933, #003a52, #00233f);
    background-size: 350% 350%;
    animation: gradientShift 14s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Smooth Page Transition */
.main, .block-container {
    animation: fadePage 0.7s ease;
}
@keyframes fadePage {
    0% { opacity: 0; transform: translateY(15px);}
    100%{ opacity: 1; transform: translateY(0);}
}

/* Section slide animation */
.section-animate {
    animation: slideIn 1s ease;
}
@keyframes slideIn {
    0% {opacity:0; transform:translateX(-30px);}
    100%{opacity:1; transform:translateX(0);}
}

/* Neon Header Glow */
.app-title {
    font-size: 44px !important;
    font-weight: 900 !important;
    color: #8af8d4 !important;
    text-align: center;
    text-shadow: 0 0 12px #7bf4c8, 0 0 26px #76ffd2;
    animation: floatTitle 4s ease infinite;
}
@keyframes floatTitle {
    0% {transform: translateY(0);}
    50%{transform: translateY(-6px);}
    100%{transform: translateY(0);}
}

/* Sidebar Glass Effect */
.stSidebar {
    background: rgba(0,0,0,0.45) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.15);
}

/* Sidebar input visibility */
.stSidebar input {
    background: rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Input container */
.input-section {
    background: rgba(255,255,255,0.15);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.25);
}

/* Navigation Buttons */
.stButton>button {
    background: linear-gradient(45deg, #8b5cf6, #ec4899);
    background-size: 200% 200%;
    animation: btnGlow 4s ease infinite;
    padding: 12px 28px;
    border-radius: 50px;
    border: none;
    font-size: 18px;
    font-weight: 800;
    color: white;
    box-shadow: 0 10px 24px rgba(139,92,246,0.4);
    transition: 0.3s;
}
.stButton>button:hover {
    transform: translateY(-4px) scale(1.04);
    box-shadow: 0 16px 40px rgba(139,92,246,0.6);
}
@keyframes btnGlow {
    0% {background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

/* Neon Cards */
.overview-card {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.22);
    padding: 26px;
    border-radius: 20px;
    backdrop-filter: blur(14px);
    text-align: center;
    box-shadow: 0 12px 36px rgba(0,0,0,0.55);
    transition: 0.3s;
}
.overview-card:hover {
    transform: translateY(-10px);
}

/* Card text */
.card-label {
    color: #dce7ff;
    font-size: 16px;
    font-weight: 600;
}
.card-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
}

/* Goal Box */
.goal-box {
    background: rgba(255,255,255,0.15);
    padding: 32px;
    border-radius: 25px;
    border: 1.5px solid rgba(255,255,255,0.25);
    animation: floatBox 5s ease-in-out infinite;
    box-shadow: 0 14px 45px rgba(0,0,0,0.55);
}
@keyframes floatBox {
    0% {transform:translateY(0);}
    50%{transform:translateY(-8px);}
    100%{transform:translateY(0);}
}

/* Goal Progress Bar */
.goal-bar {
    height: 34px;
    background: rgba(255,255,255,0.22);
    border-radius: 14px;
    overflow: hidden;
}
.goal-fill {
    height: 100%;
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    transition: width 0.7s ease;
}

/* Recommendation Boxes */
.rec-box {
    padding: 26px;
    border-radius: 18px;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.55);
}
.rec-red    { background: rgba(239,68,68,0.28); border-left: 8px solid #ef4444; }
.rec-orange { background: rgba(251,146,60,0.28); border-left: 8px solid #fb923c; }
.rec-green  { background: rgba(34,197,94,0.28); border-left: 8px solid #10b981; }
.rec-win {
    background: linear-gradient(135deg, #f72585, #7209b7, #3a0ca3);
    border-left: 10px solid #06d6a0;
    animation: celebrate 2s infinite;
}
@keyframes celebrate {
    0%{ transform: scale(1);}
    50%{ transform: scale(1.05);}
    100%{ transform: scale(1);}
}

</style>
""", unsafe_allow_html=True)



# -------------------------------------------------------------------------
#  SIDEBAR INPUTS
# -------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#8af8d4; text-align:center;'>Your Financial Inputs</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    monthly_income = st.number_input("Monthly Income (PKR)", 0, 100000000, 60000, step=1000)
    monthly_expenses = st.number_input("Monthly Expenses (PKR)", 0, 100000000, 55000, step=1000)
    current_savings = st.number_input("Current Savings (PKR)", 0, 100000000, 150000, step=5000)
    total_debt = st.number_input("Total Debt (PKR)", 0, 100000000, 0, step=1000)
    current_investments = st.number_input("Current Investments (PKR)", 0, 100000000, 50000, step=1000)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#8af8d4; text-align:center;'>Your Goal</h2>", unsafe_allow_html=True)
    goal_name = st.text_input("Goal Name (House, Car etc.)", value="My Goal")
    goal_amount = st.number_input("Goal Amount (PKR)", 1, 10000000000, 5000000, step=50000)

# -------------------------------------------------------------------------
# CALCULATIONS
# -------------------------------------------------------------------------
total_amount = monthly_income + current_savings
net_worth = current_savings + current_investments - total_debt
monthly_save = max(0, monthly_income - monthly_expenses)
goal_progress = min(100, (current_savings / goal_amount) * 100)
months_needed = (
    "N/A" if monthly_save <= 0 else int((goal_amount - current_savings) / monthly_save)
)

remaining = max(0, goal_amount - current_savings)

# ======================================================================
#  PAGE NAVIGATION
# ======================================================================
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Savings Insights", "Visuals"],
    index=0,
)


# ======================================================================
#  LOTTIE HEADER ANIMATION
# ======================================================================
lottie_header = load_lottie("https://lottie.host/2a85f74b-0408-4e3e-b15e-3f8ef0d52d30/4W7hdwS7XQ.json")
st.components.v1.html(
    f"""
    <lottie-player src='{json.dumps(lottie_header)}' 
    background='transparent' speed='1' 
    style='width:190px;height:190px;margin:auto;' loop autoplay></lottie-player>
    """,
    height=200,
)


# ======================================================================
#  OVERVIEW PAGE
# ======================================================================
if page == "Overview":
    st.markdown("<div class='section-animate'>", unsafe_allow_html=True)

    st.markdown("<h1 class='app-title'>Your Financial Overview</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='overview-card'><div class='card-label'>Monthly Savings</div>"
                    f"<div class='card-value'>{monthly_save:,.0f} PKR</div></div>",
                    unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='overview-card'><div class='card-label'>Net Worth</div>"
                    f"<div class='card-value'>{net_worth:,.0f} PKR</div></div>",
                    unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='overview-card'><div class='card-label'>Total Investments</div>"
                    f"<div class='card-value'>{current_investments:,.0f} PKR</div></div>",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------- Goal Section --------------------
    st.markdown("<h2 style='text-align:center; color:#8af8d4;'>Your Goal Progress</h2>", unsafe_allow_html=True)

    st.markdown("<div class='goal-box'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:white;text-align:center;'>{goal_name}</h3>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="goal-bar">
            <div class="goal-fill" style="width:{goal_progress}%"></div>
        </div>
        <p style='text-align:center;color:white;margin-top:12px;font-size:18px;'>
            {goal_progress:.1f}% completed — {remaining:,.0f} PKR remaining
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Celebration Animation When Goal Completed
    if goal_progress >= 100:
        celebrate = load_lottie("https://lottie.host/98453d44-55d9-42fd-bc9a-d1a184746e96/Qve3pv7WVB.json")
        st.components.v1.html(
            f"""
            <lottie-player src='{json.dumps(celebrate)}' background='transparent'
            speed='1' style='width:260px;height:260px;margin:auto;' autoplay></lottie-player>
            """,
            height=260,
        )
        st.markdown("<div class='rec-win'>🎉 Congratulations! You achieved your goal!</div>",
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # end animation wrapper


# ======================================================================
#  SAVINGS INSIGHTS PAGE
# ======================================================================
if page == "Savings Insights":
    st.markdown("<div class='section-animate'>", unsafe_allow_html=True)
    st.markdown("<h1 class='app-title'>Savings Insights</h1>", unsafe_allow_html=True)

    if monthly_save <= 0:
        st.markdown("<div class='rec-red'>⚠️ Your expenses exceed your income. Reduce spending urgently.</div>",
                    unsafe_allow_html=True)

    elif monthly_save < monthly_income * 0.10:
        st.markdown("<div class='rec-orange'>You are saving less than 10% of income. Improve savings!</div>",
                    unsafe_allow_html=True)

    else:
        st.markdown("<div class='rec-green'>Great! You are saving well every month.</div>",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📅 Estimated Time To Reach Goal")
    st.info(f"⏳ You need approximately **{months_needed} months** to reach your goal.")

    st.markdown("</div>", unsafe_allow_html=True)




# ======================================================================
#  VISUALS PAGE
# ======================================================================
if page == "Visuals":
    st.markdown("<div class='section-animate'>", unsafe_allow_html=True)
    st.markdown("<h1 class='app-title'>Financial Visuals</h1>", unsafe_allow_html=True)

    # -------------------- PIE CHART --------------------
    st.subheader("Income vs Expenses")
    fig1 = px.pie(
        names=["Income", "Expenses"],
        values=[monthly_income, monthly_expenses],
        hole=0.45
    )
    fig1.update_layout(
        title="Income vs Expenses",
        font=dict(size=18, color="white"),
        legend=dict(font=dict(color="white"))
    )
    st.plotly_chart(fig1, use_container_width=True)

    # -------------------- BAR CHART --------------------
    st.subheader("Net Worth Breakdown")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=["Savings", "Investments", "Debt"],
        y=[current_savings, current_investments, total_debt]
    ))
    fig2.update_layout(
        font=dict(size=18, color="white"),
        xaxis=dict(tickfont=dict(size=16, color="white")),
        yaxis=dict(tickfont=dict(size=16, color="white")),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)




# ======================================================================
#  END
# ======================================================================
st.markdown("<br><br><p style='text-align:center;color:#8af8d4;'>Made with ❤️ for Smart Financial Tracking</p>",
            unsafe_allow_html=True)
