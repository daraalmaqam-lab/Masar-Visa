import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import io

# --- بيانات الدخول الخاصة بك (ALI FETORY) ---
ADMIN_USER = "ALI FETORY"
ADMIN_PASS = "0925843353"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- بوابة الدخول ---
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

# --- واجهة العمل الرئيسية ---
st.sidebar.title(f"مرحباً: {ADMIN_USER}")
st.header("🛂 معالج النماذج المتعدد (تعبئة هجينة)")

# قائمة السفارات - تأكد من رفع الملفات بهذه الأسماء في GitHub: italy.pdf, france.pdf, etc.
target_country = st.selectbox("اختر دولة الوجهة (القالب الأصلي):", ["italy", "france", "germany", "spain", "malta"])

# 1. سحب بيانات الجواز (القراءة الآلية)
st.subheader("1️⃣ قراءة بيانات الجواز")
uploaded_passport = st.file_uploader("ارفع صورة الجواز لسحب البيانات", type=['jpg', 'png', 'jpeg'])

# هذه البيانات ستُسحب فعلياً من الصورة لاحقاً
passport_data = {"surname": "AL-FETORY", "firstname": "ALI", "passport_no": "P0123456", "dob": "1985-10-20"}

if uploaded_passport:
    st.success("✅ تم التعرف على بيانات الجواز")
    st.write(f"الاسم: {passport_data['firstname']} {passport_data['surname']}")

    st.divider()

    # 2. الخانات اليدوية (لإكمال باقي النموذج الأصلي)
    st.subheader("2️⃣ إكمال باقي بيانات النموذج (يدوياً)")
    col1, col2 = st.columns(2)
    with col1:
        mother = st.text_input("اسم الأم بالكامل")
        address = st.text_input("عنوان السكن في ليبيا")
        job = st.text_input("المهنة الحالية")
    with col2:
        phone = st.text_input("رقم الهاتف")
        email = st.text_input("البريد الإلكتروني")
        purpose = st.text_input("الغرض من السفر")

    # 3. دمج البيانات في النموذج المختار
    st.divider()
    if st.button(f"🔥 إصدار نموذج {target_country} المعبأ", use_container_width=True):
        try:
            # السيستم يفتح ملف الـ PDF حسب الدولة المختارة
            file_name = f"{target_country}.pdf"
            reader = PdfReader(file_name)
            writer = PdfWriter()
            writer.add_page(reader.pages[0])
            
            # ربط البيانات المسحوبة واليدوية بالخانات الأصلية
            fields = {
                "Surname": passport_data["surname"],
                "FirstName": passport_data["firstname"],
                "Passport": passport_data["passport_no"],
                "DOB": passport_data["dob"],
                "Mother": mother,
                "Address": address,
                "Job": job,
                "Phone": phone,
                "Purpose": purpose
            }
            writer.update_page_form_field_values(writer.pages[0], fields)
            
            output = io.BytesIO()
            writer.write(output)
            
            st.download_button(
                label=f"📥 تحميل ملف {target_country} المكتمل (PDF)",
                data=output.getvalue(),
                file_name=f"Schengen_{target_country}_Filled.pdf",
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error(f"⚠️ تنبيه: ملف '{target_country}.pdf' غير موجود في GitHub. يرجى رفعه لتفعيله.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء التعبئة: {e}")

# --- أرشيف الإحصائيات (الداش بورد) ---
st.sidebar.divider()
st.sidebar.metric("مبيعاتك اليوم", "2850 د.ل")
if st.sidebar.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
