import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

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
