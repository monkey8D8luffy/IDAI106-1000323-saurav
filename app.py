"""
FutureForward Wellness — Static Image Version (100% iPad Safe)
"""

import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# PAGE CONFIG (Must be first)
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
# 2. AI & MEDIA API FETCHERS
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
    url = f"https://api.jamendo.com/v3.0/tracks/?client_id=56d30c95&format=json&tags={tag}&limit=5&imagesize=200"
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

def fetch_dynamic_image(stress_level):
    """API that returns a static, high-res JPG based on stress level."""
    if stress_level >= 8:
        # High Stress: Deep Space Nebula
        return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2000&auto=format&fit=crop"
    elif stress_level >= 5:
        # Medium Stress: Soft Sunset Clouds
        return "https://images.unsplash.com/photo-1509803874385-db7c23652552?q=80&w=2000&auto=format&fit=crop"
    else:
        # Low Stress: Calm Ocean Water
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2000&auto=format&fit=crop"

# ──────────────────────────────────────────────
# 3. GLOBAL CSS & DYNAMIC STATIC BACKGROUND
# ──────────────────────────────────────────────
def inject_ui():
    active_image = fetch_dynamic_image(st.session_state.current_stress_level)
    
    ui_code = f"""
        <style>
        /* Force Transparent Backgrounds */
        #MainMenu, header, footer {{visibility: hidden;}}
        .stApp, .main {{ background: transparent !important; }}
        
        /* Apply Static Background Image directly to the Streamlit App Container */
        [data-testid="stAppViewContainer"] {{
            background-image: url("{active_image}") !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
            background-size: cover !important;
            transition: background-image 0.5s ease-in-out;
        }}
        
        /* Overlay to make text readable */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(10, 15, 25, 0.4);
            z-index: 0;
        }}
        
        /* Lift content above the dark overlay */
        .block-container {{ position: relative; z-index: 1; }}
        
        * {{ font-family: 'Helvetica Neue', sans-serif; color: #FFFFFF !important; }}
        
        /* Glass Pills for Native Buttons */
        .stButton > button {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 30px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }}
        .stButton > button:hover {{
            background: rgba(79, 195, 247, 0.4) !important;
            border-color: #4FC3F7 !important;
            transform: translateY(-2px);
        }}
        
        /* Glass Box Containers */
        .glass-box {{
            background: rgba(15, 20, 30, 0.55);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 2rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            text-align: center;
        }}
        
        /* Pulsing Circle for Breathe Page */
        .pulse-circle {{
            width: 180px; height: 180px;
            background: radial-gradient(circle, rgba(255,160,122,0.8) 0%, rgba(255,69,0,0.4) 100%);
            border-radius: 50%;
            margin: 40px auto;
            animation: pulse 8s infinite ease-in-out;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; font-weight: bold; text-transform: uppercase;
            box-shadow: 0 0 30px rgba(255,69,0,0.5);
        }}
        @keyframes pulse {{
            0% {{ transform: scale(0.8); opacity: 0.6; }}
            50% {{ transform: scale(1.4); opacity: 1; }}
            100% {{ transform: scale(0.8); opacity: 0.6; }}
        }}
        </style>
    """
    st.markdown(ui_code, unsafe_allow_html=True)

inject_ui()

# ──────────────────────────────────────────────
# 4. NAVIGATION CONTROLLER
# ──────────────────────────────────────────────
def navigate(page):
    st.session_state.current_page = page
    st.rerun()

