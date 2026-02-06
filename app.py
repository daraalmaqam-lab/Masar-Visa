import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
import re

# 1. إعدادات الصفحة (ممنوع اللمس)
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🧠 تحميل محرك الذكاء الاصطناعي مرة واحدة ---
@st.cache_resource
def load_ocr_engine():
    return easyocr.Reader(['en'])

# --- 🎨 التنسيق الأصلي (مقفل تماماً بناءً على طلبك) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] { display: none !important; }
    .stApp { background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); background-size: cover; }
    div[data-testid="stWidgetLabel"] { background-color: transparent !important; }
    div[data-testid="stWidgetLabel"] p { color: white !important; text-align: right !important; text-shadow: 2px 2px 4px black !important; font-family: 'Cairo', sans-serif !important; }
    input { text-align: right !important; font-weight: bold !important; }
    .glass-box { background: rgba(0, 0, 0, 0.45); padding: 25px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔐 نظام الدخول (بيانات علي الأصلية) ---
if 'auth' not in st.session_state: 
    st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-box" style="margin-top:100px;">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#fbbf24;'>طيران المسار الذهبي</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("البيانات خطأ!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- 🛠️ شاشة التحكم (التعديل الذكي للقارئ هنا فقط) ---
    st.markdown("<h2 style='text-align:right; color:#fbbf24;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    
    # أولاً: تعريف المتغيرات فاضية عشان ما يطلعش NameError
    scanned_name = ""
    scanned_passport = ""

    # ثانياً: خانة رفع الملف (لازم تكون قبل سطر الـ if uploaded_file)
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<p style='text-align:right; color:white;'>📸 ارفع صورة الجواز للقراءة الآلية:</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'], key="passport_uploader")
    
    # ثالثاً: معالجة الصورة لو تم الرفع
    if uploaded_file:
        reader = load_ocr_engine()
        image = Image.open(uploaded_file)
        
        # تحويل الصورة ومعالجتها (المخ الفايق)
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        # فلتر تنظيف الصورة لزيادة الدقة
        processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        with st.spinner('جاري التحليل الذكي...'):
            results = reader.readtext(processed_img, detail=0)
            full_text = "".join(results).upper().replace(" ", "")
            
            # البحث عن رقم الجواز (نمط حرف + أرقام)
            pass_match = re.search(r'[A-Z][0-9]{7,9}', full_text)
            if pass_match:
                scanned_passport = pass_match.group()
            
            # البحث عن الاسم في شفرة الجواز الليبي LBY
            if "LBY" in full_text:
                try:
                    name_part = full_text.split("LBY")[1]
                    scanned_name = name_part.split("<<")[0].replace("<", " ").strip()
                except:
                    scanned_name = results[0] if results else ""
            else:
                scanned_name = results[0] if results else ""
        
        st.success("✅ تمت القراءة بنجاح!")
    st.markdown('</div>', unsafe_allow_html=True)

    # رابعاً: عرض البيانات في الخانات
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("الاسم واللقب (تلقائي)", value=scanned_name)
    with col2:
        st.text_input("رقم الجواز (تلقائي)", value=scanned_passport)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("خروج 🚪"):
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
