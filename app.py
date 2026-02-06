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

# تهيئة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "باريس"

def update_bg():
    st.session_state.bg_choice = st.session_state.new_bg

# --- 🎨 الستايل الموحد (الشاشة الرئيسية وشاشة التحكم) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    /* منع الفراغات والمربعات تحت العنوان */
    [data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl !important;
    }}

    .glass-card {{
        background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(15px);
        padding: 30px; border-radius: 30px; max-width: 1000px; margin: 30px auto;
        border: 1px solid rgba(255, 255, 255, 0.2); color: white;
        text-align: center;
    }}

    .inner-title {{
        font-family: 'Cairo' !important; font-size: 26px !important; font-weight: 900 !important;
        color: #fbbf24; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 15px;
    }}

    /* تنسيق العناوين (حجم 23 ويمين) */
    [data-testid="stWidgetLabel"] p {{
        font-size: 23px !important; font-family: 'Cairo' !important; font-weight: 700 !important;
        color: white !important; text-align: right !important; direction: rtl !important;
        width: 100% !important; white-space: nowrap !important;
    }}

    input {{
        height: 45px !important; font-size: 18px !important; text-align: center !important;
        border-radius: 8px !important;
    }}

    .stButton > button {{
        width: 100% !important; height: 50px !important; font-size: 20px !important;
        font-weight: 900 !important; font-family: 'Cairo' !important;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        color: black !important; border-radius: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 🔐 الشاشة الأولى: تسجيل الدخول (ثابتة) ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card" style="max-width: 500px;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي ✈️</div>', unsafe_allow_html=True)
        
        st.selectbox("ثيمات", list(WALLPAPERS.keys()), index=0, key="new_bg", on_change=update_bg)
        user_input = st.text_input("اسم المستخدم").upper()
        pass_input = st.text_input("كلمة المرور", type="password")
        
        if st.button("دخول للنظام"):
            if (user_input == "ALI FETORY" or user_input == "ALI") and pass_input == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ✈️ الشاشة الثانية: لوحة تحكم ملفات السفارة ---
else:
    _, col_main, _ = st.columns([1, 8, 1])
    with col_main:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🌍 لوحة التحكم - تجهيز ملف التأشيرة الكامل</div>', unsafe_allow_html=True)
        
        # 1. نموذج السفارة الأصلي
        st.subheader("1️⃣ بيانات الجواز والمسافر")
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

        # 2. الحجوزات المبدئية
        st.subheader("2️⃣ الحجوزات المبدئية (Dummy Bookings)")
        air, hotel = st.columns(2)
        with air:
            st.markdown("✈️ **حجز طيران مبدئي**")
            st.text_input("مسار الرحلة (مثلاً: Tripoli - Rome)")
        with hotel:
            st.markdown("🏨 **حجز فندقي مبدئي**")
            st.text_input("عنوان الإقامة المقترح")

        st.divider()

        # 3. قائمة مراجعة الملف
        st.subheader("3️⃣ مستندات ملف التأشيرة")
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
        
        # أزرار العمليات
        b1, b2, b3 = st.columns([2, 2, 1])
        with b1:
            if st.button("إصدار ملف التأشيرة 🖨️"):
                st.success("جاري تجهيز الملف الموحد...")
        with b2:
            if st.button("مسح البيانات 🧹"):
                st.rerun()
        with b3:
            if st.button("خروج 🚪"):
                st.session_state.auth = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
