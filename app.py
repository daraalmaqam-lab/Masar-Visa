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

# --- بيانات الدخول ---
ADMIN_USER, ADMIN_PASS = "ALI FETORY", "0925843353"

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🏛️ المسار الذهبي</h2>", unsafe_allow_html=True)
    u_name = st.text_input("اسم المستخدم").upper().strip()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("دخول"):
        if u_name == ADMIN_USER and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 🎨 لوحة تحكم الألوان (تم تصحيح الخطأ البرمجي هنا) ---
with st.sidebar:
    st.header("🎨 إعدادات المظهر")
    bg_color = st.color_picker("لون الخلفية", "#FFFFFF")
    text_color = st.color_picker("لون النص والعناوين", "#1F2937")
    input_bg = st.color_picker("لون خانات الكتابة", "#F3F4F6")
    btn_color = st.color_picker("لون الأزرار", "#374151")

# --- 🛠️ التنسيق لإزالة الخطوط والتداخل ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; }}
    h1, h2, h3, p, label, .stMarkdown {{ color: {text_color} !important; font-weight: bold !important; }}
    
    /* تنظيف خانات الإدخال */
    input {{ 
        color: #000000 !important; 
        background-color: {input_bg} !important; 
        border: 1px solid #D1D5DB !important;
        border-radius: 5px !important;
    }}

    /* إزالة الخط المزعج في قائمة الاختيار (الجنس) */
    div[data-baseweb="select"] {{
        background-color: {input_bg} !important;
        border: none !important;
    }}
    
    div[data-baseweb="select"] > div {{
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }}

    .stButton>button {{ 
        background-color: {btn_color} !important; 
        color: white !important; 
        border-radius: 5px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = {"sn": "", "fn": "", "pno": ""}

st.title("⚖️ منظومة المسار الذهبي")

# --- 1. قسم الجواز ---
st.subheader("📸 1. بيانات الجواز")
target_country = st.selectbox("وجهة السفر:", ["italy", "france", "germany"])
uploaded_file = st.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])

if uploaded_file and st.button("🔍 قراءة بيانات الجواز"):
    with st.spinner("جاري المسح..."):
        img = Image.open(uploaded_file)
        result = ocr_reader.readtext(np.array(img))
        text_list = [res[1].upper() for res in result]
        
        st.session_state.data["sn"] = text_list[0] if len(text_list) > 0 else ""
        st.session_state.data["fn"] = text_list[1] if len(text_list) > 1 else ""
        
        found_pno = ""
        for t in text_list:
            clean_t = t.replace(" ", "")
            if len(clean_t) == 9 and clean_t.startswith('P'):
                found_pno = clean_t
                break
        st.session_state.data["pno"] = found_pno
        st.rerun()

st.markdown("---")

# --- 2. قسم التعبئة ---
st.subheader("✍️ 2. مراجعة وتعبئة البيانات")
col1, col2 = st.columns(2)

with col1:
    sn = st.text_input("اللقب", value=st.session_state.data["sn"])
    fn = st.text_input("اسم الشخص", value=st.session_state.data["fn"])
    job = st.text_input("المهنة الحالية")

with col2:
    pno = st.text_input("رقم وثيقة السفر", value=st.session_state.data["pno"])
    mother = st.text_input("اسم الأم بالكامل")
    gender = st.selectbox("الجنس المختارة:", ["Male", "Female"])

st.markdown("---")

# --- 3. زر الطباعة ---
if st.button("🖨️ طباعة نموذج التأشيرة", use_container_width=True):
    try:
        existing_pdf = PdfReader(f"{target_country}.pdf")
        output = PdfWriter()
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        can.setFont("Helvetica-Bold", 10)
        
        # الإحداثيات التلقائية
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
        st.download_button("📥 اضغط للتحميل الآن", res_file.getvalue(), f"{target_country}_final.pdf", use_container_width=True)
    except Exception as e:
        st.error(f"تأكد من وجود ملف {target_country}.pdf في المستودع")
