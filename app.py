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

# ================== 🎨 CSS التوسيط المطلق المحسن ==================
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

/* 🎯 حاوية التوسيط المطلق - تجعل كل شيء في منتصف الشاشة */
[data-testid="stVerticalBlock"] {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 500px !important; 
    text-align: center;
    background-color: transparent !important;
    z-index: 9999;
}

/* العنوان (تأشيرات   أو VISA) */
.main-title {
    color: #fbbf24;
    font-family: 'Cairo', sans-serif;
    font-size: 60px;
    font-weight: 900;
    text-shadow: 4px 4px 10px black;
    margin-bottom: 30px;
}

/* سطر الإدخال لضمان التوسط */
.input-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

/* مربعات الإدخال */
div[data-baseweb="input"] {
    width: 350px !important;
    background-color: #1e2129 !important;
    border-radius: 10px !important;
    border: 2px solid #fbbf24 !important;
    margin: 10px auto !important;
}

input {
    text-align: center !important; /* النص داخل الخانة في الوسط */
    color: white !important;
    font-size: 20px !important;
}

/* زر الدخول في الوسط */
.stButton {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.stButton button {
    height: 50px;
    width: 200px;
    background-color: #fbbf24;
    color: black;
    font-weight: bold;
    font-family: 'Cairo';
    border-radius: 12px;
    border: none;
    font-size: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# ================== نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # كلمة تأشيرات في الوسط
    st.markdown('<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)

    # الخانات (اسم المستخدم وكلمة المرور)
    u = st.text_input("اسم المستخدم", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("كلمة المرور", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    # زر الدخول
    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()

# ================== لوحة التحكم ==================
else:
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()

