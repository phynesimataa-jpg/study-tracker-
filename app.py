import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import base64
import os

# 1. PAGE SETUP
st.set_page_config(page_title="simataa_vault", layout="centered")

# --- PROFESSIONAL NEON CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #00FF89;
        color: #ffffff;
    }
    
    .main-header {
        background: linear-gradient(90deg, #C0C0C0 0%, #010101 100%);
        padding: 40px; border-radius: 20px; margin-bottom: 30px;
        border-bottom: 4px solid #FF0000;
    }
    
    .logo-text {
        font-size: 50px !important; font-weight: 900 !important;
        letter-spacing: -2px; color: white; margin: 0;
        text-transform: lowercase;
    }

    [data-testid="stMetricValue"] { color: #FF0000 !important; font-weight: 900 !important; }

    .vault-card {
        background: #0f0f0f; border: 1px solid #222;
        padding: 20px; border-radius: 12px; text-align: center;
        transition: 0.3s; margin-bottom: 10px;
    }
    .vault-card:hover { border-color: #FF0000; background: #1a0000; }
    
    .stSidebar { background-color: #000000 !important; border-right: 1px solid #222; }
    
    /* Clean file uploader styling */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255, 0, 0, 0.05);
        border: 2px dashed #FF0000;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA SYSTEM ---
def load_data():
    try:
        data = pd.read_csv("study_data.csv")
        data['Minutes'] = pd.to_numeric(data['Minutes'], errors='coerce').fillna(0)
        return data
    except:
        return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic"])

df = load_data()
subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Computing"]

# --- SIDEBAR: CONTROL ---
st.sidebar.markdown('<h2 style="color:#FF0000;">🕹️ COMMAND</h2>', unsafe_allow_html=True)

# 1. Focus Music
if st.sidebar.toggle("🎵 Focus Music", value=True):
    st.sidebar.markdown('<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX8Ueb9C7V6S7?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>', unsafe_allow_html=True)

# 2. Study Timer
st.sidebar.divider()
if st.sidebar.toggle("⏱️ Timer"):
    if "t_start" not in st.session_state: st.session_state.t_start = time.time()
    elapsed = int(time.time() - st.session_state.t_start)
    st.sidebar.metric("Live Session", f"{elapsed//60}m {elapsed%60}s")
else:
    st.session_state.t_start = None

# 3. Log Grind
st.sidebar.divider()
with st.sidebar.expander("📝 Log Session"):
    s = st.selectbox("Subject", subjects)
    t = st.text_input("Topic")
    m = st.number_input("Minutes", 5, 480, 60)
    if st.button("Commit"):
        new = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), s, float(m), t]], columns=df.columns)
        pd.concat([df, new]).to_csv("study_data.csv", index=False)
        st.rerun()

# --- MAIN INTERFACE ---
st.markdown(f'''
    <div class="main-header">
        <p class="logo-text">simataa.center</p>
        <p style="color: #FF5555; font-weight: 700; margin:0; text-transform: uppercase; font-size: 12px;">
            Elite Status | CBU STEM
        </p>
    </div>
''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 DASHBOARD", "📂 DOCUMENT VAULT"])

with tab1:
    # Top Stats
    total_h = df['Minutes'].sum() / 60
    c1, c2, c3 = st.columns(3)
    c1.metric("Lifetime Grind", f"{total_h:.1f} hrs")
    c2.metric("Rank", "GOAT")
    c3.metric("University", "CBU")

    st.write("### 📉 Momentum")
    if not df.empty:
        g1, g2 = st.columns([1, 1.5])
        with g1:
            fig_pie = px.pie(df, values='Minutes', names='Subject', hole=0.7,
                             color_discrete_sequence=['#FF0000', '#880000', '#440000'])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
        with g2:
            daily = df.groupby('Date')['Minutes'].sum().reset_index()
            fig_line = px.area(daily, x='Date', y='Minutes')
            fig_line.update_traces(line_color='#FF0000', fillcolor='rgba(255,0,0,0.2)')
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_line, use_container_width=True)
    
    st.write("### 📂 Subject Totals")
    v_cols = st.columns(5)
    for i, sub in enumerate(subjects):
        with v_cols[i]:
            val = df[df['Subject'] == sub]['Minutes'].sum() / 60
            st.markdown(f'<div class="vault-card"><p style="color:#888; font-size:12px;">{sub}</p><h3>{val:.1f}h</h3></div>', unsafe_allow_html=True)

with tab2:
    st.header("📂 Digital Resource Vault")
    st.write("Upload your tutorial sheets or notes here to keep them organized by subject.")
    
    target_sub = st.selectbox("Select Subject for Upload", subjects)
    uploaded_files = st.file_uploader("Drop Documents (PDF, Images, etc.)", accept_multiple_files=True)
    
    if uploaded_files:
        st.success(f"Successfully added {len(uploaded_files)} files to {target_sub} Vault.")
        for uploaded_file in uploaded_files:
            # Displaying the files in a clean list
            st.markdown(f'''
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #FF0000;">
                    <strong>{uploaded_file.name}</strong> <span style="color:#888; font-size:12px;">({uploaded_file.size // 1024} KB)</span>
                </div>
            ''', unsafe_allow_html=True)

