import streamlit as st

# 1. إعداد الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# 2. حالة الدخول
if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================================================
# شاشة الدخول (تأشيرات) - الخانات في وسط الشاشة بالضبط
# =========================================================
if not st.session_state.auth:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* إخفاء الهيدر والفوتر */
    [data-testid="stHeader"], header, footer { display: none !important; }
    
    /* الخلفية */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* 🎯 سر التوسيط المطلق - يضع كل شيء في نص الشاشة */
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
        z-index: 9999;
    }

    /* عنوان تأشيرات */
    .main-title {
        color: #fbbf24; font-family: 'Cairo', sans-serif;
        font-size: 70px; font-weight: 900;
        text-shadow: 4px 4px 15px black; margin-bottom: 20px;
        text-align: center;
    }

    /* تنسيق مربعات الإدخال */
    div[data-baseweb="input"] {
        width: 380px !important; 
        background-color: #1e2129 !important;
        border-radius: 12px !important; 
        border: 2px solid #fbbf24 !important;
        margin-bottom: 15px !important;
    }

    input { 
        text-align: center !important; 
        color: white !important; 
        font-size: 20px !important; 
    }

    /* زر الدخول */
    .stButton button {
        height: 50px; width: 200px; 
        background-color: #fbbf24; color: black; 
        font-weight: bold; font-family: 'Cairo';
        border-radius: 12px; border: none; font-size: 22px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
    }
    </style>
    """, unsafe_allow_html=True)

    # المحتوى الممركز
    st.markdown('<div class="main-title">تأشيرات</div>', unsafe_allow_html=True)
    
    u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_login").upper()
    p = st.text_input("Pass", placeholder="كلمة المرور", type="password", label_visibility="collapsed", key="p_login")

    if st.button("دخول للنظام"):
        if (u in ["ALI", "ALI FETORY"]) and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غير صحيحة")

# =========================================================
# لوحة التحكم - (معزولة تماماً)
# =========================================================
else:
    # إلغاء التوسيط هنا لضمان حرية العمل داخل المنظومة
    st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] { 
        position: static !important; transform: none !important; 
        display: block !important; width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Cairo;'>🌍 لوحة التحكم الذكية</h1>", unsafe_allow_html=True)
    st.write("---")
    
    st.success("أهلاً بك يا علي.. تم استعادة التنسيق بنجاح")

    if st.sidebar.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()
