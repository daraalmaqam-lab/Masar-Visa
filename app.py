import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🎨 الستايل الذهبي الإجباري ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    /* حاوية التوسيط الكبري */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 80px;
    }

    /* سطر الإدخال: يجمع الكلمة والمربع */
    .input-block {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        width: 480px; /* العرض الكلي للسطر */
        margin-bottom: 20px;
        direction: rtl;
    }

    .label-tag {
        color: white;
        font-family: 'Cairo', sans-serif;
        font-size: 24px;
        font-weight: 900;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
        min-width: 160px;
        text-align: right;
    }

    /* إجبار شكل المربع الصغير الداكن */
    div[data-baseweb="input"] {
        height: 40px !important; 
        width: 300px !important; 
        background-color: #1e2129 !important; 
        border-radius: 8px !important;
        border: 1px solid #fbbf24 !important;
    }
    
    input {
        height: 40px !important;
        font-size: 18px !important;
        text-align: right !important;
        color: white !important;
    }

    /* زر الدخول */
    .btn-row {
        width: 300px;
        margin-right: 175px; /* يخلي الزر يبدأ مع بداية المربعات من اليمين */
        text-align: right;
    }

    .stButton button {
        height: 42px !important;
        width: 140px !important; 
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
        border-radius: 8px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # تطبيق الحاوية المركزية
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="color:#fbbf24; font-family:Cairo; font-size:55px; text-shadow:3px 3px 6px black; margin-bottom:40px;">طيران المسار الذهبي</h1>', unsafe_allow_html=True)

    # سطر اسم المستخدم
    st.markdown('<div class="input-block"><div class="label-tag">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_field").upper()
    st.markdown('</div>', unsafe_allow_html=True)

    # سطر كلمة المرور
    st.markdown('<div class="input-block"><div class="label-tag">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed", key="p_field")
    st.markdown('</div>', unsafe_allow_html=True)

    # سطر الزر
    st.markdown('<div class="btn-row">', unsafe_allow_html=True)
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # شاشة التحكم
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    
    # دالة القراءة (اختياري لو تبيها)
    def get_passport_data(file):
        import easyocr
        import cv2
        reader = easyocr.Reader(['en'])
        image = Image.open(file)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return reader.readtext(processed, detail=0)

    s_name, s_pass = "", ""
    up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    if up_file:
        try:
            res = get_passport_data(up_file)
            raw = "".join(res).upper().replace(" ", "")
            p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
            if p_match: s_pass = p_match.group()
            if "LBY" in raw:
                s_name = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
            else: s_name = res[0] if res else ""
        except: pass

    st.text_input("الاسم واللقب", value=s_name, key="sc_name")
    st.text_input("رقم الجواز", value=s_pass, key="sc_pass")
    
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
