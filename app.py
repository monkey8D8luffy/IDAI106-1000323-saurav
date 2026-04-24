"""
FutureForward Wellness — Liquid Glass UI
Matches PDF Wireframes: Dashboard → Mood Sync → Breathe With Me → Relaxing Music → Reflection
"""

import streamlit as st
import pandas as pd
import time
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
        "stress_history": [
            {"date": (datetime.now() - timedelta(days=2)).strftime("%b %d"), "pre_stress": 8, "post_stress": 4},
            {"date": (datetime.now() - timedelta(days=1)).strftime("%b %d"), "pre_stress": 6, "post_stress": 3},
        ],
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
    """Fetches a calming quote from ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=3)
        data = response.json()
        return f'"{data[0]["q"]}" — {data[0]["a"]}'
    except:
        return '"Peace comes from within. Do not seek it without." — Buddha'

def fetch_calm_music(stress_level):
    """Fetches ambient music from Jamendo API based on stress level."""
    tag = "ambient" if stress_level >= 7 else "lofi"
    client_id = "56d30c95" # Public open-source client ID for Jamendo
    url = f"https://api.jamendo.com/v3.0/tracks/?client_id={client_id}&format=json&tags={tag}&limit=5&imagesize=200"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("results"):
            return [{"name": t["name"], "audio": t["audio"], "image": t["image"]} for t in data["results"]]
    except:
        pass
    
    # Bulletproof fallback if API is blocked by school firewall
    return [
        {"name": "Deep Delta Recovery", "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", "image": "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=200&q=80"},
        {"name": "Theta Brainwave Sync", "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=200&q=80"}
    ]

# ──────────────────────────────────────────────
# 3. GLOBAL CSS & BACKGROUND VIDEO
# ──────────────────────────────────────────────
def inject_ui():
    """Injects Liquid Glass UI, Morph Animations, and Video Background securely"""
    
    # We use a standard string here to avoid the Python f-string bracket bug
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
            object-fit: cover; opacity: 0.85;
        }
        
        /* Liquid Glass Card (No Sharp Edges) */
        .liquid-card {
            background: rgba(20, 25, 40, 0.45);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-radius: 35px; /* Extremely rounded */
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            padding: 2rem;
            color: #FFFFFF;
            margin-bottom: 1.5rem;
        }

        /* Typography */
        * { font-family: 'Helvetica Neue', sans-serif; color: #FFFFFF; }
        h1, h2, h3 { font-weight: 300; }

        /* Navigation Bar (Matching PDF) */
        .nav-bar {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 50px;
            padding: 0.5rem 1rem;
            margin-bottom: 2rem;
        }
        .nav-item {
            padding: 0.8rem 1.5rem; border-radius: 30px;
            cursor: pointer; font-weight: 500; font-size: 0.9rem;
            transition: all 0.3s;
        }
        .nav-item.active { background: rgba(255, 255, 255, 0.25); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }

        /* Liquid Morph Animation (Breathe with Me) */
        .liquid-morph {
            width: 250px; height: 250px;
            background: linear-gradient(135deg, rgba(79,195,247,0.5), rgba(124,77,255,0.5));
            animation: morph 8s ease-in-out infinite, breatheScale 10s ease-in-out infinite;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; font-weight: bold; letter-spacing: 2px; text-transform: uppercase;
            box-shadow: 0 0 40px rgba(79,195,247,0.3);
            margin: 0 auto;
        }
        @keyframes morph {
            0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
            50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
            100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
        }
        @keyframes breatheScale {
            0%, 100% { transform: scale(0.8); }
            40%, 60% { transform: scale(1.2); }
        }
        
        /* Interactive Elements */
        div[data-baseweb="slider"] div { background: #4FC3F7 !important; }
        button { border-radius: 30px !important; }
        </style>

        <video autoplay loop muted playsinline class="video-bg">
            <source src="https://raw.githubusercontent.com/monkey8D8luffy/IDAI106-1000323-saurav/main/334072.mp4" type="video/mp4">
        </video>
    """
    st.markdown(ui_code, unsafe_allow_html=True)

inject_ui()

# ──────────────────────────────────────────────
# 4. UTILITIES
# ──────────────────────────────────────────────
def navigate(page):
    st.session_state.current_page = page
    st.rerun()

def render_navbar():
    pages = ["Dashboard", "Mood Sync", "Breathe With Me", "Relaxing Music"]
    html = '<div class="nav-bar">'
    for p in pages:
        active = "active" if st.session_state.current_page == p else ""
        html += f'<div class="nav-item {active}">{p}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 5. PAGES
