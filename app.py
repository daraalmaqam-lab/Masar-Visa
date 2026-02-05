import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- خيارات الخلفيات الاحترافية ---
WALLPAPERS = {
    "احترافي (باريس)": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073&auto=format&fit=crop",
    "مودرن (تقني)": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop",
    "فخم (مكتب)": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop"
}

# --- الدخول ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- شريط التحكم الجانبي ---
with st.sidebar:
    st.markdown("### 🎨 تخصيص المظهر")
    bg_choice = st.selectbox("ثيم الخلفية:", list(WALLPAPERS.keys()))
    selected_bg = WALLPAPERS[bg_choice]
    st.divider()
    st.caption(f"👤 المستخدم المتصل: {ADMIN_U}")

# --- 🎨 الستايل الاحترافي (نفس شكل الصورة تماماً) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');

    /* تطبيق الخط على كامل المنظومة */
    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    .stApp {{
        background-image: url("{selected_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* تصميم البطاقات الزجاجية (نفس الصورة) */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }}

    /* العناوين الكبيرة والعريضة */
    h1, h2, h3 {{ 
        color: white !important; 
        font-weight: 800 !important; 
        text-transform: uppercase;
        letter-spacing: -1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}

    /* النصوص والتسميات */
    label, p {{ 
        color: white !important; 
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }}

    /* خانات الإدخال البيضاء والنظيفة */
    input {{
        background-color: white !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px !important;
        font-weight: 700 !important;
    }}

    /* تصميم الأزرار (Dark Blue & Bold) */
    .stButton>button {{
        background: #0F172A !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 25px !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        border: none !important;
        width: 100%;
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{
        transform: translateY(-3px);
        background: #1E293B !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }}

    /* تنظيف قائمة الاختيار */
    div[data-baseweb="select"] {{
        background-color: white !important;
        border-radius: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center;'>🏛️ GOLDEN PATH SYSTEM</h1>", unsafe_allow_html=True)
    u = st.text_input("USER").upper()
    p = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if u == ADMIN_U and p == ADMIN_P:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- محتوى المنظومة الاحترافي ---
st.markdown("<h1 style='text-align: center;'>🌐 GATEWAY TO GLOBAL VISAS</h1>", unsafe_allow_html=True)

if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# 1. قسم المسح
with st.container():
    st.markdown("### 🧳 1. IMPORT PASSPORT DATA")
    c_a, c_b = st.columns([1, 2])
    target = c_a.selectbox("Select Country", ["italy", "france", "germany"])
    file = c_b.file_uploader("Upload Passport Scan", type=['jpg', 'png', 'jpeg'])
    
    if file and st.button("⚡ READ PASSPORT DATA WITH AI"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        text = [r[1].upper() for r in res]
        st.session_state.data.update({"sn": text[0] if len(text)>0 else "", "fn": text[1] if len(text)>1 else ""})
        for t in text:
            clean = t.replace(" ","")
            if len(clean) == 9 and clean.startswith('P'): st.session_state.data["pno"] = clean
        st.rerun()

# 2. قسم المراجعة
with st.container():
    st.markdown("### 📝 2. REVIEW & EDIT DETAILS")
    col1, col2 = st.columns(2)
    sn = col1.text_input("Surname", value=st.session_state.data["sn"])
    fn = col1.text_input("First Name", value=st.session_state.data["fn"])
    pno = col2.text_input("Passport Number", value=st.session_state.data["pno"])
    job = col2.text_input("Occupation")
    mother = col1.text_input("Mother's Full Name")
    gender = col2.selectbox("Gender", ["Male", "Female"])

# 3. زر الإصدار
if st.button("✨ ISSUE FINAL VISA FORM", use_container_width=True):
    try:
        pdf = PdfReader(f"{target}.pdf")
        out, pkt = PdfWriter(), io.BytesIO()
        can = canvas.Canvas(pkt)
        can.setFont("Helvetica-Bold", 10)
        can.drawString(110, 715, sn); can.drawString(110, 687, fn)
        can.drawString(110, 659, pno); can.drawString(110, 631, mother)
        can.drawString(110, 603, job)
        can.save(); pkt.seek(0)
        
        page = pdf.pages[0]
        page.merge_page(PdfReader(pkt).pages[0])
        out.add_page(page)
        for i in range(1, len(pdf.pages)): out.add_page(pdf.pages[i])
        
        final = io.BytesIO()
        out.write(final)
        st.download_button("📥 DOWNLOAD READY PDF", final.getvalue(), f"{target}_final.pdf", use_container_width=True)
    except: st.error("Error: Make sure the base PDF file exists.")
