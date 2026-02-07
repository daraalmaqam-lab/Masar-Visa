import streamlit as st
import numpy as np
from PIL import Image

# ================== 1. إعداد الصفحة ==================
st.set_page_config(
    page_title="Golden Path",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== 2. نظام الثيمات ==================
if "theme" not in st.session_state:
    st.session_state.theme = "الذهبي الملكي"

theme_config = {
    "الذهبي الملكي": {"color": "#fbbf24", "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"},
    "الليلي الغامق": {"color": "#3b82f6", "img": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=2074"},
    "الأخضر الهادئ": {"color": "#10b981", "img": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070"}
}
current_c = theme_config[st.session_state.theme]["color"]
current_bg = theme_config[st.session_state.theme]["img"]

# ================== 3. نظام الدخول وحالة الجلسة ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

# ================== 4. التنسيق (CSS) المحمي ==================
# التعديل هنا: التوسيط يطبق فقط إذا كان المستخدم لم يسجل دخوله بعد
centering_css = ""
if not st.session_state.auth:
    centering_css = f"""
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
        z-index: 9999;
    }}
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

[data-testid="stHeader"], header, footer {{ display: none !important; }}

.stApp {{
    background-image: url("{current_bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* تطبيق التوسيط فقط في شاشة الدخول */
{centering_css}

.main-title {{
    color: {current_c};
    font-family: 'Cairo', sans-serif;
    font-size: 70px;
    font-weight: 900;
    text-shadow: 4px 4px 15px black;
    margin-bottom: 20px;
    text-align: center;
}}

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
</style>
""", unsafe_allow_html=True)

# ================== 5. عرض الشاشات ==================
if not st.session_state.auth:
    # شاشة الدخول (نفس كودك المفضل)
    st.markdown('<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)
    u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("Pass", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")
else:
    # لوحة التحكم - الآن أصبحت حرة وليست مقيدة بالتوسيط المطلق
    st.markdown(f"<h1 style='text-align:center; color:{current_c}; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # هنا تقدر تضيف شغلك الجديد (رفع ملفات، جداول، إلخ) وبتاخد مساحة الشاشة كاملة
    st.success(f"مرحباً بك يا {u if 'u' in locals() else 'علي'}")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

