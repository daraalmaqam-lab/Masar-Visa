import streamlit as st
import numpy as np
from PIL import Image
import re
import cv2

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path - Full System", layout="wide")

# --- 🧠 المحرك الذكي المطور (يسحب كل تواريخ وبيانات الجواز) ---
def advanced_passport_reader(file):
    import easyocr
    reader = easyocr.Reader(['en'])
    image = Image.open(file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # معالجة الصورة لتحسين القراءة
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    results = reader.readtext(processed, detail=0)
    full_text = " ".join(results).upper()
    
    data = {"name": "", "pass_no": "", "dob": None, "doe": None}
    
    # 1. رقم الجواز
    p_match = re.search(r'[A-Z][0-9]{7,8}', full_text.replace(" ", ""))
    if p_match: data["pass_no"] = p_match.group(0)
    
    # 2. الاسم (بعد LBY)
    for line in results:
        if "LBY" in line.upper():
            data["name"] = line.upper().split("LBY")[-1].replace("<", " ").strip()
            break
            
    # 3. محاولة استخراج التواريخ (تاريخ الميلاد والانتهاء) من منطقة MRZ
    dates = re.findall(r'[0-9]{6}', full_text.replace(" ", ""))
    if len(dates) >= 2:
        # تبسيط: أول تاريخ غالباً ميلاد، الثاني غالباً انتهاء (يحتاج تعديل يدوي للتأكيد)
        data["dob"] = dates[0] 
        data["doe"] = dates[1]

    return data

# --- 🎨 التنسيق الذهبي النظيف ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, footer { visibility: hidden; }
    .stApp { background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); background-size: cover; background-attachment: fixed; }
    .main-title { font-family: 'Cairo'; color: #fbbf24; text-align: center; font-size: 40px; font-weight: 900; text-shadow: 3px 3px 6px black; }
    .label-text { color: white; font-family: 'Cairo'; font-size: 18px; text-align: right; text-shadow: 2px 2px 4px black; margin-bottom: 5px; }
    div[data-baseweb="input"], [data-baseweb="select"], .stDateInput div { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; text-align: center !important; }
    .section-box { padding: 15px; border-bottom: 2px solid #fbbf24; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# --- نظام الدخول ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<div class="main-title">دخول المنظومة</div>', unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم").upper()
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
                st.session_state.auth = True
                st.rerun()
else:
    st.markdown('<div class="main-title">🌍 منظومة المسار الذهبي للتأشيرات والحجوزات</div>', unsafe_allow_html=True)

    # 1. القارئ الآلي
    st.markdown('<p class="label-text">📸 ارفع صورة الجواز (لتعبئة البيانات تلقائياً)</p>', unsafe_allow_html=True)
    up = st.file_uploader("up", type=['jpg','png','jpeg'], label_visibility="collapsed")
    
    res = {"name": "", "pass_no": "", "dob": "", "doe": ""}
    if up:
        with st.spinner('جاري سحب بيانات الجواز...'):
            res = advanced_passport_reader(up)

    st.write("---")

    # 2. النموذج المتكامل (تلقائي + يدوي)
    st.markdown('<p class="label-text">📑 نموذج بيانات المسافر والحجز</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<p class="label-text">الاسم بالكامل (تلقائي)</p>', unsafe_allow_html=True)
        name = st.text_input("n", value=res["name"], key="name", label_visibility="collapsed")
        st.markdown('<p class="label-text">تاريخ الميلاد</p>', unsafe_allow_html=True)
        dob = st.text_input("db", value=res["dob"], placeholder="YYMMDD", label_visibility="collapsed")

    with c2:
        st.markdown('<p class="label-text">رقم الجواز (تلقائي)</p>', unsafe_allow_html=True)
        p_no = st.text_input("pn", value=res["pass_no"], key="pno", label_visibility="collapsed")
        st.markdown('<p class="label-text">تاريخ الانتهاء</p>', unsafe_allow_html=True)
        doe = st.text_input("de", value=res["doe"], placeholder="YYMMDD", label_visibility="collapsed")

    with c3:
        st.markdown('<p class="label-text">رقم الهاتف (يدوي)</p>', unsafe_allow_html=True)
        phone = st.text_input("ph", value="0925843353", label_visibility="collapsed")
        st.markdown('<p class="label-text">الوجهة</p>', unsafe_allow_html=True)
        dest = st.selectbox("ds", ["إيطاليا", "فرنسا", "تركيا", "مالطا"], label_visibility="collapsed")

    # 3. قسم الحجز المبدئي (طيران وفندق)
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<p class="label-text">🏨 الحجز الفندقي المبدئي</p>', unsafe_allow_html=True)
    h1, h2 = st.columns(2)
    with h1: hotel_name = st.text_input("اسم الفندق المقترح", placeholder="مثلاً: Hotel Roma")
    with h2: hotel_days = st.number_input("عدد الليالي", min_value=1, value=7)
    
    st.markdown('<p class="label-text">✈️ حجز الطيران المبدئي</p>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1: flight_from = st.text_input("من مطار", value="Tripoli (MJI)")
    with t2: flight_to = st.text_input("إلى مطار", value="Rome (FCO)")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. إصدار النموذج
    if st.button("🖨️ إصدار وحفظ نموذج التأشيرة والحجز المبدئي"):
        st.balloons()
        st.success(f"تم بنجاح! المسافر: {name} | جواز: {p_no} | فندق: {hotel_name}")
        st.info("النموذج جاهز الآن للسحب كملف أصلي.")

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
