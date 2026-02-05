import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- خيارات الخلفيات ---
WALLPAPERS = {
    "احترافي (باريس)": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073&auto=format&fit=crop",
    "مودرن (تقني)": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop",
    "فخم (مكتب)": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop"
}

# --- بيانات الدخول ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل الاحترافي الزجاجي (بدون مربعات زائدة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Inter', sans-serif !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', 'احترافي (باريس)')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* تصميم الشريط الجانبي */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(15px);
    }}

    /* تصميم البطاقات الزجاجية للشاشات */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(15, 23, 42, 0.65) !important; /* خلفية داكنة شفافة فخمة */
        backdrop-filter: blur(15px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }}

    h1, h2, h3 {{ color: white !important; font-weight: 800 !important; }}
    label, p {{ color: #E2E8F0 !important; font-weight: 600 !important; }}

    /* الخانات (نظيفة بدون خلفية بيضاء تشتت العين) */
    input {{
        background-color: rgba(255, 255, 255, 0.9) !important; 
        color: #0F172A !important;
        border-radius: 10px !important; border: none !important;
        padding: 12px !important; font-weight: 700 !important;
    }}

    /* الأزرار */
    .stButton>button {{
        background: #3B82F6 !important; color: white !important;
        border-radius: 10px !important; padding: 12px;
        font-weight: 800 !important; text-transform: uppercase;
        border: none !important; width: 100%; transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: translateY(-2px); background: #2563EB !important; }}

    /* إخفاء الشوائب */
    #MainMenu, footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- الجانب ---
with st.sidebar:
    st.markdown("### ⚙️ SETTINGS")
    bg_choice = st.selectbox("Background Theme:", list(WALLPAPERS.keys()), key='bg_choice')
    st.divider()
    if st.button("LOGOUT"):
        st.session_state.auth = False
        st.rerun()

# --- الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>🏛️ GOLDEN PATH</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("USER NAME").upper()
        p = st.text_input("PASSWORD", type="password")
        if st.button("LOGIN"):
            if u == ADMIN_U and p == ADMIN_P:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center;'>🌍 GLOBAL VISA GATEWAY</h1>", unsafe_allow_html=True)

if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# الشاشة 1: استيراد البيانات
with st.container():
    st.markdown("### 📥 1. DATA IMPORT")
    c1, c2 = st.columns([1, 2])
    target = c1.selectbox("Target Country", ["italy", "france", "germany"])
    file = c2.file_uploader("Upload Passport Scan", type=['jpg', 'png', 'jpeg'])
    if file and st.button("⚡ AI AUTO-SCAN"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        text = [r[1].upper() for r in res]
        st.session_state.data.update({"sn": text[0] if len(text)>0 else "", "fn": text[1] if len(text)>1 else ""})
        for t in text:
            cl = t.replace(" ","")
            if len(cl)==9 and cl.startswith('P'): st.session_state.data["pno"] = cl
        st.rerun()

# الشاشة 2: مراجعة النموذج
with st.container():
    st.markdown("### 📝 2. VERIFICATION")
    col1, col2 = st.columns(2)
    sn = col1.text_input("Surname", value=st.session_state.data["sn"])
    fn = col1.text_input("First Name", value=st.session_state.data["fn"])
    pno = col2.text_input("Passport No.", value=st.session_state.data["pno"])
    job = col2.text_input("Occupation")
    mother = col1.text_input("Mother's Name")
    gender = col2.selectbox("Gender", ["Male", "Female"])

# الشاشة 3: الطباعة
if st.button("✨ GENERATE FINAL DOCUMENT", use_container_width=True):
    try:
        pdf = PdfReader(f"{target}.pdf")
        out, pkt = PdfWriter(), io.BytesIO()
        can = canvas.Canvas(pkt)
        can.setFont("Helvetica-Bold", 10)
        # الإحداثيات
        can.drawString(110, 715, sn); can.drawString(110, 687, fn)
        can.drawString(110, 659, pno); can.drawString(110, 631, mother)
        can.drawString(110, 603, job)
        can.save(); pkt.seek(0)
        page = pdf.pages[0]
        page.merge_page(PdfReader(pkt).pages[0])
        out.add_page(page)
        for i in range(1, len(pdf.pages)): out.add_page(pdf.pages[i])
        final = io.BytesIO(); out.write(final)
        st.download_button("📥 DOWNLOAD PDF", final.getvalue(), f"{target}_visa.pdf", use_container_width=True)
    except: st.error("PDF Missing!")
