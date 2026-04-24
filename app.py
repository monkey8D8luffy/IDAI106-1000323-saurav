import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime
import random

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="FutureForward Wellness", layout="wide")

# ==================== GLOBAL CSS ====================
def inject_css():
    st.markdown("""
    <style>
    /* Hide Streamlit UI */
    #MainMenu, header, footer {visibility: hidden;}

    /* Background */
    .stApp {
        background: url("https://media.giphy.com/media/3o7TKsQ8UQ6Z0LrVb2/giphy.gif");
        background-size: cover;
        background-attachment: fixed;
        color: white;
        font-family: 'Inter', sans-serif;
    }

    /* Center container */
    .main-container {
        max-width: 900px;
        margin: auto;
        padding: 20px;
    }

    /* Glass Card */
    .glass {
        background: rgba(20, 20, 30, 0.45);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    /* Button */
    div.stButton > button {
        background: rgba(255,255,255,0.1);
        border: none;
        border-radius: 20px;
        color: white;
        padding: 12px 24px;
        font-size: 16px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: rgba(255,255,255,0.25);
        transform: scale(1.05);
    }

    /* Breathing Animation */
    .breath {
        width: 150px;
        height: 150px;
        margin: auto;
        border-radius: 50%;
        background: radial-gradient(circle, #6dd5fa, #2980b9);
        animation: breathe 10s infinite;
    }

    @keyframes breathe {
        0% {transform: scale(1);}
        40% {transform: scale(1.4);}
        100% {transform: scale(1);}
    }

    </style>
    """, unsafe_allow_html=True)

inject_css()

# ==================== SESSION STATE ====================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "stress_history" not in st.session_state:
    st.session_state.stress_history = []

if "current_stress_level" not in st.session_state:
    st.session_state.current_stress_level = 5

if "zen_garden_score" not in st.session_state:
    st.session_state.zen_garden_score = 1

# ==================== ROUTING ====================
def go(page):
    st.session_state.current_page = page

# ==================== PAGE 1: DASHBOARD ====================
def dashboard():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.title("Welcome back. Take a breath.")

    # Zen Garden
    score = st.session_state.zen_garden_score
    plant = "🌱" if score < 3 else "🌿" if score < 6 else "🌳"
    st.subheader(f"Your Zen Garden: {plant} (Level {score})")

    # Mock Data
    data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Pre": [7,6,8,5,7],
        "Post": [4,3,5,2,4]
    })

    fig = px.line(data, x="Day", y=["Pre","Post"])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    if st.button("I need a reset ➔"):
        go("Check-In")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE 2: CHECK-IN ====================
def checkin():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Speak your mind...")

    audio = st.audio_input("")

    stress = st.slider("Or rate your stress manually", 1, 10, 5)

    if audio or stress:
        with st.spinner("Analyzing vocal sentiment..."):
            time.sleep(2)
            st.session_state.current_stress_level = stress
            go("MoodSync")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE 3: MOODSYNC ====================
def moodsync():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # AI Output
    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        stress = st.session_state.current_stress_level

        if stress > 7:
            msg = "High Stress Detected. Deep Recovery Mode Activated."
        elif stress > 4:
            msg = "Moderate Stress. Balancing Mind & Body."
        else:
            msg = "Low Stress. Gentle Relaxation Mode."

        st.subheader(msg)
        st.markdown('</div>', unsafe_allow_html=True)

    # Controls
    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.slider("Chair Intensity", 1, 10, 5)
        st.color_picker("Light Hue", "#6dd5fa")
        st.slider("Diffuser Strength", 1, 10, 5)

        st.selectbox("Reserve Pod Time", ["Now", "15 mins", "1 hour"])

        if st.button("Initialize Pod ➔"):
            go("Immersion")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE 4: IMMERSION ====================
def immersion():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.markdown('<div class="breath"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Inhale... Exhale...</h3>", unsafe_allow_html=True)

    mode = st.radio("", ["FutureForward Originals", "Connect Spotify"], horizontal=True)

    if mode == "FutureForward Originals":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    else:
        st.components.v1.html("""
        <iframe style="border-radius:12px"
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ"
        width="100%" height="352"></iframe>
        """)

    st.toast("You've been focused. Enjoy this moment.")

    time.sleep(2)

    if st.button("End Session ➔"):
        go("Reflection")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE 5: REFLECTION ====================
def reflection():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.text_area("How are you feeling now?")
    post = st.slider("Current Stress Level", 1, 10, 3)

    if st.button("Save & Return"):
        st.session_state.stress_history.append({
            "date": datetime.now(),
            "pre": st.session_state.current_stress_level,
            "post": post
        })
        st.session_state.zen_garden_score += 1
        go("Dashboard")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ROUTER ====================
page = st.session_state.current_page

if page == "Dashboard":
    dashboard()
elif page == "Check-In":
    checkin()
elif page == "MoodSync":
    moodsync()
elif page == "Immersion":
    immersion()
elif page == "Reflection":
    reflection()