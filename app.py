import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="FutureForward Wellness",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State Variables
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'current_stress_level' not in st.session_state:
    st.session_state.current_stress_level = 5
if 'zen_garden_score' not in st.session_state:
    st.session_state.zen_garden_score = 1
if 'stress_history' not in st.session_state:
    # Mock data for the dashboard
    today = datetime.today()
    st.session_state.stress_history = pd.DataFrame({
        "Date": [(today - timedelta(days=i)).strftime("%b %d") for i in range(4, -1, -1)],
        "Pre-Session Stress": [8, 7, 9, 6, 8],
        "Post-Session Stress": [3, 2, 4, 2, 3]
    })

# ==========================================
# 2. "LIQUID GLASS" UI & CSS
# ==========================================
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Ambient Background Video/GIF */
        .stApp {
            background: url("https://cdn.pixabay.com/animation/2023/06/26/03/02/03-02-03-917_512.gif") no-repeat center center fixed;
            background-size: cover;
        }
        
        /* Glassmorphism Styling applied to standard Streamlit containers */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background: rgba(20, 20, 30, 0.45);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            color: #E0E0E0;
        }

        /* Typography fixes for dark theme */
        h1, h2, h3, p, label, .stMarkdown {
            color: #FFFFFF !important;
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* Hide Default Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {background: transparent !important;}

        /* Breathing Animation CSS */
        .breathe-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }
        .breathe-circle {
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(130,200,255,0.8) 0%, rgba(80,120,200,0.4) 100%);
            border-radius: 50%;
            animation: breathe 10s infinite ease-in-out;
            box-shadow: 0 0 20px rgba(130,200,255,0.5);
        }
        @keyframes breathe {
            0% { transform: scale(1); opacity: 0.6; }
            40% { transform: scale(1.8); opacity: 1; } /* Inhale */
            60% { transform: scale(1.8); opacity: 1; } /* Hold */
            100% { transform: scale(1); opacity: 0.6; } /* Exhale */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

inject_custom_css()

# ==========================================
# 3. NAVIGATION ENGINE
# ==========================================
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ==========================================
# 4. PAGE MODULES
# ==========================================

def render_dashboard():
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.title("Welcome back. Take a breath.")
        
        # Gamification: Digital Zen Garden
        stages = ["🌱 (Sprout)", "🪴 (Potted Plant)", "🌿 (Flourishing)", "🌳 (Deep Roots)"]
        garden_level = min(st.session_state.zen_garden_score // 2, 3)
        st.subheader(f"Your Digital Zen Garden: {stages[garden_level]}")
        st.write("Your garden grows as you take time to reset your mind.")
        
        st.markdown("---")
        
        # Stress Tracking Dashboard
        st.subheader("Your Stress History")
        fig = px.line(
            st.session_state.stress_history, 
            x="Date", 
            y=["Pre-Session Stress", "Post-Session Stress"],
            markers=True,
            color_discrete_sequence=["#FF6B6B", "#4ECDC4"]
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            legend_title_text='Metric',
            yaxis=dict(range=[0, 10], showgrid=False),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

        if st.button("I need a reset ➔", use_container_width=True):
            navigate_to("Voice_CheckIn")

def render_voice_checkin():
    col1, col2, col3 = st.columns([2, 6, 2])
    with col2:
        st.title("🎙️ Voice-Vitals Check-In")
        st.write("Speak your mind. How is your day going? What is causing you friction?")
        
        audio_value = st.audio_input("Record your voice")
        
        st.markdown("<br><center><p>— OR —</p></center><br>", unsafe_allow_html=True)
        
        # Fallback Input
        manual_stress = st.slider("Rate your current stress manually (1 = Calm, 10 = Overwhelmed)", 1, 10, 5)
        
        if st.button("Analyze & Continue ➔", use_container_width=True):
            with st.spinner("Analyzing vocal sentiment and biometric data..."):
                time.sleep(1.5) # Simulate AI processing time
                st.session_state.current_stress_level = manual_stress
                navigate_to("MoodSync")

def render_moodsync():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("🧠 MoodSync AI")
        stress = st.session_state.current_stress_level
        
        if stress >= 7:
            st.error(f"High Stress Detected (Level {stress}).")
            st.write("**Prescription:** Deep Delta Recovery. Calibrating pod for sensory isolation, cooling ambient temperatures, and slow-wave binaural beats.")
        elif stress >= 4:
            st.warning(f"Moderate Stress Detected (Level {stress}).")
            st.write("**Prescription:** Flow State Reset. Calibrating pod for warm lighting, Lo-Fi focus beats, and eucalyptus aroma.")
        else:
            st.success(f"Low Stress Detected (Level {stress}).")
            st.write("**Prescription:** Gentle Maintenance. Calibrating pod for natural sunlight emulation and acoustic piano.")
            
        st.markdown("---")
        st.subheader("Pod Scheduler")
        st.selectbox("Reserve Pod Time:", ["Right Now (Pod A Available)", "In 15 Minutes", "In 1 Hour"])

    with col2:
        st.title("🎛️ Hardware Simulator")
        st.write("Manual Override Controls")
        st.slider("Biometric Chair Massage Intensity", 0, 100, stress * 10)
        st.color_picker("Ambient Light Hue", "#2A52BE" if stress > 6 else "#FFB732")
        st.toggle("Activate Aroma Diffuser", value=True)
        
    st.write("")
    if st.button("Initialize Pod Session ➔", use_container_width=True):
        navigate_to("Immersion")

def render_immersion():
    # Simulate a smart notification trigger
    st.toast("You've been working hard. Enjoy this moment of peace.", icon="🌊")
    
    col1, col2, col3 = st.columns([2, 6, 2])
    with col2:
        st.title("🌊 The Immersion Zone")
        st.write("Follow the rhythm. Inhale as it expands, exhale as it contracts.")
        
        # Breathe with Me Animation
        st.markdown(
            """
            <div class="breathe-container">
                <div class="breathe-circle"></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.write("")
        
        # Hybrid Audio Engine
        st.subheader("Audio Source")
        audio_choice = st.radio("Select your track:", ["FutureForward Originals (High-Fidelity)", "Connect Spotify"], horizontal=True)
        
        if audio_choice == "FutureForward Originals (High-Fidelity)":
            st.write("🎶 Playing: *Deep Delta Waves*")
            # Mock audio file URL (replace with actual royalty free audio if desired)
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            st.caption("Visualizer active in physical pod environment.")
        else:
            st.write("🎧 Spotify Connected")
            # Embed Spotify Focus Playlist
            st.components.v1.html(
                """
                <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                """,
                height=160
            )

        st.write("")
        if st.button("End Session ➔", use_container_width=True):
            navigate_to("Reflection")

def render_reflection():
    col1, col2, col3 = st.columns([2, 6, 2])
    with col2:
        st.title("📝 Post-Session Journal")
        st.write("Take a moment to reflect on your session.")
        
        st.text_area("How are you feeling now? (Optional)", placeholder="My mind feels much clearer...")
        
        # Delta Check
        post_stress = st.slider("Rate your post-session stress level", 1, 10, max(1, st.session_state.current_stress_level - 4))
        
        if st.button("Save & Return to Work ➔", use_container_width=True):
            # Update Dashboard Data
            new_data = pd.DataFrame({
                "Date": [datetime.today().strftime("%b %d")],
                "Pre-Session Stress": [st.session_state.current_stress_level],
                "Post-Session Stress": [post_stress]
            })
            st.session_state.stress_history = pd.concat([st.session_state.stress_history, new_data], ignore_index=True)
            
            # Level up Zen Garden
            st.session_state.zen_garden_score += 1
            navigate_to("Dashboard")

# ==========================================
# 5. ROUTING EXECUTION
# ==========================================
if st.session_state.current_page == "Dashboard":
    render_dashboard()
elif st.session_state.current_page == "Voice_CheckIn":
    render_voice_checkin()
elif st.session_state.current_page == "MoodSync":
    render_moodsync()
elif st.session_state.current_page == "Immersion":
    render_immersion()
elif st.session_state.current_page == "Reflection":
    render_reflection()
