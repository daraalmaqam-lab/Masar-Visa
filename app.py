import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject
import io

# --- بيانات الدخول الخاصة بعلي ---
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

# --- الواجهة الرئيسية ---
st.header("🛂 معالج النماذج الأصلي (إصدار الدقة)")

# اختيار الدولة (يجب رفع ملفات بأسماء italy.pdf, france.pdf على GitHub)
target_country = st.selectbox("اختر دولة الوجهة:", ["italy", "france", "germany"])

# 1. سحب بيانات الجواز
uploaded_passport = st.file_uploader("ارفع صورة الجواز للقراءة", type=['jpg', 'png', 'jpeg'])

# بيانات الجواز المسحوبة (ستكون حقيقية عند ربط OCR)
passport_data = {"Surname": "AL-FETORY", "FirstName": "ALI", "PassportNo": "P0123456"}

if uploaded_passport:
    st.success("✅ تم استلام بيانات الجواز")
    
    # 2. الخانات اليدوية لإكمال النموذج
    st.subheader("📝 إكمال بيانات النموذج الأصلي")
    col1, col2 = st.columns(2)
    with col1:
        mother = st.text_input("اسم الأم")
        job = st.text_input("المهنة")
    with col2:
        address = st.text_input("العنوان الحالي")
        phone = st.text_input("رقم الهاتف")

    # 3. معالجة وتعبئة الملف الأصلي
    if st.button(f"إصدار نموذج {target_country} النهائي"):
        try:
            file_path = f"{target_country}.pdf"
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            # محاولة حل مشكلة الـ AcroForm برمجياً
            writer.add_page(reader.pages[0])
            if "/AcroForm" not in writer.root_object:
                writer.root_object.update({
                    NameObject("/AcroForm"): DictionaryObject()
                })

            # قائمة البيانات المراد تعبئتها (يجب أن تطابق أسماء الخانات في الـ PDF)
            fields = {
                "Surname": passport_data["Surname"],
                "GivenNames": passport_data["FirstName"],
                "PassportNumber": passport_data["PassportNo"],
                "MotherName": mother,
                "Occupation": job,
                "Address": address,
                "Phone": phone
            }
            
            # التعبئة
            writer.update_page_form_field_values(writer.pages[0], fields)
            
            output = io.BytesIO()
            writer.write(output)
            
            st.download_button(
                label=f"📥 تحميل نموذج {target_country} المعبأ (PDF)",
                data=output.getvalue(),
                file_name=f"Visa_{target_country}_Form.pdf",
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error(f"❌ ملف '{target_country}.pdf' غير موجود على GitHub.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")

# إحصائياتك من الصور السابقة
st.sidebar.metric("إجمالي المبيعات", "2850 د.ل")
