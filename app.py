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
    st.markdown("<h2 style='text-align: center;'>🏛️ المسار الذهبي</h2>", unsafe_allow_html=True)
    u_name = st.text_input("اسم المستخدم").upper().strip()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("دخول"):
        if u_name == ADMIN_USER and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 🎨 لوحة تحكم الألوان المعدلة ---
with st.sidebar:
    st.header("🎨 إعدادات المظهر")
    bg_color = st.color_picker("لون الخلفية", "#FFFFFF")
    text_color = st.color_picker("لون النص والعناوين", "#1F2937")
    input_bg = st.color_picker("لون خانات الكتابة", "#F3F4F6")
    btn_color = st.color_picker("لون الأزرار", "#374151")

# تطبيق التنسيق (مع إزالة الخط اللي بجنب الاختيار)
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; }}
    h1, h2, h3, p, label, .stMarkdown {{ color: {text_color} !important; font-weight: bold !important; }}
    
    /* تنسيق الخانات وإزالة الحدود المزعجة */
    input, .stSelectbox div[data-baseweb="select"] {{ 
        color: #000000 !important;
