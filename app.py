import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. الإعدادات المقفلة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة المخ الذكي للقارئ ---
def get_passport_data(file):
    import easyocr
    import cv2
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return reader.readtext(processed, detail=0)

# --- 🎨 الستايل الذهبي (توسيع المربعات لتناسب حجم العنوان) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    /* العنوان الرئيسي */
    .main-title {
        text-align: center; 
        color: #fbbf24; 
        font-family: 'Cairo', sans-serif; 
        font-size: 45px; 
        font-weight: 900;
        text-shadow: 3px 3px 6px black;
        margin-bottom: 20px;
    }

    /* 🏷️ العناوين (اسم المستخدم / كلمة المرور): يمين، حجم 23، حافة سوداء */
    [data-testid="stWidgetLabel"] p { 
        color: white !important; 
        text-align: right !important; 
        direction: rtl !important; 
        font-family: 'Cairo', sans-serif !important;
        font-size: 23px !important; 
        font-weight: 900 !important;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000 !important;
        margin-bottom: 8px !important;
    }

    /* ✍️ تكبير وتوسيع المربعات لتناسب فخامة العنوان */
    div[data-baseweb="input"] {
        height: 60px !important; /* زيادة الارتفاع ليكون واضح ومريح */
        background-color: white !important;
        border-radius: 15px !important;
        border: 2px solid #fbbf24 !important;
    }
    
    input {
        height: 60px !important;
        font-size: 22px !important; /* تكبير الخط داخل المربع */
        text-align: right !important;
        direction: rtl !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* ستايل الأزرار */
    .stButton button {
        height: 60px !important;
        border-radius: 15px !important;
        background-color: #fbbf24 !important;
        color: black !important;
        font-size: 22px !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
        width: 100% !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
    }

    .glass-box { 
        background: rgba(0, 0, 0, 0.5); 
        padding: 40px; 
        border-radius: 30px; 
        border: 1px solid rgba(255, 255, 255, 0.2); 
        margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 2, 1]) # جعل العمود أوسع ليناسب التصميم الجديد
    with col:
        st.markdown('<div class="glass-box" style="margin-top:80px;">', unsafe_allow_html=True)
        st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم", key="u_login").upper()
        p = st.text_input("كلمة المرور", type="password", key="p_login")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # شاشة التحكم
    st.markdown('<div class="main-title" style="text-align:right;">🌍 لوحة التحكم الذكية</div>', unsafe_allow_html=True)
    
    s_name, s_pass = "", ""
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    if up_file:
        with st.spinner('جاري المسح...'):
            try:
                res = get_passport_data(up_file)
                raw = "".join(res).upper().replace(" ", "")
                p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
                if p_match: s_pass = p_match.group()
                if "LBY" in raw:
                    s_name = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
                else: s_name = res[0] if res else ""
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.text_input("الاسم واللقب", value=s_name, key="sc_name")
    with c2: st.text_input("رقم الجواز", value=s_pass, key="sc_pass")
    if st.button("خروج 🚪"):
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
