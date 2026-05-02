import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Personal Study Tracker", layout="wide")
st.title("📚 StudyTrack Dashboard")

# --- DATA LOADING ---
def load_data():
    try:
        return pd.read_csv("study_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic"])

df = load_data()

# --- SIDEBAR: LOGGING SESSIONS ---
st.sidebar.header("Log New Session")
subject = st.sidebar.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "Biology", "Other"])
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
