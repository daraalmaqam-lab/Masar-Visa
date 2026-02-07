import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="centered")

# 2. نظام الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل الذهبي (توسيط إجباري 100%)
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-position: center;
    }

    /* 🎯 توسيط العنوان والخانات في نص الشاشة */
    .login-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; width: 100%; margin-top: 50px;
    }

    .main-title {
        color: #fbbf24; font-family: 'Cairo'; font-size: 55px; font-weight: 900;
        text-shadow: 3px 3px 8px black; margin-bottom: 20px;
    }

    .custom-label {
        color: white; font-family: 'Cairo'; font-size: 24px; font-weight: 700;
        text-align: center; width: 100%; margin-bottom: 5px; margin-top: 15px;
        text-shadow: 2px 2px 4px black;
    }

    /* ✍️ تنسيق المربعات */
    div[data-baseweb="input"] {
        height: 45px !important; width: 320px !important; 
        margin: 0 auto !important; background-color: white !important; 
        border-radius: 10px !important; border: 2px solid #fbbf24 !important;
    }
    
    input { text-align: center !important; color: black !important; font-size: 18px !important; font-weight: bold !important; }

    /* 🔘 الزر */
    .stButton button {
        height: 55px !important; width: 220px !important; 
        background-color: #fbbf24 !important; color: black !important; 
        font-weight: bold !important; font-family: 'Cairo' !important;
        font-size: 22px !important; margin-top: 30px !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🏠 المحتوى المنطقي
# =========================================================
if not st.session_state.auth:
    # شاشة الدخول الممركزة
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("user", label_visibility="collapsed", key="u_login").upper()
    
    st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("pass", type="password", label_visibility="collapsed", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # لوحة التحكم (النموذج المبدئي)
    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم</h1>", unsafe_allow_html=True)
    st.success(f"مرحباً بك يا {st.session_state.get('u_login', 'علي')}")
    
    with st.container():
        st.write("### 📝 نموذج حجز مبدئي")
        name = st.text_input("اسم المسافر")
        passport = st.text_input("رقم الجواز")
        if st.button("حفظ الحجز"):
            st.info("تم الحجز")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
