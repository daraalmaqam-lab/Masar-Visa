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

# ================== 🎨 CSS التوسيط الكامل ==================
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
    width: 100% !important; 
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    background-color: transparent !important;
    z-index: 9999;
}

/* 🏷️ تنسيق كلمة تأشيرات في الوسط */
.main-title {
    color: #fbbf24;
    font-family: 'Cairo', sans-serif;
    font-size: 70px; /* حجم كبير وواضح */
    font-weight: 900;
    text-shadow: 4px 4px 15px black;
    margin-bottom: 20px;
    text-align: center;
    width: 100%;
}

/* ⌨️ مربعات الإدخال في الوسط */
div[data-baseweb="input"] {
    width: 380px !important; /* عرض متناسق */
    background-color: #1e2129 !important;
    border-radius: 12px !important;
    border: 2px solid #fbbf24 !important;
    margin-bottom: 15px !important;
}

input {
    text-align: center !important; /* النص اللي تكتبه يجي في نص الخانة */
    color: white !important;
    font-size: 20px !important;
    height: 45px !important;
}

/* 🔘 زر الدخول في الوسط */
.stButton {
    display: flex;
    justify-content: center;
    width: 100%;
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
    font-size: 22px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
}

/* تحسين شكل الفراغات */
.stTextInput {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}
</style>
""", unsafe_allow_html=True)

# ================== نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # 1. كلمة تأشيرات في السنتر
    st.markdown('<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)

    # 2. الخانات في السنتر (بدون ليبل خارجي)
    u = st.text_input("اسم المستخدم", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("كلمة المرور", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    # 3. زر الدخول في السنتر
    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()

# ================== لوحة التحكم ==================
else:
    st.markdown("<h2 style='text-align:right; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h2>", unsafe_allow_html=True)
    # باقي الكود الخاص بك...
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
