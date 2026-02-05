import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import easyocr
import numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

ocr_reader = load_reader()

# --- الدخول ---
ADMIN_USER, ADMIN_PASS = "ALI FETORY", "0925843353"

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏛️ المسار الذهبي - تسجيل الدخول</h2>", unsafe_allow_html=True)
    u_name = st.text_input("اسم المستخدم").upper().strip()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("دخول", use_container_width=True):
        if u_name == ADMIN_USER and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 🎨 التنسيق الجديد (ألوان مريحة وعملية) ---
st.markdown("""
    <style>
    /* جعل الخلفية بيضاء بالكامل */
    .stApp { background-color: #FFFFFF !important; }
    
    /* جعل النصوص واضحة باللون الأسود */
    p, label, .stMarkdown { color: #1F2937 !important; font-weight: 500 !important; }
    
    /* تنسيق خانات الإدخال: خلفية بيضاء، نص أسود، إطار رمادي */
    input { 
        color: #000000 !important; 
        background-color: #F9FAFB !important; 
        border: 2px solid #E5E7EB !important;
        border-radius: 8px !important;
    }

    /* زر الطباعة - أزرق احترافي */
    .stButton>button { 
        background-color: #2563EB !important; 
        color: white !important; 
        border: none !important;
        padding: 12px !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ منظومة المسار الذهبي")

if 'data' not in st.session_state:
    st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# --- القسم الأول ---
st.subheader("📸 1. بيانات الجواز")
target_country = st.selectbox("وجهة السفر:", ["italy", "france", "germany"])
uploaded_file = st.file_uploader("ارفع الصورة هنا", type=['jpg', 'png', 'jpeg'])

if uploaded_file and st.button("🔍 قراءة بيانات الجواز"):
    with st.spinner("جاري المسح..."):
        img = Image.open(uploaded_file)
        result = ocr_reader.readtext(np.array(img))
        text = " ".join([res[1].upper() for res in result])
        st.session_state.data["sn"] = result[0][1] if len(result) > 0 else ""
        st.session_state.data["fn"] = result[1][1] if len(result) > 1 else ""
        st.session_state.data["pno"] = [t for t in text.split() if len(t) == 9 and t.startswith('P')][0] if 'P' in text else ""
        st.rerun()

st.markdown("---")

# --- القسم الثاني ---
st.subheader("✍️ 2. مراجعة وتعبئة البيانات")
col1, col2 = st.columns(2)

with col1:
    sn = st.text_input("اللقب", value=st.session_state.data["sn"])
    fn = st.text_input("الاسم", value=st.session_state.data["fn"])
    job = st.text_input("المهنة")

with col2:
    pno = st.text_input("رقم الجواز", value=st.session_state.data["pno"])
    mother = st.text_input("اسم الأم")
    gender = st.selectbox("الجنس:", ["Male", "Female"])

st.markdown("---")

# --- الزر النهائي ---
if st.button("🖨️ طباعة النموذج النهائي", use_container_width=True):
    try:
        existing_pdf = PdfReader(f"{target_country}.pdf")
        output = PdfWriter()
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        
        # الطباعة التلقائية (X, Y)
        can.setFont("Helvetica-Bold", 10)
        can.drawString(110, 715, sn)
        can.drawString(110, 687, fn)
        can.drawString(110, 659, pno)
        can.drawString(110, 631, mother)
        can.drawString(110, 603, job)
        
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        for i in range(1, len(existing_pdf.pages)): output.add_page(existing_pdf.pages[i])
        
        res_file = io.BytesIO()
        output.write(res_file)
        st.download_button("📥 جاهز! اضغط هنا للتحميل", res_file.getvalue(), f"{target_country}_visa.pdf", use_container_width=True)
    except Exception as e:
        st.error(f"تأكد من وجود ملف {target_country}.pdf في المستودع")
