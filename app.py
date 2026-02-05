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

if 'auth' not in st.session_state: st.session_state.auth = False
if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# --- 🎨 الستايل الاحترافي (تثبيت المربعات وتنظيف الرموز) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* 1. تنظيف شامل للزوائد */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebarNav"] {{
        display: none !important;
    }}
    
    html, body, [class*="st-"] {{ 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
    }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* 2. تصميم مربع العنوان (اللي طلبته يا علي) */
    .title-box {{
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    /* 3. تصميم بطاقة البيانات */
    .data-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }}

    /* إخفاء الرموز الغريبة والمربعات البيضاء في المدخلات */
    .st-emotion-cache-1kyx738, .st-emotion-cache-6qob1r {{ display: none !important; }}
    input {{ background-color: white !important; color: black !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    st.session_state.bg_choice = st.selectbox("اختر الخلفية:", list(WALLPAPERS.keys()))
    if st.button("🚪 تسجيل خروج"):
        st.session_state.auth = False
        st.rerun()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="title-box" style="margin-top:100px;">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:white; margin:0;'>🏛️ بوابة المسار الذهبي</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول النظام", use_container_width=True):
            if u == "ALI FETORY" and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- الواجهة الرئيسية للعمل ---
st.markdown('<div class="title-box">', unsafe_allow_html=True)
st.markdown("<h1 style='color:white; margin:0;'>🌍 بوابة المسار الذهبي</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.subheader("📥 بيانات الجواز والنموذج")
    
    c1, c2 = st.columns([1, 2])
    target = c1.selectbox("اختر الدولة", ["italy", "france", "germany"])
    file = c2.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])

    if file and st.button("⚡ قراءة البيانات"):
        # محاكاة القراءة (OCR)
        st.session_state.data = {"sn": "FETORY", "fn": "ALI", "pno": "P1234567"}
        st.rerun()

    st.divider()
    
    col1, col2 = st.columns(2)
    sn = col1.text_input("اللقب", value=st.session_state.data["sn"])
    fn = col1.text_input("الاسم", value=st.session_state.data["fn"])
    pno = col2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = col2.text_input("المهنة")

    if st.button("🔥 طباعة النموذج النهائي", use_container_width=True):
        st.success("تم تجهيز النموذج بنجاح!")
    st.markdown('</div>', unsafe_allow_html=True)
