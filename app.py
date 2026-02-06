import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. الإعدادات الأصلية المقفلة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ الذكي (مخ المنظومة) ---
def smart_ocr_reader(file):
    import easyocr
    import cv2
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # تحسين الصورة للقراءة الصعبة
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return reader.readtext(processed, detail=0)

# --- 🎨 الستايل الذهبي الأصلي (ممنوع التغيير) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] { display: none !important; }
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }
    div[data-testid="stWidgetLabel"] { background-color: transparent !important; }
    div[data-testid="stWidgetLabel"] p { 
        color: white !important; text-align: right !important; 
        text-shadow: 2px 2px 4px black !important; font-family: 'Cairo', sans-serif !important;
    }
    input { text-align: right !important; font-weight: bold !important; }
    .glass-box { background: rgba(0, 0, 0, 0.45); padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # الشاشة الرئيسية كما كانت تماماً
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-box" style="margin-top:100px;">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#fbbf24;'>طيران المسار الذهبي</h1>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # شاشة التحكم (التعديل في الوظيفة وليس الشكل)
    st.markdown("<h2 style='text-align:right; color:#fbbf24;'>لوحة التحكم</h2>", unsafe_allow_html=True)
    
    # تعريف المتغيرات لتجنب الأخطاء
    s_name, s_pass = "", ""

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    up_file = st.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    if up_file:
        with st.spinner('جاري القراءة بدقة...'):
            try:
                res = smart_ocr_reader(up_file)
                raw = "".join(res).upper().replace(" ", "")
                # استخراج رقم الجواز
                p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
                if p_match: s_pass = p_match.group()
                # استخراج الاسم من كود LBY
                if "LBY" in raw:
                    s_name = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
                else:
                    s_name = res[0] if res else ""
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

    # خانات البيانات المستخرجة
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.text_input("الاسم", value=s_name)
    with c2: st.text_input("رقم الجواز", value=s_pass)
    
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
