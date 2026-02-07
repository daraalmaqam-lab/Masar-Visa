import streamlit as st
import numpy as np
from PIL import Image
import re
import cv2

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ الذكي (الجواز الليبي) ---
def smart_passport_reader(file):
    import easyocr
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # تحسين الصورة
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    results = reader.readtext(processed, detail=0)
    full_text = "".join(results).upper().replace(" ", "")
    
    # استخراج البيانات بدقة
    p_num = re.search(r'[A-Z][0-9]{7,8}', full_text)
    passport = p_num.group(0) if p_num else ""
    
    name = ""
    if "LBY" in full_text:
        name = full_text.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
        
    return name, passport

if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل النهائي (لا سوداء ولا لخبطة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, footer, [data-testid="stHeader"] { display: none !important; }

    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed; 
    }

    .main-title { font-family: 'Cairo'; color: #fbbf24; text-align: center; font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black; margin-bottom: 20px; }
    .label-text { color: white; font-family: 'Cairo'; font-size: 20px; text-align: right; text-shadow: 2px 2px 4px black; margin-bottom: 5px; }

    /* تنسيق الخانات */
    div[data-baseweb="input"], [data-baseweb="select"] { background-color: white !important; border-radius: 10px !important; border: 2px solid #fbbf24 !important; }
    input { color: black !important; font-weight: bold !important; text-align: center !important; }

    /* إلغاء المربعات السوداء تماماً */
    [data-testid="stVerticalBlock"] { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# --- التطبيق ---
if not st.session_state.auth:
    # شاشة الدخول الممركزة
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
        st.markdown('<p class="label-text">اسم المستخدم</p>', unsafe_allow_html=True)
        u = st.text_input("u", label_visibility="collapsed", key="u").upper()
        st.markdown('<p class="label-text">كلمة المرور</p>', unsafe_allow_html=True)
        p = st.text_input("p", type="password", label_visibility="collapsed", key="p")
        if st.button("دخول للنظام"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
else:
    # لوحة التحكم الكاملة
    st.markdown('<div class="main-title">🌍 لوحة التحكم الذكية</div>', unsafe_allow_html=True)

    # 1. القارئ
    st.markdown('<p class="label-text">📸 خطوة 1: مسح الجواز</p>', unsafe_allow_html=True)
    up = st.file_uploader("upload", type=['jpg','png','jpeg'], label_visibility="collapsed")
    n_res, p_res = "", ""
    if up:
        with st.spinner('جاري القراءة...'): n_res, p_res = smart_passport_reader(up)

    # 2. النموذج الكامل
    st.markdown('<p class="label-text">📝 خطوة 2: نموذج الحجز والبيانات</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<p class="label-text">الاسم بالكامل</p>', unsafe_allow_html=True)
        st.text_input("name", value=n_res, label_visibility="collapsed")
        st.markdown('<p class="label-text">تاريخ الميلاد</p>', unsafe_allow_html=True)
        st.date_input("birth", label_visibility="collapsed")
    with c2:
        st.markdown('<p class="label-text">رقم الجواز</p>', unsafe_allow_html=True)
        st.text_input("pass", value=p_res, label_visibility="collapsed")
        st.markdown('<p class="label-text">تاريخ الانتهاء</p>', unsafe_allow_html=True)
        st.date_input("exp", label_visibility="collapsed")
    with c3:
        st.markdown('<p class="label-text">الوجهة</p>', unsafe_allow_html=True)
        st.selectbox("dest", ["إيطاليا", "تركيا", "فرنسا", "مصر"], label_visibility="collapsed")
        st.markdown('<p class="label-text">رقم الهاتف</p>', unsafe_allow_html=True)
        st.text_input("phone", value="0925843353", label_visibility="collapsed")

    # أزرار الإجراءات
    st.write("---")
    b1, b2, b3 = st.columns(3)
    with b1: st.button("حفظ وإصدار التذكرة 🖨️")
    with b2: 
        if st.button("مسح البيانات 🧹"): st.rerun()
    with b3:
        if st.button("خروج 🚪"):
            st.session_state.auth = False
            st.rerun()
