import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import base64

# 1. Page Configuration
st.set_page_config(page_title="simataa studytracker", layout="wide", initial_sidebar_state="expanded")

# --- VIDEO BACKGROUND ENGINE ---
def get_base64_bin(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    # Uses your exact Mbappé video filename
    bin_str = get_base64_bin("6fd39406a1b61d04b0c9c39e6b3c51b9.mp4")
    st.markdown(f'''
        <style>
        #bgVideo {{
          position: fixed; right: 0; bottom: 0;
          min-width: 100%; min-height: 100%;
          z-index: -1; filter: brightness(35%) contrast(115%) blur(1px);
        }}
        /* THE RED TITLE FROM TIKTOK */
        .red-title {{
            color: #FF0000 !important; font-size: 65px !important;
            font-weight: 900 !important; text-transform: lowercase;
            font-family: 'Arial Black', sans-serif; letter-spacing: -3px;
            margin-bottom: -20px; padding-top: 20px;
        }}
        /* STYLING FOR THE DASHBOARD NUMBERS */
        .stMetric {{
            background: rgba(0, 0, 0, 0.5); border: 2px solid #FF0000;
            border-radius: 12px; padding: 10px;
        }}
        </style>
        <video autoplay muted loop id="bgVideo"><source src="data:video/mp4;base64,{bin_str}" type="video/mp4"></video>
    ''', unsafe_allow_html=True)
except Exception:
    st.warning("Video not found. Ensure '6fd39406a1b61d04b0c9c39e6b3c51b9.mp4' is uploaded to GitHub.")

# --- THE HEADER ---
st.markdown('<h1 class="red-title">simataa studytracker</h1>', unsafe_allow_html=True)
st.write("---")

# 2. Data Logic
def load_data():
    try:
        return pd.read_csv("study_data.csv")
    except:
        return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic"])

df = load_data()

# --- SIDEBAR: CONTROL CENTER ---
st.sidebar.markdown('<h2 style="color: #FF0000; font-weight: 900;">🕹️ CONTROLS</h2>', unsafe_allow_html=True)

# LIVE TIMER
st.sidebar.subheader("⏲️ Study Timer")
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

col1, col2 = st.sidebar.columns(2)
if col1.button("▶️ Start"):
    st.session_state.start_time = time.time()
    st.session_state.timer_running = True
if col2.button("⏹️ Stop"):
    st.session_state.timer_running = False

if st.session_state.timer_running and st.session_state.start_time:
    timer_place = st.sidebar.empty()
    # Live counting loop
    while st.session_state.timer_running:
        elapsed = time.time() - st.session_state.start_time
        m, s = divmod(int(elapsed), 60)
        timer_place.metric("Focusing for:", f"{m:02d}:{s:02d}")
        time.sleep(1)

# MUSIC PLAYER
st.sidebar.divider()
show_music = st.sidebar.toggle("🎵 Focus Music", value=True)
if show_music:
    st.sidebar.markdown("""
        <iframe style="border-radius:12px" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DX8Uebhn9wzrS" 
        width="100%" height="152" frameBorder="0" allowfullscreen="" 
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    """, unsafe_allow_html=True)

# LOGGING
st.sidebar.divider()
with st.sidebar.expander("📝 Log Session"):
    # Pre-filled with standard STEM subjects
    subj = st.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "Biology", "Computing"])
    top = st.text_input("Topic Worked On")
    mins = st.number_input("Minutes", 5, 300, 60)
    if st.button("Save to Dashboard"):
        new = pd.DataFrame([[datetime.now().date(), subj, mins, top]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv("study_data.csv", index=False)
        st.rerun()

# --- MAIN DASHBOARD VISUALS ---
if not df.empty:
    # Top Stats Row
    total_m = df['Minutes'].sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Focus Time", f"{total_m // 60}h {total_m % 60}m")
    c2.metric("Sessions Logged", len(df))
    c3.metric("Latest Subject", df['Subject'].iloc[-1])

    st.divider()

    # The Chart (Digital Wellbeing Horizontal Style)
    st.subheader("Time Distribution")
    chart_df = df.groupby('Subject')['Minutes'].sum().reset_index().sort_values('Minutes')
    fig = px.bar(chart_df, x='Minutes', y='Subject', orientation='h',
                 color='Subject', color_discrete_sequence=['#FF0000', '#CC0000', '#990000', '#660000'])
    
    fig.update_layout(
        showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="white", xaxis=dict(showgrid=False, showticklabels=False, title=""), 
        yaxis=dict(showgrid=False, title="")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Subject Mastery List
    st.markdown("### 📖 Subject Mastery")
    for s in df['Subject'].unique():
        # Gathers all topics you've logged under this specific subject
        topics = df[df['Subject'] == s]['Topic'].dropna().unique()
        topics_str = ", ".join(topics) if len(topics) > 0 else "General"
        st.write(f"🔴 **{s}**: {topics_str}")

else:
    st.info("Your dashboard is empty. Use the sidebar on the left to log your first session!")
