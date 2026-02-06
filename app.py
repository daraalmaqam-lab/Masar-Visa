import streamlit as st

# =========================================================
# الغرفة رقم (1): شاشة الدخول (تأشيرات) - "ممنوع التغيير"
# =========================================================
def show_login_page():
    # كود التنسيق المعتمد اللي ثبتناه مع بعض
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    [data-testid="stHeader"], header, footer {{ display: none !important; }}
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    [data-testid="stVerticalBlock"] {{
        position: fixed !important; top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important; width: 100% !important; 
        display: flex !important; flex-direction: column !important;
        align-items: center !important; justify-content: center !important;
    }}
    .main-title {{
        color: #fbbf24; font-family: 'Cairo', sans-serif; font-size: 70px;
        font-weight: 900; text-shadow: 4px 4px 15px black; margin-bottom: 20px;
    }}
    div[data-baseweb="input"] {{
        width: 380px !important; background-color: #1e2129 !important;
        border-radius: 12px !important; border: 2px solid #fbbf24 !important;
        margin-bottom: 15px !important;
    }}
    input {{ text-align: center !important; color: white !important; font-size: 20px !important; }}
    .stButton button {{
        height: 50px; width: 200px; background-color: #fbbf24;
        color: black; font-weight: bold; font-family: 'Cairo';
        border-radius: 12px; border: none; font-size: 22px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.6);
    }}
    </style>
    """, unsafe_allow_html=True)

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
# الغرفة رقم (2): لوحة التحكم - "هنا عدل براحتك يا علي"
# =========================================================
def show_dashboard():
    # تنسيق بسيط للوحة التحكم عشان تكون واضحة ومريحة
    st.markdown("""
    <style>
    .dash-header { text-align: center; color: #fbbf24; font-family: 'Cairo'; font-size: 50px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="dash-header">🌍 لوحة التحكم الذكية</h1>', unsafe_allow_html=True)
    st.write("---")

    # 👇👇👇👇 (بداية منطقة التعديل الخاصة بك) 👇👇👇👇
    
    st.subheader("مرحباً بك يا علي.. ابدأ بإضافة مهامك هنا")
    
    # مثال لزر جديد:
    if st.button("📸 رفع جواز سفر جديد"):
        st.write("سيتم فتح نظام الكاميرا قريباً...")

    # 👆👆👆👆 (نهاية منطقة التعديل) 👆👆👆👆

    # زر خروج في القائمة الجانبية
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

# =========================================================
# المنظم: المحرك الرئيسي للمنظومة
# =========================================================
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

if "auth" not in st.session_state:
    st.session_state.auth = False

# التنقل بين الغرف
if not st.session_state.auth:
    show_login_page()
else:
    show_dashboard()
