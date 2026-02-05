import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- مكتبة الثيمات الـ 14 ---
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

# --- نصوص اللغات ---
LANGS = {
    "العربية": {"dir": "rtl", "title": "بوابة المسار الذهبي", "user": "المستخدم", "pass": "كلمة المرور", "login": "دخول", "settings": "إعدادات"},
    "English": {"dir": "ltr", "title": "Golden Path Gateway", "user": "Username", "pass": "Password", "login": "Login", "settings": "Settings"}
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}
cur_l = LANGS[st.session_state.lang]

# --- 🎨 الستايل النهائي (حل مشكلة المربعات والـ Fork) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: {cur_l['dir']}; }}
    
    /* إخفاء Fork و footer */
    header, footer, .stAppDeployButton, [data-testid="stStatusWidget"] {{ visibility: hidden !important; height: 0 !important; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.get('bg_choice', '🌆 باريس')]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* إخفاء المربع الأبيض (المؤشر) في القوائم */
    input[role="combobox"] {{ caret-color: transparent !important; color: transparent !important; text-shadow: 0 0 0 white !important; }}
    div[data-baseweb="select"] {{ border: none !important; box-shadow: none !important; background: rgba(255,255,255,0.1) !important; }}

    /* البطاقات الزجاجية */
    .glass-card {{
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(20px);
        padding: 25px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown(f"<h1 style='color:white; text-align:center; padding-top:50px;'>🏛️ {cur_l['title']}</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        u = st.text_input(cur_l['user']).upper()
        p = st.text_input(cur_l['pass'], type="password")
        if st.button(cur_l['login']):
            if u == "ALI FETORY" and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### ⚙️ {cur_l['settings']}")
    st.session_state.lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)
    st.session_state.bg_choice = st.selectbox("🎨 الثيم", list(WALLPAPERS.keys()))
    if st.button("Logout | خروج"):
        st.session_state.auth = False
        st.rerun()

# --- الواجهة الرئيسية (النموذج اللي كان مختفي) ---
st.markdown(f"<h1 style='color:white; text-align:center;'>{cur_l['title']}</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📸 1. سحب بيانات الجواز")
    col_a, col_b = st.columns([1, 2])
    target_country = col_a.radio("الوجهة:", ["italy", "france", "germany"])
    uploaded_file = col_b.file_uploader("ارفع صورة الجواز هنا", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file and st.button("⚡ بدء المسح الضوئي"):
        with st.spinner('جاري القراءة...'):
            img = Image.open(uploaded_file)
            res = ocr_reader.readtext(np.array(img))
            text = [r[1].upper() for r in res]
            # استخراج ذكي
            st.session_state.data["sn"] = text[0] if len(text) > 0 else ""
            st.session_state.data["fn"] = text[1] if len(text) > 1 else ""
            for t in text:
                clean_t = t.replace(" ", "")
                if len(clean_t) == 9 and clean_t.startswith('P'):
                    st.session_state.data["pno"] = clean_t
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📝 2. مراجعة البيانات")
    c1, c2 = st.columns(2)
    final_sn = c1.text_input("اللقب", value=st.session_state.data["sn"])
    final_fn = c1.text_input("الاسم", value=st.session_state.data["fn"])
    final_pno = c2.text_input("رقم الجواز", value=st.session_state.data["pno"])
    job = c2.text_input("المهنة")
    
    if st.button("✨ إصدار ملف PDF المعبأ", use_container_width=True):
        try:
            pdf_path = f"{target_country}.pdf"
            existing_pdf = PdfReader(pdf_path)
            output = PdfWriter()
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            can.setFont("Helvetica-Bold", 11)
            # إحداثيات افتراضية (عدلها حسب ملفك)
            can.drawString(100, 700, final_sn)
            can.drawString(100, 680, final_fn)
            can.drawString(100, 660, final_pno)
            can.save()
            packet.seek(0)
            new_pdf = PdfReader(packet)
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)
            for i in range(1, len(existing_pdf.pages)): output.add_page(existing_pdf.pages[i])
            
            final_buffer = io.BytesIO()
            output.write(final_buffer)
            st.download_button("📥 تحميل طلب التأشيرة", final_buffer.getvalue(), f"{final_sn}_visa.pdf")
        except Exception as e:
            st.error(f"تأكد من وجود ملف {target_country}.pdf في المجلد")
    st.markdown('</div>', unsafe_allow_html=True)
