import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- مكتبة الثيمات السياحية الـ 14 ---
WALLPAPERS = {
    "🌆 باريس (فرنسا)": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما (إيطاليا)": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🎡 لندن (بريطانيا)": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070",
    "🕌 اسطنبول (تركيا)": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2071",
    "🗼 طوكيو (اليابان)": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974",
    "🏙️ دبي (الإمارات)": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🏖️ جزر المالديف": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=1965",
    "⛰️ سويسرا (الألب)": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=2070",
    "🗽 نيويورك (أمريكا)": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=2070",
    "🏜️ الأهرامات (مصر)": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?q=80&w=2070",
    "🏮 سور الصين العظيم": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?q=80&w=2070",
    "🕌 مراكش (المغرب)": "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?q=80&w=2071",
    "🌊 سانتوريني (اليونان)": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2022",
    "🌉 سان فرانسيسكو": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?q=80&w=2070"
}

# --- بيانات الدخول الخاصة بك يا علي ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل الملكي (Glass UI + No Cursors) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس (فرنسا)')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* إخفاء المربع الأبيض ومؤشر البحث */
    .block-container {{ padding-top: 1rem !important; max-width: 950px !important; background: transparent !important; }}
    
    div[data-baseweb="select"] input {{ 
        caret-color: transparent !important; 
        cursor: pointer !important;
        text-shadow: 0 0 0 white !important;
        color: transparent !important;
    }}

    /* إلغاء أي إطارات عند الضغط */
    div[data-baseweb="select"], div[data-baseweb="select"] > div {{
        border: none !important; outline: none !important; box-shadow: none !important;
    }}

    /* تصميم البطاقات الزجاجية الشفافة */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(20px);
        padding: 35px; border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 45px rgba(0,0,0,0.6);
        margin-bottom: 20px;
    }}

    h1, h2, h3 {{ color: #FFFFFF !important; font-weight: 900 !important; text-align: center; text-transform: uppercase; }}
    label {{ color: #F8FAFC !important; font-size: 1rem !important; font-weight: 700 !important; }}

    input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #1E293B !important; border-radius: 12px !important;
        padding: 12px !important; font-weight: 700 !important; border: none !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important; border-radius: 12px !important;
        font-weight: 800 !important; border: none !important; width: 100%; height: 3.5em;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(10px);
    }}

    #MainMenu, footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- الجانب (لوحة التحكم) ---
with st.sidebar:
    st.markdown("### 🗺️ وجهات المسار الذهبي")
    bg_choice = st.selectbox("اختر ثيم الرحلة:", list(WALLPAPERS.keys()), key='bg_choice')
    st.divider()
    st.markdown(f"👤 **المسؤول:** {ADMIN_U}")
    if st.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='margin-top: 80px;'>🏛️ المسار الذهبي للسفر</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول النظام"):
            if u == ADMIN_U and p == ADMIN_P:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- الواجهة الرئيسية ---
st.markdown("<h1>🌍 منظومة التأشيرات العالمية</h1>", unsafe_allow_html=True)
if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

with st.container():
    st.markdown("### 📸 1. سحب بيانات الجواز")
    c1, c2 = st.columns([1, 2])
    target = c1.selectbox("دولة التأشيرة", ["italy", "france", "germany"])
    file = c2.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    if file and st.button("⚡ قراءة ذكية بالذكاء الاصطناعي"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        text = [r[1].upper() for r in res]
        st.session_state.data.update({"sn": text[0] if len(text)>0 else "", "fn": text[1] if len(text)>1 else ""})
        for t in text:
            cl = t.replace(" ","")
            if len(cl)==9 and cl.startswith('P'): st.session_state.data["pno"] = cl
        st.rerun()

with st.container():
    st.markdown("### 📝 2. مراجعة بيانات النموذج")
    col1, col2 = st.columns(2)
    sn = col1.text_input("اللقب (Surname)", value=st.session_state.data["sn"])
    fn = col1.text_input("الاسم (First Name)", value=st.session_state.data["fn"])
    pno = col2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = col2.text_input("المهنة")
    mother = col1.text_input("اسم الأم بالكامل")
    gender = col2.selectbox("الجنس", ["Male", "Female"])

if st.button("🖨️ إصدار وطباعة النموذج النهائي", use_container_width=True):
    try:
        pdf = PdfReader(f"{target}.pdf")
        out, pkt = PdfWriter(), io.BytesIO()
        can = canvas.Canvas(pkt); can.setFont("Helvetica-Bold", 10)
        can.drawString(110, 715, sn); can.drawString(110, 687, fn)
        can.drawString(110, 659, pno); can.drawString(110, 631, mother)
        can.drawString(110, 603, job); can.save(); pkt.seek(0)
        page = pdf.pages[0]; page.merge_page(PdfReader(pkt).pages[0])
        out.add_page(page)
        for i in range(1, len(pdf.pages)): out.add_page(pdf.pages[i])
        final = io.BytesIO(); out.write(final)
        st.download_button("📥 تحميل الملف الجاهز للطباعة", final.getvalue(), f"{target}_final.pdf", use_container_width=True)
    except: st.error("خطأ: ملف النموذج الأساسي غير موجود!")
