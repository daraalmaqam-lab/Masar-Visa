import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- الدخول ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🏛️ GOLDEN PATH")
    u, p = st.text_input("المستخدم").upper(), st.text_input("الرقم السري", type="password")
    if st.button("دخول", use_container_width=True):
        if u == ADMIN_U and p == ADMIN_P:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 🎨 الستايل (Modern & Clean) ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F5F9; }
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px;
    }
    .stButton>button { background: #0F172A !important; color: white !important; border-radius: 8px !important; font-weight: bold; }
    input { border-radius: 8px !important; background: #F8FAFC !important; }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

st.title("📑 منظومة التأشيرات")

# --- 1. القراءة ---
with st.container():
    st.markdown("### 📸 سحب البيانات")
    target = st.selectbox("الدولة", ["italy", "france", "germany"])
    file = st.file_uploader("صورة الجواز", type=['jpg', 'png', 'jpeg'])
    if file and st.button("⚡ قراءة تلقائية"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        text = [r[1].upper() for r in res]
        st.session_state.data.update({"sn": text[0] if len(text)>0 else "", "fn": text[1] if len(text)>1 else ""})
        for t in text:
            if len(t.replace(" ","")) == 9 and t.replace(" ","").startswith('P'):
                st.session_state.data["pno"] = t.replace(" ","")
        st.rerun()

# --- 2. المراجعة ---
with st.container():
    st.markdown("### 📝 البيانات")
    c1, c2 = st.columns(2)
    sn = c1.text_input("اللقب", value=st.session_state.data["sn"])
    fn = c1.text_input("الاسم", value=st.session_state.data["fn"])
    pno = c2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = c2.text_input("المهنة")
    mother = c1.text_input("الأم")
    gender = c2.selectbox("الجنس", ["Male", "Female"])

# --- 3. الطباعة ---
if st.button("🖨️ طباعة النموذج", use_container_width=True):
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
        
        final = io.BytesIO()
        out.write(final)
        st.download_button("📥 تحميل الملف", final.getvalue(), f"{target}_visa.pdf", use_container_width=True)
    except: st.error("تأكد من وجود ملف الـ PDF")
