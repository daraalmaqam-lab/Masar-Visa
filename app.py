import streamlit as st
import numpy as np
from PIL import Image
import re
import cv2

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path - AI Visa", layout="wide", initial_sidebar_state="collapsed")

# --- 🧠 محرك القراءة المخصص والدقيق (MRZ Specialist) ---
def extract_libyan_data(file):
    import easyocr
    # استخدام CPU فقط لضمان عدم الانهيار كما في الـ Logs
    reader = easyocr.Reader(['en'], gpu=False)
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # تحسين الصورة (رمادي + تباين عالي)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    results = reader.readtext(processed, detail=0)
    
    data = {"name": "", "p_no": "", "dob": "", "doe": ""}
    
    full_blob = "".join(results).upper().replace(" ", "")
    
    # 🔍 استخراج رقم الجواز (حرف + 7 أو 8 أرقام)
    p_match = re.search(r'([A-Z][0-9]{7,8})', full_blob)
    if p_match: data["p_no"] = p_match.group(1)
    
    # 🔍 استخراج الاسم (بين LBY و <<)
    if "LBY" in full_blob:
        try:
            name_raw = full_blob.split("LBY")[1].split("<<")[0]
            data["name"] = name_raw.replace("<", " ").strip()
        except: pass

    # 🔍 استخراج التواريخ (YYMMDD) من سطر الأكواد
    date_matches = re.findall(r'[0-9]{6}', full_blob)
    if len(date_matches) >= 2:
        data["dob"] = date_matches[0] # تاريخ الميلاد
        data["doe"] = date_matches[1] # تاريخ الانتهاء
        
    return data

# --- 🎨 الستايل الذهبي النظيف (بدون مربعات سوداء) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed; 
    }
    .title { font-family: 'Cairo'; color: #fbbf24; text-align: center; font-size: 45px; text-shadow: 3px 3px 6px black; }
    .label { color: white; font-family: 'Cairo'; font-size: 18px; text-align: right; text-shadow: 2px 2px 4px black; margin-bottom: 2px; }
    input, .stSelectbox div { background-color: white !important; border-radius: 8px !important; color: black !important; font-weight: bold !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# --- نظام الدخول ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<h1 class="title">المسار الذهبي</h1>', unsafe_allow_html=True)
        u = st.text_input("User").upper()
        p = st.text_input("Pass", type="password")
        if st.button("دخول"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
else:
    st.markdown('<h1 class="title">🌍 منظومة حجز التأشيرات المتكاملة</h1>', unsafe_allow_html=True)

    # 1. القارئ
    st.markdown('<p class="label">📸 ارفع الجواز (تعبئة تلقائية)</p>', unsafe_allow_html=True)
    up = st.file_uploader("up", type=['jpg','jpeg','png'], label_visibility="collapsed")
    
    passport_data = {"name": "", "p_no": "", "dob": "", "doe": ""}
    if up:
        with st.spinner('جاري القراءة بدقة...'):
            passport_data = extract_libyan_data(up)

    # 2. النموذج الكامل
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p class="label">الاسم بالكامل (تلقائي)</p>', unsafe_allow_html=True)
        f_name = st.text_input("name", value=passport_data["name"])
        st.markdown('<p class="label">تاريخ الميلاد (تلقائي)</p>', unsafe_allow_html=True)
        f_dob = st.text_input("dob", value=passport_data["dob"], placeholder="YYMMDD")

    with col2:
        st.markdown('<p class="label">رقم الجواز (تلقائي)</p>', unsafe_allow_html=True)
        f_pass = st.text_input("pass", value=passport_data["p_no"])
        st.markdown('<p class="label">تاريخ الانتهاء (تلقائي)</p>', unsafe_allow_html=True)
        f_doe = st.text_input("doe", value=passport_data["doe"], placeholder="YYMMDD")

    with col3:
        st.markdown('<p class="label">الوجهة (يدوي)</p>', unsafe_allow_html=True)
        f_dest = st.selectbox("dest", ["إيطاليا", "فرنسا", "تركيا", "إسبانيا"])
        st.markdown('<p class="label">رقم الهاتف (يدوي)</p>', unsafe_allow_html=True)
        f_phone = st.text_input("phone", value="0925843353")

    # 3. قسم الحجز المبدئي (طيران وفندق)
    st.markdown('<p class="label">✈️ بيانات الحجز المبدئي (فندق وطيران)</p>', unsafe_allow_html=True)
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        f_hotel = st.text_input("اسم الفندق المبدئي", placeholder="Hotel Name")
    with h_col2:
        f_flight = st.text_input("مسار الرحلة المبدئي", value="Tripoli - Rome")

    # 4. السحب النهائي
    st.write("")
    if st.button("🖨️ إصدار نموذج التأشيرة والحجز الأصلي"):
        st.success(f"تم بنجاح تجهيز النموذج للمسافر: {f_name}")
        st.write(f"✅ بيانات الجواز: {f_pass} | الوجهة: {f_dest}")
        st.write(f"✅ الحجز: فندق ({f_hotel}) | طيران ({f_flight})")
        st.info("جاهز للطباعة.")

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
