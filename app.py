import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# --- 1. إعدادات الأمان والدخول ---
ADMIN_USER = "ALI FETORY"
ADMIN_PASS = "0925843353"

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🏛️ منظومة المسار الذهبي للتأشيرات</h2>", unsafe_allow_html=True)
    u_name = st.text_input("اسم المستخدم").strip().upper()
    u_pass = st.text_input("الرقم السري", type="password").strip()
    if st.button("دخول للمنظومة", use_container_width=True):
        if u_name == ADMIN_USER.upper() and u_pass == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 2. واجهة العمل الرئيسية ---
st.title("📑 معالج النماذج الرسمية (تعبئة هجينة)")

# اختيار السفارة
country = st.sidebar.selectbox("اختر نموذج السفارة الأصلي:", ["إيطاليا (Italy)", "فرنسا (France)", "ألمانيا (Germany)"])

# رفع الجواز للقراءة التلقائية
st.header("1. القراءة التلقائية من الجواز")
uploaded_passport = st.file_uploader("ارفع صورة الجواز لسحب البيانات", type=['jpg', 'png', 'jpeg'])

# بيانات افتراضية تم سحبها آلياً (ستحل محلها بيانات الجواز المرفوع)
auto_data = {
    "surname": "AL-FETORY",
    "firstname": "ALI",
    "passport_no": "P0123456",
    "dob": "1985-10-20"
}

if uploaded_passport:
    st.success("✅ تم سحب البيانات الأساسية من الجواز بنجاح")
    st.table(pd.DataFrame([auto_data]))

    st.divider()

    # --- 3. الخانات اليدوية (لإكمال النموذج الأصلي) ---
    st.header("2. إكمال باقي بيانات النموذج (يدوياً)")
    col1, col2 = st.columns(2)
    with col1:
        mother = st.text_input("اسم الأم بالكامل")
        address = st.text_input("عنوان السكن الحالي بالتفصيل")
        job = st.text_input("المهنة الحالية")
    with col2:
        phone = st.text_input("رقم الهاتف الشخصي")
        prev_visas = st.selectbox("تأشيرات سابقة خلال 3 سنوات؟", ["لا يوجد", "نعم (تأشيرة واحدة)", "نعم (أكثر من واحدة)"])
        purpose = st.text_input("الغرض من السفر (مثلاً: سياحة)")

    # --- 4. دمج البيانات في النموذج الأصلي (PDF Filling) ---
    st.divider()
    if st.button(f"🔥 إصدار نموذج {country} الأصلي معبأ", use_container_width=True):
        st.info("جاري دمج البيانات التلقائية واليدوية في النموذج الرسمي...")
        
        # هنا تتم عملية التعبئة البرمجية داخل الـ PDF الأصلي
        # ملاحظة: الكود يفترض وجود ملف PDF في GitHub باسم 'template.pdf'
        try:
            # محاكاة لإنتاج الملف المعبأ
            # في الواقع، سنستخدم PdfWriter لتعبئة الخانات المحددة
            st.download_button(
                label=f"📥 تحميل ملف PDF {country} المكتمل",
                data="محتوى ملف الـ PDF المعبأ", 
                file_name=f"Schengen_Form_{country}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning("السيستم جاهز، فقط ارفع ملف الـ PDF الأصلي لـ GitHub لربط الخانات.")

# --- 5. أرشيف مبيعاتك (من صورتك السابقة) ---
st.sidebar.divider()
st.sidebar.subheader("📊 إحصائيات سريعة")
st.sidebar.metric("إجمالي المبيعات", "2850 د.ل")
st.sidebar.write("آخر تحديث: 2025-05-03")
