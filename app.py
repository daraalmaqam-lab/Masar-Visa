import streamlit as st

# --- إعدادات الحساب الخاص بك (المدير) ---
ADMIN_USERNAME = "ALI FETORY"
ADMIN_PASSWORD = "0925843353"

# --- إدارة حالة الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- شاشة تسجيل الدخول ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>🏛️ شركة المسار الذهبي</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>تسجيل دخول المستخدم</h3>", unsafe_allow_html=True)
    
    # الخانتين اللتين طلبتهما
    user_name = st.text_input("اسم المستخدم").strip().upper()
    user_pass = st.text_input("الرقم السري", type="password").strip()
    
    if st.button("دخول"):
        # التحقق من بياناتك (لا تهم حالة الأحرف في الاسم)
        if user_name == ADMIN_USERNAME.upper() and user_pass == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.user_role = "admin"
            st.rerun()
        # هنا يمكنك إضافة مستخدمين آخرين مستقبلاً
        elif user_name == "USER1" and user_pass == "12345":
            st.session_state.authenticated = True
            st.session_state.user_role = "user"
            st.rerun()
        else:
            st.error("❌ اسم المستخدم أو الرقم السري غير صحيح")
    st.stop()

# --- واجهة المنظومة بعد الدخول الناجح ---
if st.session_state.user_role == "admin":
    st.sidebar.success(f"مرحباً بالمدير: {ADMIN_USERNAME}")
    st.title("📊 لوحة تحكم شركة المسار الذهبي")
    
    # هنا تضع كود الإحصائيات (Invoice Dashboard)
    st.write("أهلاً بك يا علي، يمكنك الآن رؤية كافة التقارير والبيانات.")
    
else:
    st.sidebar.info("واجهة المستخدم")
    st.title("🛂 نظام سحب الجوازات")
    st.write("يمكنك البدء برفع الملفات الآن.")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.authenticated = False
    st.rerun()
