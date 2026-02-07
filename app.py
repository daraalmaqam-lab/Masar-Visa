import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
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

# --- 🎨 الستايل الذهبي المطور (التوسيط الكامل) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    /* 🎯 حاوية التوسيط المطلق للشاشة الرئيسية */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh; /* يعطي مساحة عمودية للتوسيط */
        width: 100%;
    }

    .main-title {
        text-align: center; color: #fbbf24; font-family: 'Cairo'; 
        font-size: 55px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-bottom: 20px;
    }

    /* 🏷️ العناوين: توسيط النص فوق الخانات */
    [data-testid="stWidgetLabel"] p { 
        color: white !important; 
        text-align: center !important; /* خليت العنوان في النص */
        direction: rtl !important; 
        font-family: 'Cairo', sans-serif !important;
        font-size: 20px !important; 
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px black !important;
        width: 100% !important;
        margin-bottom: 5px !important;
    }

    /* ✍️ تنسيق الخانات (العرض 300px وممركزة) */
    div[data-baseweb="input"] {
        height: 45px !important; 
        width: 320px !important; 
        margin: 0 auto !important; 
        background-color: rgba(30, 33, 41, 0.9) !important; 
        border-radius: 10px !important;
        border: 2px solid #fbbf24 !important;
    }
    
    input {
        height: 45px !important;
        font-size: 18px !important;
        text-align: center !important; /* الكتابة داخل الخانة تكون في النص */
        color: white !important;
    }

    /* الزر الأصفر الممركز */
    .stButton { 
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .stButton button {
        height: 50px !important;
        width: 180px !important; 
        border-radius: 12px !important;
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Cairo' !important;
        font-size: 20px !important;
        margin-top: 25px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # استخدام حاوية الـ wrapper لتوسيط كل شيء
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    u = st.text_input("اسم المستخدم", key="u_login").upper()
    p = st.text_input("كلمة المرور", type="password", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # لوحة التحكم (تظهر بشكل طبيعي بعد الدخول)
    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h1>", unsafe_allow_html=True)
    st.write("---")
    
    with st.container():
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
            
            s_name, s_pass = "", ""
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

            st.text_input("الاسم المستخرج", value=s_name)
            st.text_input("رقم الجواز المستخرج", value=s_pass)
            
            if st.button("تسجيل الخروج"):
                st.session_state.auth = False
                st.rerun()
