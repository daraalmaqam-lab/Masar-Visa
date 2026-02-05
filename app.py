import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract # قارئ سريع جداً وخفيف

# إعدادات الصفحة المعتمدة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# دالة معالجة الصورة لتحسين الدقة
def preprocess_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # تحويل لرمادي
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] # توضيح الحروف
    return gray

# --- الثيمات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'data' not in st.session_state: st.session_state.data = {"n": "", "s": "", "p": ""}

# --- 🎨 الستايل الزجاجي ---
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
        background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px);
        padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); color: white;
    }}
    input {{ height: 45px !important; font-size: 16px !important; text-align: center !important; font-weight: bold !important; }}
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
        if st.button("دخول", use_container_width=True):
            if (u == "ALI FETORY" or u == "ALI") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # شاشة العمل
    st.markdown('<div class="main-title">🌍 قارئ بيانات الجواز الذكي</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 4, 1])
    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        up_file = st.file_uploader("📷 ارفع صورة الجواز (واضحة)", type=['jpg', 'png', 'jpeg'])
        
        if up_file:
            if st.button("⚡ قراءة سريعة الآن"):
                # معالجة الصورة قبل القراءة لتحسين الدقة
                raw_img = Image.open(up_file)
                processed = preprocess_image(raw_img)
                
                # قراءة النص باستخدام محرك سريع
                text = pytesseract.image_to_string(processed, lang='eng')
                lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 3]
                
                # توزيع البيانات بشكل ذكي
                if len(lines) > 2:
                    st.session_state.data["s"] = lines[0] # اللقب
                    st.session_state.data["n"] = lines[1] # الاسم
                    st.session_state.data["p"] = lines[2] # رقم الجواز
                st.success("تمت القراءة بنجاح في ثواني!")

        st.divider()
        st.subheader("📋 مراجعة البيانات")
        c1, c2 = st.columns(2)
        fname = c1.text_input("الاسم الأول", value=st.session_state.data["n"])
        lname = c1.text_input("اللقب", value=st.session_state.data["s"])
        pnum = c2.text_input("رقم الجواز", value=st.session_state.data["p"])
        job = c2.text_input("المهنة")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 خروج", use_container_width=True):
            st.session_state.auth = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
