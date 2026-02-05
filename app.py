import streamlit as st
import numpy as np
from PIL import Image

# إعدادات الصفحة الأساسية لإلغاء أي هوامش
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الثيمات الـ 14 (رجعتها لك كاملة) ---
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

# تهيئة الحالة
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"

# --- 🎨 الستايل النهائي (القضاء على الرموز والمربعات السوداء) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* 1. حذف كل زوائد ستريمليت والرموز الغريبة نهائياً */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], 
    [data-testid="stSidebarNav"], .st-emotion-cache-6qob1r, 
    .st-emotion-cache-1kyx738, [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    /* 2. تنظيف اتجاه الصفحة والخط */
    html, body, [class*="st-"] {{ 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
        color: white;
    }}

    /* 3. تعيين الخلفية */
    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 4. المربع الشفاف للعنوان (بدون سواد وبدون رموز) */
    .main-title {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        max-width: 700px;
        margin: 40px auto;
        font-size: 30px;
        font-weight: 900;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}

    /* 5. المربع الشفاف للبيانات */
    .content-card {{
        background: rgba(0, 0, 0, 0.3); /* خففت السواد جداً */
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 900px;
        margin: 20px auto;
    }}

    /* تنسيق المدخلات */
    input {{ 
        background-color: white !important; 
        color: black !important; 
        border-radius: 10px !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (للثيمات واللغة) ---
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    st.session_state.bg_choice = st.selectbox("🎨 اختر الثيم:", list(WALLPAPERS.keys()))
    st.divider()
    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()

# --- منطق الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    user = st.text_input("اسم المستخدم").upper()
    passw = st.text_input("كلمة المرور", type="password")
    if st.button("دخول النظام", use_container_width=True):
        if user == "ALI FETORY" and passw == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- الواجهة الرئيسية بعد الدخول ---
st.markdown('<div class="main-title">🌍 بوابة المسار الذهبي</div>', unsafe_allow_html=True)

st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.subheader("📋 بيانات المنظومة")
col1, col2 = st.columns(2)
with col1:
    st.text_input("اللقب")
    st.text_input("الاسم")
with col2:
    st.text_input("رقم الجواز")
    st.selectbox("الدولة", ["إيطاليا", "فرنسا", "ألمانيا"])

if st.button("تحميل النموذج", use_container_width=True):
    st.success("تم التجهيز")
st.markdown('</div>', unsafe_allow_html=True)
