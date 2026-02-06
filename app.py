import streamlit as st
import numpy as np
from PIL import Image
import re

st.set_page_config(
    page_title="Golden Path",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

header, footer, [data-testid="stHeader"] {
    display: none !important;
}

/* الخلفية */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070");
    background-size: cover;
    background-position: center;
}

/* العنوان */
.main-title-center {
    text-align: center;
    color: #fbbf24;
    font-family: 'Cairo';
    font-size: 55px;
    font-weight: 900;
    text-shadow: 4px 4px 8px black;
    margin-top: 60px;
    margin-bottom: 40px;
}

/* 🔴 الحاوية الجديدة للخانات فقط */
.inputs-center {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    z-index: 9999;
}

/* صف الإدخال */
.input-row {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    margin-bottom: 20px;
    direction: rtl;
}

.label-style {
    color: white;
    font-family: 'Cairo';
    font-size: 24px;
    font-weight: 900;
    text-shadow: -2px -2px 0 #000, 2px -2px 0 #000,
                 -2px 2px 0 #000, 2px 2px 0 #000;
    min-width: 150px;
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
    width: 300px;
    text-align: right;
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
}
</style>
""", unsafe_allow_html=True)

# ---------- AUTH ----------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    # العنوان (يبقى فوق)
    st.markdown('<div class="main-title-center">طيران المسار الذهبي</div>', unsafe_allow_html=True)

    # 🔴 الخانات فقط في وسط الشاشة
    st.markdown('<div class="inputs-center">', unsafe_allow_html=True)

    st.markdown('<div class="input-row"><div class="label-style">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed").upper()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-row"><div class="label-style">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.success("تم تسجيل الدخول ✅")
