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

# --- 🎨 الستايل الذهبي (ترتيب العناصر لليمين) ---
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
        font-size: 45px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-bottom: 40px;
    }

    /* 🏷️ العناوين (اسم المستخدم / كلمة المرور): حجم 23، حافة سوداء */
    [data-testid="stWidgetLabel"] p { 
        color: white !important; 
        text-align: right !important; 
        direction: rtl !important; 
        font-family: 'Cairo', sans-serif !important;
        font-size: 23px !important; 
        font-weight: 900 !important;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000 !important;
        margin: 0 !important;
        padding-top: 5px !important;
    }

    /* ✍️ المربعات: طول 300px وارتفاع 40px */
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

    /* زر دخول النظام على اليمين */
    .stButton { text-align: right !important; width: 300px !important; }
    .stButton button {
        height: 45px !important;
        width: 150px !important; 
        border-radius: 10px !important;
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
    }

    /* حاوية لتوسيط الطاقم كله في نص الشاشة */
    .login-box-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="login-box-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    # استخدام الأعمدة لوضع الكلمات يمين المربعات
    # كولوم للمربعات وكولوم للكلمات
    
    # السطر الأول: اسم المستخدم
    col1, col2 = st.columns([2, 1])
    with col1:
        u = st.text_input("", key="u_login", label_visibility="collapsed").upper()
    with col2:
        st.markdown('<p style="color:white; font-size:23px; font-weight:900; text-align:right; font-family:Cairo; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;">اسم المستخدم</p>', unsafe_allow_html=True)

    # السطر الثاني: كلمة المرور
    col1_p, col2_p = st.columns([2, 1])
    with col1_p:
        p = st.text_input("", type="password", key="p_login", label_visibility="collapsed")
    with col2_p:
        st.markdown('<p style="color:white; font-size:23px; font-weight:900; text-align:right; font-family:Cairo; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;">كلمة المرور</p>', unsafe_allow_html=True)

    # السطر الثالث: زر الدخول (تحت المربعات على اليمين)
    col_btn, _ = st.columns([2, 1])
    with col_btn:
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # شاشة التحكم
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>لوحة التحكم</h2>", unsafe_allow_html=True)
    # باقي الكود كما هو...
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
