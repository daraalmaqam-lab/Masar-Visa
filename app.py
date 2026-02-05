import streamlit as st
import numpy as np
from PIL import Image

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="Golden Path", layout="wide")

# --- مكتبة الثيمات الـ 14 كاملة ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🎡 لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070",
    "🕌 اسطنبول": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2071",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🏖️ المالديف": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=1965",
    "⛰️ سويسرا": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=2070",
    "🗽 نيويورك": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=2070",
    "🏜️ الأهرامات": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?q=80&w=2070",
    "🏮 سور الصين": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?q=80&w=2070",
    "🕌 مراكش": "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?q=80&w=2071",
    "🌊 سانتوريني": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2022",
    "🌉 سان فرانسيسكو": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?q=80&w=2070"
}

# تهيئة حالة الجلسة
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل (تنظيف شامل + شفافية زجاجية) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف شريط Fork والأيقونات المشوهة */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], 
    .st-emotion-cache-6qob1r, .st-emotion-cache-1kyx738 {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    html, body, [class*="st-"] {{ 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
    }}

    /* الخلفية المتحركة */
    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* المربع الشفاف للعنوان */
    .glass-header {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        max-width: 600px;
        margin: 40px auto;
        color: white;
        font-size: 28px;
        font-weight: 900;
    }}

    /* البطاقة الزجاجية المتناسقة للبيانات */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 500px;
        margin: 0 auto;
        color: white;
    }}

    /* تنسيق الخانات */
    input {{ 
        background-color: white !important; 
        color: black !important; 
        border-radius: 10px !important;
        height: 45px !important;
        font-weight: bold !important;
        text-align: center;
    }}

    /* تنسيق الأزرار */
    .stButton > button {{
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        height: 50px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (رجوع الثيمات) ---
with st.sidebar:
    st.markdown("### ⚙️ إعدادات المنظومة")
    st.session_state.bg_choice = st.selectbox("🎨 تغيير الثيم:", list(WALLPAPERS.keys()))
    st.divider()
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="glass-header">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        user = st.text_input("اسم المستخدم").upper()
        passw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول النظام", use_container_width=True):
            if user == "ALI FETORY" and passw == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- شاشة العمل بعد الدخول ---
st.markdown('<div class="glass-header">🌍 بوابة المسار الذهبي</div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 3, 1])
with col_b:
    st.markdown('<div class="glass-card" style="max-width: 1000px;">', unsafe_allow_html=True)
    st.subheader("📝 إدخال البيانات")
    c1, c2 = st.columns(2)
    c1.text_input("اللقب")
    c1.text_input("الاسم")
    c2.text_input("رقم الجواز")
    c2.selectbox("الدولة", ["إيطاليا", "فرنسا", "ألمانيا"])
    
    if st.button("🔥 طباعة النموذج", use_container_width=True):
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)
