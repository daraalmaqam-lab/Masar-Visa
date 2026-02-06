import streamlit as st
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path - AI Reader", layout="wide", initial_sidebar_state="collapsed")

# --- 🌆 مكتبة الخلفيات ---
WALLPAPERS = {
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076"
}

EUROPE_AIRPORTS = ["Tripoli (MJI)", "Benghazi (BEN)", "Istanbul (IST)", "Rome (FCO)", "Paris (CDG)", "Madrid (MAD)", "Other / أخرى"]

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "دبي"

# --- 🎨 الستايل (شفافية كاملة + تنسيق احترافي) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"] {{ display: none !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* إزالة المربعات البيضاء عن العناوين */
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
        font-size: 19px !important; 
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
    }}

    input, [data-baseweb="select"], [data-baseweb="input"], .stSelectbox div {{
        background-color: white !important;
        border-radius: 10px !important;
        text-align: right !important;
        color: black !important;
        font-weight: bold !important;
    }}

    .inner-title {{
        font-family: 'Cairo' !important; font-size: 30px !important; color: #fbbf24;
        text-align: center; text-shadow: 2px 2px 5px black;
        border-bottom: 3px solid #fbbf24; padding-bottom: 10px; margin-bottom: 30px;
    }}

    .section-head {{
        font-size: 22px !important; font-weight: 800 !important; color: #fbbf24 !important;
        text-align: right !important; margin: 15px 0; border-right: 6px solid #fbbf24; padding-right: 15px;
    }}

    .glass-box {{
        background: rgba(0, 0, 0, 0.45); padding: 25px; border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.2); margin-bottom: 20px;
    }}

    /* ستايل خاص لخانة رفع الملفات */
    [data-testid="stFileUploadDropzone"] {{
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed #fbbf24 !important;
        border-radius: 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- منطق الدخول ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-box" style="margin-top:80px;">', unsafe_allow_html=True)
        st.markdown('<div class="inner-title">🛂 طيران المسار الذهبي</div>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="inner-title">🌍 لوحة التحكم الذكية - قارئ الجوازات الآلي</div>', unsafe_allow_html=True)

    # حجة 1: قارئ الجواز (التحميل والمعالجة)
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">📸 الخطوة الأولى: مسح الجواز ضوئياً</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("قم برفع صورة الجواز هنا (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    
    # محاكاة تعبئة البيانات (يمكن ربطها بمكتبة EasyOCR لاحقاً)
    scanned_data = {"name": "", "passport": "", "dob": None, "expiry": None}
    
    if uploaded_file:
        with st.spinner('جاري قراءة بيانات الجواز وتعبئة الخانات...'):
            time.sleep(2) # محاكاة وقت المعالجة
            scanned_data = {
                "name": "ALI FETORY",
                "passport": "P12345678",
                "dob": time.struct_time((1990, 1, 1, 0, 0, 0, 0, 0, 0)),
                "expiry": time.struct_time((2030, 12, 31, 0, 0, 0, 0, 0, 0))
            }
            st.success("تم استخراج البيانات بنجاح!")
    st.markdown('</div>', unsafe_allow_html=True)

    # حجة 2: البيانات المستخرجة (تتعبأ تلقائياً)
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">2️⃣ بيانات الجواز والمسافر (تعبئة آلية)</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        name_val = st.text_input("الاسم واللقب (EN)", value=scanned_data["name"])
        st.date_input("تاريخ الميلاد")
    with c2:
        pass_val = st.text_input("رقم الجواز", value=scanned_data["passport"])
        st.date_input("تاريخ انتهاء الجواز")
    with c3:
        st.selectbox("الوجهة", ["إيطاليا", "فرنسا", "تركيا", "ألمانيا"])
        st.text_input("رقم الهاتف", value="0925843353")
    st.markdown('</div>', unsafe_allow_html=True)

    # حجة 3: مسار الرحلة
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">3️⃣ تفاصيل حجز الطيران</p>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1: st.selectbox("من", EUROPE_AIRPORTS, index=0)
    with f2: st.selectbox("إلى", EUROPE_AIRPORTS, index=3)
    with f3: st.date_input("تاريخ الذهاب")
    with f4: st.date_input("تاريخ العودة")
    st.markdown('</div>', unsafe_allow_html=True)

    # أزرار التحكم
    st.markdown('<br>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([2, 2, 1])
    with b1: st.button("إصدار ملف التأشيرة 🖨️")
    with b2:
        if st.button("مسح البيانات 🧹"): st.rerun()
    with b3:
        if st.button("خروج 🚪"):
            st.session_state.auth = False
            st.rerun()