# ──────────────────────────────────────────────

def page_dashboard():
    render_navbar()
    
    # AI Quote Fetcher
    if st.session_state.api_quote == "Loading mindfulness...":
        st.session_state.api_quote = fetch_ai_quote()

    st.markdown(f'<div class="liquid-card" style="text-align:center;"><h2>{st.session_state.api_quote}</h2><p style="opacity:0.6;">— AI Stress Nudge</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="liquid-card"><h3>Zen Score</h3><h1 style="color:#4FC3F7;">{} 🌱</h1></div>'.format(st.session_state.zen_score), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="liquid-card"><h3>Start Session</h3><p>Initialize the Smart Pod to begin your journey.</p></div>', unsafe_allow_html=True)
        if st.button("Start Session ➔", use_container_width=True):
            navigate("Mood Sync")

def page_moodsync():
    render_navbar()
    
    st.markdown('<div class="liquid-card" style="text-align:center;"><h2>Mood Sync & Calibration</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="liquid-card">', unsafe_allow_html=True)
        st.write("### How are you feeling?")
        st.session_state.current_stress_level = st.slider("Stress Level (1=Calm, 10=Overwhelmed)", 1, 10, st.session_state.current_stress_level)
        
        # AI Prescription logic
        if st.session_state.current_stress_level > 6:
            st.warning("AI: High stress detected. Prescribing Deep Delta Waves and Blue Hue.")
        else:
            st.success("AI: Balanced state. Prescribing Lo-Fi Focus and Amber Hue.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="liquid-card">', unsafe_allow_html=True)
        st.write("### Session Duration")
        # Matching Page 6 of PDF exactly
        st.session_state.session_timer = st.radio("Select Timer:", ["1 min", "5 min", "10 min", "Custom"], horizontal=True)
        st.write("### Pod Controls")
        st.toggle("Smart Background Video", value=True)
        st.toggle("Aroma Diffuser", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Initialize Pod Environment ➔", use_container_width=True):
        navigate("Breathe With Me")

def page_breathe():
    # Locked Environment (No Navbar) - Hides tabs as requested for this stage
    st.markdown("""
        <style>
        .nav-bar { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="liquid-card" style="text-align:center; margin-top: 5vh; min-height: 60vh; display:flex; flex-direction:column; justify-content:center;">', unsafe_allow_html=True)
    
    st.write("### Follow the Rhythm")
    st.write(f"Session Time: {st.session_state.session_timer}")
    
    # Liquid Morph Animation
    st.markdown("""
        <div class="liquid-morph">
            <span style="opacity: 0.8;">Breathe</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("Transition to Audio ➔", use_container_width=True):
        navigate("Relaxing Music")
    st.markdown('</div>', unsafe_allow_html=True)

def page_music():
    render_navbar()
    
    # Fetch API tracks if empty
    if not st.session_state.music_tracks:
        st.session_state.music_tracks = fetch_calm_music(st.session_state.current_stress_level)

    # Matching Page 8 of PDF exactly (Player on Left, List on Right)
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown('<div class="liquid-card" style="text-align:center; height: 100%;">', unsafe_allow_html=True)
        active_track = st.session_state.music_tracks[0]
        if "unsplash" in active_track["image"]:
            st.image(active_track["image"], width=200)
        st.write(f"### {active_track['name']}")
        st.write("▶ Currently Playing")
        st.audio(active_track["audio"], format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="liquid-card" style="height: 100%;">', unsafe_allow_html=True)
        st.write("### Recommended Tracks")
        for idx, track in enumerate(st.session_state.music_tracks):
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 15px; margin-bottom: 10px; display:flex; justify-content:space-between;">
                    <span>🎵 {track['name']}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("End Session ➔", use_container_width=True):
        navigate("Reflection")

def page_reflection():
    render_navbar()
    
    # Matching Page 5/7 of PDF exactly
    st.markdown('<div class="liquid-card" style="text-align:center;">', unsafe_allow_html=True)
    st.write("## How much better do you feel now?")
    
    post_stress = st.slider("Adjust Slider", 1, 10, max(1, st.session_state.current_stress_level - 3))
    delta = st.session_state.current_stress_level - post_stress
    
    st.write(f"### Stress Reduced by: {delta} levels")
    
    if st.button("Save & Return to Dashboard", use_container_width=True):
        st.session_state.zen_score += 1
        st.session_state.music_tracks = [] # Reset tracks for next session
        navigate("Dashboard")
    st.markdown('</div>', unsafe_allow_html=True)

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
