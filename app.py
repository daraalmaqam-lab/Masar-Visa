import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract # مكتبة أخف بكتير من easyocr للسيرفرات الضعيفة
import re

# إعداد الصفحة وتنسيق طيران المسار الذهبي
st.set_page_config(page_title="Masar Visa System", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #fbbf24; text-align: center; font-family: 'Cairo', sans-serif; font-size: 35px; text-shadow: 2px 2px black; }
    .stTextInput input, .stSelectbox div { background-color: white !important; border: 2px solid #fbbf24 !important; border-radius: 10px !important; }
    label { color: white !important; font-size: 18px !important; text-shadow: 1px 1px black; }
    .stApp { background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); background-size: cover; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# نظام الدخول بالبيانات الخاصة بك
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<h1 class="main-title">طيران المسار الذهبي</h1>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
else:
    st.markdown('<h1 class="main-title">لوحة التحكم الذكية - شركة المسار الذهبي</h1>', unsafe_allow_html=True)

    # 1. رفع الجواز (التعبئة التلقائية)
    up = st.file_uploader("ارفع صورة الجواز بدقة عالية (سيتم تعبئة البيانات تلقائياً)", type=['jpg', 'png', 'jpeg'])
    
    # بيانات افتراضية
    passport_data = {"name": "", "number": "", "dob": "", "expiry": ""}

    if up:
        with st.spinner('جاري القراءة...'):
            img = np.array(Image.open(up))
            # معالجة بسيطة للصورة لجعلها أوضح
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            text = pytesseract.image_to_string(gray).upper()
            
            # استخراج رقم الجواز (حرف + 7 أو 8 أرقام)
            p_num = re.search(r'[A-Z][0-9]{7,8}', text)
            if p_num: passport_data["number"] = p_num.group()
            
            # استخراج الاسم (بناءً على نمط الجواز الليبي LBY)
            if "LBY" in text:
                try:
                    name_part = text.split("LBY")[1].split("\n")[0]
                    passport_data["name"] = name_part.replace("<", " ").strip()
                except: pass

    # 2. الخانات (تلقائي + يدوي)
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        v_name = st.text_input("الاسم واللقب (EN)", value=passport_data["name"])
        v_dob = st.text_input("تاريخ الميلاد", placeholder="YYYY/MM/DD")
    
    with col2:
        v_num = st.text_input("رقم الجواز", value=passport_data["number"])
        v_exp = st.text_input("تاريخ انتهاء الجواز", placeholder="YYYY/MM/DD")
        
    with col3:
        v_dest = st.selectbox("الوجهة المختارة", ["إيطاليا", "تركيا", "فرنسا", "مالطا"])
        v_phone = st.text_input("رقم الهاتف", value="0925843353")

    # 3. تفاصيل الحجز (يدوي)
    st.write("---")
    st.markdown('<h3 style="color:white; text-align:right;">تفاصيل حجز الطيران والفندق</h3>', unsafe_allow_html=True)
    c_h1, c_h2 = st.columns(2)
    with c_h1:
        hotel = st.text_input("اسم الفندق (Booking المبدئي)")
    with c_h2:
        flight = st.text_input("مسار الرحلة (Tripoli - Destination)")

    # 4. الأزرار
    st.write("")
    if st.button("💾 حفظ وإصدار ملف التأشيرة"):
        st.success(f"تم بنجاح! المسافر: {v_name} | الوجهة: {v_dest}")
        st.info(f"الحجز المبدئي: {hotel} | رحلة: {flight}")

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
