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
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #1E293B; font-family: sans-serif;'>🏛️ GOLDEN PATH</h1>
            <p style='color: #64748B;'>منظومة المسار الذهبي للتأشيرات</p>
        </div>
    """, unsafe_allow_html=True)
    u_name = st.text_input("اسم المستخدم").upper().strip()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("تسجيل الدخول", use_container_width=True):
        if u_name == ADMIN_USER and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 🎨 الستايل الاحترافي (CSS) ---
st.markdown("""
    <style>
    /* خلفية النظام */
    .stApp { background-color: #F1F5F9 !important; }
    
    /* تنسيق العناوين */
    h1, h2, h3 { color: #0F172A !important; font-family: 'Inter', sans-serif !important; letter-spacing: -0.5px; }
    
    /* تصميم البطاقات (Containers) */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    
    /* الخانات (Inputs) */
    input {
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-size: 16px !important;
    }
    input:focus { border-color: #3B82F6 !important; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important; }

    /* الأزرار الاحترافية */
    .stButton>button {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* إخفاء العلامات الزائدة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# --- واجهة المنظومة ---
st.title("📑 معالج النماذج القنصلية")

# القسم الأول: رفع البيانات
with st.container():
    st.markdown("### 🛃 الخطوة 1: استيراد البيانات")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        target_country = st.selectbox("الدولة المستهدفة", ["italy", "france", "germany"])
    with col_b:
        uploaded_file = st.file_uploader("قم بسحب صورة الجواز هنا", type=['jpg', 'png', 'jpeg'])

    if uploaded_file and st.button("⚡ قراءة الجواز بالذكاء الاصطناعي"):
        with st.spinner("جاري المعالجة..."):
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

# القسم الثاني: المراجعة
with st.container():
    st.markdown("### 📝 الخطوة 2: مراجعة البيانات")
    c1, c2 = st.columns(2)
    with c1:
        sn = st.text_input("اللقب الرسمي", value=st.session_state.data["sn"])
        fn = st.text_input("الاسم الأول", value=st.session_state.data["fn"])
        job = st.text_input("المهنة / الوظيفة")
    with c2:
        pno = st.text_input("رقم وثيقة السفر", value=st.session_state.data["pno"])
        mother = st.text_input("اسم الأم")
        gender = st.selectbox("الجنس", ["Male", "Female"])

# القسم الثالث: الطباعة
if st.button("🖨️ إصدار النموذج النهائي"):
    try:
        existing_pdf = PdfReader(f"{target_country}.pdf")
        output = PdfWriter()
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        can.setFont("Helvetica-Bold", 10)
        
        # إحداثيات الطباعة
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
        st.download_button("📥 تحميل الملف الجاهز للطباعة", res_file.getvalue(), f"{target_country}_final.pdf", use_container_width=True)
    except Exception as e:
        st.error(f"تأكد من وجود ملف {target_country}.pdf في المستودع")

st.sidebar.markdown(f"**نظام المسار الذهبي v2.0**")
st.sidebar.caption(f"مرحباً، {ADMIN_USER}")
