import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🌆 مكتبة الثيمات العالمية ---
WALLPAPERS = {
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076", 
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070", 
    "لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070",
    "اسطنبول": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2071"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "باريس"

def update_bg():
    st.session_state.bg_choice = st.session_state.new_bg

# --- 🎨 الستايل (العناوين والبطاقة شفافة بظل أسود) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    [data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl !important;
    }}

    /* البطاقة الزجاجية وتعديل الشفافية */
    .glass-card {{
        background: rgba(0, 0, 0, 0.45); 
        backdrop-filter: blur(10px);
        padding: 30px; border-radius: 30px; max-width: 1100px; margin: 20px auto;
        border: 1px solid rgba(255, 255, 255, 0.2); color: white;
        text-align: right !important;
    }}

    /* 🛑 جعل مربع العنوان العلوي شفافاً ومنسجماً 🛑 */
    .inner-title {{
        font-family: 'Cairo' !important; font-size: 28px !important; font-weight: 900 !important;
        color: #fbbf24; text-align: center; 
        background: transparent !important; /* شفاف تماماً */
        margin-bottom: 25px; border-bottom: 2px solid #fbbf24;
        padding-bottom: 15px;
        text-shadow: 2px 2px 5px rgba(0,0,0,1); /* تحديد أسود قوي */
    }}

    h3, p, span, label, .stMarkdown, [data-testid="stWidgetLabel"] p {{
        color: white !important;
        text-align: right !important;
        direction: rtl !important;
        font-family: 'Cairo' !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
    }}

    [data-testid="stWidgetLabel"] p {{
        font-size: 23px !important; 
        font-weight: 700 !important;
        margin-bottom: 8px !important;
    }}

    .section-head {{
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #fbbf24 !important;
        margin: 20px 0 !important;
        border-right: 5px solid #fbbf24;
        padding-right: 15px;
        text-align: right !important;
    }}

    /* توحيد لون الخانات */
    input, [data-baseweb="select"], [data-baseweb="input"], .stSelectbox div {{
        background-color: #FFFFFF !important;
        color: black !important;
        border-radius: 8px !important;
        text-align: right !important;
        height: 45px !important;
    }}

    [data-baseweb="select"] div {{
        color: black !important;
        font-weight: bold !important;
    }}

    .stButton > button {{
        width: 100% !important; height: 55px !important; font-size: 22px !important;
        font-weight: 900 !important; font-family: 'Cairo' !important;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        color: black !important; border-radius: 12px !important;
        text-shadow: none !important;
    }}

    hr {{ border: 0; height: 1px; background-image: linear-gradient(to left, rgba(255,255,255,0), rgba(255,255,255,0.75), rgba(255,255,255,0)); margin: 20px 0; }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card" style="max-width: 500px;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي ✈️</div>', unsafe_allow_html=True)
        st.selectbox("ثيمات", list(WALLPAPERS.keys()), index=0, key="new_bg", on_change=update_bg)
        user_input_val = st.text_input("اسم المستخدم").upper()
        pass_input = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (user_input_val == "ALI FETORY" or user_input_val == "ALI") and pass_input == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    _, col_main, _ = st.columns([1, 10, 1])
    with col_main:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # العنوان هنا أصبح شفافاً تماماً كما طلبت
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
            st.selectbox("الوجهة", ["إيطاليا", "فرنسا", "تركيا", "إسبانيا"])
            st.text_input("رقم الهاتف")

        st.divider()

        st.markdown('<p class="section-head">2️⃣ الحجوزات المبدئية (Dummy Bookings)</p>', unsafe_allow_html=True)
        air, hotel = st.columns(2)
        with air:
            st.text_input("مسار الرحلة (Tripoli - Rome)")
        with hotel:
            st.text_input("عنوان الإقامة المقترح")

        st.divider()

        st.markdown('<p class="section-head">3️⃣ مستندات ملف التأشيرة</p>', unsafe_allow_html=True)
        ch1, ch2, ch3 = st.columns(3)
        with ch1:
            st.checkbox("الجواز الأصلي + صورة")
            st.checkbox("صور شخصية (3.5x4.5)")
        with ch2:
            st.checkbox("كشف حساب بنكي")
            st.checkbox("إفادة عمل مترجمة")
        with ch3:
            st.checkbox("التأمين الصحي")
            st.checkbox("حجز الطيران والفندق")

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns([2, 2, 1])
        with b1:
            if st.button("إصدار ملف التأشيرة 🖨️"):
                st.success("جاري تجهيز الملف...")
        with b2:
            if st.button("مسح البيانات 🧹"):
                st.rerun()
        with b3:
            if st.button("خروج 🚪"):
                st.session_state.auth = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
