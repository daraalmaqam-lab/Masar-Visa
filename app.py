import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io, easyocr, numpy as np
from PIL import Image
import random # لاستخدام خلفيات عشوائية

# قائمة بالخلفيات الاحترافية (يمكنك إضافة المزيد)
BACKGROUND_IMAGES = [
    "https://images.unsplash.com/photo-1542435503-956c469947f6?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1498050108023-c5249f4cd085?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1542831371-d10882be1e78?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
]

# اختيار خلفية عشوائية عند بدء التشغيل
selected_background = random.choice(BACKGROUND_IMAGES)

# إعداد قارئ الجوازات
@st.cache_resource
def load_reader(): return easyocr.Reader(['en'])
ocr_reader = load_reader()

# --- الدخول ---
ADMIN_U, ADMIN_P = "ALI FETORY", "0925843353"
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{selected_background}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .login-card {{
            background: rgba(255, 255, 255, 0.9); /* خلفية شفافة بيضاء */
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }}
        h1 {{ color: #0F172A !important; font-size: 3em; margin-bottom: 20px; }}
        input {{ border-radius: 8px !important; background: #F0F4F8 !important; border: 1px solid #CBD5E1 !important; padding: 12px; }}
        .stButton>button {{
            background: linear-gradient(135deg, #0F172A 0%, #334155 100%) !important;
            color: white !important; border-radius: 8px !important; font-weight: bold; padding: 12px;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }}
        </style>
        <div class="login-card">
            <h1 style='color: #0F172A;'>🏛️ المسار الذهبي</h1>
            <p style='color: #64748B; margin-bottom: 20px;'>سجل الدخول للمنظومة</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    u, p = st.text_input("اسم المستخدم", key="login_user").upper(), st.text_input("الرقم السري", type="password", key="login_pass")
    if st.button("دخول", use_container_width=True, key="login_btn"):
        if u == ADMIN_U and p == ADMIN_P:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("اسم المستخدم أو الرقم السري غير صحيح!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 🎨 الستايل العام للمنظومة (Modern & Professional) ---
st.markdown(f"""
    <style>
    /* الخلفية الرئيسية للمنظومة */
    .stApp {{
        background-image: url("{selected_background}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed; /* لتثبيت الخلفية عند التمرير */
        background-repeat: no-repeat;
    }}
    /* صندوق المحتوى الرئيسي (البطاقات) */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background: rgba(255, 255, 255, 0.9); /* خلفية بيضاء شفافة قليلاً */
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        backdrop-filter: blur(5px); /* تأثير ضبابي على الخلفية */
    }}
    h1, h2, h3, .stMarkdown {{ color: #0F172A !important; font-family: 'Segoe UI', sans-serif !important; font-weight: 700; }}
    label, p, .stText {{ color: #334155 !important; font-family: 'Segoe UI', sans-serif !important; }}

    input, .stSelectbox div[data-baseweb="select"] {{
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-size: 16px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); /* ظل داخلي خفيف */
    }}
    input:focus, .stSelectbox div[data-baseweb="select"]:focus {{ border-color: #3B82F6 !important; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2); }}

    .stButton>button {{
        background: linear-gradient(135deg, #0F172A 0%, #334155 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        border: none;
    }}
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        background: linear-gradient(135deg, #334155 0%, #0F172A 100%) !important;
    }}
    .stSuccess, .stError {{ border-radius: 8px; font-weight: bold; }}
    /* إخفاء شريط Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state: st.session_state.data = {"sn": "", "fn": "", "pno": ""}

st.title("🌐 بوابة المسار الذهبي للتأشيرات")

# --- 1. قسم استيراد البيانات ---
with st.container():
    st.markdown("### 🧳 1. استيراد بيانات الجواز")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        target_country = st.selectbox("وجهة السفر", ["italy", "france", "germany"])
    with col_b:
        uploaded_file = st.file_uploader("ارفع صورة الجواز هنا", type=['jpg', 'png', 'jpeg'])

    if uploaded_file and st.button("⚡ قراءة الجواز بالذكاء الاصطناعي"):
        with st.spinner("جاري سحب البيانات..."):
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

# --- 2. قسم مراجعة وتعبئة البيانات ---
with st.container():
    st.markdown("### ✍️ 2. مراجعة وتعديل البيانات")
    c1, c2 = st.columns(2)
    with c1:
        sn = st.text_input("اللقب", value=st.session_state.data["sn"])
        fn = st.text_input("الاسم", value=st.session_state.data["fn"])
        job = st.text_input("المهنة")
    with c2:
        pno = st.text_input("رقم الجواز", value=st.session_state.data["pno"])
        mother = st.text_input("اسم الأم")
        gender = st.selectbox("الجنس", ["Male", "Female"])

# --- 3. قسم الطباعة ---
if st.button("🖨️ إصدار النموذج النهائي", use_container_width=True):
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
        st.download_button("✅ تحميل ملف التأشيرة الجاهز", res_file.getvalue(), f"{target_country}_visa_ready.pdf", use_container_width=True)
    except Exception as e:
        st.error(f"خطأ في تجهيز النموذج: تأكد من وجود ملف {target_country}.pdf. ({e})")

st.sidebar.markdown(f"**نظام المسار الذهبي الاحترافي**")
st.sidebar.caption(f"مرحباً بك، {ADMIN_U} 👋")
