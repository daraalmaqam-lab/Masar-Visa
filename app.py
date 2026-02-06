import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ ---
def get_passport_data(file):
    import easyocr
    import cv2
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return reader.readtext(processed, detail=0)

# --- 🎨 الستايل الذهبي (إجبار التمركز والترتيب اليميني) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    .main-title {
        text-align: center; color: #fbbf24; font-family: 'Cairo'; 
        font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-top: 50px; margin-bottom: 40px;
    }

    /* 📦 الحاوية المركزية - تلم الكلمات والمربعات في النص */
    .auth-container {
        max-width: 550px; /* عرض ضيق يجمع العناصر */
        margin: 0 auto; /* توسيط الحاوية في الشاشة */
        direction: rtl;
    }

    /* ستايل السطر: الكلمة بجانب المربع */
    .input-group {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 15px;
        margin-bottom: 20px;
    }

    .custom-label {
        color: white;
        font-family: 'Cairo', sans-serif;
        font-size: 23px;
        font-weight: 900;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
        min-width: 150px; /* ضمان بقاء الكلمات في خط واحد */
        text-align: right;
    }

    /* إجبار مقاس المربع وشكله الداكن */
    div[data-baseweb="input"] {
        height: 40px !important; 
        width: 320px !important; 
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
    .btn-wrapper {
        margin-right: 165px; /* موازنته ليكون تحت المربعات تماماً */
        margin-top: 10px;
    }

    .stButton button {
        height: 42px !important;
        width: 140px !important; 
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    # بداية الحاوية المركزية
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # سطر اسم المستخدم
    st.markdown('<div class="input-group"><div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_field").upper()
    st.markdown('</div>', unsafe_allow_html=True)

    # سطر كلمة المرور
    st.markdown('<div class="input-group"><div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed", key="p_field")
    st.markdown('</div>', unsafe_allow_html=True)

    # سطر زر الدخول
    st.markdown('<div class="btn-wrapper">', unsafe_allow_html=True)
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True) # نهاية الحاوية

else:
    # شاشة التحكم
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    # ... بقية كود التحكم ...
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
    st.text_input("الاسم", value=s_name, key="sc_name")
    st.text_input("رقم الجواز", value=s_pass, key="sc_pass")
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
