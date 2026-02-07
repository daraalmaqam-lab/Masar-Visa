import streamlit as st
import numpy as np
from PIL import Image
import re
import cv2

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ الذكي (تحسين القراءة للجواز الليبي) ---
def smart_ocr_reader(file):
    import easyocr
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # تحسين الصورة للقراءة
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    results = reader.readtext(gray, detail=0)
    full_text = "".join(results).upper().replace(" ", "")
    
    passport = ""
    name = ""
    
    # البحث عن رقم الجواز (حرف + 7 أو 8 أرقام)
    p_match = re.search(r'([A-Z][0-9]{7,8})', full_text)
    if p_match: passport = p_match.group(1)
    
    # البحث عن الاسم بعد كود الدولة LBY
    if "LBY" in full_text:
        try:
            name_part = full_text.split("LBY")[1].split("<<")[0]
            name = name_part.replace("<", " ").strip()
        except: name = results[0] if results else ""
            
    return name, passport

# --- نظام الجلسة ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- 🎨 الستايل (بدون مربعات سوداء - شفافية ونظافة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, footer, [data-testid="stHeader"] { display: none !important; }

    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed; 
    }

    /* تنسيق العناوين فوق الخلفية مباشرة */
    .title-text {
        font-family: 'Cairo'; color: #fbbf24; text-align: center;
        font-size: 45px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-bottom: 30px;
    }

    .label-text {
        color: white; font-family: 'Cairo'; font-size: 20px;
        text-align: right; font-weight: bold; text-shadow: 2px 2px 4px black;
        margin-top: 10px;
    }

    /* الخانات بيضاء ونظيفة */
    div[data-baseweb="input"], [data-baseweb="select"] {
        background-color: white !important;
        border-radius: 10px !important;
        border: 2px solid #fbbf24 !important;
    }
    
    input { color: black !important; font-weight: bold !important; text-align: center !important; }

    /* أزرار التحكم */
    .stButton button {
        width: 100%; height: 50px; background-color: #fbbf24 !important;
        color: black !important; font-weight: bold; border-radius: 10px;
        font-family: 'Cairo'; font-size: 18px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🏠 المحتوى
# =========================================================

if not st.session_state.auth:
    # شاشة الدخول الممركزة (بدون زجاج أسود)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="title-text">طيران المسار الذهبي</div>', unsafe_allow_html=True)
        st.markdown('<p class="label-text">اسم المستخدم</p>', unsafe_allow_html=True)
        u = st.text_input("u", label_visibility="collapsed", key="u_login").upper()
        st.markdown('<p class="label-text">كلمة المرور</p>', unsafe_allow_html=True)
        p = st.text_input("p", type="password", label_visibility="collapsed", key="p_login")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
else:
    # لوحة التحكم - منظمة وبدون مربعات سوداء
    st.markdown('<div class="title-text">🌍 لوحة التحكم الذكية</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<p class="label-text">📸 مسح الجواز</p>', unsafe_allow_html=True)
        up_file = st.file_uploader("ارفع الصورة", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        name_val, pass_val = "", ""
        if up_file:
            with st.spinner('جاري القراءة...'):
                name_val, pass_val = smart_ocr_reader(up_file)

    with col2:
        st.markdown('<p class="label-text">📝 البيانات المستخرجة</p>', unsafe_allow_html=True)
        
        # توزيع البيانات في أعمدة نظيفة
        a, b = st.columns(2)
        with a:
            st.markdown('<p class="label-text">الاسم واللقب</p>', unsafe_allow_html=True)
            name = st.text_input("n", value=name_val, label_visibility="collapsed")
            st.markdown('<p class="label-text">تاريخ الميلاد</p>', unsafe_allow_html=True)
            st.date_input("d", label_visibility="collapsed")
        with b:
            st.markdown('<p class="label-text">رقم الجواز</p>', unsafe_allow_html=True)
            passport = st.text_input("pass", value=pass_val, label_visibility="collapsed")
            st.markdown('<p class="label-text">الوجهة</p>', unsafe_allow_html=True)
            st.selectbox("dest", ["إيطاليا", "فرنسا", "تركيا", "مصر"], label_visibility="collapsed")

    # أزرار الإجراءات في الأسفل
    st.write("---")
    b1, b2, b3 = st.columns(3)
    with b1: st.button("حفظ وإصدار التذكرة 🖨️")
    with b2: 
        if st.button("مسح البيانات 🧹"): st.rerun()
    with b3:
        if st.button("خروج 🚪"):
            st.session_state.auth = False
            st.rerun()
