import streamlit as st
import numpy as np
from PIL import Image
import re

# ================== 1. إعداد الصفحة ==================
st.set_page_config(
    page_title="Golden Path System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== 2. نظام الثيمات ==================
if "theme" not in st.session_state:
    st.session_state.theme = "الذهبي الملكي"

# تعريف خصائص الثيمات (الألوان والخلفيات)
themes = {
    "الذهبي الملكي": {
        "bg_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
        "primary": "#fbbf24",
        "text_shadow": "4px 4px 15px black"
    },
    "الليلي الغامق": {
        "bg_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=2074",
        "primary": "#3b82f6",
        "text_shadow": "2px 2px 10px blue"
    },
    "السحابي الهادئ": {
        "bg_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070",
        "primary": "#10b981",
        "text_shadow": "2px 2px 10px green"
    }
}

current_theme = themes[st.session_state.theme]

# ================== 3. الـ CSS (التوسيط وتعديل السايد بار) ==================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

/* إخفاء الهيدر */
[data-testid="stHeader"], header, footer {{
    display: none !important;
}}

/* الخلفية المتغيرة حسب الثيم */
.stApp {{
    background-image: url("{current_theme['bg_url']}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* 🎯 تنسيق السايد بار ومربع الثيمات (قصير ومتوسط) */
[data-testid="stSidebar"] {{
    background-color: rgba(0, 0, 0, 0.7) !important;
    width: 250px !important;
}}

/* تصغير مربع اختيار الثيم */
div[data-testid="stSidebar"] div[data-baseweb="select"] {{
    width: 180px !important; 
    margin: 0 auto !important; 
    border-radius: 10px !important;
    border: 1px solid {current_theme['primary']} !important;
}}

/* 🎯 التوسيط المطلق للمحتوى في نص الشاشة */
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

/* العنوان الرئيسي */
.main-title {{
    color: {current_theme['primary']};
    font-family: 'Cairo', sans-serif;
    font-size: 80px;
    font-weight: 900;
    text-shadow: {current_theme['text_shadow']};
    margin-bottom: 20px;
    text-align: center;
}}

/* مربعات الإدخال */
div[data-baseweb="input"] {{
    width: 380px !important;
    background-color: rgba(30, 33, 41, 0.9) !important;
    border-radius: 12px !important;
    border: 2px solid {current_theme['primary']} !important;
    margin-bottom: 10px !important;
}}

input {{
    text-align: center !important;
    color: white !important;
    font-size: 20px !important;
    height: 45px !important;
}}

/* زر الدخول */
.stButton button {{
    height: 55px;
    width: 220px;
    background-color: {current_theme['primary']};
    color: black;
    font-weight: bold;
    font-family: 'Cairo';
    border-radius: 15px;
    border: none;
    font-size: 22px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
    transition: 0.3s;
    margin-top: 15px;
}}

.stButton button:hover {{
    transform: scale(1.05);
    background-color: white;
    color: {current_theme['primary']};
}}
</style>
""", unsafe_allow_html=True)

# ================== 4. السايد بار (الاختيار) ==================
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center; color:{current_theme['primary']}; font-family:Cairo;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    st.session_state.theme = st.selectbox(
        "الثيم:",
        ["الذهبي الملكي", "الليلي الغامق", "السحابي الهادئ"],
        key="theme_selector"
    )
    st.write("---")

# ================== 5. نظام الدخول ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # كلمة تأشيرات في السنتر
    st.markdown(f'<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)

    # خانات الإدخال
    u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_field").upper()
    p = st.text_input("Pass", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_field")

    # زر الدخول
    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ البيانات غير صحيحة")

# ================== 6. لوحة التحكم (بعد الدخول) ==================
else:
    st.markdown(f"<div class='main-title' style='font-size:40px;'>🌍 لوحة تحكم {st.session_state.theme}</div>", unsafe_allow_html=True)
    
    # دالة قراءة الجواز (اختصارية)
    def get_passport_data(file):
        import easyocr, cv2
        reader = easyocr.Reader(['en'])
        image = Image.open(file)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return reader.readtext(img, detail=0)

    up_file = st.file_uploader("📸 ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    # حقول البيانات
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("الاسم واللقب")
    with col2:
        st.text_input("رقم الجواز")

    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
