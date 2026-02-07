import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة (ثابتة)
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🛡️ الجزء الأول: شاشة الدخول (ممنوع اللمس - ثابتة للأبد)
# =========================================================
if not st.session_state.auth:
    # تنسيق خاص فقط بشاشة الدخول
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .stApp { 
            background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
            background-size: cover; background-position: center; background-attachment: fixed;
        }

        /* 🎯 التوسيط الإجباري (خاص بهده الشاشة فقط) */
        [data-testid="stVerticalBlock"] {
            position: absolute !important;
            top: 50% !important; left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 100% !important; max-width: 450px !important;
            display: flex !important; flex-direction: column !important;
            align-items: center !important; justify-content: center !important;
        }

        .main-title {
            text-align: center; color: #fbbf24; font-family: 'Cairo'; 
            font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black;
            margin-bottom: 20px;
        }

        .custom-label {
            color: white; font-family: 'Cairo'; font-size: 22px; font-weight: 700;
            text-align: center; width: 100%; margin-bottom: 5px; margin-top: 10px;
            text-shadow: 2px 2px 4px black;
        }

        div[data-baseweb="input"] {
            height: 45px !important; width: 320px !important; 
            margin: 0 auto !important; background-color: #f0f2f6 !important; 
            border-radius: 10px !important; border: 2px solid #fbbf24 !important;
        }
        
        input { text-align: center !important; color: #333 !important; font-size: 18px !important; font-weight: bold !important;}

        .stButton button {
            height: 55px !important; width: 220px !important; 
            background-color: #fbbf24 !important; color: black !important; 
            font-weight: bold !important; font-size: 22px !important;
            border-radius: 12px !important; margin-top: 30px !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # محتوى الشاشة الرئيسية
    st.markdown('<div class="main-title">تاشيرات</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("user", label_visibility="collapsed", key="u_login").upper()
    st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("pass", type="password", label_visibility="collapsed", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()

# =========================================================
# 🚀 الجزء الثاني: لوحة التحكم (منطقة العمل - عدل هنا براحتك)
# =========================================================
else:
    # تنسيق "تنظيف" يمسح كل ما سبق ويبدأ صفحة جديدة تماماً
    st.markdown("""
        <style>
        /* إلغاء التوسيط المطلق */
        [data-testid="stVerticalBlock"] { 
            position: static !important; transform: none !important; 
            width: 100% !important; max-width: 100% !important;
            display: block !important;
        }
        /* خلفية بسيطة للعمل */
        .stApp { background-image: none !important; background-color: #111 !important; }
        </style>
        """, unsafe_allow_html=True)

    st.title("🌍 لوحة التحكم - منطقة العمل")
    st.write("---")

    # 👇👇 ابدأ ضيف كودك الجديد هنا يا علي 👇👇
    # مثلاً: رفع ملف الجواز
    up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    # 👆👆 أي تعديل هنا لن يلمس الشاشة الرئيسية أبداً 👆👆

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
