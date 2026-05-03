import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
import base64
import random
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. PAGE SETUP
st.set_page_config(page_title="simataa command center", layout="wide", initial_sidebar_state="expanded")

# --- AI CONFIGURATION ---
# Using the key you just provided
genai.configure(api_key="AIzaSyCVGqqt5sMc514q5FQivrawod71iovY_eM")
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# --- STYLE ENGINE ---
st.markdown("""
    <style>
    .subject-card {
        padding: 20px; border-radius: 15px; margin-bottom: 15px;
        border-left: 12px solid; background: rgba(255, 255, 255, 0.08);
        transition: transform 0.3s; color: white;
    }
    .subject-card:hover { transform: scale(1.03); background: rgba(255, 255, 255, 0.15); }
    .greeting-box {
        padding: 25px; border-radius: 15px; background: rgba(255, 0, 0, 0.15);
        border: 2px solid #FF0000; text-align: center; margin-bottom: 20px;
    }
    .red-title { 
        color: #FF0000 !important; font-size: 60px !important; 
        font-weight: 900 !important; text-transform: lowercase; letter-spacing: -3px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- VIDEO BACKGROUND ---
def get_base64_bin(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

bin_str = get_base64_bin("6fd39406a1b61d04b0c9c39e6b3c51b9.mp4")
if bin_str:
    st.markdown(f'''
        <style>#bgVideo {{ position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -1; filter: brightness(25%); }}</style>
        <video autoplay muted loop id="bgVideo"><source src="data:video/mp4;base64,{bin_str}" type="video/mp4"></video>
    ''', unsafe_allow_html=True)

# --- GREETINGS ---
hour = datetime.now().hour
if 5 <= hour < 12: msg, sub = "Good Morning, Simataa", "The GOATs are already awake. Let's work."
elif 12 <= hour < 18: msg, sub = "Good Afternoon", "Keep the momentum going."
elif 18 <= hour < 22: msg, sub = "Good Evening", "Finishing strong today."
else: msg, sub = "Midnight Focus", "Silent hours are for the champions."
st.markdown(f'''<div class="greeting-box"><h1>{msg}</h1><p>{sub}</p></div>''', unsafe_allow_html=True)

# --- DATA LOAD ---
def load_data():
    try: return pd.read_csv("study_data.csv")
    except: return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic", "Achievement", "Grade"])
df = load_data()
df['Date'] = pd.to_datetime(df['Date'])

# --- TABS ---
tab1, tab2 = st.tabs(["🚀 Dashboard & Vaults", "🤖 AI Study Partner"])

with tab1:
    st.markdown('<h1 class="red-title">simataa studytracker</h1>', unsafe_allow_html=True)
    
    # Weekly Stats
    last_7 = df[df['Date'] >= (datetime.now() - timedelta(days=7))]
    weekly_hrs = last_7['Minutes'].sum() / 60
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Focus this Week", f"{weekly_hrs:.1f} hrs")
        st.progress(min(weekly_hrs/25, 1.0)) 
    with c2:
        st.subheader("🏆 CBU Leaderboard")
        lb = pd.DataFrame({"User": ["Simataa", "Musoka", "Grace", "James"], "Hrs": [weekly_hrs, 18.5, 22.1, 15.0]}).sort_values("Hrs", ascending=False)
        st.table(lb)

    # Subject Vaults
    st.write("### Your Memory Vaults")
    subs = {"Mathematics": "#FF1744", "Physics": "#2979FF", "Chemistry": "#00E676", "Biology": "#FFEA00", "Computing": "#D500F9"}
    v_cols = st.columns(5)
    for i, (s_name, s_clr) in enumerate(subs.items()):
        with v_cols[i]:
            st.markdown(f'<div class="subject-card" style="border-color:{s_clr}">{s_name}</div>', unsafe_allow_html=True)
            with st.expander("Vault"):
                s_df = df[df['Subject'] == s_name]
                st.write(f"Total: {s_df['Minutes'].sum()/60:.1f}h")
                if not s_df.empty:
                    st.caption(s_df.tail(3)[['Date', 'Topic']])

with tab2:
    st.subheader("🤖 Chat with Tutorial Sheets")
    doc = st.file_uploader("Upload PDF (Tutorials/Notes)", type="pdf")
    if doc:
        reader = PdfReader(doc)
        doc_text = "".join([p.extract_text() for p in reader.pages])
        st.success("Document Loaded!")
        
        if "messages" not in st.session_state: st.session_state.messages = []
        user_in = st.chat_input("Ask about the tutorial questions...")
        
        if user_in:
            prompt = f"Context: {doc_text}\n\nQuestion: {user_in}"
            resp = ai_model.generate_content(prompt)
            st.session_state.messages.append({"u": user_in, "b": resp.text})
            
        for m in st.session_state.messages:
            with st.chat_message("user"): st.write(m["u"])
            with st.chat_message("assistant"): st.write(m["b"])

# --- SIDEBAR LABS ---
st.sidebar.markdown('<h1 style="color:#FF0000">🧪 THE LABS</h1>', unsafe_allow_html=True)

# Live Timer
if "t_start" not in st.session_state: st.session_state.t_start = None
if st.sidebar.button("⏱️ Start/Reset Timer"): st.session_state.t_start = time.time()

if st.session_state.t_start:
    elapsed = int(time.time() - st.session_state.t_start)
    st.sidebar.metric("Active Session", f"{elapsed//60}m {elapsed%60}s")
    if elapsed >= 1200: 
        st.sidebar.warning("🔥 20 MINS! STAY FOCUSED.")
        st.sidebar.image("https://www.brainyquote.com/photos_tr/en/e/elonmusk/630403/elonmusk1-2x.jpg")

# Countdown
exam = st.sidebar.date_input("Exam Date", datetime(2026, 6, 1))
st.sidebar.error(f"⚠️ {(exam - datetime.now().date()).days} Days to Exam")

# Log Data
with st.sidebar.expander("📝 Log Session"):
    sub_log = st.selectbox("Subject", list(subs.keys()))
    top_log = st.text_input("Topic")
    min_log = st.number_input("Minutes", 5, 300, 60)
    if st.button("Commit"):
        new_row = pd.DataFrame([[datetime.now().date(), sub_log, min_log, top_log, "Done", 0]], columns=df.columns)
        pd.concat([df, new_row]).to_csv("study_data.csv", index=False)
        st.rerun()
