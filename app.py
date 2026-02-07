import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ الذكي ---
def get_passport_data(file):
    import easyocr
    import cv2
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return reader.readtext(processed, detail=0)

# --- 🎨 الستايل الذهبي (توسيط إجباري 100%) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    /* 🎯 التوسيط المطلق في وسط الشاشة بالضبط */
    [data-testid="stVerticalBlock"] {
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 400px !important; /* عرض منطقة الدخول */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .main-title {
        text-align: center; color: #fbbf24; font-family: 'Cairo'; 
        font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-bottom: 20px; white-space: nowrap;
    }

    /* 🏷️ العناوين: ممركزة فوق الخانات */
    [data-testid="stWidgetLabel"] p { 
        color: white !important; 
        text-align: center !important; 
        width: 100% !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 22px !important; 
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px black !important;
    }

    /* ✍️ المربعات: عرض 300px ممركزة */
    div[data-baseweb="input"] {
        height: 45px !important; 
        width: 300px !important; 
        margin: 0 auto !important; 
        background-color: #1e2129 !important; 
        border-radius: 10px !important;
        border: 2px solid #fbbf24 !important;
    }
    
    input {
        text-align: center !important;
        color: white !important;
        font-size: 18px !important;
    }

    /* زر الدخول */
    .stButton button {
        height: 50px !important;
        width: 200px !important; 
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
        font-size: 22px !important;
        margin-top: 20px !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    u = st.text_input("اسم المستخدم", key="u_login").upper()
    p = st.text_input("كلمة المرور", type="password", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")
else:
    # لوحة التحكم - نلغي التوسيط المطلق عشان تخدم براحتك
    st.markdown("""<style>[data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; }</style>""", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم</h1>", unsafe_allow_html=True)
    
    up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    if st.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
