import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path - AI System", layout="wide", initial_sidebar_state="collapsed")

# --- 🧠 إعداد محرك الذكاء الاصطناعي (EasyOCR) ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# --- 🌆 مكتبة الخلفيات والمطارات ---
WALLPAPERS = {
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073"
}

EUROPE_AIRPORTS = ["Tripoli (MJI)", "Benghazi (BEN)", "Istanbul (IST)", "Rome (FCO)", "Paris (CDG)", "Madrid (MAD)", "Frankfurt (FRA)", "Other / أخرى"]

if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل (شفافية كاملة + إخفاء المربعات البيضاء) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, footer, [data-testid="stHeader"] { display: none !important; }

    .stApp { background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); background-size: cover; background-attachment: fixed; }

    /* حذف المربعات البيضاء نهائياً */
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] > div { background-color: transparent !important; }
    [data-testid="stWidgetLabel"] p { color: white !important; text-align: right !important; direction: rtl !important; font-family: 'Cairo' !important; font-size: 20px !important; text-shadow: 2px 2px 4px black !important; }

    input, [data-baseweb="select"], [data-baseweb="input"] { background-color: white !important; border-radius: 10px !important; text-align: right !important; color: black !important; font-weight: bold !important; }

    .glass-box { background: rgba(0, 0, 0, 0.45); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.2); margin-bottom: 20px; }
    .inner-title { font-family: 'Cairo' !important; font-size: 30px !important; color: #fbbf24; text-align: center; text-shadow: 2px 2px 5px black; border-bottom: 3px solid #fbbf24; padding-bottom: 10px; margin-bottom: 30px; }
    .section-head { font-size: 22px !important; font-weight: 800 !important; color: #fbbf24 !important; text-align: right !important; margin: 15px 0; border-right: 6px solid #fbbf24; padding-right: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-box" style="margin-top:100px;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي</div>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="inner-title">🌍 لوحة التحكم الذكية - شركة المسار الذهبي</div>', unsafe_allow_html=True)

    # 1️⃣ حجة: قارئ الجواز الذكي
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">📸 الخطوة الأولى: مسح الجواز آلياً</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("ارفع صورة الجواز بدقة عالية (سيتم تعبئة البيانات تلقائياً)", type=['jpg', 'jpeg', 'png'])
    
    scanned_data = {"name": "", "passport": ""}
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY) # تحسين التباين
        
        with st.spinner('جاري استخدام الذكاء الاصطناعي لقراءة البيانات...'):
            results = reader.readtext(gray, detail=0)
            # خوارزمية البحث عن رقم الجواز
            for line in results:
                clean_line = line.upper().replace(" ", "")
                if len(clean_line) >= 8 and any(c.isdigit() for c in clean_line):
                    scanned_data["passport"] = clean_line[:9]
            scanned_data["name"] = " ".join(results[:2]).upper() if results else ""
            st.success("تمت القراءة! راجع البيانات في الأسفل.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2️⃣ حجة: البيانات الشخصية
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">2️⃣ بيانات الجواز والمسافر</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("الاسم واللقب (EN)", value=scanned_data["name"])
        st.date_input("تاريخ الميلاد")
    with c2:
        st.text_input("رقم الجواز", value=scanned_data["passport"])
        st.date_input("تاريخ انتهاء الجواز")
    with c3:
        st.selectbox("الوجهة المختارة", ["إيطاليا", "فرنسا", "إسبانيا", "ألمانيا"])
        st.text_input("رقم الهاتف", value="0925843353")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3️⃣ حجة: حجز الطيران (مطارات أوروبا)
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">3️⃣ تفاصيل حجز الطيران (Flight Route)</p>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1: st.selectbox("مطار المغادرة (من)", EUROPE_AIRPORTS, index=0)
    with f2: st.selectbox("مطار الوصول (إلى)", EUROPE_AIRPORTS, index=3)
    with f3: st.date_input("تاريخ الذهاب")
    with f4: st.date_input("تاريخ العودة")
    st.markdown('</div>', unsafe_allow_html=True)

    # أزرار الإجراءات
    st.markdown('<br>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([2, 2, 1])
    with b1: st.button("حفظ وإصدار ملف التأشيرة 🖨️")
    with b2:
        if st.button("مسح البيانات 🧹"): st.rerun()
    with b3:
        if st.button("خروج 🚪"):
            st.session_state.auth = False
            st.rerun()
