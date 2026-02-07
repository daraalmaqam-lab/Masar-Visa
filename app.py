import streamlit as st

# 1. إعدادات الصفحة - أبسط إعداد ممكن لضمان التشغيل
st.set_page_config(page_title="Golden Path", layout="centered")

# 2. نظام الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل الذهبي (نسخة الاستقرار الكامل)
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* إخفاء القوائم المزعجة */
    header, footer, [data-testid="stHeader"] { display: none !important; }
    
    /* الخلفية */
    .stApp { 
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
        background-size: cover; background-position: center;
    }

    /* تنسيق النصوص */
    .main-title {
        text-align: center; color: #fbbf24; font-family: 'Cairo'; 
        font-size: clamp(30px, 8vw, 55px); font-weight: 900; 
        text-shadow: 3px 3px 8px black; margin-top: 50px;
    }

    .custom-label {
        color: white; font-family: 'Cairo'; font-size: 22px; 
        text-align: center; text-shadow: 2px 2px 4px black;
        margin-top: 20px;
    }

    /* تنسيق الخانات والزر ليكونوا في المنتصف */
    div.stButton > button {
        width: 100%; background-color: #fbbf24 !important;
        color: black !important; font-weight: bold !important;
        height: 50px; border-radius: 10px; font-family: 'Cairo';
    }
    
    /* جعل المدخلات ممركزة */
    .stTextInput input {
        text-align: center !important;
        border-radius: 10px !important;
        border: 2px solid #fbbf24 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🏠 المحتوى المنطقي
# =========================================================

if not st.session_state.auth:
    # شاشة الدخول
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    
    # استخدام حاوية ممركزة من Streamlit نفسه لضمان عدم الانهيار
    with st.container():
        st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
        u = st.text_input("user", label_visibility="collapsed", key="u_login").upper()
        
        st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
        p = st.text_input("pass", type="password", label_visibility="collapsed", key="p_login")
        
        st.write("") # مسافة
        if st.button("دخول للنظام"):
            # التحقق من البيانات (علي الفيتوري)
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("تأكد من اسم المستخدم أو كلمة المرور")
else:
    # لوحة التحكم - نسخة مبسطة جداً للتأكد من العمل
    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Cairo;'>لوحة التحكم</h1>", unsafe_allow_html=True)
    st.success("تم الدخول بنجاح يا علي!")
    
    # نموذج الحجز المبدئي
    with st.expander("📝 إصدار حجز جديد", expanded=True):
        name = st.text_input("اسم المسافر")
        p_no = st.text_input("رقم الجواز")
        if st.button("حفظ الحجز"):
            st.info(f"تم تسجيل الحجز لـ {name}")

    if st.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