def render_navbar():
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Dashboard"): navigate("Dashboard")
    with c2:
        if st.button("Mood Sync"): navigate("Mood Sync")
    with c3:
        if st.button("Breathe With Me"): navigate("Breathe With Me")
    with c4:
        if st.button("Relaxing Music"): navigate("Relaxing Music")
    st.markdown('<hr style="border-top: 1px solid rgba(255,255,255,0.2);">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 5. PAGE MODULES
# ──────────────────────────────────────────────

def page_dashboard():
    render_navbar()
    
    if st.session_state.api_quote == "Loading mindfulness...":
        st.session_state.api_quote = fetch_ai_quote()

    st.markdown(f'<div class="glass-box"><h2>{st.session_state.api_quote}</h2><p style="color:#FFA07A; font-size:12px; letter-spacing:2px; text-transform:uppercase;">— AI Stress Nudge</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="glass-box"><h3>Zen Score</h3><h1 style="color:#FFA07A; font-size: 3.5rem;">{st.session_state.zen_score} 🌱</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-box" style="padding-bottom: 1rem;"><h3>Start Session</h3><p>Initialize the Smart Pod to begin your journey.</p></div>', unsafe_allow_html=True)
        if st.button("Initialize Pod ➔", key="dash_start"):
            navigate("Mood Sync")

def page_moodsync():
    render_navbar()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🎚️ How are you feeling?")
        # Changing the slider instantly triggers the background API to swap the static image!
        st.session_state.current_stress_level = st.slider("Stress Level (1=Calm, 10=Overwhelmed)", 1, 10, st.session_state.current_stress_level)
        st.write("")
        if st.session_state.current_stress_level >= 8:
            st.error("AI Protocol: High stress detected. Prescribing Deep Delta Waves.")
        elif st.session_state.current_stress_level >= 5:
            st.warning("AI Protocol: Moderate stress detected. Prescribing Cloud Flow.")
        else:
            st.success("AI Protocol: Balanced state. Prescribing Nature Reset.")

    with col2:
        st.write("### ⚙️ Session Setup")
        st.session_state.session_timer = st.radio("Select Timer:", ["1 min", "5 min", "10 min", "Custom"], horizontal=True)
        st.write("")
        st.toggle("Smart Background Mode", value=True)
        st.toggle("Hardware Aroma Diffuser", value=True)

    st.write("---")
    if st.button("Confirm Settings & Begin Breathing ➔"):
        navigate("Breathe With Me")

def page_breathe():
    st.markdown('<style>.stButton>button:nth-child(1), hr {display:none;}</style>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.write("## Follow the Rhythm")
    st.write(f"Session Duration: {st.session_state.session_timer}")
    
    st.markdown('<div class="pulse-circle">Breathe</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("Transition to Audio & Music ➔"):
        navigate("Relaxing Music")

def page_music():
    render_navbar()
    
    if not st.session_state.music_tracks:
        st.session_state.music_tracks = fetch_calm_music(st.session_state.current_stress_level)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### 🎧 Now Playing")
        active_track = st.session_state.music_tracks[0]
        st.markdown(f'<div class="glass-box"><h3>{active_track["name"]}</h3></div>', unsafe_allow_html=True)
        st.audio(active_track["audio"], format="audio/mp3")

    with col2:
        st.write("### 🎵 Recommended Queue")
        st.markdown('<div class="glass-box" style="text-align:left;">', unsafe_allow_html=True)
        for track in st.session_state.music_tracks[1:]:
            st.write(f"- {track['name']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("---")
    if st.button("End Session & Reflect ➔"):
        navigate("Reflection")

def page_reflection():
    render_navbar()
    
    st.markdown('<div class="glass-box"><h2>How much better do you feel now?</h2></div>', unsafe_allow_html=True)
    
    post_stress = st.slider("Adjust Slider to Current Feeling", 1, 10, max(1, st.session_state.current_stress_level - 3))
    delta = st.session_state.current_stress_level - post_stress
    
    st.write("")
    st.markdown(f'<div class="glass-box"><h2 style="color:#FFA07A;">Stress Reduced by: {delta} levels</h2></div>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("Save Log & Return to Dashboard ➔"):
        st.session_state.zen_score += 1
        st.session_state.music_tracks = [] 
        navigate("Dashboard")

# ──────────────────────────────────────────────
# 6. ROUTER EXECUTION
# ──────────────────────────────────────────────
pages = {
    "Dashboard": page_dashboard,
    "Mood Sync": page_moodsync,
    "Breathe With Me": page_breathe,
    "Relaxing Music": page_music,
    "Reflection": page_reflection
}

pages.get(st.session_state.current_page, page_dashboard)()
