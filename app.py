"""
FutureForward Wellness — Corporate Stress-Relief Application
A premium, calming, glassmorphism-styled Streamlit app.
5-page routing: Dashboard → Check-In → MoodSync → Immersion → Reflection
100% Streamlit Community Cloud compatible.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime, timedelta
import random
import streamlit.components.v1 as components

# ──────────────────────────────────────────────
# PAGE CONFIG (must be the very first Streamlit call)
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="FutureForward Wellness",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# 1. SESSION STATE INITIALISATION
# ──────────────────────────────────────────────

def init_state():
    """Initialise all session-state keys with sensible defaults."""
    defaults = {
        "current_page": "Dashboard",
        "stress_history": [
            {"date": (datetime.now() - timedelta(days=4)).strftime("%b %d"), "pre_stress": 7, "post_stress": 4},
            {"date": (datetime.now() - timedelta(days=3)).strftime("%b %d"), "pre_stress": 6, "post_stress": 3},
            {"date": (datetime.now() - timedelta(days=2)).strftime("%b %d"), "pre_stress": 8, "post_stress": 5},
            {"date": (datetime.now() - timedelta(days=1)).strftime("%b %d"), "pre_stress": 5, "post_stress": 2},
        ],
        "current_stress_level": 5,
        "zen_garden_score": 3,
        "audio_choice": "FutureForward Originals",
        "pod_intensity": 5,
        "pod_hue": "#4FC3F7",
        "pod_diffuser": 3,
        "pod_schedule": "Now",
        "session_journal": "",
        "post_stress": 3,
        "session_start_time": None,
        "immersion_started": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ──────────────────────────────────────────────
# 2. GLOBAL CSS — injected once, controls everything
# ──────────────────────────────────────────────

def inject_global_css():
    """
    Single helper that injects all CSS:
    - Hides Streamlit chrome (header, footer, sidebar toggle)
    - Animated ambient background (CSS-driven deep-ocean gradient)
    - Glassmorphism card styles
    - Typography (Google Fonts)
    - Custom button styles
    - Breathing animation
    - Audio visualiser bars
    - Zen garden growth
    - Nav pill styles
    """
    css = """
    /* ── GOOGLE FONTS ── */
    @import url('[https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,200;0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=Syne:wght@300;400;500;600;700&display=swap](https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,200;0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=Syne:wght@300;400;500;600;700&display=swap)');

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu, header, footer,
    [data-testid="stToolbar"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    .stDeployButton { display: none !important; }

    /* ── AMBIENT ANIMATED BACKGROUND ── */
    @keyframes liquidShift {
        0%   { background-position: 0% 50%; }
        25%  { background-position: 50% 100%; }
        50%  { background-position: 100% 50%; }
        75%  { background-position: 50% 0%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes grainDrift {
        0%,100% { transform: translate(0,0); }
        10%      { transform: translate(-2%,-3%); }
        30%      { transform: translate(3%,2%); }
        60%      { transform: translate(-1%,4%); }
        80%      { transform: translate(2%,-2%); }
    }

    /* Body & app root */
    html, body, [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    .main .block-container { background: transparent !important; }

    body::before {
        content: '';
        position: fixed;
        inset: 0;
        background: linear-gradient(
            135deg,
            #020818 0%,
            #031a2e 15%,
            #051e38 30%,
            #0a1628 45%,
            #071224 60%,
            #030d1e 75%,
            #0d1f35 90%,
            #020818 100%
        );
        background-size: 400% 400%;
        animation: liquidShift 18s ease infinite;
        z-index: -3;
    }
    body::after {
        content: '';
        position: fixed;
        inset: -50%;
        width: 200%;
        height: 200%;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='[http://www.w3.org/2000/svg'%3E%3Cfilter](http://www.w3.org/2000/svg'%3E%3Cfilter) id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
        opacity: 0.35;
        pointer-events: none;
        z-index: -2;
        animation: grainDrift 8s steps(1) infinite;
    }

    /* Flowing orbs for depth */
    [data-testid="stApp"]::before {
        content: '';
        position: fixed;
        width: 60vw; height: 60vw;
        top: -20vw; left: -10vw;
        background: radial-gradient(ellipse, rgba(32,110,180,0.18) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
        animation: liquidShift 22s ease infinite reverse;
    }

    /* ── GLOBAL TYPOGRAPHY ── */
    *, *::before, *::after { box-sizing: border-box; }
    body, .stMarkdown, p, span, label, div {
        font-family: 'DM Sans', sans-serif !important;
        color: rgba(220,230,255,0.92) !important;
    }
    h1, h2, h3, h4 {
        font-family: 'Syne', sans-serif !important;
        letter-spacing: -0.02em;
        color: #e8f0ff !important;
    }

    /* ── BLOCK CONTAINER ── */
    .main .block-container {
        padding: 2rem 1rem !important;
        max-width: 900px !important;
    }

    /* ── GLASSMORPHISM CARD ── */
    .glass-card {
        background: rgba(14, 22, 45, 0.55) !important;
        backdrop-filter: blur(20px) saturate(1.4) !important;
        -webkit-backdrop-filter: blur(20px) saturate(1.4) !important;
        border: 1px solid rgba(100,160,255,0.12) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.06) !important;
        padding: 2rem 2.2rem !important;
        margin-bottom: 1.4rem !important;
    }
    .glass-card-sm {
        background: rgba(14, 22, 45, 0.45) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(100,160,255,0.1) !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
        padding: 1.4rem 1.6rem !important;
        margin-bottom: 1rem !important;
    }

    /* ── STREAMLIT WIDGETS RESTYLING ── */
    /* Inputs & text areas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(14, 22, 45, 0.6) !important;
        border: 1px solid rgba(100,160,255,0.2) !important;
        border-radius: 12px !important;
        color: #e0eaff !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus {
        border-color: rgba(100,180,255,0.5) !important;
        box-shadow: 0 0 0 3px rgba(100,180,255,0.1) !important;
    }

    /* Sliders */
    .stSlider > div > div > div { color: #7ab8f5 !important; }
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background: linear-gradient(135deg, #4fc3f7, #7c4dff) !important;
        box-shadow: 0 0 12px rgba(79,195,247,0.5) !important;
    }
    [data-testid="stSliderTrackActive"] { background: linear-gradient(90deg, #4fc3f7, #7c4dff) !important; }

    /* Radio buttons */
    .stRadio > div { flex-direction: row !important; gap: 1rem; }
    .stRadio label {
        background: rgba(14,22,45,0.5) !important;
        border: 1px solid rgba(100,160,255,0.2) !important;
        border-radius: 50px !important;
        padding: 0.4rem 1.2rem !important;
        cursor: pointer !important;
        transition: all 0.25s !important;
    }
    .stRadio label:hover { border-color: rgba(100,200,255,0.5) !important; }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(14,22,45,0.55) !important;
        border: 1px solid rgba(100,160,255,0.2) !important;
        border-radius: 12px !important;
        color: #e0eaff !important;
    }

    /* ── CUSTOM GLASS BUTTON ── */
    .glass-btn {
        display: inline-block;
        background: linear-gradient(135deg, rgba(79,195,247,0.18), rgba(124,77,255,0.18));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(100,200,255,0.3);
        border-radius: 50px;
        padding: 0.85rem 2.4rem;
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        color: #e0f4ff;
        cursor: pointer;
        letter-spacing: 0.04em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(79,195,247,0.15), inset 0 1px 0 rgba(255,255,255,0.1);
        text-align: center;
        width: 100%;
        margin-top: 0.5rem;
    }
    .glass-btn:hover {
        background: linear-gradient(135deg, rgba(79,195,247,0.3), rgba(124,77,255,0.3));
        box-shadow: 0 6px 30px rgba(79,195,247,0.3);
        transform: translateY(-2px);
        border-color: rgba(100,220,255,0.5);
    }

    /* Streamlit native buttons */
    .stButton > button {
        background: linear-gradient(135deg, rgba(79,195,247,0.2), rgba(124,77,255,0.2)) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(100,200,255,0.3) !important;
        border-radius: 50px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #e0f4ff !important;
        letter-spacing: 0.03em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(79,195,247,0.12) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(79,195,247,0.35), rgba(124,77,255,0.35)) !important;
        box-shadow: 0 6px 30px rgba(79,195,247,0.28) !important;
        transform: translateY(-2px) !important;
        border-color: rgba(100,220,255,0.5) !important;
    }
    .stButton > button:active { transform: translateY(0px) !important; }

    /* ── NAV PILLS ── */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 2.2rem;
        flex-wrap: wrap;
    }
    .nav-pill {
        padding: 0.45rem 1.1rem;
        border-radius: 50px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: 1px solid rgba(100,160,255,0.18);
        background: rgba(14,22,45,0.4);
        color: rgba(160,190,255,0.7);
        cursor: default;
        transition: all 0.2s;
    }
    .nav-pill.active {
        background: linear-gradient(135deg, rgba(79,195,247,0.25), rgba(124,77,255,0.25));
        border-color: rgba(100,200,255,0.4);
        color: #c8e8ff;
        box-shadow: 0 0 14px rgba(79,195,247,0.2);
    }

    /* ── BREATHING ANIMATION ── */
    @keyframes breatheExpand {
        0%   { transform: scale(0.78); opacity: 0.55; box-shadow: 0 0 30px rgba(79,195,247,0.2), 0 0 80px rgba(79,195,247,0.05); }
        40%  { transform: scale(1.0); opacity: 0.85; box-shadow: 0 0 60px rgba(79,195,247,0.4), 0 0 120px rgba(124,77,255,0.2); }
        100% { transform: scale(0.78); opacity: 0.55; box-shadow: 0 0 30px rgba(79,195,247,0.2), 0 0 80px rgba(79,195,247,0.05); }
    }
    @keyframes breatheText {
        0%,100% { opacity: 0.4; letter-spacing: 0.1em; }
        40%      { opacity: 0.95; letter-spacing: 0.18em; }
    }
    .breathe-outer {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 0;
    }
    .breathe-circle {
        width: 200px; height: 200px;
        border-radius: 50%;
        background: radial-gradient(ellipse at 35% 35%,
            rgba(79,195,247,0.35) 0%,
            rgba(124,77,255,0.25) 45%,
            rgba(14,22,45,0.4) 100%);
        border: 1.5px solid rgba(79,195,247,0.3);
        animation: breatheExpand 10s ease-in-out infinite;
        display: flex; align-items: center; justify-content: center;
    }
    .breathe-label {
        font-family: 'Syne', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(160,220,255,0.8) !important;
        animation: breatheText 10s ease-in-out infinite;
        text-align: center;
        padding: 0 1rem;
    }
    .breathe-hint {
        margin-top: 1.4rem;
        font-size: 0.75rem;
        color: rgba(140,170,220,0.5) !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    /* ── AUDIO VISUALISER ── */
    @keyframes bar1 { 0%,100%{height:8px} 50%{height:32px} }
    @keyframes bar2 { 0%,100%{height:20px} 50%{height:10px} }
    @keyframes bar3 { 0%,100%{height:14px} 50%{height:38px} }
    @keyframes bar4 { 0%,100%{height:28px} 50%{height:12px} }
    @keyframes bar5 { 0%,100%{height:10px} 50%{height:30px} }
    @keyframes bar6 { 0%,100%{height:22px} 50%{height:8px} }
    @keyframes bar7 { 0%,100%{height:16px} 50%{height:36px} }
    @keyframes bar8 { 0%,100%{height:30px} 50%{height:14px} }
    .visualiser {
        display: flex;
        align-items: flex-end;
        gap: 4px;
        height: 44px;
        justify-content: center;
        margin: 1rem 0;
    }
    .vis-bar {
        width: 6px; border-radius: 4px 4px 0 0;
        background: linear-gradient(180deg, #4fc3f7, #7c4dff);
        box-shadow: 0 0 8px rgba(79,195,247,0.4);
    }
    .vis-bar:nth-child(1){animation:bar1 0.8s ease-in-out infinite;}
    .vis-bar:nth-child(2){animation:bar2 0.6s ease-in-out infinite;}
    .vis-bar:nth-child(3){animation:bar3 0.9s ease-in-out infinite;}
    .vis-bar:nth-child(4){animation:bar4 0.7s ease-in-out infinite;}
    .vis-bar:nth-child(5){animation:bar5 1.0s ease-in-out infinite;}
    .vis-bar:nth-child(6){animation:bar6 0.65s ease-in-out infinite;}
    .vis-bar:nth-child(7){animation:bar7 0.85s ease-in-out infinite;}
    .vis-bar:nth-child(8){animation:bar8 0.75s ease-in-out infinite;}

    /* ── ZEN GARDEN ORBS ── */
    @keyframes orbFloat {
        0%,100%{transform:translateY(0) scale(1);} 
        50%{transform:translateY(-8px) scale(1.05);}
    }
    .zen-garden {
        display:flex; align-items:center; justify-content:center;
        flex-wrap:wrap; gap:0.6rem; padding:1rem 0;
    }
    .zen-orb {
        border-radius:50%;
        animation: orbFloat 3s ease-in-out infinite;
        box-shadow: 0 0 16px currentColor;
    }

    /* ── METRIC GLOW PILLS ── */
    .metric-pill {
        background: rgba(14,22,45,0.5);
        border: 1px solid rgba(100,160,255,0.15);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-pill .value {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #4fc3f7, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-pill .label {
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(140,170,220,0.6) !important;
    }

    /* ── PRESCRIPTION CARD ── */
    .rx-card {
        background: linear-gradient(135deg, rgba(79,195,247,0.08), rgba(124,77,255,0.08));
        border: 1px solid rgba(100,200,255,0.2);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .rx-card::before {
        content: 'Rx';
        position: absolute; top:-8px; right:16px;
        font-family:'Syne',sans-serif; font-size:4rem;
        font-weight:700; color:rgba(79,195,247,0.06);
        pointer-events:none;
    }
    .rx-level {
        font-family:'Syne',sans-serif;
        font-size:0.72rem; letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:0.5rem;
    }
    .rx-level.high { color:#ff6b8a !important; }
    .rx-level.medium { color:#f9a825 !important; }
    .rx-level.low { color:#4fc3f7 !important; }
    .rx-title {
        font-family:'Syne',sans-serif;
        font-size:1.1rem; font-weight:600; line-height:1.4;
        color:#e8f0ff !important; margin-bottom:0.8rem;
    }
    .rx-detail { font-size:0.85rem; color:rgba(180,210,255,0.75) !important; line-height:1.6; }

    /* ── SECTION LABELS ── */
    .section-eyebrow {
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: rgba(100,170,255,0.55) !important;
        margin-bottom: 0.3rem;
    }
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.9rem; font-weight: 600;
        color: #e8f0ff !important;
        line-height: 1.2; margin-bottom: 0.2rem;
    }
    .section-sub {
        font-size: 0.9rem;
        color: rgba(160,190,240,0.65) !important;
        margin-bottom: 1.6rem; line-height: 1.5;
    }

    /* ── DIVIDER ── */
    .glass-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(100,160,255,0.2), transparent);
        margin: 1.4rem 0;
    }

    /* ── SCORE BADGE ── */
    .score-badge {
        display:inline-flex; align-items:center; gap:0.5rem;
        background: rgba(79,195,247,0.12);
        border:1px solid rgba(79,195,247,0.25);
        border-radius:50px; padding:0.3rem 0.9rem;
        font-size:0.8rem; color:rgba(160,220,255,0.9) !important;
    }

    /* ── GREETING ANIMATION ── */
    @keyframes fadeSlideUp {
        from{opacity:0;transform:translateY(20px);}
        to{opacity:1;transform:translateY(0);}
    }
    .animated-in { animation: fadeSlideUp 0.7s ease both; }
    .animated-in.delay-1 { animation-delay: 0.1s; }
    .animated-in.delay-2 { animation-delay: 0.22s; }
    .animated-in.delay-3 { animation-delay: 0.36s; }
    .animated-in.delay-4 { animation-delay: 0.52s; }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

inject_global_css()

# ──────────────────────────────────────────────
# 3. HELPER UTILITIES
# ──────────────────────────────────────────────

def navigate_to(page: str):
    """Change current page in session state."""
    st.session_state.current_page = page
    st.rerun()

def glass_card(content_fn, extra_class=""):
    """Wrap a Streamlit render function in a glassmorphism div."""
    st.markdown(f'<div class="glass-card {extra_class}">', unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)

def render_nav():
    """Render the top navigation bar as HTML pills (display-only)."""
    pages = ["Dashboard", "Check-In", "MoodSync", "Immersion", "Reflection"]
    labels = ["🌊 Home", "🎙️ Check-In", "🧠 MoodSync", "🌀 Immersion", "✨ Reflect"]
    pills = ""
    for p, l in zip(pages, labels):
        active = "active" if st.session_state.current_page == p else ""
        pills += f'<span class="nav-pill {active}">{l}</span>'
    st.markdown(f'<div class="nav-container">{pills}</div>', unsafe_allow_html=True)

def stress_color(level: int) -> str:
    """Return a CSS color string based on stress level 1-10."""
    if level >= 8: return "#ff6b8a"
    if level >= 5: return "#f9a825"
    return "#4fc3f7"

def zen_garden_html(score: int) -> str:
    """Generate the Digital Zen Garden visual based on score."""
    orbs = []
    stages = [
        (1,  "🌱", 28, "#4fc3f7"),
        (2,  "🌿", 34, "#26a69a"),
        (3,  "🌸", 38, "#f48fb1"),
        (4,  "🌻", 42, "#ffd54f"),
        (5,  "🌳", 46, "#66bb6a"),
        (6,  "🌺", 40, "#ef9a9a"),
        (7,  "✨", 32, "#b39ddb"),
        (8,  "🌙", 36, "#90caf9"),
        (9,  "⭐", 30, "#ffe082"),
        (10, "🌌", 44, "#7986cb"),
    ]
    visible = [s for s in stages if s[0] <= score]
    if not visible:
        visible = [stages[0]]
    for i, (_, emoji, size, color) in enumerate(visible):
        delay = i * 0.4
        orbs.append(
            f'<div class="zen-orb" style="width:{size}px;height:{size}px;'
            f'background:radial-gradient(ellipse,{color}44 0%,transparent 70%);'
            f'color:{color};font-size:{size*0.6}px;display:flex;align-items:center;'
            f'justify-content:center;animation-delay:{delay}s;">{emoji}</div>'
        )
    return f'<div class="zen-garden">{"".join(orbs)}</div>'

def build_stress_chart(history: list) -> go.Figure:
    """Return a sleek dark-mode Plotly line chart for stress trends."""
    df = pd.DataFrame(history)
    fig = go.Figure()

    # Gradient fill under pre-stress line
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["pre_stress"],
        name="Pre-Session", mode="lines+markers",
        line=dict(color="#ff6b8a", width=2.5, shape="spline"),
        marker=dict(size=8, color="#ff6b8a", line=dict(width=1.5, color="rgba(255,255,255,0.3)")),
        fill="tozeroy",
        fillcolor="rgba(255,107,138,0.06)",
    ))
    # Post-stress line
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["post_stress"],
        name="Post-Session", mode="lines+markers",
        line=dict(color="#4fc3f7", width=2.5, shape="spline"),
        marker=dict(size=8, color="#4fc3f7", line=dict(width=1.5, color="rgba(255,255,255,0.3)")),
        fill="tozeroy",
        fillcolor="rgba(79,195,247,0.06)",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="rgba(180,210,255,0.75)", size=12),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)", font=dict(size=11)
        ),
        xaxis=dict(showgrid=False, zeroline=False, showline=False,
                   tickfont=dict(color="rgba(140,180,240,0.6)", size=11)),
        yaxis=dict(showgrid=False, zeroline=False, showline=False, range=[0, 11],
                   tickfont=dict(color="rgba(140,180,240,0.6)", size=11)),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="rgba(14,22,45,0.85)", font_color="#e0eaff",
                        bordercolor="rgba(100,160,255,0.3)"),
    )
    return fig

# ──────────────────────────────────────────────
# 4. PAGE RENDERERS
# ──────────────────────────────────────────────

# ── PAGE 1: DASHBOARD ──────────────────────────

def page_dashboard():
    render_nav()

    # ── Greeting
    _, col, _ = st.columns([1, 3, 1])
    with col:
        hour = datetime.now().hour
        greeting_word = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")

        st.markdown(f"""
        <div class="animated-in">
            <p class="section-eyebrow">{greeting_word}</p>
            <h1 class="section-title" style="font-size:2.4rem;font-weight:700;">
                Welcome back.<br>
                <span style="color:rgba(140,190,255,0.65);font-weight:300;">Take a breath.</span>
            </h1>
        </div>
        """, unsafe_allow_html=True)

        # ── Metrics row
        st.markdown('<div class="animated-in delay-1">', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            sessions = len(st.session_state.stress_history)
            st.markdown(f"""
            <div class="metric-pill">
                <div class="value">{sessions}</div>
                <div class="label">Sessions</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            score = st.session_state.zen_garden_score
            st.markdown(f"""
            <div class="metric-pill">
                <div class="value">{score}</div>
                <div class="label">Zen Score</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            if st.session_state.stress_history:
                last = st.session_state.stress_history[-1]
                delta = last["pre_stress"] - last["post_stress"]
            else:
                delta = 0
            st.markdown(f"""
            <div class="metric-pill">
                <div class="value">−{delta}</div>
                <div class="label">Last Δ Stress</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

        # ── Digital Zen Garden
        st.markdown('<div class="animated-in delay-2">', unsafe_allow_html=True)
        st.markdown('<p class="section-eyebrow">Digital Zen Garden</p>', unsafe_allow_html=True)
        garden_html = zen_garden_html(st.session_state.zen_garden_score)
        st.markdown(
            f'<div class="glass-card-sm">{garden_html}'
            f'<p style="text-align:center;font-size:0.78rem;color:rgba(130,170,230,0.5)!important;'
            f'margin-top:0.5rem;letter-spacing:0.08em;">Complete sessions to grow your garden</p>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Stress Trend Chart
        st.markdown('<div class="animated-in delay-3">', unsafe_allow_html=True)
        st.markdown('<p class="section-eyebrow">Stress Trend — Last Sessions</p>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card-sm" style="padding:1rem;">', unsafe_allow_html=True)
        if len(st.session_state.stress_history) >= 1:
            chart = build_stress_chart(st.session_state.stress_history)
            st.plotly_chart(chart, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(
                '<p style="text-align:center;color:rgba(140,180,240,0.4)!important;'
                'padding:2rem;">Complete your first session to see trends.</p>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── CTA
        st.markdown('<div class="animated-in delay-4">', unsafe_allow_html=True)
        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
        if st.button("I need a reset  ➔", key="dash_cta"):
            navigate_to("Check-In")
        st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE 2: CHECK-IN ───────────────────────────

def page_checkin():
    render_nav()
    _, col, _ = st.columns([1, 2.5, 1])
    with col:
        st.markdown("""
        <div class="animated-in">
        <p class="section-eyebrow">Voice · Vitals · Check-In</p>
        <h2 class="section-title">How are you<br>feeling right now?</h2>
        <p class="section-sub">Take a moment to tune in. Your session begins with awareness.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # ── Audio input
        st.markdown("""
        <p style="font-family:'Syne',sans-serif;font-size:0.85rem;font-weight:500;
        letter-spacing:0.06em;color:rgba(160,210,255,0.8)!important;margin-bottom:0.3rem;">
        🎙️ Speak your mind...</p>
        <p style="font-size:0.78rem;color:rgba(130,170,230,0.5)!important;margin-bottom:0.8rem;">
        Record a voice note and our AI will analyse your vocal sentiment.</p>
        """, unsafe_allow_html=True)

        audio_data = st.audio_input("Voice recording", label_visibility="collapsed")

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

        # ── Manual slider fallback
        st.markdown("""
        <p style="font-family:'Syne',sans-serif;font-size:0.85rem;font-weight:500;
        letter-spacing:0.06em;color:rgba(160,210,255,0.8)!important;margin-bottom:0.3rem;">
        Or rate your stress manually</p>
        """, unsafe_allow_html=True)

        slider_val = st.slider(
            "Stress level", 1, 10,
            value=st.session_state.current_stress_level,
            key="checkin_slider",
            label_visibility="collapsed"
        )

        # Stress level indicator
        color = stress_color(slider_val)
        label = "High Stress" if slider_val >= 8 else ("Moderate Stress" if slider_val >= 5 else "Low Stress")
        bars = "■" * slider_val + "□" * (10 - slider_val)
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
        margin:0.6rem 0 1rem;">
            <span style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700;
            color:{color}!important;">{slider_val}</span>
            <span style="font-size:0.72rem;letter-spacing:0.08em;color:{color}!important;
            text-transform:uppercase;">{label}</span>
            <span style="font-family:monospace;font-size:0.7rem;
            color:{color}55!important;letter-spacing:0.12em;">{bars}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close glass-card

        # ── Process & navigate
        if audio_data is not None or st.button("Analyse & Continue  ➔", key="checkin_cta"):
            if audio_data is not None:
                with st.spinner("Analysing vocal sentiment..."):
                    time.sleep(2)
                # Simulate sentiment → stress level mapping
                inferred = random.randint(4, 9)
                st.session_state.current_stress_level = inferred
                st.toast(f"Vocal analysis complete · Stress indicator: {inferred}/10", icon="🎙️")
                time.sleep(0.5)
            else:
                st.session_state.current_stress_level = slider_val
            navigate_to("MoodSync")

# ── PAGE 3: MOODSYNC ──────────────────────────

def page_moodsync():
    render_nav()

    st.markdown("""
    <div class="animated-in" style="text-align:center;margin-bottom:1.8rem;">
        <p class="section-eyebrow">MoodSync AI · Pod Calibration</p>
        <h2 class="section-title" style="font-size:2rem;">Your prescription is ready.</h2>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    # ── LEFT — AI Prescription
    with left:
        lvl = st.session_state.current_stress_level

        if lvl >= 8:
            rx_level_class, rx_level_text = "high", "⚠ High Stress Detected"
            rx_title = "AI calibrating pod for Deep Delta Recovery."
            rx_detail = (
                "Your biometric indicators suggest significant cortisol elevation. "
                "Protocol: 40-minute deep-delta binaural session, chair intensity at max, "
                "lavender diffusion, and blue-spectrum chromotherapy. "
                "Heart coherence training initiated."
            )
            rx_protocols = ["Delta Wave Binaural", "Progressive Muscle Release", "Heart Coherence Training"]
        elif lvl >= 5:
            rx_level_class, rx_level_text = "medium", "◈ Moderate Tension Detected"
            rx_title = "AI recommending Theta-State Reset session."
            rx_detail = (
                "Mild tension patterns identified. "
                "Protocol: 25-minute theta-wave session with guided box-breathing overlay, "
                "medium chair vibration, citrus diffusion, and warm amber lighting."
            )
            rx_protocols = ["Theta Binaural Blend", "Box Breathing Overlay", "Amber Chromotherapy"]
        else:
            rx_level_class, rx_level_text = "low", "◎ Balanced State"
            rx_title = "AI selecting Mindful Flow maintenance session."
            rx_detail = (
                "Your baseline is calm. This session will deepen focus and creativity. "
                "Protocol: 20-minute alpha-wave flow state, gentle chair movement, "
                "eucalyptus diffusion, and cool teal lighting."
            )
            rx_protocols = ["Alpha Flow State", "Gentle Somatic Release", "Focus Amplification"]

        st.markdown(f"""
        <div class="glass-card">
            <p class="section-eyebrow">AI Engine Output</p>
            <div class="rx-card">
                <div class="rx-level {rx_level_class}">{rx_level_text} · {lvl}/10</div>
                <div class="rx-title">{rx_title}</div>
                <div class="rx-detail">{rx_detail}</div>
                <div style="margin-top:1rem;display:flex;flex-wrap:wrap;gap:0.5rem;">
        """, unsafe_allow_html=True)

        for proto in rx_protocols:
            st.markdown(
                f'<span class="score-badge">◈ {proto}</span>',
                unsafe_allow_html=True
            )

        st.markdown("</div></div></div>", unsafe_allow_html=True)  # close rx-card + glass-card

    # ── RIGHT — Hardware Control Panel
    with right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <p class="section-eyebrow">Pod Hardware Controls</p>
        <p style="font-size:0.82rem;color:rgba(150,190,240,0.6)!important;
        margin-bottom:1rem;">Override AI recommendations manually.</p>
        """, unsafe_allow_html=True)

        st.markdown('<p style="font-size:0.8rem;letter-spacing:0.05em;margin-bottom:0.2rem;">⚡ Biometric Chair Intensity</p>', unsafe_allow_html=True)
        st.session_state.pod_intensity = st.slider(
            "Chair", 1, 10, st.session_state.pod_intensity,
            label_visibility="collapsed", key="pod_intensity_slider"
        )

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem;letter-spacing:0.05em;margin-bottom:0.2rem;">💡 Light Hue</p>', unsafe_allow_html=True)
        st.session_state.pod_hue = st.color_picker(
            "Hue", st.session_state.pod_hue,
            label_visibility="collapsed", key="pod_hue_picker"
        )

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem;letter-spacing:0.05em;margin-bottom:0.2rem;">🌿 Diffuser Strength</p>', unsafe_allow_html=True)
        st.session_state.pod_diffuser = st.slider(
            "Diffuser", 1, 5, st.session_state.pod_diffuser,
            label_visibility="collapsed", key="pod_diffuser_slider"
        )

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem;letter-spacing:0.05em;margin-bottom:0.4rem;">🕐 Reserve Pod Time</p>', unsafe_allow_html=True)
        schedule_options = ["Now", "In 15 mins", "In 30 mins", "In 1 hour", "Tomorrow AM"]
        st.session_state.pod_schedule = st.selectbox(
            "Schedule", schedule_options,
            index=schedule_options.index(st.session_state.pod_schedule),
            label_visibility="collapsed", key="pod_schedule_select"
        )

        # Live preview pill
        h = st.session_state.pod_hue
        st.markdown(f"""
        <div style="margin-top:1rem;padding:0.6rem 1rem;border-radius:10px;
        background:linear-gradient(135deg,{h}22,{h}11);
        border:1px solid {h}44;font-size:0.78rem;color:rgba(200,230,255,0.7)!important;">
            Preview · Chair {st.session_state.pod_intensity}/10 ·
            Diffuser {st.session_state.pod_diffuser}/5 ·
            {st.session_state.pod_schedule}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Initialize Pod  ➔", key="moodsync_cta"):
            with st.spinner("Syncing pod settings..."):
                time.sleep(1.2)
            st.session_state.session_start_time = time.time()
            st.session_state.immersion_started = False
            navigate_to("Immersion")

# ── PAGE 4: IMMERSION ZONE ─────────────────────

def page_immersion():
    render_nav()
    _, col, _ = st.columns([1, 2.8, 1])

    with col:
        st.markdown("""
        <div class="animated-in" style="text-align:center;margin-bottom:0.5rem;">
            <p class="section-eyebrow">Immersion Zone · Active Session</p>
            <h2 class="section-title" style="font-size:2rem;">Your pod is ready.</h2>
        </div>
        """, unsafe_allow_html=True)

        # ── Breathing Animation
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("""
        <div class="breathe-outer">
            <div class="breathe-circle">
                <div class="breathe-label">Inhale...<br>Exhale...</div>
            </div>
            <p class="breathe-hint">4 sec in · 6 sec out</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

        # ── Audio Engine
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-eyebrow" style="margin-bottom:0.8rem;">Hybrid Audio Engine</p>', unsafe_allow_html=True)

        audio_choice = st.radio(
            "Audio source",
            ["FutureForward Originals", "Connect Spotify"],
            index=0 if st.session_state.audio_choice == "FutureForward Originals" else 1,
            horizontal=True,
            label_visibility="collapsed",
            key="audio_radio"
        )
        st.session_state.audio_choice = audio_choice

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

        if audio_choice == "FutureForward Originals":
            # Royalty-free placeholder audio
            st.markdown('<p style="font-size:0.8rem;color:rgba(150,200,255,0.6)!important;margin-bottom:0.5rem;">▶ Deep Delta Recovery · 40 min</p>', unsafe_allow_html=True)
            st.audio(
                "[https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3](https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3)",
                format="audio/mp3"
            )
            # CSS visualiser
            bars_html = '<div class="visualiser">' + ''.join(
                [f'<div class="vis-bar" style="height:{random.randint(8,36)}px;"></div>' for _ in range(8)]
            ) + '</div>'
            st.markdown(bars_html, unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:0.72rem;color:rgba(100,160,220,0.4)!important;letter-spacing:0.12em;">LIVE FREQUENCY VISUALISER</p>', unsafe_allow_html=True)

        else:
            # Valid Spotify embed
            st.markdown('<p style="font-size:0.8rem;color:rgba(150,200,255,0.6)!important;margin-bottom:0.5rem;">Spotify · Deep Focus Playlist</p>', unsafe_allow_html=True)
            components.html(
                """
                <iframe style="border-radius:12px" src="[https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ?utm_source=generator](https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ?utm_source=generator)" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                """,
                height=170
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Toast notification (simulated smart break reminder)
        if not st.session_state.immersion_started:
            st.session_state.immersion_started = True
            st.toast("You've been focused. Enjoy this moment. 🌊", icon="🌙")

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

        # ── End session button
        st.markdown("""
        <div style="text-align:center;margin-bottom:0.5rem;">
            <p style="font-size:0.75rem;color:rgba(120,160,220,0.45)!important;
            letter-spacing:0.1em;text-transform:uppercase;">
            Session in progress · take your time
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("End Session  ➔", key="immersion_end"):
            navigate_to("Reflection")

# ── PAGE 5: REFLECTION ─────────────────────────

def page_reflection():
    render_nav()
    _, col, _ = st.columns([1, 2.5, 1])

    with col:
        st.markdown("""
        <div class="animated-in" style="text-align:center;margin-bottom:1.8rem;">
            <p class="section-eyebrow">Post-Session · Reflection</p>
            <h2 class="section-title" style="font-size:2rem;">How do you feel<br>after your session?</h2>
            <p class="section-sub" style="margin-top:0.5rem;">
                A few moments of reflection seal your progress.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # ── Journal
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:0.85rem;font-weight:500;letter-spacing:0.06em;color:rgba(160,210,255,0.8)!important;margin-bottom:0.4rem;">📝 How are you feeling now?</p>', unsafe_allow_html=True)
        journal = st.text_area(
            "Journal",
            value=st.session_state.session_journal,
            placeholder="Write freely... This is your space. No judgment, just presence.",
            height=120,
            label_visibility="collapsed",
            key="reflection_journal"
        )
        st.session_state.session_journal = journal

        st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

        # ── Post-session stress slider
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:0.85rem;font-weight:500;letter-spacing:0.06em;color:rgba(160,210,255,0.8)!important;margin-bottom:0.4rem;">📊 Current Stress Level</p>', unsafe_allow_html=True)
        post = st.slider(
            "Post stress", 1, 10,
            value=max(1, st.session_state.current_stress_level - 2),
            label_visibility="collapsed",
            key="post_stress_slider"
        )
        st.session_state.post_stress = post

        # Delta visualization
        pre = st.session_state.current_stress_level
        delta = pre - post
        delta_color = "#4fc3f7" if delta >= 0 else "#ff6b8a"
        arrow = "↓" if delta >= 0 else "↑"
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;gap:2rem;
        padding:1rem 0;margin:0.5rem 0;">
            <div style="text-align:center;">
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:600;
                color:#ff6b8a!important;">{pre}</div>
                <div style="font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;
                color:rgba(140,160,200,0.5)!important;">Before</div>
            </div>
            <div style="font-size:2rem;color:{delta_color}!important;">{arrow}</div>
            <div style="text-align:center;">
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:600;
                color:#4fc3f7!important;">{post}</div>
                <div style="font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;
                color:rgba(140,160,200,0.5)!important;">After</div>
            </div>
            <div style="background:rgba(79,195,247,0.1);border:1px solid rgba(79,195,247,0.25);
            border-radius:50px;padding:0.4rem 1rem;text-align:center;">
                <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:600;
                color:{delta_color}!important;">{delta:+d}</div>
                <div style="font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;
                color:rgba(140,160,200,0.5)!important;">Delta</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # close glass-card

        # ── Save & return
        if st.button("Save & Return to Dashboard  ✦", key="reflect_save"):
            # Append to history
            today = datetime.now().strftime("%b %d")
            st.session_state.stress_history.append({
                "date": today,
                "pre_stress": pre,
                "post_stress": post,
            })
            # Keep only last 7 sessions for chart legibility
            if len(st.session_state.stress_history) > 7:
                st.session_state.stress_history = st.session_state.stress_history[-7:]

            # Increment zen score (capped at 10 display, uncapped in state)
            st.session_state.zen_garden_score = min(
                st.session_state.zen_garden_score + 1, 10
            )

            # Reset per-session state
            st.session_state.session_journal = ""
            st.session_state.immersion_started = False

            st.toast("Session saved! Your garden grows. 🌱", icon="✨")
            time.sleep(0.8)
            navigate_to("Dashboard")

# ──────────────────────────────────────────────
# 5. ROUTER — dispatch to the correct page
# ──────────────────────────────────────────────

PAGES = {
    "Dashboard":  page_dashboard,
    "Check-In":   page_checkin,
    "MoodSync":   page_moodsync,
    "Immersion":  page_immersion,
    "Reflection": page_reflection,
}

# Render the current page
current = st.session_state.get("current_page", "Dashboard")
if current in PAGES:
    PAGES[current]()
else:
    st.session_state.current_page = "Dashboard"
    page_dashboard()
