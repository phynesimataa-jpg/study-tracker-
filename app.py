import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import base64
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. PAGE CONFIG
st.set_page_config(page_title="simataa center", layout="wide", initial_sidebar_state="expanded")

# --- AI CONFIG ---
# Using your key from the screenshot
genai.configure(api_key="AIzaSyCVGqqt5sMc514q5FQivrawod71iovY_eM")
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# --- HYPER-VIBRANT CSS ---
st.markdown("""
    <style>
    /* Animated Vibrant Background */
    .stApp {
        background: linear-gradient(-45deg, #000000, #1a0000, #660000, #000000);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glow Cards */
    .subject-card {
        padding: 20px; border-radius: 15px; margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 0, 0, 0.3);
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.2);
        text-align: center; transition: 0.3s;
    }
    .subject-card:hover {
        border-color: #FF0000;
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.6);
        transform: scale(1.02);
    }

    /* Metrics & Titles */
    .red-title { 
        color: #FF0000; font-size: 65px; font-weight: 900; 
        text-transform: lowercase; letter-spacing: -4px;
        text-shadow: 0 0 20px rgba(255,0,0,0.5);
    }
    [data-testid="stMetricValue"] { color: #FF0000 !important; font-size: 40px !important; }
    
    /* Clean Sidebar */
    .css-1d391kg { background-color: rgba(0,0,0,0.8); }
    </style>
    """, unsafe_allow_html=True)

# --- VIDEO BACKGROUND ---
def get_base64_bin(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# Matches your file: 6fd39406a1b61d04b0c9c39e6b3c51b9.mp4
vid_str = get_base64_bin("6fd39406a1b61d04b0c9c39e6b3c51b9.mp4")
if vid_str:
    st.markdown(f'''
        <style>#bgVideo {{ position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -1; filter: brightness(25%) contrast(120%); }}</style>
        <video autoplay muted loop id="bgVideo"><source src="data:video/mp4;base64,{vid_str}" type="video/mp4"></video>
    ''', unsafe_allow_html=True)

# --- DATA SYSTEM ---
def load_data():
    try:
        data = pd.read_csv("study_data.csv")
        data['Minutes'] = pd.to_numeric(data['Minutes'], errors='coerce').fillna(0)
        return data
    except:
        return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic"])

df = load_data()

# --- SIDEBAR: COMMAND ---
st.sidebar.markdown('<h1 style="color:#FF0000">🕹️ COMMAND</h1>', unsafe_allow_html=True)

# 1. Focus Music
if st.sidebar.toggle("🎵 Focus Music"):
    st.sidebar.markdown('<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX8Ueb9C7V6S7" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)

# 2. Timer
if st.sidebar.toggle("⏱️ Study Timer"):
    if "t_start" not in st.session_state: st.session_state.t_start = time.time()
    elapsed = int(time.time() - st.session_state.t_start)
    st.sidebar.metric("Live Session", f"{elapsed//60}m {elapsed%60}s")

# 3. Logging (Fixed ValueError)
st.sidebar.divider()
with st.sidebar.expander("📝 Log Session"):
    sub_list = ["Mathematics", "Physics", "Chemistry", "Biology", "Computing"]
    s = st.selectbox("Subject", sub_list)
    t = st.text_input("Topic")
    d = st.number_input("Minutes", 5, 300, 60)
    if st.button("Commit"):
        new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), s, float(d), t]], columns=["Date", "Subject", "Minutes", "Topic"])
        pd.concat([df, new_entry]).to_csv("study_data.csv", index=False)
        st.rerun()

# --- MAIN DASHBOARD ---
tab1, tab2 = st.tabs(["📊 Analytics", "🤖 AI Tutor"])

with tab1:
    st.markdown('<p class="red-title">simataa tracker</p>', unsafe_allow_html=True)
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    total_h = df['Minutes'].sum() / 60
    c1.metric("Total Grind", f"{total_h:.1f} hrs")
    c2.metric("Rank", "GOAT")
    c3.metric("University", "CBU")

    # GRAPHS (Vibrant Plotly)
    st.write("### 📈 Performance Visuals")
    if not df.empty:
        g1, g2 = st.columns(2)
        with g1:
            fig_pie = px.pie(df, values='Minutes', names='Subject', hole=0.7, 
                             color_discrete_sequence=px.colors.sequential.Reds_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False, title="Time Share")
            st.plotly_chart(fig_pie, use_container_width=True)
        with g2:
            daily = df.groupby('Date')['Minutes'].sum().reset_index()
            fig_line = px.area(daily, x='Date', y='Minutes', title="Momentum")
            fig_line.update_traces(line_color='#FF0000', fillcolor='rgba(255,0,0,0.3)')
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_line, use_container_width=True)
    
    # VAULTS
    st.write("### 📂 Subject Vaults")
    v_cols = st.columns(5)
    for i, sub in enumerate(sub_list):
        with v_cols[i]:
            st.markdown(f'<div class="subject-card">{sub}</div>', unsafe_allow_html=True)
            val = df[df['Subject'] == sub]['Minutes'].sum() / 60
            st.write(f"**{val:.1f}h**")

with tab2:
    st.subheader("🤖 Chat with Tutorial Sheets")
    # Fixed file_uploader to prevent image crashes
    doc = st.file_uploader("Upload PDF Tutorials", type=["pdf"])
    
    if doc:
        try:
            reader = PdfReader(doc)
            full_text = "".join([p.extract_text() for p in reader.pages])
            st.success("Document analyzed. The AI is ready.")
            
            if "chat" not in st.session_state: st.session_state.chat = []
            prompt = st.chat_input("Ask a question about the tutorial...")
            
            if prompt:
                context = f"Tutorial Data: {full_text[:8000]}\n\nUser Question: {prompt}"
                response = ai_model.generate_content(context)
                st.session_state.chat.append({"u": prompt, "b": response.text})
            
            for c in st.session_state.chat:
                with st.chat_message("user"): st.write(c["u"])
                with st.chat_message("assistant"): st.write(c["b"])
        except Exception as e:
            st.error(f"Error reading PDF: {e}. Please ensure it is a valid document.")
