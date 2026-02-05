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
        "dir": "rtl", "title": "بوابة المسار الذهبي", "login": "دخول", "user": "المستخدم", "pass": "كلمة المرور",
        "settings": "إعدادات النظام", "lang": "اللغة", "theme": "ثيم المنظومة", "logout": "خروج", "scan": "البيانات"
    },
    "English": {
        "dir": "ltr", "title": "Golden Path Gateway", "login": "Login", "user": "User", "pass": "Pass",
        "settings": "Settings", "lang": "Language", "theme": "Theme", "logout": "Logout", "scan": "Import"
    }
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
L = LANG[st.session_state.lang]

# --- 🎨 الستايل (تنظيف كامل وشامل) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: {L['dir']}; }}

    /* 🛑 إخفاء كل زوائد Streamlit المزعجة */
    header, footer, .stAppDeployButton, [data-testid="stStatusWidget"] {{ visibility: hidden !important; display: none !important; }}
    
    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* تنظيف المربعات تحت اللغة وفوق العناوين */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{ border: none !important; }}
    
    /* إخفاء إطار الراديو (اللغة والجنس) */
    div[data-testid="stWidgetLabel"] {{ background: transparent !important; border: none !important; }}
    div[role="radiogroup"] {{ border: none !important; padding: 0 !important; gap: 20px; }}

    /* إخفاء الخط الأبيض (المؤشر) ومربع البحث في أي قائمة */
    div[data-baseweb="select"] input {{ caret-color: transparent !important; color: transparent !important; text-shadow: 0 0 0 white !important; }}
    div[data-baseweb="select"] {{ border: none !important; outline: none !important; box-shadow: none !important; background: rgba(255,255,255,0.1) !important; border-radius: 10px; }}

    /* تصميم البطاقات الزجاجية الشفافة جداً */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(25px); padding: 25px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 15px;
    }}

    /* تجميل المدخلات */
    input {{ background-color: white !important; color: black !important; border-radius: 10px !important; border: none !important; font-weight: 700; }}
    
    .stButton>button {{
        background: linear-gradient(90deg, #1D4ED8, #3B82F6) !important;
        border: none !important; color: white !important; border-radius: 10px !important; font-weight: 800 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (شكل جديد للثيمات) ---
with st.sidebar:
    st.markdown(f"### ⚙️ {L['settings']}")
    # اختيار اللغة بدون مربعات
    st.session_state.lang = st.radio(f"{L['lang']}:", ["العربية", "English"], horizontal=True)
    st.divider()
    # عرض الثيمات كقائمة نظيفة
    st.session_state.bg_choice = st.selectbox(f"🎨 {L['theme']}", list(WALLPAPERS.keys()))
    st.divider()
    if st.button(L['logout']):
        st.session_state.auth = False
        st.rerun()

# --- الدخول ---
if not st.session_state.auth:
    st.markdown(f"<h1 style='color:white; text-align:center; margin-top:100px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);'>🏛️ {L['title']}</h1>", unsafe_allow_html=True)
    u = st.text_input(L['user']).upper()
    p = st.text_input(L['pass'], type="password")
    if st.button(L['login']):
        if u == "ALI FETORY" and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='color:white; text-align:center; text-shadow: 2px 2px 15px rgba(0,0,0,0.7);'>{L['title']}</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"### 📥 {L['scan']}")
    c1, c2 = st.columns([1, 2])
    # أزرار الدولة بدون مربعات خلفية
    target = c1.radio("الدولة:", ["italy", "france", "germany"], horizontal=False)
    file = c2.file_uploader(L['upload'] if st.session_state.lang=="English" else "ارفع الجواز", type=['jpg', 'png', 'jpeg'])

with st.container():
    st.markdown(f"### 📝 التحقق من البيانات")
    col1, col2 = st.columns(2)
    sn = col1.text_input("اللقب", value=st.session_state.get('sn', ''))
    fn = col1.text_input("الاسم", value=st.session_state.get('fn', ''))
    pno = col2.text_input("رقم الجواز")
    gender = col2.radio("الجنس", ["Male", "Female"], horizontal=True)

if st.button(f"✨ تنفيذ", use_container_width=True):
    st.balloons()
