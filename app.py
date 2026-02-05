import streamlit as st
from docx import Document
import io

# إعدادات الصفحة
st.set_page_config(page_title="منظومة المسار الذهبي", layout="centered")

# دالة لتنسيق الواجهة (CSS)
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004aad; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 1. تعريف المستخدمين (يمكنك إضافة زبائن هنا مستقبلاً)
ADMIN_PHONE = "0910000000"  # ضع رقم هاتفك هنا كمدير
ADMIN_NAME = "علي"

# 2. نظام الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None

if not st.session_state.logged_in:
    st.title("🔒 نظام الدخول الذكي")
    st.subheader("شركة المسار الذهبي للخدمات السياحية")
    
    name_input = st.text_input("الأسم الكريم")
    phone_input = st.text_input("رقم الهاتف (للتفعيل)")
    
    if st.button("دخول المنظومة"):
        if phone_input == ADMIN_PHONE and name_input == ADMIN_NAME:
            st.session_state.logged_in = True
            st.session_state.user_type = "admin"
            st.rerun()
        elif len(phone_input) >= 10 and len(name_input) > 2:
            st.session_state.logged_in = True
            st.session_state.user_type = "user"
            st.session_state.user_info = {"name": name_input, "phone": phone_input}
            st.rerun()
        else:
            st.error("الرجاء إدخال بيانات صحيحة")

# 3. عرض الواجهة بناءً على نوع المستخدم
else:
    if st.session_state.user_type == "admin":
        st.sidebar.success(f"مرحباً يا مدير: {ADMIN_NAME}")
        st.title("👨‍💻 لوحة تحكم المدير")
        st.info("هنا تظهر لك إحصائيات النظام والتحكم الكامل.")
        # هنا تضع ميزات المدير فقط
    else:
        st.sidebar.info(f"الزبون: {st.session_state.user_info['name']}")
        st.title("🛂 واجهة سحب بيانات الجوازات")
        st.write("مرحباً بك في شركة المسار الذهبي. يمكنك البدء برفع صور الجوازات.")
        # هنا تضع ميزات سحب الجوازات للزبون

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
