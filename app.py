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
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🎡 لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070",
    "🕌 اسطنبول": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2071",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🏖️ المالديف": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=1965",
    "⛰️ سويسرا": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=2070",
    "🗽 نيويورك": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=2070",
    "🏜️ الأهرامات": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?q=80&w=2070",
    "🏮 سور الصين": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?q=80&w=2070",
    "🕌 مراكش": "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?q=80&w=2071",
    "🌊 سانتوريني": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2022",
    "🌉 سان فرانسيسكو": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?q=80&w=2070"
}

# --- بيانات الدخول ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل النهائي (إلغاء البحث نهائياً) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* إلغاء المربعات الافتراضية */
    .block-container {{ padding-top: 1rem !important; max-width: 950px !important; }}
    
    /* تصميم أزرار الاختيار بدلاً من قائمة البحث */
    div[data-testid="stMarkdownContainer"] p {{ color: white !important; font-weight: 700 !important; }}
    
    /* تصميم البطاقات الزجاجية */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(0, 0, 0, 0.65) !important;
        backdrop-filter: blur(25px);
        padding: 30px; border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }}

    /* تصميم المدخلات */
    input {{
        background-color: white !important; color: #0F172A !important;
        border-radius: 12px !important; font-weight: 700 !important; border: none !important;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #3B82F6, #2563EB) !important;
        color: white !important; border-radius: 12px !important;
        font-weight: 800 !important; border: none !important; width: 100%;
    }}

    /* إخفاء شعار المنصة */
    #MainMenu, footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='color:white; text-align:center; margin-top:100px;'>🏛️ المسار الذهبي</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("USER").upper()
        p = st.text_input("PASS", type="password")
        if st.button("دخول"):
            if u == ADMIN_U and p == ADMIN_P:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- الشريط الجانبي (تحويل القائمة لأزرار) ---
with st.sidebar:
    st.markdown("### 🎨 ثيم النظام")
    # استبدال قائمة البحث بأزرار اختيار راديو (Radio)
    st.session_state.bg_choice = st.radio("اختر الوجهة:", list(WALLPAPERS.keys()))
    st.divider()
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='color:white; text-align:center;'>🌍 منظومة التأشيرات</h1>", unsafe_allow_html=True)

if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

with st.container():
    st.markdown("### 📸 1. البيانات")
    col_a, col_b = st.columns([1, 2])
    # هنا استخدمنا أزرار Pills بدلاً من Selectbox لإلغاء البحث
    target = col_a.radio("الدولة:", ["italy", "france", "germany"], horizontal=True)
    file = col_b.file_uploader("صورة الجواز", type=['jpg', 'png', 'jpeg'])
    
    if file and st.button("⚡ مسح ذكي"):
        res = ocr_reader.readtext(np.array(Image.open(file)))
        text = [r[1].upper() for r in res]
        st.session_state.data.update({"sn": text[0] if len(text)>0 else "", "fn": text[1] if len(text)>1 else ""})
        for t in text:
            cl = t.replace(" ","")
            if len(cl)==9 and cl.startswith('P'): st.session_state.data["pno"] = cl
        st.rerun()

with st.container():
    st.markdown("### 📝 2. التحقق")
    c1, c2 = st.columns(2)
    sn = c1.text_input("اللقب", value=st.session_state.data["sn"])
    fn = c1.text_input("الاسم", value=st.session_state.data["fn"])
    pno = c2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = c2.text_input("المهنة")
    mother = c1.text_input("اسم الأم")
    # تم تغيير الجنس أيضاً لأزرار راديو لجمالية أكثر
    gender = c2.radio("الجنس:", ["Male", "Female"], horizontal=True)

if st.button("✨ طباعة النموذج", use_container_width=True):
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
        st.download_button("📥 تحميل الملف", final.getvalue(), f"{target}_visa.pdf", use_container_width=True)
    except: st.error("تأكد من وجود ملف الـ PDF الأصلي")
