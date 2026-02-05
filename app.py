import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الثيمات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974",
    "🎡 لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070"
}

if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل (تنسيق الأحجام وفصل الشاشات) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* تنظيف الواجهة تماماً */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    .block-container {{ padding-top: 2rem !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-attachment: fixed;
    }}

    /* مربع العنوان */
    .main-title {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 20px; border-radius: 15px;
        text-align: center; max-width: 550px;
        margin: 20px auto; color: white;
        font-family: 'Cairo', sans-serif; font-size: 30px; font-weight: 900;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    /* بطاقة الدخول (أحجام متناسقة) */
    .glass-card {{
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        padding: 40px; border-radius: 25px;
        max-width: 500px; margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* تكبير وتنسيق الخانات */
    input {{ 
        height: 55px !important; 
        font-size: 20px !important; 
        text-align: center !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }}

    /* تنسيق الزر */
    .stButton > button {{
        width: 100% !important;
        height: 55px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- منطق العرض (فصل الشاشات) ---

if not st.session_state.auth:
    # 1. شاشة الدخول فقط
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # اختيار الثيم هنا قبل الدخول
        st.session_state.bg_choice = st.selectbox("🎨 اختر واجهة المنظومة:", list(WALLPAPERS.keys()))
        st.divider()
        user = st.text_input("اسم المستخدم", placeholder="ادخل اسمك هنا").upper()
        passw = st.text_input("كلمة المرور", type="password", placeholder="ادخل الرمز السري")
        
        if st.button("دخول للنظام"):
            if (user == "ALI FETORY" or user == "ALI") and passw == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("خطأ في البيانات!")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # 2. شاشة العمل (ما تطلعش إلا بعد الدخول)
    st.markdown('<div class="main-title">🌍 لوحة التحكم - المسار الذهبي</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 3, 1])
    with col_b:
        st.markdown('<div class="glass-card" style="max-width: 800px;">', unsafe_allow_html=True)
        st.subheader("📝 إدخال بيانات المسافرين")
        
        c1, c2 = st.columns(2)
        c1.text_input("الاسم الأول")
        c1.text_input("اللقب")
        c2.text_input("رقم الجواز")
        c2.selectbox("دولة الوجهة", ["إيطاليا", "فرنسا", "ألمانيا"])
        
        st.divider()
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
