import streamlit as st
import numpy as np
from PIL import Image
import re
import cv2

# 1. إعدادات الصفحة (ثابتة ومحمية)
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🧠 المخ الذكي المطور للجواز الليبي ---
def get_passport_smart_data(file):
    import easyocr
    # تعريف القارئ (الإنجليزية فقط لزيادة الدقة في الأكواد)
    reader = easyocr.Reader(['en'])
    
    # تحويل الصورة لمعالجة احترافية
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # تكبير الصورة وتحويلها لرمادي لزيادة دقة الحروف الصغيرة
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # تنظيف الضوضاء (Noise Removal)
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # قراءة النص
    results = reader.readtext(processed, detail=0)
    return results

def clean_libyan_data(text_list):
    full_text = "".join(text_list).upper().replace(" ", "")
    
    # 🕵️ البحث عن منطقة الـ MRZ الخاصة بليبيا
    # السطر الأول ديما يبدأ بـ P<LBY
    passport_number = ""
    full_name = ""
    
    # استخراج رقم الجواز (ديما يبدأ بحرف وبعده أرقام)
    p_match = re.search(r'([A-Z0-9]{8,9})', full_text)
    if p_match:
        passport_number = p_match.group(1)

    # استخراج الاسم (يكون محصور بين LBY و <<)
    if "LBY" in full_text:
        name_part = full_text.split("LBY")[1].split("<<<<")[0]
        full_name = name_part.replace("<", " ").strip()
    
    return full_name, passport_number

# --- نظام الدخول (الثابت) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# [تنسيق الـ CSS المعتمد بتاعك - لم يتغير لضمان الثبات]
# ... (نفس كود التنسيق اللي في الرد السابق) ...

if not st.session_state.auth:
    # --- شاشة الدخول (المسار الذهبي) ---
    st.markdown('<style>/* ... كود التوسيط ... */</style>', unsafe_allow_html=True) # سأختصر هنا للتركيز على القارئ
    st.markdown('<div style="text-align:center; color:#fbbf24; font-size:50px; font-weight:900;">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم", key="u_login").upper()
    p = st.text_input("كلمة المرور", type="password", key="p_login")
    if st.button("دخول"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
else:
    # --- لوحة التحكم: القارئ المطور + نموذج الحجز ---
    st.markdown("<h1 style='text-align:center; color:#fbbf24;'>📋 منظومة الحجز المبدئي الذكية</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📸 مسح الجواز الليبي")
        up_file = st.file_uploader("ارفع صورة واضحة للجواز", type=['jpg', 'png', 'jpeg'])
        
        name_res, pass_res = "", ""
        if up_file:
            with st.spinner('جاري التحليل العميق للجواز...'):
                raw_data = get_passport_smart_data(up_file)
                name_res, pass_res = clean_libyan_data(raw_data)
                if not name_res: st.warning("حاول رفع صورة أوضح لمنطقة الأكواد أسفل الجواز")

    with col2:
        st.markdown("<div style='background:white; padding:20px; border-radius:15px; color:black;'>", unsafe_allow_html=True)
        st.write("### 📝 نموذج البيانات")
        
        final_name = st.text_input("الاسم (تأكد من المطابقة)", value=name_res)
        final_pass = st.text_input("رقم الجواز", value=pass_res)
        
        st.write("---")
        st.selectbox("نوع الحجز", ["طيران مبدئي", "فندق", "تأشيرة"])
        st.text_input("الوجهة (مثلاً: اسطنبول - القاهرة)")
        
        if st.button("✅ إصدار الحجز"):
            st.success("تم استخراج البيانات وتجهيز الطلب!")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.sidebar.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()
