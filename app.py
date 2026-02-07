import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_config(page_title="Golden Path | AI Booking System", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .stApp { background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://images.unsplash.com/photo-1436491865332-7a61a109c0f3?q=80&w=2070"); background-size: cover; }
    .main-header { color: #fbbf24; text-align: center; font-size: 40px; font-weight: bold; text-shadow: 2px 2px 5px #000; border-bottom: 2px solid #fbbf24; padding-bottom: 10px; }
    .section-box { background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px; border: 1px solid #fbbf24; margin-bottom: 20px; }
    label { color: #fff !important; font-weight: bold !important; }
    .stButton>button { width: 100%; background-color: #fbbf24 !important; color: black !important; font-weight: bold !important; border-radius: 10px !important; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. التحقق من الهوية (علي الفيتوري) ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<h1 class="main-header">تسجيل الدخول للمنظومة</h1>', unsafe_allow_html=True)
        user = st.text_input("اسم المستخدم (الاسم بالكامل)").upper()
        pwd = st.text_input("كلمة المرور (رقم الهاتف)", type="password")
        if st.button("دخول آمن"):
            if (user == "ALI" or user == "ALI FETORY") and pwd == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
else:
    st.markdown('<h1 class="main-header">لوحة التحكم الذكية - المسار الذهبي للخدمات السياحية</h1>', unsafe_allow_html=True)

    # --- 3. قسم رفع الجواز (OCR) ---
    with st.container():
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📑 الخطوة الأولى: مسح الجواز آلياً")
        up = st.file_uploader("ارفع صورة الجواز (JPG/PNG)", label_visibility="collapsed")
        
        passport_data = {"name": "", "num": ""}
        if up:
            with st.spinner('جاري استخراج البيانات...'):
                img = np.array(Image.open(up))
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                text = pytesseract.image_to_string(gray).upper()
                # استخراج رقم الجواز
                p_match = re.search(r'[A-Z][0-9]{7,8}', text)
                if p_match: passport_data["num"] = p_match.group()
                # استخراج الاسم (تبسيط للمثال)
                if "LBY" in text:
                    passport_data["name"] = text.split("LBY")[1].split("\n")[0].replace("<", " ").strip()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. تفاصيل المسافر والرحلة (نظام شبيه بـ Amadeus) ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("👤 بيانات المسافر")
        f_name = st.text_input("الاسم بالكامل (كما في الجواز)", value=passport_data["name"])
        f_pass = st.text_input("رقم الجواز", value=passport_data["num"])
        f_phone = st.text_input("رقم هاتف التواصل", value="0925843353")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("✈️ تفاصيل الطيران (Flight)")
        dep_city = st.selectbox("مطار المغادرة", ["Tripoli (MJI)", "Benghazi (BEN)", "Misrata (MRA)"])
        arr_city = st.selectbox("وجهة الوصول", ["Rome (FCO)", "Istanbul (IST)", "Paris (CDG)", "Malta (MLA)", "Tunis (TUN)"])
        flight_date = st.date_input("تاريخ الذهاب", datetime.now() + timedelta(days=7))
        return_date = st.date_input("تاريخ العودة", datetime.now() + timedelta(days=14))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🏨 تفاصيل الفندق (Hotel)")
        hotel_name = st.text_input("اسم الفندق المقترح", placeholder="مثال: Marriott Grand Hotel")
        room_type = st.selectbox("نوع الغرفة", ["Single Room", "Double Room", "Suite"])
        meal_plan = st.radio("نظام الوجبات", ["Bed & Breakfast", "Half Board", "Full Board"], horizontal=True)
        hotel_stars = st.slider("تصنيف الفندق", 1, 5, 4)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📑 نوع التأشيرة")
        visa_type = st.selectbox("الغرض من السفر", ["Schengen - Tourism", "Business Visa", "Medical Treatment"])
        notes = st.text_area("ملاحظات إضافية")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. إصدار المستند النهائي ---
    if st.button("🖨️ إصدار ملف الحجز المتكامل (PNR)"):
        st.balloons()
        st.success("تم تجهيز ملف الحجز المبدئي بنجاح!")
        
        # عرض ملخص احترافي
        st.markdown(f"""
        ### 🎫 ملخص الحجز - {f_name}
        ---
        * **رقم الحجز المرجعي:** `GP-{np.random.randint(1000, 9999)}`
        * **مسار الرحلة:** من {dep_city} إلى {arr_city} | بتاريخ: {flight_date}
        * **الإقامة:** فندق {hotel_name} ({hotel_stars} نجوم) | نظام {meal_plan}
        * **حالة الجواز:** {f_pass} | الهاتف: {f_phone}
        ---
        """)
        st.info("جاهز للطباعة أو الإرسال بصيغة PDF.")

    if st.sidebar.button("تسجيل خروج"):
        st.session_state.auth = False
        st.rerun()
