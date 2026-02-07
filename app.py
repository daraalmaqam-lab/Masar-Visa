import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ الذكي ---
def get_passport_data(file):
    import easyocr
    import cv2
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return reader.readtext(processed, detail=0)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل (عزل كامل + تنسيق نموذج الحجز)
# =========================================================
if not st.session_state.auth:
    # شاشة الدخول (تأشيرات) - ممنوع اللمس
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .stApp { background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); background-size: cover; background-position: center; background-attachment: fixed; }
        [data-testid="stVerticalBlock"] { position: absolute !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; width: 100% !important; max-width: 450px !important; display: flex !important; flex-direction: column !important; align-items: center !important; }
        .main-title { text-align: center; color: #fbbf24; font-family: 'Cairo'; font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black; margin-bottom: 20px; }
        .custom-label { color: white; font-family: 'Cairo'; font-size: 22px; font-weight: 700; text-align: center; width: 100%; margin-bottom: 5px; text-shadow: 2px 2px 4px black; }
        div[data-baseweb="input"] { height: 45px !important; width: 320px !important; margin: 0 auto !important; background-color: #f0f2f6 !important; border-radius: 10px !important; border: 2px solid #fbbf24 !important; }
        input { text-align: center !important; color: #333 !important; font-size: 18px !important; font-weight: bold !important;}
        .stButton button { height: 55px !important; width: 220px !important; background-color: #fbbf24 !important; color: black !important; font-weight: bold !important; font-size: 22px !important; border-radius: 12px !important; margin-top: 30px !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    # لوحة التحكم (نموذج الحجز)
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; display: block !important; }
        .stApp { background-image: none !important; background-color: #f4f7f6 !important; }
        .booking-card { background-color: white; padding: 30px; border-radius: 15px; border-top: 5px solid #fbbf24; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 20px; direction: rtl; }
        h1, h3 { font-family: 'Cairo'; color: #2c3e50; text-align: center; }
        label { font-family: 'Cairo' !important; font-size: 18px !important; color: #2c3e50 !important; }
        </style>
        """, unsafe_allow_html=True)

# =========================================================
# 🏠 المحتوى المنطقي
# =========================================================
if not st.session_state.auth:
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_login").upper()
    st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
else:
    # --- لوحة التحكم: نموذج الحجز المبدئي ---
    st.markdown("<h1>📋 منظومة الحجز المبدئي (طيران + فندق)</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📸 خطوة 1: مسح الجواز")
        up_file = st.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
        
        extracted_name, extracted_pass = "", ""
        if up_file:
            with st.spinner('جاري القراءة...'):
                try:
                    res = get_passport_data(up_file)
                    raw = "".join(res).upper().replace(" ", "")
                    p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
                    if p_match: extracted_pass = p_match.group()
                    if "LBY" in raw:
                        extracted_name = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
                    else: extracted_name = res[0] if res else ""
                except: st.error("خطأ في الصورة")

    with col2:
        st.markdown('<div class="booking-card">', unsafe_allow_html=True)
        st.markdown("### 📝 خطوة 2: نموذج البيانات المبدئي")
        
        # بيانات الجواز المسحوبة تلقائياً
        name = st.text_input("الاسم بالكامل (من الجواز)", value=extracted_name)
        passport = st.text_input("رقم الجواز", value=extracted_pass)
        
        # بيانات الحجز الإضافية (يدوية)
        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            flight_type = st.selectbox("نوع الحجز", ["حجز طيران مبدئي", "حجز فندقي", "طيران + فندق"])
            destination = st.text_input("الوجهة")
        with c2:
            travel_date = st.date_input("تاريخ السفر المتوقع")
            hotel_stars = st.slider("تصنيف الفندق", 1, 5, 3)
            
        if st.button("✅ إصدار الحجز المبدئي"):
            st.success(f"تم تجهيز نموذج الحجز لـ {name} بنجاح!")
            st.balloons()
            
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()
