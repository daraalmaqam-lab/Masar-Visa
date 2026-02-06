import streamlit as st
import numpy as np
from PIL import Image
import re

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Golden Path - System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== نظام الثيمات ==================
if "theme" not in st.session_state:
    st.session_state.theme = "الذهبي الملكي"

with st.sidebar:
    st.title("⚙️ إعدادات الشكل")
    st.session_state.theme = st.selectbox(
        "اختر الثيم المفضل:",
        ["الذهبي الملكي", "الليلي الغامق", "السحابي الهادئ"]
    )

# تعريف خصائص كل ثيم
themes = {
    "الذهبي الملكي": {
        "bg_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
        "primary": "#fbbf24",
        "text_shadow": "4px 4px 15px black"
    },
    "الليلي الغامق": {
        "bg_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=2074",
        "primary": "#3b82f6",
        "text_shadow": "2px 2px 10px blue"
    },
    "السحابي الهادئ": {
        "bg_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070",
        "primary": "#10b981",
        "text_shadow": "2px 2px 10px green"
    }
}

current_theme = themes[st.session_state.theme]

# ================== 🎨 CSS المتفاعل مع الثيمات ==================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

[data-testid="stHeader"], header, footer {{
    display: none !important;
}}

.stApp {{
    background-image: url("{current_theme['bg_url']}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* حاوية التوسيط */
[data-testid="stVerticalBlock"] {{
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 100% !important; 
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 9999;
}}

.main-title {{
    color: {current_theme['primary']};
    font-family: 'Cairo', sans-serif;
    font-size: 80px;
    font-weight: 900;
    text-shadow: {current_theme['text_shadow']};
    margin-bottom: 20px;
    text-align: center;
}}

div[data-baseweb="input"] {{
    width: 380px !important;
    background-color: rgba(30, 33, 41, 0.9) !important;
    border-radius: 12px !important;
    border: 2px solid {current_theme['primary']} !important;
    margin-bottom: 15px !important;
}}

input {{
    text-align: center !important;
    color: white !important;
    font-size: 20px !important;
}}

.stButton button {{
    height: 55px;
    width: 220px;
    background-color: {current_theme['primary']};
    color: black;
    font-weight: bold;
    font-family: 'Cairo';
    border-radius: 15px;
    border: none;
    font-size: 22px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
    transition: 0.3s;
}}

.stButton button:hover {{
    transform: scale(1.05);
    background-color: white;
    color: {current_theme['primary']};
}}
</style>
""", unsafe_allow_html=True)

# ================== نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown(f'<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)

    u = st.text_input("اسم المستخدم", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("كلمة المرور", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

else:
    st.markdown(f"<h1 style='text-align:center; color:{current_theme['primary']}; font-family:Cairo;'>🌍 لوحة التحكم - {st.session_state.theme}</h1>", unsafe_allow_html=True)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
