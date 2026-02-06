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

# ================== 🎨 CSS التوسيط بدون المربع الأسود ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

/* إخفاء الهيدر */
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

/* 🎯 التوسيط المطلق للكتلة بالكامل */
[data-testid="stVerticalBlock"] {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 550px !important; 
    padding: 0 !important;
    background-color: transparent !important; /* إزالة أي خلفية سوداء */
    border: none !important;
    z-index: 9999;
}

/* صف الإدخال (الكلمة + المربع) */
.input-row {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    margin-bottom: 20px;
    direction: rtl;
}

/* ستايل الكلمات (اسم المستخدم / كلمة المرور) */
.label-style {
    color: white;
    font-family: 'Cairo', sans-serif;
    font-size: 24px;
    font-weight: 900;
    text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
    min-width: 160px;
    text-align: right;
}

/* مربعات الإدخال */
div[data-baseweb="input"] {
    width: 300px !important;
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
    margin-top: 10px;
}

.stButton button {
    height: 45px;
    width: 150px;
    background-color: #fbbf24;
    color: black;
    font-weight: bold;
    font-family: 'Cairo';
    border-radius: 10px;
    border: none;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.8);
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
    st.markdown('<div class="main-title-center">طيران المسار الذهبي</div>', unsafe_allow_html=True)

    # حقل اسم المستخدم
    st.markdown('<div class="input-row"><div class="label-style">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_login").upper()
    st.markdown('</div>', unsafe_allow_html=True)

    # حقل كلمة المرور
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

# ================== لوحة التحكم ==================
else:
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    
    # ... (باقي كود لوحة التحكم الخاص بك) ...
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
