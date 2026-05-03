import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
import base64
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. PAGE SETUP
st.set_page_config(page_title="simataa command center", layout="wide", initial_sidebar_state="expanded")

# --- AI CONFIGURATION ---
genai.configure(api_key="AIzaSyCVGqqt5sMc514q5FQivrawod71iovY_eM")
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# --- VIBRANT STYLE ENGINE ---
st.markdown("""
    <style>
    /* Vibrant Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #4d0000 100%);
    }
    
    /* Neon Glow Cards */
    .subject-card {
        padding: 25px; border-radius: 15px; margin-bottom: 20px;
        border: 1px solid rgba(255, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
        transition: all 0.3s ease; color: white; text-align: center;
    }
    .subject-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 8px 25px rgba(255, 0, 0, 0.5);
        background: rgba(255, 0, 0, 0.1);
    }

    /* Vibrant Greeting Box */
    .greeting-box {
        padding: 30px; border-radius: 20px; 
        background: linear-gradient(90deg, rgba(255,0,0,0.2) 0%, rgba(0,0,0,0.6) 100%);
        border-left: 10px solid #FF0000;
        margin-bottom: 30px; box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
    }

    .red-title { 
        color: #FF0000 !important; font-size: 60px !important; 
        font-weight: 900 !important; text-transform: lowercase; 
        letter-spacing: -3px; text-shadow: 2px 2px 10px rgba(255,0,0,0.4);
    }
    
    /* Fix for metric text visibility */
    [data-testid="stMetricValue"] { color: #FF3333 !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #FFAAAA !important; }
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
        <style>#bgVideo {{ position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -1; filter: brightness(20%) saturate(150%); }}</style>
        <video autoplay muted loop id="bgVideo"><source src="data:video/mp4;base64,{bin_str}" type="video/mp4"></video>
    ''', unsafe_allow_html=True)

# --- GREETINGS ---
hour = datetime.now().hour
msg = "Good Morning, Simataa" if 5 <= hour < 12 else "Good Afternoon" if 12 <= hour < 18 else "Good Evening"
st.markdown(f'''<div class="greeting-box"><h1 style="margin:0;">{msg}</h1><p style="color:#FF5555;">Focus like a champion today.</p></div>''', unsafe_allow_html=True)

# --- DATA ENGINE ---
def load_data():
    try: 
        data = pd.read_csv("study_data.csv")
        data['Date'] = pd.to_datetime(data['Date'])
        data['Minutes'] = pd.to_numeric(data['Minutes'], errors='coerce').fillna(0)
        return data
    except: 
        return pd.DataFrame(columns=["Date", "Subject", "Minutes", "Topic"])
df = load_data()

# --- SIDEBAR: CONTROLS ---
st.sidebar.markdown('<h1 style="color:#FF0000">🕹️ COMMAND</h1>', unsafe_allow_html=True)

# 1. MUSIC
music_on = st.sidebar.toggle("🎵 Focus Music")
if music_on:
    st.sidebar.markdown('<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX8Ueb9C7V6S7" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)

# 2. TIMER
st.sidebar.divider()
timer_on = st.sidebar.toggle("⏱️ Study Timer")
if timer_on:
    if "t_start" not in st.session_state: st.session_state.t_start = time.time()
    elapsed = int(time.time() - st.session_state.t_start)
    st.sidebar.metric("Active Session", f"{elapsed//60}m {elapsed%60}s")
    if elapsed >= 1200: st.sidebar.warning("🔥 20 MINS! STAY LETHAL.")
else:
    st.session_state.t_start = None

# 3. LOGGING
st.sidebar.divider()
with st.sidebar.expander("📝 Log Grind"):
    sub_list = ["Mathematics", "Physics", "Chemistry", "Biology", "Computing"]
    s_choice = st.selectbox("Subject", sub_list)
    t_choice = st.text_input("Topic")
    d_choice = st.number_input("Minutes", 5, 300, 60)
    if st.button("Commit to Vault"):
        new_row = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), s_choice, float(d_choice), t_choice]], columns=df.columns)
        pd.concat([df, new_row]).to_csv("study_data.csv", index=False)
        st.rerun()

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["📊 Analytics", "🤖 AI Tutor"])

with tab1:
    st.markdown('<h1 class="red-title">simataa studytracker</h1>', unsafe_allow_html=True)
    
    # ROW 1: METRICS
    total_h = df['Minutes'].sum() / 60
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Hours", f"{total_h:.1f}h")
    m2.metric("Sessions", len(df))
    m3.metric("Goal Progress", f"{min((total_h/30)*100, 100):.0f}%")

    # ROW 2: VIBRANT GRAPHS
    if not df.empty:
        g1, g2 = st.columns(2)
        with g1:
            fig_pie = px.pie(df, values='Minutes', names='Subject', hole=0.6, 
                             title="Focus Distribution", color_discrete_sequence=px.colors.sequential.Reds_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
        with g2:
            daily = df.groupby('Date')['Minutes'].sum().reset_index()
            fig_line = px.area(daily, x='Date', y='Minutes', title="Grind Momentum")
            fig_line.update_traces(line_color='#FF0000', fillcolor='rgba(255,0,0,0.2)')
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_line, use_container_width=True)

    # ROW 3: VAULTS
    st.write("### 📂 Subject Vaults")
    v_cols = st.columns(5)
    clrs = ["#FF1744", "#2979FF", "#00E676", "#FFEA00", "#D500F9"]
    for i, s in enumerate(sub_list):
        with v_cols[i]:
            st.markdown(f'<div class="subject-card" style="border-color:{clrs[i]}">{s}</div>', unsafe_allow_html=True)
            s_val = df[df['Subject'] == s]['Minutes'].sum() / 60
            st.write(f"<h4 style='text-align:center; color:{clrs[i]}'>{s_val:.1f}h</h4>", unsafe_allow_html=True)

with tab2:
    st.subheader("🤖 Chat with Tutorial Sheets")
    doc = st.file_uploader("Upload PDF", type="pdf")
    if doc:
        reader = PdfReader(doc)
        txt = "".join([p.extract_text() for p in reader.pages])
        st.success("Analysis Complete.")
        
        if "chat" not in st.session_state: st.session_state.chat = []
        u_in = st.chat_input("Ask a question...")
        
        if u_in:
            prompt = f"Doc: {txt[:8000]}\nQuestion: {u_in}"
            response = ai_model.generate_content(prompt)
            st.session_state.chat.append({"u": u_in, "b": response.text})
            
        for c in st.session_state.chat:
            with st.chat_message("user"): st.write(c["u"])
            with st.chat_message("assistant"): st.write(c["b"])
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
