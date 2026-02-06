import streamlit as st
import numpy as np
from PIL import Image
import re

# ================== 1. إعداد الصفحة ==================
st.set_page_config(
    page_title="Golden Path",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== 2. نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

# ================== 3. شاشة الدخول (تأشيرات) - "المنطقة المحمية" ==================
if not st.session_state.auth:
    # تنسيق خاااص فقط بشاشة الدخول مستحيل يهرب للشاشة التانية
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* إخفاء الهيدر */
    [data-testid="stHeader"], header, footer { display: none !important; }
    
    /* الخلفية */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* 🎯 التوسيط المطلق (شاشتك اللي تحبها) */
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
    }

    .main-title {
        color: #fbbf24; font-family: 'Cairo', sans-serif;
        font-size: 70px; font-weight: 900;
        text-shadow: 4px 4px 15px black; margin-bottom: 20px;
        text-align: center; width: 100%;
    }

    /* المربعات */
    div[data-baseweb="input"] {
        width: 380px !important; background-color: #1e2129 !important;
        border-radius: 12px !important; border: 2px solid #fbbf24 !important;
        margin-bottom: 15px !important;
    }

    input { text-align: center !important; color: white !important; font-size: 20px !important; }

    /* زر الدخول */
    .stButton button {
        height: 50px; width: 200px; background-color: #fbbf24;
        color: black !important; font-weight: bold !important; font-family: 'Cairo' !important;
        border-radius: 12px !important; border: none !important; font-size: 22px !important;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)
    
    u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("Pass", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")

# ================== 4. شاشة لوحة التحكم - "منطقة العمل" ==================
else:
    # تنسيق مختلف تماماً للوحة التحكم باش ما يخربش الشاشة الرئيسية
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* تصفير التوسيط المطلق عشان ترجع الشاشة طبيعية للشغل */
    [data-testid="stVerticalBlock"] {
        position: static !important;
        transform: none !important;
        display: block !important;
        width: 100% !important;
        margin-top: 0 !important;
    }

    .dash-header {
        text-align: center;
        padding: 50px 0;
        width: 100%;
    }

    .dash-title {
        color: #fbbf24;
        font-family: 'Cairo', sans-serif;
        font-size: 55px;
        font-weight: 900;
        text-shadow: 3px 3px 10px black;
    }
    
    /* زر الخروج نخليه أحمر ومميز */
    .stButton button {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # كلمة لوحة التحكم في السنتر (لكن من فوق)
    st.markdown('<div class="dash-header">', unsafe_allow_html=True)
    st.markdown('<div class="dash-title">🌍 لوحة التحكم الذكية</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    # محتوى لوحة التحكم
    st.success(f"أهلاً بك يا {u if 'u' in locals() else 'علي'}")
    
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
