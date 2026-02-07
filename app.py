import streamlit as st
import numpy as np
from PIL import Image
import cv2
import re
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة (تم تصحيح السطر هنا) ---
st.set_page_config(page_title="Golden Path | AI Booking", layout="wide")

# --- 🎨 التنسيق البصري (ثيم المسار الذهبي) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
        url("https://images.unsplash.com/photo-1436491865332-7a61a109c0f3?q=80&w=2070"); 
        background-size: cover; 
    }
    .main-header { color: #fbbf24; text-align: center; font-size: 38px; text-shadow: 2px 2px 5px #000; padding: 10px; }
    .section-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid #fbbf24; margin-bottom: 20px; }
    label { color: #fbbf24 !important; font-size: 16px !important; }
    input, .stSelectbox div { background-color: white !important; color: black !important; font-weight: bold !important; }
    .stButton>button { background-color: #fbbf24 !important; color: black !important; font-weight: bold; width: 100%; height: 50px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 🧠 وظيفة استخراج بيانات الجواز (OCR خفيف) ---
def quick_ocr(file):
    import pytesseract
    img = np.array(Image.open(file))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(gray).upper()
    
    data = {"name": "", "num": ""}
    # البحث عن رقم الجواز
    p_match = re.search(r'[A-Z][0-9]{7,8}', text)
    if p_match: data["num"] = p_match.group()
    # محاولة جلب الاسم
    if "LBY" in text:
        try:
            data["name"] = text.split("LBY")[1].split("\n")[0].replace("<", " ").strip()
        except: pass
    return data

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
            else: st.error("خطأ في البيانات")
else:
    st.markdown('<h1 class="main-header">🌍 منظومة الحجز المتكاملة - PNR System</h1>', unsafe_allow_html=True)

    # 1. رفع الجواز
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    up = st.file_uploader("📸 ارفع صورة الجواز للتعبئة التلقائية", type=['jpg','png','jpeg'])
    scanned = {"name": "", "num": ""}
    if up:
        with st.spinner('جاري المسح...'):
            scanned = quick_ocr(up)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. بيانات المسافر والطيران
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("👤 بيانات المسافر")
        f_name = st.text_input("الاسم بالكامل (EN)", value=scanned["name"])
        f_pass = st.text_input("رقم الجواز", value=scanned["num"])
        f_phone = st.text_input("رقم الهاتف", value="0925843353")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("✈️ حجز الطيران")
        dep = st.selectbox("المغادرة", ["Tripoli (MJI)", "Benghazi (BEN)", "Misrata (MRA)"])
        arr = st.selectbox("الوصول", ["Rome (FCO)", "Istanbul (IST)", "Paris (CDG)", "Tunis (TUN)"])
        d_date = st.date_input("تاريخ الذهاب", datetime.now() + timedelta(days=7))
        r_date = st.date_input("تاريخ العودة", datetime.now() + timedelta(days=14))
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🏨 حجز الفندق")
        h_name = st.text_input("اسم الفندق", placeholder="مثال: Hilton Grand")
        h_room = st.selectbox("نوع الغرفة", ["Single", "Double", "Suite"])
        h_meal = st.radio("نظام الوجبات", ["B&B", "Half Board", "Full Board"], horizontal=True)
        h_stay = st.number_input("عدد الليالي", 1, 30, 7)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🛂 بيانات التأشيرة")
        v_type = st.selectbox("نوع التأشيرة", ["Tourism", "Business", "Medical"])
        v_notes = st.text_area("ملاحظات")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. الزر النهائي
    if st.button("💾 حفظ وإصدار ملف الحجز المتكامل"):
        st.success(f"تم تسجيل الحجز بنجاح للمسافر: {f_name}")
        st.write(f"🎫 رقم الحجز (PNR): GP-{np.random.randint(1000, 9999)}")
        st.balloons()

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
