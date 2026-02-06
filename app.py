import streamlit as st
import numpy as np
from PIL import Image
import re

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Golden Path",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== 🎨 CSS التوسيط المطلق ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

/* إخفاء الهيدر تماماً */
[data-testid="stHeader"], header, footer {
    display: none !important;
}

/* الخلفية */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 🎯 هذا هو الكود الذي يضع كل شيء في وسط الشاشة بالظبط */
[data-testid="stVerticalBlock"] {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 550px !important; /* عرض الحاوية لضمان عدم تشتت العناصر */
    padding: 30px !important;
    background-color: rgba(0, 0, 0, 0.2); /* خلفية خفيفة للتركيز */
    border-radius: 20px;
    z-index: 9999;
}

/* تنسيق السطر (الكلمة + المربع) */
.input-row {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    margin-bottom: 20px;
    direction: rtl;
}

/* النصوص التوضيحية (يمين المربع) */
.label-style {
    color: white;
    font-family: 'Cairo', sans-serif;
    font-size: 24px;
    font-weight: 900;
    text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
    min-width: 160px;
    text-align: right;
}

/* تصميم المربعات الداكنة */
div[data-baseweb="input"] {
    width: 320px !important;
    background-color: #1e2129 !important;
    border-radius: 8px !important;
    border: 2px solid #fbbf24 !important;
}

input {
    font-size: 18px !important;
    text-align: right !important;
    color: white !important;
}

/* زر الدخول */
.button-container {
    width: 100%;
    display: flex;
    justify-content: flex-start;
    padding-right: 170px; /* موازنته ليكون تحت المربعات */
    margin-top: 15px;
}

.stButton button {
    height: 48px;
    width: 160px;
    background-color: #fbbf24;
    color: black;
    font-weight: bold;
    font-family: 'Cairo';
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

/* العنوان الرئيسي */
.main-title-center {
    text-align: center;
    color: #fbbf24;
    font-family: 'Cairo';
    font-size: 55px;
    font-weight: 900;
    text-shadow: 4px 4px 10px black;
    margin-bottom: 40px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ================== نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # العنوان
    st.markdown('<div class="main-title-center">تاشيرات</div>', unsafe_allow_html=True)

    # اسم المستخدم
    st.markdown('<div class="input-row"><div class="label-style">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_login").upper()
    st.markdown('</div>', unsafe_allow_html=True)

    # كلمة المرور
    st.markdown('<div class="input-row"><div class="label-style">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed", key="p_login")
    st.markdown('</div>', unsafe_allow_html=True)

    # الزر
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================== لوحة التحكم (تظهر بعد الدخول) ==================
else:
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    
    # دالة قراءة الجواز
    def get_passport_data(file):
        import easyocr, cv2
        reader = easyocr.Reader(['en'])
        image = Image.open(file)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return reader.readtext(processed, detail=0)

    s_name, s_pass = "", ""
    up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])

    if up_file:
        try:
            res = get_passport_data(up_file)
            raw = "".join(res).upper().replace(" ", "")
            p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
            if p_match: s_pass = p_match.group()
            if "LBY" in raw:
                s_name = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
        except: pass

    st.text_input("الاسم واللقب", value=s_name)
    st.text_input("رقم الجواز", value=s_pass)

    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()

