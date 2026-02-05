import streamlit as st
import numpy as np
from PIL import Image

# إعدادات الصفحة الأساسية لإلغاء أي هوامش
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الخلفيات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"
}

# --- 🎨 الستايل النهائي (القضاء على الرموز والمربعات السوداء) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* 1. حذف كل زوائد ستريمليت والرموز الغريبة نهائياً */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], 
    [data-testid="stSidebarNav"], .st-emotion-cache-6qob1r, 
    .st-emotion-cache-1kyx738, [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    /* 2. تنظيف اتجاه الصفحة والخط */
    html, body, [class*="st-"] {{ 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
        color: white;
    }}

    /* 3. تعيين الخلفية */
    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 4. المربع الشفاف للعنوان (بدون سواد) */
    .main-title {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        max-width: 800px;
        margin: 40px auto;
        font-size: 32px;
        font-weight: 900;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}

    /* 5. المربع الشفاف للبيانات */
    .content-card {{
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 900px;
        margin: 20px auto;
    }}

    /* تنسيق المدخلات */
    input {{ 
        background-color: white !important; 
        color: black !important; 
        border-radius: 10px !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- منطق الدخول (بسيط ونظيف) ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    user = st.text_input("اسم المستخدم").upper()
    passw = st.text_input("كلمة المرور", type="password")
    if st.button("دخول النظام", use_container_width=True):
        if user == "ALI FETORY" and passw == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- الواجهة الرئيسية بعد الدخول ---
st.markdown('<div class="main-title">🌍 بوابة المسار الذهبي</div>', unsafe_allow_html=True)

st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.subheader("📋 بيانات المنظومة")
col1, col2 = st.columns(2)
with col1:
    st.text_input("اللقب")
    st.text_input("الاسم")
with col2:
    st.text_input("رقم الجواز")
    st.selectbox("الدولة", ["إيطاليا", "فرنسا", "ألمانيا"])

if st.button("🚪 خروج", use_container_width=True):
    st.session_state.auth = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
