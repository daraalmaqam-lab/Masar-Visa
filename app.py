import streamlit as st

# --- بيانات المدير (أنت) ---
ADMIN_DATA = {
    "NAME": "ALI FETORY",
    "PHONE": "0925843353"
}

# --- حالة الجلسة ---
if 'auth_level' not in st.session_state:
    st.session_state.auth_level = None

# --- شاشة الدخول الذكية ---
if st.session_state.auth_level is None:
    st.title("🏦 شركة المسار الذهبي")
    st.subheader("بوابة الدخول للمنظومة")
    
    name_input = st.text_input("الأسم الكريم").strip().upper()
    phone_input = st.text_input("رقم الهاتف").strip()
    
    if st.button("دخول"):
        # التحقق إذا كان الداخل هو أنت (المدير)
        if name_input == ADMIN_DATA["NAME"] and phone_input == ADMIN_DATA["PHONE"]:
            st.session_state.auth_level = "admin"
            st.rerun()
        # التحقق إذا كان زبوناً (يجب أن يدخل بياناته)
        elif len(name_input) > 2 and len(phone_input) >= 10:
            st.session_state.auth_level = "user"
            st.session_state.user_name = name_input
            st.rerun()
        else:
            st.error("الرجاء التأكد من إدخال البيانات بشكل صحيح")
    st.stop()

# --- بعد الدخول السليم ---
if st.session_state.auth_level == "admin":
    st.sidebar.success(f"مرحباً بالقائد: {ADMIN_DATA['NAME']}")
    st.title("📊 لوحة تحكم المدير")
    # هنا تظهر الإحصائيات (مثل صورة Invoice Dashboard التي أرفقتها)
    st.write("إحصائيات العمليات والمبيعات تظهر هنا...")
    
else:
    st.sidebar.info(f"الزبون: {st.session_state.user_name}")
    st.title("🛂 واجهة سحب بيانات الجوازات")
    # هنا تظهر واجهة الزبون البسيطة لسحب الجوازات فقط
    st.file_uploader("ارفع صورة الجواز هنا")

if st.sidebar.button("خروج"):
    st.session_state.auth_level = None
    st.rerun()
