import streamlit as st
import numpy as np
from PIL import Image
import easyocr  # مكتبة القارئ الذكي

# إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# تحميل قارئ الجوازات في الذاكرة (مرة واحدة)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])
reader = load_ocr()

# --- مكتبة الثيمات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974"
}

# تهيئة حالة الجلسة للبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'passport_data' not in st.session_state:
    st.session_state.passport_data = {"name": "", "surname": "", "p_num": ""}

# --- 🎨 الستايل المعتمد ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}
    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-attachment: fixed;
    }}
    .main-title {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        padding: 20px; border-radius: 15px; text-align: center; max-width: 550px;
        margin: 20px auto; color: white; font-family: 'Cairo', sans-serif;
        font-size: 30px; font-weight: 900; border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .glass-card {{
        background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px);
        padding: 30px; border-radius: 25px; margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.1); color: white;
    }}
    input {{ height: 50px !important; font-size: 18px !important; text-align: center !important; font-weight: bold !important; border-radius: 10px !important; }}
    .stButton > button {{ width: 100% !important; height: 50px !important; font-weight: bold !important; border-radius: 10px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- نظام الشاشات ---

if not st.session_state.auth:
    # شاشة الدخول
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.session_state.bg_choice = st.selectbox("🎨 اختر واجهة المنظومة:", list(WALLPAPERS.keys()))
        st.divider()
        user = st.text_input("اسم المستخدم").upper()
        passw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if (user == "ALI FETORY" or user == "ALI") and passw == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # شاشة العمل - القارئ والنموذج
    st.markdown('<div class="main-title">🌍 معالجة بيانات الجواز</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 4, 1])
    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # قسم رفع الجواز
        st.subheader("📸 مسح الجواز")
        uploaded_file = st.file_uploader("ارفع صورة الجواز هنا", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            if st.button("⚡ قراءة بيانات الجواز"):
                with st.spinner('جاري القراءة...'):
                    image = Image.open(uploaded_file)
                    results = reader.readtext(np.array(image))
                    # محاكاة استخراج البيانات (تحتاج تخصيص حسب شكل الجواز)
                    st.session_state.passport_data = {
                        "name": results[1][1] if len(results) > 1 else "غير معروف",
                        "surname": results[0][1] if len(results) > 0 else "غير معروف",
                        "p_num": results[2][1] if len(results) > 2 else "P000000"
                    }
                    st.success("تمت القراءة بنجاح!")

        st.divider()
        
        # قسم خانات النموذج
        st.subheader("📝 بيانات النموذج")
        c1, c2 = st.columns(2)
        
        name = c1.text_input("الاسم", value=st.session_state.passport_data["name"])
        surname = c1.text_input("اللقب", value=st.session_state.passport_data["surname"])
        
        p_num = c2.text_input("رقم الجواز", value=st.session_state.passport_data["p_num"])
        job = c2.text_input("المهنة")
        
        dest = st.selectbox("الوجهة", ["إيطاليا", "فرنسا", "ألمانيا", "بريطانيا"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("✅ حفظ البيانات"):
            st.toast("تم الحفظ!")
            
        if col_btn2.button("🚪 خروج"):
            st.session_state.auth = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
