import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- مكتبة الثيمات الـ 14 ---
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

# --- نصوص اللغات ---
LANG = {
    "العربية": {
        "dir": "rtl", "title": "بوابة المسار الذهبي", "login": "دخول النظام", "user": "اسم المستخدم", "pass": "كلمة المرور",
        "settings": "الإعدادات", "lang": "اللغة", "theme": "اختر الثيم:", "logout": "خروج", "scan": "قراءة الجواز",
        "visa_target": "الدولة:", "upload": "ارفع الجواز", "surname": "اللقب", "name": "الاسم", "passport": "رقم الجواز",
        "job": "المهنة", "gender": "الجنس", "print": "إصدار النموذج"
    },
    "English": {
        "dir": "ltr", "title": "Golden Path Gateway", "login": "System Login", "user": "Username", "pass": "Password",
        "settings": "Settings", "lang": "Language", "theme": "Select Theme:", "logout": "Logout", "scan": "Passport Scan",
        "visa_target": "Country:", "upload": "Upload Passport", "surname": "Surname", "name": "First Name", "passport": "Passport No",
        "job": "Job", "gender": "Gender", "print": "Generate Document"
    }
}

# --- تهيئة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
L = LANG[st.session_state.lang]

# --- 🎨 الستايل المتطور ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: {L['dir']}; }}

    /* إخفاء شريط Fork وكل زوائد GitHub */
    .stAppDeployButton, [data-testid="stStatusWidget"], footer {{ display: none !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* إلغاء مربعات البحث والمؤشرات */
    div[data-baseweb="select"] input, input[role="combobox"] {{ caret-color: transparent !important; color: transparent !important; text-shadow: 0 0 0 white !important; }}
    div[data-baseweb="select"] {{ border: none !important; outline: none !important; box-shadow: none !important; }}

    /* البطاقة الزجاجية */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(20px); padding: 30px; border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #1D4ED8, #2563EB) !important;
        color: white !important; border-radius: 12px !important; font-weight: 800 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### ⚙️ {L['settings']}")
    # تغيير اللغة
    st.session_state.lang = st.radio(f"🌐 {L['lang']}:", ["العربية", "English"], horizontal=True)
    st.divider()
    # تغيير الثيم
    st.session_state.bg_choice = st.radio(f"🎨 {L['theme']}", list(WALLPAPERS.keys()))
    st.divider()
    if st.button(L['logout']):
        st.session_state.auth = False
        st.rerun()

# --- الدخول ---
if not st.session_state.auth:
    st.markdown(f"<h1 style='color:white; text-align:center; margin-top:100px;'>🏛️ {L['title']}</h1>", unsafe_allow_html=True)
    u = st.text_input(L['user']).upper()
    p = st.text_input(L['pass'], type="password")
    if st.button(L['login']):
        if u == "ALI FETORY" and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='color:white; text-align:center;'>{L['title']}</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"### 📥 {L['scan']}")
    c1, c2 = st.columns([1, 2])
    target = c1.radio(L['visa_target'], ["italy", "france", "germany"], horizontal=True)
    file = c2.file_uploader(L['upload'], type=['jpg', 'png', 'jpeg'])

with st.container():
    st.markdown(f"### 📝 {L['settings']}")
    col1, col2 = st.columns(2)
    sn = col1.text_input(L['surname'])
    fn = col1.text_input(L['name'])
    pno = col2.text_input(L['passport'])
    job = col2.text_input(L['job'])
    gender = col2.radio(L['gender'], ["Male", "Female"], horizontal=True)

if st.button(f"✨ {L['print']}", use_container_width=True):
    st.success("جاري المعالجة...")
