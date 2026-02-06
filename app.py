import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🌆 مكتبة الخلفيات ---
WALLPAPERS = {
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "دبي"

# --- 🎨 الستايل (إزالة المربع الأبيض + تنسيق يمين) ---
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

    /* 🛡️ إخفاء المربع الأبيض نهائياً عن العناوين 🛡️ */
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] > div {{
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }}

    [data-testid="stWidgetLabel"] p {{
        color: white !important;
        text-align: right !important;
        direction: rtl !important;
        font-family: 'Cairo' !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        background: transparent !important;
    }}

    /* تصميم الخانات من الداخل */
    input, [data-baseweb="select"], [data-baseweb="input"], .stSelectbox div {{
        background-color: white !important;
        border-radius: 10px !important;
        text-align: right !important;
        color: black !important;
    }}

    .inner-title {{
        font-family: 'Cairo' !important; font-size: 30px !important; color: #fbbf24;
        text-align: center; text-shadow: 2px 2px 5px black;
        border-bottom: 3px solid #fbbf24; padding-bottom: 10px; margin-bottom: 40px;
    }}

    .section-head {{
        font-size: 24px !important; font-weight: 800 !important; color: #fbbf24 !important;
        text-align: right !important; margin: 25px 0 15px 0; 
        border-right: 6px solid #fbbf24; padding-right: 15px;
        text-shadow: 2px 2px 4px black;
    }}

    .glass-box {{
        background: rgba(0, 0, 0, 0.4); 
        padding: 30px; border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-box" style="margin-top:100px;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي</div>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- شاشة التحكم بالترتيب (بالحجة) ---
    st.markdown('<div class="inner-title">🌍 لوحة التحكم - تجهيز ملف التأشيرة الكامل</div>', unsafe_allow_html=True)
    
    # بالحجة 1: بيانات الجواز
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">1️⃣ بيانات الجواز والمسافر</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("الاسم واللقب (EN)")
        st.date_input("تاريخ الميلاد")
    with c2:
        st.text_input("رقم الجواز")
        st.date_input("تاريخ انتهاء الجواز")
    with c3:
        st.selectbox("الوجهة", ["إيطاليا", "فرنسا", "تركيا", "إسبانيا"])
        st.text_input("رقم الهاتف")
    st.markdown('</div>', unsafe_allow_html=True)

    # بالحجة 2: الحجوزات
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">2️⃣ الحجوزات المبدئية (Dummy Bookings)</p>', unsafe_allow_html=True)
    air, hotel = st.columns(2)
    with air:
        st.text_input("مسار الرحلة (Tripoli - Rome)")
    with hotel:
        st.text_input("عنوان الإقامة المقترح")
    st.markdown('</div>', unsafe_allow_html=True)

    # بالحجة 3: المستندات والأزرار
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">3️⃣ الإجراءات النهائية</p>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([2, 2, 1])
    with b1:
        if st.button("إصدار ملف التأشيرة 🖨️"):
            st.success("تم تجهيز البيانات بنجاح!")
    with b2:
        if st.button("مسح البيانات 🧹"):
            st.rerun()
    with b3:
        if st.button("خروج 🚪"):
            st.session_state.auth = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
