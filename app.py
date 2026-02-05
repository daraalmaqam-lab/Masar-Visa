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

# --- بيانات الدخول الخاصة بعلي الفيتوري ---
ADMIN_USER, ADMIN_PASS = "ALI FETORY", "0925843353"

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏛️ المسار الذهبي - دخول</h2>", unsafe_allow_html=True)
    u_name = st.text_input("اسم المستخدم").upper().strip()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("دخول للمنظومة", use_container_width=True):
        if u_name == ADMIN_USER and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 🛠️ تعديل الألوان ليكون النص واضحاً جداً ---
st.markdown("""
    <style>
    /* خلفية التطبيق بيضاء مريحة */
    .stApp { background-color: #FFFFFF; }
    
    /* جعل خانات الكتابة بيضاء والنص داخلها أسود */
    input { color: #000000 !important; background-color: #FFFFFF !important; border: 1px solid #D1D5DB !important; }
    
    /* تعديل لون العناوين */
    h1, h2, h3, p, label { color: #1E3A8A !important; font-weight: bold; }
    
    /* زر الطباعة - أزرق واضح */
    .stButton>button { 
        background-color: #1E3A8A !important; 
        color: white !important; 
        border-radius: 8px; 
        padding: 10px;
        font-size: 18px;
    }
    
    /* خانات الاختيار */
    .stSelectbox div { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📑 معالج نماذج التأشيرات")

# --- تخزين البيانات ---
if 'data' not in st.session_state:
    st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# --- القسم الأول: الجواز ---
st.markdown("### 1️⃣ بيانات الجواز")
target_country = st.selectbox("اختر وجهة السفر:", ["italy", "france", "germany"])
uploaded_file = st.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])

if uploaded_file and st.button("🔍 قراءة الجواز"):
    with st.spinner("جاري سحب البيانات..."):
        img = Image.open(uploaded_file)
        result = ocr_reader.readtext(np.array(img))
        text = " ".join([res[1].upper() for res in result])
        st.session_state.data["sn"] = result[0][1] if len(result) > 0 else ""
        st.session_state.data["fn"] = result[1][1] if len(result) > 1 else ""
        st.session_state.data["pno"] = [t for t in text.split() if len(t) == 9 and t.startswith('P')][0] if 'P' in text else ""
        st.rerun()

st.markdown("---")

# --- القسم الثاني: البيانات التكميلية ---
st.markdown("### 2️⃣ مراجعة وتكملة البيانات")
col1, col2 = st.columns(2)

with col1:
    sn = st.text_input("اللقب (Surname)", value=st.session_state.data["sn"])
    fn = st.text_input("الاسم (First Name)", value=st.session_state.data["fn"])
    gender = st.selectbox("الجنس:", ["Male", "Female"])

with col2:
    pno = st.text_input("رقم الجواز", value=st.session_state.data["pno"])
    mother = st.text_input("اسم الأم")
    job = st.text_input("المهنة")

st.markdown("---")

# --- الزر المختصر ---
if st.button("🖨️ طباعة النموذج", use_container_width=True):
    try:
        existing_pdf = PdfReader(f"{target_country}.pdf")
        output = PdfWriter()
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        
        # إحداثيات الطباعة (X, Y)
        x, y = 110, 715
        can.setFont("Helvetica-Bold", 10)
        can.drawString(x, y, sn)
        can.drawString(x, y - 28, fn)
        can.drawString(x, y - 56, pno)
        can.drawString(x, y - 84, mother)
        can.drawString(x, y - 112, job)
        
        can.save()
        packet.seek(0)
        
        new_pdf = PdfReader(packet)
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        
        for i in range(1, len(existing_pdf.pages)): 
            output.add_page(existing_pdf.pages[i])
        
        res_file = io.BytesIO()
        output.write(res_file)
        
        st.download_button("📥 تحميل الملف المطبوع", res_file.getvalue(), f"{target_country}_final.pdf", use_container_width=True)
    except Exception as e:
        st.error(f"خطأ: تأكد من وجود ملف {target_country}.pdf")

st.sidebar.info(f"المستخدم المتصل: {ADMIN_USER}")
