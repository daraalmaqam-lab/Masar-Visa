import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🎨 الستايل الذهبي (تنسيق العناوين في المنتصف) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-attachment: fixed;
    }

    /* 🎯 حاوية التوسيط المطلق */
    [data-testid="stVerticalBlock"] {
        position: absolute !important;
        top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 450px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .main-title {
        text-align: center; color: #fbbf24; font-family: 'Cairo'; 
        font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black;
        margin-bottom: 20px; width: 100%;
    }

    /* 🏷️ تنسيق العناوين الجديدة (يدوي لضمان التوسيط) */
    .custom-label {
        color: white; font-family: 'Cairo'; font-size: 22px; font-weight: 700;
        text-align: center; width: 100%; margin-bottom: 5px; margin-top: 10px;
        text-shadow: 2px 2px 4px black;
    }

    /* ✍️ المربعات: عرض ثابت وممركز */
    div[data-baseweb="input"] {
        height: 45px !important; width: 320px !important; 
        margin: 0 auto !important; background-color: #f0f2f6 !important; 
        border-radius: 10px !important; border: 2px solid #fbbf24 !important;
    }
    
    input { text-align: center !important; color: #333 !important; font-size: 18px !important; font-weight: bold !important;}

    /* زر الدخول */
    .stButton button {
        height: 55px !important; width: 220px !important; 
        background-color: #fbbf24 !important; color: black !important; 
        font-weight: bold !important; font-family: 'Cairo' !important;
        font-size: 22px !important; margin-top: 30px !important;
        border-radius: 12px !important; box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # العنوان الكبير
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    # الخانة الأولى (عنوان + مربع)
    st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("user", label_visibility="collapsed", key="u_login").upper()
    
    # الخانة الثانية (عنوان + مربع)
    st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("pass", type="password", label_visibility="collapsed", key="p_login")
    
    # الزر
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")
else:
    # لوحة التحكم الحرة
    st.markdown("""<style>[data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; }</style>""", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم</h1>", unsafe_allow_html=True)
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
