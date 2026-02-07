import streamlit as st
import numpy as np
from PIL import Image
import re

# ================== 1. إعداد الصفحة (ثابت) ==================
st.set_page_config(
    page_title="Golden Path",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 2. نظام الثيمات (اختياري) ========
if "theme" not in st.session_state:
    st.session_state.theme = "الذهبي الملكي"

# القائمة الجانبية لتغيير الثيم
with st.sidebar:
    st.markdown("<h3 style='text-align:center; font-family:Cairo;'>⚙️ التنسيق</h3>", unsafe_allow_html=True)
    theme_choice = st.selectbox("اختر الثيم:", ["الذهبي الملكي", "الليلي الغامق", "الأخضر الهادئ"])
    st.session_state.theme = theme_choice

# تعريف ألوان الثيمات
theme_config = {
    "الذهبي الملكي": {"color": "#fbbf24", "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"},
    "الليلي الغامق": {"color": "#3b82f6", "img": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=2074"},
    "الأخضر الهادئ": {"color": "#10b981", "img": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070"}
}
current_c = theme_config[st.session_state.theme]["color"]
current_bg = theme_config[st.session_state.theme]["img"]

# ================== 3. 🎨 CSS التوسيط الكامل (المعتمد) ==================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

/* إخفاء الهيدر والفوتر */
[data-testid="stHeader"], header, footer {{ display: none !important; }}

/* الخلفية الثابتة */
.stApp {{
    background-image: url("{current_bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* 🎯 حاوية التوسيط المطلق (شاشتك المفضلة) */
[data-testid="stVerticalBlock"] {{
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
}}

/* تنسيق كلمة تأشيرات */
.main-title {{
    color: {current_c};
    font-family: 'Cairo', sans-serif;
    font-size: 70px;
    font-weight: 900;
    text-shadow: 4px 4px 15px black;
    margin-bottom: 20px;
    text-align: center;
}}

/* مربعات الإدخال */
div[data-baseweb="input"] {{
    width: 380px !important;
    background-color: rgba(30, 33, 41, 0.9) !important;
    border-radius: 12px !important;
    border: 2px solid {current_c} !important;
    margin-bottom: 15px !important;
}}

input {{
    text-align: center !important;
    color: white !important;
    font-size: 20px !important;
    height: 45px !important;
}}

/* زر الدخول */
.stButton button {{
    height: 50px;
    width: 200px;
    background-color: {current_c};
    color: black;
    font-weight: bold;
    font-family: 'Cairo';
    border-radius: 12px;
    border: none;
    font-size: 22px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
}}

.stTextInput {{
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}}
</style>
""", unsafe_allow_html=True)

# ================== 4. نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)

    u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("Pass", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")

# ================== 5. لوحة التحكم (الداخلية) ==================
else:
    st.markdown(f"<h1 style='text-align:center; color:{current_c}; font-family:Cairo;'>🌍 لوحة التحكم - {st.session_state.theme}</h1>", unsafe_allow_html=True)
    
    # هنا تضع باقي أكوادك الخاصة بمعالجة الجوازات
    if st.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()


