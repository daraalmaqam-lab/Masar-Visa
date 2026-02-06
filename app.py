import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
import time

# 1. إعدادات الصفحة (نفس إعداداتك الأصلية)
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🧠 تحميل القارئ في الخلفية ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

# --- 🌆 المكتبة (نفس صورك) ---
WALLPAPERS = {
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076", 
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "دبي"

# --- 🎨 الستايل الأصلي (الذي حافظنا عليه بناءً على طلبك) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"] {{ display: none !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* الشفافية ومنع المربع الأبيض */
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] > div {{ background-color: transparent !important; }}
    [data-testid="stWidgetLabel"] p {{
        color: white !important; text-align: right !important; direction: rtl !important;
        font-family: 'Cairo' !important; font-size: 20px !important; text-shadow: 2px 2px 4px black !important;
    }}

    input, [data-baseweb="select"], [data-baseweb="input"] {{
        background-color: white !important; border-radius: 10px !important; text-align: right !important; color: black !important;
    }}

    .glass-box {{
        background: rgba(0, 0, 0, 0.45); padding: 25px; border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.2); margin-bottom: 20px;
    }}

    .inner-title {{
        font-family: 'Cairo' !important; font-size: 30px !important; color: #fbbf24;
        text-align: center; text-shadow: 2px 2px 5px black;
        border-bottom: 3px solid #fbbf24; padding-bottom: 10px; margin-bottom: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 1️⃣ الشاشة الرئيسية (بدون أي تغيير) ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-box" style="margin-top:100px;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي ✈️</div>', unsafe_allow_html=True)
        user_input_val = st.text_input("اسم المستخدم").upper()
        pass_input = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (user_input_val == "ALI" or user_input_val == "ALI FETORY") and pass_input == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2️⃣ شاشة التحكم (هنا أضفنا القارئ فقط) ---
else:
    st.markdown('<div class="inner-title">🌍 لوحة التحكم - شركة المسار الذهبي</div>', unsafe_allow_html=True)
    
    # حجة القارئ الآلي
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📸 ارفع صورة الجواز لتعبئة البيانات تلقائياً", type=['jpg', 'jpeg', 'png'])
    
    scanned_res = {"name": "", "pass": ""}
    if uploaded_file:
        reader = load_ocr()
        image = Image.open(uploaded_file)
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        with st.spinner('جاري المسح الضوئي...'):
            results = reader.readtext(img_cv, detail=0)
            if results:
                scanned_res["name"] = results[0].upper()
                scanned_res["pass"] = results[1] if len(results) > 1 else ""
        st.success("تمت القراءة!")
    st.markdown('</div>', unsafe_allow_html=True)

    # حجة البيانات
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.text_input("الاسم", value=scanned_res["name"])
    with c2: st.text_input("رقم الجواز", value=scanned_res["pass"])
    with c3: st.selectbox("الوجهة", ["إيطاليا", "فرنسا", "ألمانيا"])
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("خروج 🚪"):
        st.session_state.auth = False
        st.rerun()
