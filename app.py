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

# --- 🎨 الستايل (تنظيف شامل وعرض زجاجي) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف كل الزوائد والرموز الغريبة */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebarNav"], .st-emotion-cache-6qob1r {{
        display: none !important;
    }}
    
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: rtl; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* المربع الشفاف للعنوان */
    .glass-header {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }}

    /* المربع الشفاف للبيانات */
    .glass-card {{
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }}

    input {{ background-color: white !important; color: black !important; font-weight: bold !important; border-radius: 10px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    st.session_state.bg_choice = st.selectbox("تغيير الخلفية", list(WALLPAPERS.keys()))
    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="glass-header" style="margin-top:100px;"><h1>🏛️ بوابة المسار الذهبي</h1></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        u = st.text_input("المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if u == "ALI FETORY" and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- الواجهة الرئيسية ---
st.markdown('<div class="glass-header"><h1>🌍 بوابة المسار الذهبي</h1></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📥 سحب ومعالجة البيانات")
    
    col_file, col_btn = st.columns([3, 1])
    file = col_file.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
    
    if file and st.button("⚡ مسح"):
        img = Image.open(file)
        res = ocr_reader.readtext(np.array(img))
        st.session_state.data = {"sn": res[0][1].upper(), "fn": res[1][1].upper(), "pno": "P12345678"}
        st.rerun()

    st.divider()
    
    c1, c2 = st.columns(2)
    sn = c1.text_input("اللقب", value=st.session_state.data["sn"])
    fn = c1.text_input("الاسم", value=st.session_state.data["fn"])
    pno = c2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = c2.text_input("المهنة")

    if st.button("🔥 طباعة النموذج", use_container_width=True):
        st.success("تم التجهيز!")
    st.markdown('</div>', unsafe_allow_html=True)
