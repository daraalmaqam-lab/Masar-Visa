import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import easyocr
from PIL import Image
import numpy as np

# --- إعداد قارئ الجوازات (OCR) ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader_ocr = load_ocr()

# --- الدخول ---
ADMIN_USER = "ALI FETORY"
ADMIN_PASS = "0925843353"

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏛️ منظومة المسار الذهبي")
    u_name = st.text_input("اسم المستخدم").strip().upper()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("دخول"):
        if u_name == ADMIN_USER.upper() and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

st.header("🛂 معالج النماذج الذكي (ضبط الإحداثيات والقارئ)")

target_country = st.selectbox("اختر الدولة:", ["italy", "france", "germany"])

# 1. سحب بيانات الجواز الحقيقية
uploaded_passport = st.file_uploader("ارفع صورة الجواز للقراءة", type=['jpg', 'png', 'jpeg'])

passport_data = {"Surname": "", "FirstName": "", "PassportNo": ""}

if uploaded_passport:
    with st.spinner("جاري قراءة بيانات الجواز..."):
        image = Image.open(uploaded_passport)
        # تحويل الصورة لقراءة النص
        results = reader_ocr.readtext(np.array(image))
        full_text = " ".join([res[1] for res in results])
        
        # محاولة ذكية لاستخراج البيانات (مثال مبسط)
        if "P<LBY" in full_text or "PASSPORT" in full_text.upper():
            st.success("✅ تم التعرف على الجواز الليبي")
            # هنا نضع منطق استخراج الاسم واللقب بناءً على الكلمات المكتشفة
            passport_data["Surname"] = results[0][1] # تجريبي
            passport_data["FirstName"] = results[1][1] # تجريبي

    # 2. الخانات اليدوية (تقدر تعدل اللي قراه الجواز)
    st.subheader("📝 مراجعة وتكملة البيانات")
    col1, col2 = st.columns(2)
    with col1:
        sn = st.text_input("اللقب", value=passport_data["Surname"])
        fn = st.text_input("الاسم", value=passport_data["FirstName"])
    with col2:
        mother = st.text_input("اسم الأم")
        job = st.text_input("المهنة")

    # 3. ضبط الإحداثيات (هنا تقدر تغير الأرقام لين يجي النص في المربع)
    st.info("💡 نصيحة: إذا النص جاء فوق أو تحت، غير أرقام (Y)، وإذا جاء يمين أو يسار غير أرقام (X).")
    
    col_x, col_y = st.columns(2)
    with col_x:
        pos_x = st.slider("تحريك النص أفقياً (X)", 0, 500, 110)
    with col_y:
        pos_y = st.slider("تحريك النص عمودياً (Y)", 0, 800, 710)

    if st.button(f"🚀 طباعة نموذج {target_country} بالقياسات الجديدة"):
        try:
            existing_pdf = PdfReader(f"{target_country}.pdf")
            output = PdfWriter()
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 11)

            # طباعة البيانات حسب الإحداثيات المختارة
            can.drawString(pos_x, pos_y, sn)             # اللقب
            can.drawString(pos_x, pos_y - 25, fn)        # الاسم (تحته بـ 25 نقطة)
            can.drawString(pos_x, pos_y - 50, mother)    # الأم (تحتها بـ 50 نقطة)
            can.drawString(pos_x, pos_y - 75, job)       # المهنة
            
            can.save()
            packet.seek(0)
            new_pdf = PdfReader(packet)
            
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

            for i in range(1, len(existing_pdf.pages)):
                output.add_page(existing_pdf.pages[i])

            final_output = io.BytesIO()
            output.write(final_output)
            
            st.download_button(
                label="📥 تحميل الملف وتجربة القياس",
                data=final_output.getvalue(),
                file_name=f"Test_{target_country}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"خطأ: {e}")
