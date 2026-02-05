import streamlit as st
import numpy as np
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الخلفيات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"
}

# --- 🎨 الستايل (تنسيق المربعات وحذف الشوائب) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف الزوائد */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], 
    [data-testid="stSidebarNav"], .st-emotion-cache-6qob1r, 
    .st-emotion-cache-1kyx738, [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}
    
    html, body, [class*="st-"] {{ 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
    }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* مربع العنوان الشفاف */
    .main-title {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        max-width: 600px;
        margin: 40px auto 20px auto;
        color: white;
        font-size: 28px;
        font-weight: 900;
    }}

    /* بطاقة الدخول المتناسقة */
    .login-card {{
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 500px; /* تحديد عرض البطاقة لتنسيق الخانات */
        margin: 0 auto;
        color: white;
    }}

    /* تنسيق الخانات لتكون متساوية */
    .stTextInput > div > div > input {{
        background-color: white !important;
        color: black !important;
        height: 45px !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center;
    }}
    
    /* تنسيق زر الدخول */
    .stButton > button {{
        height: 50px !important;
        border-radius: 10px !important;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        margin-top: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- منطق الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    
    # استخدام حاوية لمركزية العناصر
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    
    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        user = st.text_input("👤 اسم المستخدم", placeholder="ادخل الاسم هنا").upper()
        passw = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••")
        
        if st.button("دخول النظام", use_container_width=True):
            if user == "ALI FETORY" and passw == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("البيانات غير صحيحة")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- بعد الدخول ---
st.markdown('<div class="main-title">🌍 بوابة المسار الذهبي</div>', unsafe_allow_html=True)
st.info("تم تسجيل الدخول بنجاح يا علي")
if st.button("خروج"):
    st.session_state.auth = False
    st.rerun()
