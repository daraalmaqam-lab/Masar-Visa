import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ (نسخة خفيفة لتجنب الأخطاء) ---
def simple_reader(file):
    try:
        import easyocr
        reader = easyocr.Reader(['en'])
        image = Image.open(file)
        results = reader.readtext(np.array(image), detail=0)
        return results
    except Exception as e:
        return []

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل (عزل كامل - شاشة دخول ثابتة + لوحة تحكم هادئة)
# =========================================================
if not st.session_state.auth:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .stApp { background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); background-size: cover; background-position: center; }
        [data-testid="stVerticalBlock"] { position: absolute !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; width: 100% !important; max-width: 450px !important; display: flex !important; flex-direction: column !important; align-items: center !important; }
        .main-title { text-align: center; color: #fbbf24; font-family: 'Cairo'; font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black; margin-bottom: 20px; }
        .custom-label { color: white; font-family: 'Cairo'; font-size: 20px; font-weight: 700; text-align: center; width: 100%; margin-bottom: 5px; text-shadow: 2px 2px 4px black; }
        div[data-baseweb="input"] { height: 45px !important; width: 320px !important; margin: 0 auto !important; background-color: white !important; border-radius: 10px !important; border: 2px solid #fbbf24 !important; }
        input { text-align: center !important; color: black !important; font-size: 18px !important; }
        .stButton button { height: 50px !important; width: 200px !important; background-color: #fbbf24 !important; color: black !important; font-weight: bold; border-radius: 12px !important; margin-top: 20px !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; display: block !important; }
        .stApp { background-image: none !important; background-color: #f0f2f6 !important; }
        .booking-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); direction: rtl; }
        </style>
        """, unsafe_allow_html=True)

# =========================================================
# 🏠 عرض المحتوى
# =========================================================
if not st.session_state.auth:
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_login").upper()
    st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
else:
    # --- لوحة التحكم: نموذج الحجز المبدئي ---
    st.markdown("<h1 style='text-align:center; font-family:Cairo; color:#2c3e50;'>📋 نموذج حجز طيران وفنادق</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    name_res, pass_res = "", ""
    with col1:
        st.write("### 📸 سحب بيانات الجواز")
        up_file = st.file_uploader("ارفع الصورة", type=['jpg', 'png', 'jpeg'])
        if up_file:
            res = simple_reader(up_file)
            raw = "".join(res).upper()
            p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
            if p_match: pass_res = p_match.group()
            if "LBY" in raw: name_res = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()

    with col2:
        st.markdown('<div class="booking-card">', unsafe_allow_html=True)
        st.write("### 📝 تفاصيل الحجز المبدئي")
        name = st.text_input("اسم المسافر", value=name_res)
        passport = st.text_input("رقم الجواز", value=pass_res)
        
        st.write("---")
        h_type = st.selectbox("نوع الحجز", ["حجز طيران مبدئي", "حجز فندقي", "حجز طيران + فندق"])
        dest = st.text_input("الوجهة المطلوبة")
        
        if st.button("✅ تأكيد وإصدار النموذج"):
            st.success(f"تم حجز طلب مبدئي لـ {name}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()
