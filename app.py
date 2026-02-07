import streamlit as st
import numpy as np
from PIL import Image
import cv2
import re
from datetime import datetime, timedelta

# --- 1. إعداد الصفحة بشكل صحيح ---
st.set_page_config(page_title="Golden Path | PNR System", layout="wide")

# --- 🎨 التنسيق البصري الفخم ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
        url("https://images.unsplash.com/photo-1436491865332-7a61a109c0f3?q=80&w=2070"); 
        background-size: cover; 
    }
    .main-header { color: #fbbf24; text-align: center; font-size: 35px; font-weight: bold; padding: 20px; border-bottom: 2px solid #fbbf24; margin-bottom: 30px; }
    .card { background: rgba(255, 255, 255, 0.08); padding: 25px; border-radius: 15px; border-right: 5px solid #fbbf24; margin-bottom: 20px; }
    h3 { color: #fbbf24 !important; border-bottom: 1px solid #444; padding-bottom: 10px; }
    label { color: #ffffff !important; font-size: 15px !important; }
    .stButton>button { background: #fbbf24 !important; color: #000 !important; font-weight: bold !important; width: 100%; border-radius: 8px; height: 50px; font-size: 18px; }
    .stTextInput input, .stSelectbox div { background: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🛡️ نظام الدخول (علي الفيتوري) ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<h1 class="main-header">طيران المسار الذهبي</h1>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور (رقم الهاتف)", type="password")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
else:
    st.markdown('<div class="main-header">🌍 منظومة الحجز الذكية - PNR System</div>', unsafe_allow_html=True)

    # 1. قسم رفع الجواز (تصميم نظيف)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📸 الخطوة الأولى: مسح جواز السفر")
    up = st.file_uploader("ارفع صورة الجواز هنا (JPG/PNG)", label_visibility="collapsed")
    scanned_name = ""
    scanned_num = ""
    # ملاحظة: تم تبسيط الـ OCR لضمان عدم توقف السيرفر
    if up: st.info("تم رفع الصورة بنجاح، يمكنك الآن تأكيد البيانات أدناه.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. تقسيم الشاشة لبيانات منظمة
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 👤 بيانات المسافر")
        f_name = st.text_input("الاسم بالكامل (English)", placeholder="مثال: ALI FETORY")
        f_pass = st.text_input("رقم الجواز", placeholder="مثال: Y5601011")
        f_phone = st.text_input("رقم هاتف التواصل", value="0925843353")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ✈️ تفاصيل الطيران")
        dep = st.selectbox("من (مطار المغادرة)", ["Tripoli (MJI)", "Benghazi (BEN)", "Misrata (MRA)"])
        arr = st.selectbox("إلى (وجهة الوصول)", ["Rome (FCO)", "Istanbul (IST)", "Paris (CDG)", "Malta (MLA)"])
        d_date = st.date_input("تاريخ الذهاب", datetime.now() + timedelta(days=7))
        r_date = st.date_input("تاريخ العودة", datetime.now() + timedelta(days=14))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🏨 تفاصيل الإقامة")
        h_name = st.text_input("اسم الفندق", placeholder="مثال: Marriott Grand Hotel")
        h_room = st.selectbox("نوع الغرفة", ["Single Room", "Double Room", "Triple Room", "Suite"])
        h_meal = st.radio("نظام الوجبات", ["Bed & Breakfast", "Half Board", "Full Board"], horizontal=True)
        h_nights = st.number_input("عدد الليالي", 1, 30, 7)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🛂 بيانات التأشيرة")
        v_type = st.selectbox("نوع التأشيرة", ["Tourism", "Business", "Medical", "Student"])
        v_notes = st.text_area("ملاحظات إضافية للملف")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. زر الحفظ النهائي
    st.write("")
    if st.button("💾 إصدار وحفظ ملف الحجز المتكامل"):
        st.balloons()
        st.success(f"✅ تم الحجز بنجاح! رقم المرجع: GP-{np.random.randint(1000, 9999)}")
        
        # ملخص سريع
        st.info(f"المسافر: {f_name} | المسار: {dep} ✈️ {arr} | الفندق: {h_name}")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
