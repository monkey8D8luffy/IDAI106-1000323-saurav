"""
FutureForward Wellness — Fixed UI & Navigation
"""

import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(page_title="FutureForward Wellness", page_icon="🌊", layout="wide", initial_sidebar_state="collapsed")

# ──────────────────────────────────────────────
# 1. STATE INITIALIZATION
# ──────────────────────────────────────────────
def init_state():
    defaults = {
        "current_page": "Dashboard",
        "current_stress_level": 5,
        "zen_score": 3,
        "session_timer": "5 min",
        "api_quote": "Loading mindfulness...",
        "music_tracks": []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ──────────────────────────────────────────────
# 2. API FETCHERS
# ──────────────────────────────────────────────
def fetch_ai_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=3)
        data = response.json()
        return f'"{data[0]["q"]}" — {data[0]["a"]}'
    except:
        return '"Peace comes from within. Do not seek it without." — Buddha'

def fetch_calm_music(stress_level):
    tag = "ambient" if stress_level >= 7 else "lofi"
    client_id = "56d30c95"
    url = f"https://api.jamendo.com/v3.0/tracks/?client_id={client_id}&format=json&tags={tag}&limit=5&imagesize=200"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("results"):
            return [{"name": t["name"], "audio": t["audio"], "image": t["image"]} for t in data["results"]]
    except:
        pass
    
    return [
        {"name": "Deep Delta Recovery", "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", "image": "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=200&q=80"},
        {"name": "Theta Brainwave Sync", "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=200&q=80"}
    ]

# ──────────────────────────────────────────────
# 3. GLOBAL CSS & BACKGROUND VIDEO
# ──────────────────────────────────────────────
def inject_ui():
    ui_code = """
        <style>
        /* Hide Default Streamlit Elements */
        #MainMenu, header, footer {visibility: hidden;}
        .stApp { background: transparent !important; }
        
        /* Video Background */
        .video-bg {
            position: fixed; right: 0; bottom: 0;
            min-width: 100%; min-height: 100%;
            width: auto; height: auto; z-index: -100;
            object-fit: cover; opacity: 0.7;
        }
        
        /* Typography */
        * { font-family: 'Helvetica Neue', sans-serif; color: #FFFFFF; }

        /* Style Streamlit Buttons to look like the Nav Bar */
        div[data-testid="column"] button {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 30px !important;
            color: white !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="column"] button:hover {
            background: rgba(255, 255, 255, 0.3) !important;
            border-color: #4FC3F7 !important;
        }
        
        /* Glass Cards for Content */
        .glass-box {
            background: rgba(20, 25, 40, 0.5);
            backdrop-filter: blur(16px);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        </style>

        <video autoplay loop muted playsinline class="video-bg">
            <source src="https://cdn.pixabay.com/video/2020/05/24/40061-424683030_large.mp4" type="video/mp4">
        </video>
    """
    st.markdown(ui_code, unsafe_allow_html=True)

inject_ui()

# ──────────────────────────────────────────────
# 4. UTILITIES (WORKING NAVIGATION)
# ──────────────────────────────────────────────
def navigate(page):
    st.session_state.current_page = page
    st.rerun()

def render_navbar():
    # Using Native Streamlit Buttons so they actually click!
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Dashboard", use_container_width=True): navigate("Dashboard")
    with c2:
        if st.button("Mood Sync", use_container_width=True): navigate("Mood Sync")
    with c3:
        if st.button("Breathe With Me", use_container_width=True): navigate("Breathe With Me")
    with c4:
        if st.button("Relaxing Music", use_container_width=True): navigate("Relaxing Music")
    st.write("---")

# ──────────────────────────────────────────────
# 5. PAGES
# ──────────────────────────────────────────────

def page_dashboard():
    render_navbar()
    
    if st.session_state.api_quote == "Loading mindfulness...":
        st.session_state.api_quote = fetch_ai_quote()

    st.markdown(f'<div class="glass-box" style="text-align:center;"><h2>{st.session_state.api_quote}</h2><p style="color:#4FC3F7;">— AI Stress Nudge</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="glass-box" style="text-align:center;"><h3>Zen Score</h3><h1 style="color:#4FC3F7; font-size: 4rem;">{st.session_state.zen_score} 🌱</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-box" style="text-align:center;"><h3>Start Session</h3><p>Initialize the Smart Pod to begin your journey.</p></div>', unsafe_allow_html=True)
        if st.button("Initialize Pod ➔", use_container_width=True):
            navigate("Mood Sync")

