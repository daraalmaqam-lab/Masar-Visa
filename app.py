import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🌆 مكتبة الثيمات ---
WALLPAPERS = {
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "دبي"

# --- 🎨 الستايل (إصلاح المربع الأبيض الموضح في الصورة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"] {{
        display: none !important;
    }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* 🛡️ إزالة المربع الأبيض عن كلمة الوجهة وغيرها 🛡️ */
    div[data-testid="stWidgetLabel"], 
    div[data-testid="stWidgetLabel"] > div,
    label {{
        background-color: transparent !important; /* شفافية كاملة */
        background: none !important;
        box-shadow: none !important;
        border: none !important;
        display: block !important;
        width: 100% !important;
    }}

    div[data-testid="stWidgetLabel"] p {{
        color: white !important;
        text-align: right !important; /* العودة لليمين */
        direction: rtl !important;
        font-family: 'Cairo' !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        margin-bottom: 5px !important;
        background: transparent !important;
    }}

    /* تحسين شكل الخانات الملونة بالأبيض من الداخل */
    input, [data-baseweb="select"], [data-baseweb="input"] {{
        background-color: white !important;
        border-radius: 10px !important;
        text-align: right !important;
        color: black !important;
    }}

    .inner-title {{
        font-family: 'Cairo' !important; font-size: 28px !important; color: #fbbf24;
        text-align: center; text-shadow: 2px 2px 5px black;
        border-bottom: 2px solid #fbbf24; padding-bottom: 10px; margin-bottom: 30px;
    }}

    .section-head {{
        font-size: 22px !important; font-weight: 800 !important; color: #fbbf24 !important;
        text-align: right !important; margin: 15px 0; border-right: 5px solid #fbbf24; padding-right: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    # شاشة الدخول (مختصرة للأمان)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div style="background:rgba(0,0,0,0.6); padding:30px; border-radius:20px; border:1px solid gold;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي</div>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # شاشة التحكم
    st.markdown('<div class="inner-title">🌍 لوحة التحكم - تجهيز ملف التأشيرة الكامل</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-head">1️⃣ بيانات الجواز والمسافر</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("الاسم واللقب (EN)")
        st.date_input("تاريخ الميلاد")
    with c2:
        st.text_input("رقم الجواز")
        st.date_input("تاريخ انتهاء الجواز")
    with c3:
        # كلمة "الوجهة" هنا ستظهر بدون المربع الأبيض المزعج
        st.selectbox("الوجهة", ["إيطاليا", "فرنسا", "تركيا", "إسبانيا"])
        st.text_input("رقم الهاتف")

    st.markdown('<p class="section-head">2️⃣ الحجوزات المبدئية (Dummy Bookings)</p>', unsafe_allow_html=True)
    air, hotel = st.columns(2)
    with air:
        st.text_input("مسار الرحلة (Tripoli - Rome)")
    with hotel:
        st.text_input("عنوان الإقامة المقترح")
    
    if st.button("خروج 🚪"):
        st.session_state.auth = False
        st.rerun()
