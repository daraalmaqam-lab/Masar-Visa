import streamlit as st
import numpy as np
from PIL import Image
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- دالة القارئ الذكي (المخ) ---
def get_passport_data(file):
    import easyocr
    import cv2
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return reader.readtext(processed, detail=0)

# --- نظام الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل (عزل كامل لضمان ثبات الشاشة الرئيسية)
# =========================================================
if not st.session_state.auth:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .stApp { 
            background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
            background-size: cover; background-position: center; background-attachment: fixed;
        }
        [data-testid="stVerticalBlock"] {
            position: absolute !important; top: 50% !important; left: 50% !important;
            transform: translate(-50%, -50%) !important; width: 100% !important;
            max-width: 450px !important; display: flex !important;
            flex-direction: column !important; align-items: center !important;
        }
        .main-title { text-align: center; color: #fbbf24; font-family: 'Cairo'; font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black; margin-bottom: 20px; }
        .custom-label { color: white; font-family: 'Cairo'; font-size: 22px; font-weight: 700; text-align: center; width: 100%; margin-bottom: 5px; text-shadow: 2px 2px 4px black; }
        div[data-baseweb="input"] { height: 45px !important; width: 320px !important; margin: 0 auto !important; background-color: #f0f2f6 !important; border-radius: 10px !important; border: 2px solid #fbbf24 !important; }
        input { text-align: center !important; color: #333 !important; font-size: 18px !important; font-weight: bold !important;}
        .stButton button { height: 55px !important; width: 220px !important; background-color: #fbbf24 !important; color: black !important; font-weight: bold !important; font-size: 22px !important; border-radius: 12px !important; margin-top: 30px !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; display: block !important; }
        .stApp { background-image: none !important; background-color: #0e1117 !important; }
        .dash-title { color: #fbbf24; font-family: 'Cairo'; font-size: 40px; text-align: center; padding: 20px; }
        /* تحسين شكل خانات النتائج في لوحة التحكم */
        div[data-baseweb="input"] { background-color: #1e2129 !important; border: 1px solid #fbbf24 !important; width: 100% !important; }
        input { color: #fbbf24 !important; text-align: right !important; }
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
    # --- لوحة التحكم (القارئ فقط) ---
    st.markdown('<h1 class="dash-title">📸 قارئ جوازات السفر الذكي</h1>', unsafe_allow_html=True)
    
    with st.container():
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            up_file = st.file_uploader("ارفع صورة الجواز هنا", type=['jpg', 'png', 'jpeg'])
            
            extracted_name = ""
            extracted_pass = ""
            
            if up_file:
                with st.spinner('جاري قراءة البيانات...'):
                    try:
                        res = get_passport_data(up_file)
                        raw = "".join(res).upper().replace(" ", "")
                        # بحث عن رقم الجواز
                        p_match = re.search(r'[A-Z][0-9]{7,9}', raw)
                        if p_match: extracted_pass = p_match.group()
                        # محاولة استخراج الاسم
                        if "LBY" in raw:
                            extracted_name = raw.split("LBY")[1].split("<<")[0].replace("<", " ").strip()
                        else:
                            extracted_name = res[0] if res else ""
                    except:
                        st.error("حدث خطأ أثناء معالجة الصورة")

            st.write("### البيانات المستخرجة:")
            st.text_input("الاسم بالكامل", value=extracted_name, key="res_name")
            st.text_input("رقم الجواز", value=extracted_pass, key="res_pass")
            
            st.write("---")
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.auth = False
                st.rerun()
