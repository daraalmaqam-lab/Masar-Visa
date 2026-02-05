import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- مكتبة الثيمات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# --- 🎨 الستايل الاحترافي (حذف الشوائب والمربعات السوداء) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* 1. إخفاء شريط Fork وكل الأيقونات والرموز الغريبة نهائياً */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], 
    .st-emotion-cache-6qob1r, .st-emotion-cache-1kyx738, button[title="View source"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: rtl; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* 2. مربع شفاف للعنوان (بدون سواد) */
    .glass-header {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        color: white;
    }}

    /* 3. مربع شفاف للبيانات */
    .glass-box {{
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }}

    /* تحسين شكل المدخلات وحذف أي ظلال غريبة */
    input {{ 
        background-color: white !important; 
        color: black !important; 
        border: none !important; 
        border-radius: 8px !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (نظيفة جداً) ---
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    st.session_state.bg_choice = st.selectbox("تغيير الخلفية", list(WALLPAPERS.keys()))
    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="glass-header"><h1>🏛️ بوابة المسار الذهبي</h1></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if (u == "ALI FETORY" or u == "ALI") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- الواجهة الرئيسية للعمل ---
st.markdown('<div class="glass-header"><h1>🌍 بوابة المسار الذهبي</h1></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("📥 معالجة الجواز")
    
    file = st.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    if file and st.button("⚡ قراءة ذكية"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        st.session_state.data["sn"] = res[0][1].upper() if len(res) > 0 else ""
        st.session_state.data["fn"] = res[1][1].upper() if len(res) > 1 else ""
        st.rerun()

    st.divider()
    
    c1, c2 = st.columns(2)
    sn = c1.text_input("اللقب", value=st.session_state.data["sn"])
    fn = c1.text_input("الاسم", value=st.session_state.data["fn"])
    pno = c2.text_input("رقم الجواز")
    job = c2.text_input("المهنة")

    if st.button("🔥 طباعة النموذج", use_container_width=True):
        st.success("جاهز للتحميل!")
    st.markdown('</div>', unsafe_allow_html=True)
