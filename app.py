import streamlit as st

# --- إعدادات الأمان الخاصة بك ---
ADMIN_NAME = "ALI FETORY"
ADMIN_PHONE = "0925843353"
MASTER_KEY = "MASAR2026" # كود سري إضافي لك إذا أردت

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- واجهة الدخول الموحدة ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>🏛️ شركة المسار الذهبي</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>بوابة الدخول للمنظومة</h3>", unsafe_allow_html=True)
    
    # خانة واحدة ذكية تقبل (الاسم أو رقم الهاتف أو كود التفعيل)
    user_input = st.text_input("أدخل كود التفعيل أو اسم المدير الخاص بك:", type="password").strip().upper()
    
    if st.button("دخول"):
        # التحقق إذا كان الداخل هو أنت (عن طريق الاسم أو الهاتف)
        if user_input == ADMIN_NAME or user_input == ADMIN_PHONE or user_input == MASTER_KEY:
            st.session_state.authenticated = True
            st.session_state.user_type = "admin"
            st.rerun()
        # التحقق إذا كان زبوناً لديه كود تفعيل (مثال لكود زبون)
        elif user_input == "USER123":
            st.session_state.authenticated = True
            st.session_state.user_type = "user"
            st.rerun()
        else:
            st.error("❌ الكود غير صحيح أو غير مفعل")
    st.stop()

# --- واجهة المنظومة بعد الدخول (لوحة التحكم التي ظهرت في صورك) ---
if st.session_state.user_type == "admin":
    st.title("📊 Invoice Dashboard - لوحة تحكم المدير")
    st.sidebar.success(f"مرحباً بالقائد: {ADMIN_NAME}")
    
    # هنا تظهر بيانات الإحصائيات التي رأيناها في صورتك
    st.info("إحصائية: 2025-05-03 بمبلغ إجمالي 2850")
    # ... باقي كود الإحصائيات والرسم البياني ...
else:
    st.title("🛂 واجهة سحب الجوازات")
    st.write("مرحباً بك في نظام شركة المسار الذهبي.")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.authenticated = False
    st.rerun()
