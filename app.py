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
    "مودرن (أزرق)": "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop",
    "احترافي (مكتب)": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop",
    "فخم (خشب)": "https://images.unsplash.com/photo-1499914485622-a88fac536970?q=80&w=2070&auto=format&fit=crop",
    "هادئ (طبيعة)": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070&auto=format&fit=crop",
    "تقني (شبكات)": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"
}

# --- الدخول ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- شريط التحكم الجانبي ---
with st.sidebar:
    st.header("🎨 تخصيص المظهر")
    bg_choice = st.selectbox("اختر الخلفية المفضلة:", list(WALLPAPERS.keys()))
    selected_bg = WALLPAPERS[bg_choice]
    st.divider()
    st.caption(f"المستخدم: {ADMIN_U}")

# --- تطبيق الستايل الاحترافي (Glass UI) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{selected_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* تصميم البطاقات الزجاجية الشفافة */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    h1, h2, h3 {{ color: #0F172A !important; font-weight: 800 !important; }}
    input, .stSelectbox div {{ border-radius: 12px !important; border: 1px solid #CBD5E1 !important; }}
    .stButton>button {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 3em;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    st.title("🏛️ دخول المسار الذهبي")
    u = st.text_input("المستخدم").upper()
    p = st.text_input("الكلمة السرية", type="password")
    if st.button("تسجيل الدخول", use_container_width=True):
        if u == ADMIN_U and p == ADMIN_P:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- محتوى المنظومة ---
st.title("🌐 منظومة التأشيرات الاحترافية")

if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

# 1. القراءة
with st.container():
    st.markdown("### 📸 الخطوة 1: مسح الجواز")
    c_a, c_b = st.columns([1, 2])
    target = c_a.selectbox("الوجهة", ["italy", "france", "germany"])
    file = c_b.file_uploader("ارفع صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    if file and st.button("⚡ قراءة ذكية"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        text = [r[1].upper() for r in res]
        st.session_state.data.update({"sn": text[0] if len(text)>0 else "", "fn": text[1] if len(text)>1 else ""})
        for t in text:
            clean = t.replace(" ","")
            if len(clean) == 9 and clean.startswith('P'): st.session_state.data["pno"] = clean
        st.rerun()

# 2. البيانات
with st.container():
    st.markdown("### 📝 الخطوة 2: المراجعة")
    col1, col2 = st.columns(2)
    sn = col1.text_input("اللقب", value=st.session_state.data["sn"])
    fn = col1.text_input("الاسم", value=st.session_state.data["fn"])
    pno = col2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = col2.text_input("المهنة")
    mother = col1.text_input("اسم الأم")
    gender = col2.selectbox("الجنس", ["Male", "Female"])

# 3. الطباعة
if st.button("🖨️ إصدار النموذج المطبوع", use_container_width=True):
    try:
        pdf = PdfReader(f"{target}.pdf")
        out, pkt = PdfWriter(), io.BytesIO()
        can = canvas.Canvas(pkt)
        can.setFont("Helvetica-Bold", 10)
        # إحداثيات تعبئة النموذج
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
        st.download_button("✅ تحميل الملف الجاهز", final.getvalue(), f"{target}_final.pdf", use_container_width=True)
    except: st.error("تأكد من وجود ملف PDF الدولة المختارة")
