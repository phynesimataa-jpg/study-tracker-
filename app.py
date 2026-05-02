import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import base64

# 1. Page Configuration
st.set_page_config(page_title="simataa studytracker", layout="wide")

# --- VIDEO BACKGROUND ENGINE ---
def get_base64_bin(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    # Using the exact filename you requested
    bin_str = get_base64_bin("6fd39406a1b61d04b0c9c39e6b3c51b9.mp4")
    st.markdown(f'''
        <style>
        #bgVideo {{
          position: fixed;
          right: 0;
          bottom: 0;
          min-width: 100%; 
          min-height: 100%;
          z-index: -1;
          filter: brightness(40%) contrast(115%) blur(1px);
        }}
        /* THE RED TITLE STYLE FROM YOUR TIKTOK SCREENSHOT */
        .red-title {{
            color: #FF0000 !important;
            font-size: 65px !important;
            font-weight: 900 !important;
            text-transform: lowercase;
            font-family: 'Arial Black', sans-serif;
            letter-spacing: -3px;
            margin-bottom: -20px;
            padding-top: 20px;
        }}
        .stMetric {{
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid #FF0000;
            border-radius: 12px;
            padding: 10px;
        }}
        </style>
        <video autoplay muted loop id="bgVideo">
          <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
        </video>
    ''', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("Error: Please ensure '6fd39406a1b61d04b0c9c39e6b3c51b9.mp4' is uploaded to your GitHub repository.")

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
st.sidebar.markdown('<h2 style="color: #FF0000; font-weight: 900;">🕹️ CONTROL</h2>', unsafe_allow_html=True)

# MUSIC PLAYER
show_music = st.sidebar.toggle("🎵 Focus Music", value=True)
if show_music:
    st.sidebar.markdown("""
        <iframe style="border-radius:12px" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DX8Ueb990JyS3" 
        width="100%" height="152" frameBorder="0" allowfullscreen="" 
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    """, unsafe_allow_html=True)

# TIMER
timer_on = st.sidebar.toggle("⏲️ Study Timer")
if timer_on:
    t_place = st.sidebar.empty()
    # Basic session tracker
    t_place.metric("Current Session", "Active")

# LOGGING
st.sidebar.divider()
with st.sidebar.expander("📝 Log Subject"):
    subj = st.selectbox("Subject", ["Physics", "Chemistry", "Mathematics", "Biology", "Computing"])
    top = st.text_input("Topic")
    mins = st.number_input("Minutes", 5, 300, 60)
    if st.button("Save to Dashboard"):
        new = pd.DataFrame([[datetime.now().date(), subj, mins, top]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv("study_data.csv", index=False)
        st.sidebar.success("Logged!")
        st.rerun()

# --- MAIN DASHBOARD ---
if not df.empty:
    total_m = df['Minutes'].sum()
    c1, c2 = st.columns(2)
    c1.metric("Total Hours", f"{total_m // 60}h {total_m % 60}m")
    c2.metric("Sessions", len(df))

    st.divider()

    # THE CHART
    chart_df = df.groupby('Subject')['Minutes'].sum().reset_index().sort_values('Minutes')
    fig = px.bar(chart_df, x='Minutes', y='Subject', orientation='h',
                 color_discrete_sequence=['#FF0000'])
    
    fig.update_layout(
        showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="white", xaxis=dict(showgrid=False, visible=False), yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

    # SUBJECT DETAILS
    for s in df['Subject'].unique():
        st.write(f"🔴 **{s}**")
else:
    st.info("Log a session to activate the full dashboard view!")
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

# Function to convert local image to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get your image string
img_path = 'Screenshot_20260502_210303_TikTok.jpg'
bin_str = get_base64(img_path)

# Unified CSS Block
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* This adds the dark overlay/blur you had in your code */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.4); 
        backdrop-filter: blur(10px);
        z-index: -1;
    }}

    /* Global text color */
    .stApp {{
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# Function to convert local image to base64 so it can be used in CSS
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Replace 'Screenshot_20260502_210303_TikTok.jpg' with your actual file name from GitHub
bin_str = get_base64('Screenshot_20260502_210303_TikTok.jpg')

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.4); /* Dark overlay */
        backdrop-filter: blur(10px); /* This adds the blur */
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- APP CONFIG ---
st.set_page_config(page_title="Personal Study Tracker", layout="wide")
st.title("📚 Simataa studytracker Dashboard")

# --- DATA LOADING ---
def load_data():
    try:
        return pd.read_csv("study_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic"])

df = load_data()

# --- SIDEBAR: LOGGING SESSIONS ---
st.sidebar.header("Log New Session")
subject = st.sidebar.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "Biology", "introducing to computing", "communication skills", "Other"])
topic = st.sidebar.text_input("Topic (e.g. Kinematics)")
minutes = st.sidebar.slider("Duration (Minutes)", 15, 180, 60)

if st.sidebar.button("Add Session"):
    new_data = pd.DataFrame([[datetime.now().date(), subject, minutes, topic]], 
                            columns=["Date", "Subject", "Minutes", "Topic"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("study_data.csv", index=False)
    st.sidebar.success("Session Saved!")

# --- MAIN DASHBOARD ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recent Activity")
    st.dataframe(df.tail(10), use_container_width=True)

with col2:
    st.subheader("Study Distribution")
    if not df.empty:
        fig = px.pie(df, values='Minutes', names='Subject', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data yet. Start logging from the sidebar!")

# --- PROGRESS TRACKER ---
st.divider()
st.subheader("Weekly Momentum")
if not df.empty:
    daily_totals = df.groupby("Date")["Minutes"].sum().reset_index()
    fig_line = px.line(daily_totals, x="Date", y="Minutes", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)
