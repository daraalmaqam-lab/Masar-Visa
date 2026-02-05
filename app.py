import streamlit as st
import numpy as np
from PIL import Image
import cv2

# محاولة تحميل مكتبة القراءة الذكية (PaddleOCR)
try:
    from paddleocr import PaddleOCR
    # تهيئة القارئ للغة الإنجليزية (يشتغل مرة واحدة ويقعد في الذاكرة)
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
except ImportError:
    st.error("الرجاء إضافة paddleocr و paddlepaddle في ملف requirements.txt")

# إعدادات الصفحة المعتمدة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- الثيمات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'p_data' not in st.session_state: st.session_state.p_data = {"n": "", "s": "", "p": ""}

# --- 🎨 الستايل الزجاجي النظيف ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, footer, .stAppDeployButton, [data-testid="stHeader"] {{ display: none !important; }}
    .stApp {{ background-image: url("{WALLPAPERS[st.session_state.bg_choice]}"); background-size: cover; background-attachment: fixed; }}
    .main-title {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        padding: 15px; border-radius: 15px; text-align: center; max-width: 500px;
        margin: 10px auto; color: white; font-family: 'Cairo'; font-size: 26px; font-weight: 900;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .glass-card {{
        background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(10px);
        padding: 30px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); color: white;
    }}
    input {{ height: 50px !important; font-size: 18px !important; text-align: center !important; font-weight: bold !important; border-radius: 10px !important; }}
    .stButton > button {{ width: 100% !important; height: 50px !important; font-weight: bold !important; border-radius: 10px !important; }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    # شاشة الدخول
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.session_state.bg_choice = st.selectbox("🎨 اختر الثيم:", list(WALLPAPERS.keys()))
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if (u == "ALI FETORY" or u == "ALI") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # شاشة العمل
    st.markdown('<div class="main-title">🌍 نظام قراءة بيانات الجواز</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 4, 1])
    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        up_file = st.file_uploader("📷 ارفع صورة الجواز (واضحة)", type=['jpg', 'png', 'jpeg'])
        
        if up_file:
            if st.button("⚡ بدء المسح الضوئي"):
                with st.spinner('جاري التحليل بدقة عالية...'):
                    img = Image.open(up_file)
                    img_array = np.array(img)
                    
                    # القراءة باستخدام PaddleOCR
                    result = ocr.ocr(img_array, cls=True)
                    
                    # استخراج النصوص المكتوبة
                    texts = [line[1][0] for res in result for line in res]
                    
                    if len(texts) > 5:
                        st.session_state.p_data["p"] = texts[0] # مثال لرقم الجواز
                        st.session_state.p_data["s"] = texts[1] # اللقب
                        st.session_state.p_data["n"] = texts[2] # الاسم
                    st.success("تم استخراج البيانات!")

        st.divider()
        st.subheader("📝 البيانات المستخرجة")
        c1, c2 = st.columns(2)
        fname = c1.text_input("الاسم الأول", value=st.session_state.p_data["n"])
        lname = c1.text_input("اللقب", value=st.session_state.p_data["s"])
        pnum = c2.text_input("رقم الجواز", value=st.session_state.p_data["p"])
        job = c2.text_input("المهنة")
        
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.auth = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
