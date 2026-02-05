import streamlit as st

# --- بيانات الدخول الخاصة بك (المدير) ---
ADMIN_USER = "ALI FETORY"
ADMIN_PASS = "0925843353"

# --- إدارة حالة الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- شاشة تسجيل الدخول بخانتين ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>🏛️ شركة المسار الذهبي</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>بوابة الدخول للمنظومة</h3>", unsafe_allow_html=True)
    
    # الخانة الأولى: اسم المستخدم
    user_name = st.text_input("اسم المستخدم").strip().upper()
    
    # الخانة الثانية: الرقم السري (تظهر كنجوم)
    user_password = st.text_input("الرقم السري", type="password").strip()
    
    if st.button("دخول"):
        # التحقق من بياناتك (علي فيتوري)
        if user_name == ADMIN_USER.upper() and user_password == ADMIN_PASS:
            st.session_state.authenticated = True
            st.session_state.user_type = "admin"
            st.rerun()
        else:
            st.error("❌ اسم المستخدم أو الرقم السري غير صحيح")
    st.stop()

# --- ما يظهر بعد الدخول الناجح (لوحة التحكم) ---
st.title("📊 Invoice Dashboard")
st.sidebar.success(f"مرحباً بك: {ADMIN_USER}")

# هنا تظهر الإحصائيات التي كانت في صورتك السابقة
st.write("إحصائية أعلى فاتورة: 2025-05-03 بمبلغ 2850")
