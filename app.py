import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# --- إعدادات الصفحة وجو الشاشة ---
st.set_page_config(page_title="المسار الذهبي - منظومة التأشيرات", layout="wide")

# --- بيانات الدخول ---
ADMIN_USER = "ALI FETORY"
ADMIN_PASS = "0925843353"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- تنسيق الواجهة (CSS) لجعل الجو احترافي ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- شاشة الدخول ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ Masar Gold</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>الرجاء تسجيل الدخول للمتابعة</p>", unsafe_allow_html=True)
        u_name = st.text_input("اسم المستخدم").strip().upper()
        u_pass = st.text_input("الرقم السري", type="password").strip()
        if st.button("دخول"):
            if u_name == ADMIN_USER.upper() and u_pass == ADMIN_PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- الواجهة الرئيسية بعد الدخول ---
st.sidebar.title("🛂 قائمة التحكم")
st.sidebar.info(f"المستخدم: {ADMIN_USER}")
if st.sidebar.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()

st.markdown("<h2 style='text-align: right;'>📑 معالج نماذج السفارات الأصلية</h2>", unsafe_allow_html=True)

# --- الخطوات العملية ---
col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("1️⃣ قراءة بيانات الجواز")
    uploaded_file = st.file_uploader("ارفع صورة الجواز هنا", type=['jpg', 'png', 'jpeg'])
    
    # محاكاة القراءة التلقائية
    passport_data = {"surname": "AL-FETORY", "firstname": "ALI", "passport_no": "P0123456"}
    
    if uploaded_file:
        st.success("✅ تم سحب بيانات الجواز")
        st.write(f"**الاسم:** {passport_data['firstname']} {passport_data['surname']}")
        st.write(f"**رقم الجواز:** {passport_data['passport_no']}")

with col_b:
    st.subheader("2️⃣ إكمال البيانات يدوياً")
    country = st.selectbox("اختر السفارة:", ["إيطاليا (Italy)", "فرنسا (France)", "ألمانيا (Germany)"])
    mother = st.text_input("اسم الأم")
    address = st.text_input("عنوان السكن في ليبيا")
    job = st.text_input("المهنة")

st.divider()

# --- إصدار الملف النهائي ---
st.subheader("3️⃣ إصدار ملف التأشيرة الكامل")
if st.button("🚀 توليد وتعبئة النموذج الأصلي (PDF)"):
    try:
        # البحث عن ملف PDF المرفوع على GitHub
        # ملاحظة: تأكد أن اسم الملف في GitHub هو italy_form.pdf
        reader = PdfReader("italy_form.pdf")
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        
        # تعبئة الخانات (هنا نربط البيانات التلقائية واليدوية)
        fields = {
            "Surname": passport_data["surname"],
            "GivenNames": passport_data["firstname"],
            "PassportNo": passport_data["passport_no"],
            "MotherName": mother,
            "Address": address
        }
        writer.update_page_form_field_values(writer.pages[0], fields)
        
        output = io.BytesIO()
        writer.write(output)
        
        st.download_button(
            label=f"📥 تحميل نموذج {country} المعبأ جاهزاً للطباعة",
            data=output.getvalue(),
            file_name=f"Schengen_{country}.pdf",
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.error("⚠️ لم نجد ملف 'italy_form.pdf' على GitHub. تأكد من رفعه بنفس الاسم.")
    except Exception as e:
        st.error(f"حدث خطأ فني: {e}")

# --- الإحصائيات في الأسفل (جو الشاشة) ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("مبيعات اليوم", "2850 د.ل")
c2.metric("الجوازات المسحوبة", "12")
c3.metric("الملفات المكتملة", "8")
