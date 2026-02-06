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

# --- 🎨 الستايل الذهبي (تطبيق مقاسات المربعات الحمراء في الصورة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    /* 🏷️ العناوين (اسم المستخدم / كلمة المرور): حجم 23، حافة سوداء، يمين */
    [data-testid="stWidgetLabel"] p { 
        color: white !important; 
        text-align: right !important; 
        direction: rtl !important; 
        font-family: 'Cairo', sans-serif !important;
        font-size: 23px !important; 
        font-weight: 900 !important;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000 !important;
    }

    /* ✍️ تعديل المربعات لتكون "نحيفة وعريضة" زي الصورة */
    div[data-baseweb="input"] {
        height: 40px !important; /* الارتفاع النحيف زي المربع الأحمر */
        background-color: #1e2129 !important; /* لون داكن زي الصورة */
        border-radius: 10px !important;
        border: 1px solid #fbbf24 !important; /* حافة ذهبية رقيقة */
    }
    
    input {
        height: 40px !important;
        font-size: 18px !important;
        text-align: right !important;
        color: white !important;
        font-weight: bold !important;
    }

    /* الزر الأصفر الصغير (نفس اللي في الصورة) */
    .stButton button {
        height: 45px !important;
        width: 150px !important; /* حجم صغير زي الصورة */
        border-radius: 10px !important;
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
        float: right !important; /* يجي عاليمين تحت المربعات */
    }

    .glass-box { 
        background: transparent !important; /* إخفاء الصندوق الكبير باش تبرز المربعات */
        padding: 20px;
        margin-top: 50px;
    }

    .main-title {
        text-align: center; color: #fbbf24; font-family: 'Cairo'; 
        font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([0.5, 2, 0.5]) # توسيع العمود ليعطي عرض للمربعات
    with col:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
        
        u = st.text_input("اسم المستخدم", key="u_login").upper()
        p = st.text_input("كلمة المرور", type="password", key="p_login")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # شاشة التحكم (ثابتة بنفس المقاسات الرشيقة)
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>لوحة التحكم</h2>", unsafe_allow_html=True)
    
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

    c1, c2 = st.columns(2)
    with c1: st.text_input("الاسم", value=s_name, key="sc_name")
    with c2: st.text_input("رقم الجواز", value=s_pass, key="sc_pass")
    
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