def page_moodsync():
    render_navbar()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-box"><h3>How are you feeling?</h3></div>', unsafe_allow_html=True)
        st.session_state.current_stress_level = st.slider("Stress Level (1=Calm, 10=Overwhelmed)", 1, 10, st.session_state.current_stress_level)
        
        if st.session_state.current_stress_level > 6:
            st.error("AI: High stress detected. Prescribing Deep Delta Waves and Blue Hue.")
        else:
            st.success("AI: Balanced state. Prescribing Lo-Fi Focus and Amber Hue.")

    with col2:
        st.markdown('<div class="glass-box"><h3>Session Setup</h3></div>', unsafe_allow_html=True)
        st.session_state.session_timer = st.radio("Select Timer:", ["1 min", "5 min", "10 min", "Custom"], horizontal=True)
        st.toggle("Smart Background Video", value=True)
        st.toggle("Aroma Diffuser", value=True)

    st.write("")
    if st.button("Confirm Settings & Begin Breathing ➔", use_container_width=True):
        navigate("Breathe With Me")

def page_breathe():
    render_navbar()
    
    st.markdown('<div class="glass-box" style="text-align:center;">', unsafe_allow_html=True)
    st.write("## Follow the Rhythm")
    st.write(f"Session Time: {st.session_state.session_timer}")
    
    # Simple CSS Pulsing Animation
    st.markdown("""
        <style>
        .pulse-circle {
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(79,195,247,0.8) 0%, rgba(124,77,255,0.4) 100%);
            border-radius: 50%;
            margin: 40px auto;
            animation: pulse 8s infinite ease-in-out;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; font-weight: bold;
        }
        @keyframes pulse {
            0% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.4); opacity: 1; }
            100% { transform: scale(0.8); opacity: 0.5; }
        }
        </style>
        <div class="pulse-circle">BREATHE</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Transition to Audio ➔", use_container_width=True):
        navigate("Relaxing Music")

def page_music():
    render_navbar()
    
    if not st.session_state.music_tracks:
        st.session_state.music_tracks = fetch_calm_music(st.session_state.current_stress_level)

    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        active_track = st.session_state.music_tracks[0]
        st.markdown(f'<div class="glass-box" style="text-align:center;"><h3>{active_track["name"]}</h3><p>▶ Currently Playing</p></div>', unsafe_allow_html=True)
        st.audio(active_track["audio"], format="audio/mp3")

    with col2:
        st.markdown('<div class="glass-box"><h3>Recommended Tracks</h3>', unsafe_allow_html=True)
        for track in st.session_state.music_tracks[1:]:
            st.write(f"🎵 {track['name']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("")
    if st.button("End Session ➔", use_container_width=True):
        navigate("Reflection")

def page_reflection():
    render_navbar()
    
    st.markdown('<div class="glass-box" style="text-align:center;"><h2>How much better do you feel now?</h2></div>', unsafe_allow_html=True)
    
    post_stress = st.slider("Adjust Slider", 1, 10, max(1, st.session_state.current_stress_level - 3))
    delta = st.session_state.current_stress_level - post_stress
    
    st.markdown(f'<div class="glass-box" style="text-align:center;"><h2 style="color:#4FC3F7;">Stress Reduced by: {delta} levels</h2></div>', unsafe_allow_html=True)
    
    if st.button("Save & Return to Dashboard", use_container_width=True):
        st.session_state.zen_score += 1
        st.session_state.music_tracks = [] 
        navigate("Dashboard")

# ──────────────────────────────────────────────
# 6. ROUTER
# ──────────────────────────────────────────────
pages = {
    "Dashboard": page_dashboard,
    "Mood Sync": page_moodsync,
    "Breathe With Me": page_breathe,
    "Relaxing Music": page_music,
    "Reflection": page_reflection
}

pages.get(st.session_state.current_page, page_dashboard)()
