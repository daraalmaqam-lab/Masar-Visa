import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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

# --- الواجهة الرئيسية للمنظومة ---
st.header("🛂 نظام الطباعة المباشرة فوق النماذج")

# اختيار الدولة (يجب رفع ملفات مثل italy.pdf على GitHub)
target_country = st.selectbox("اختر دولة الوجهة:", ["italy", "france", "germany"])

# 1. سحب بيانات الجواز
uploaded_passport = st.file_uploader("ارفع صورة الجواز للقراءة", type=['jpg', 'png', 'jpeg'])

# بيانات الجواز (ستصبح تلقائية عند ربط محرك القراءة)
passport_data = {"Surname": "AL-FETORY", "FirstName": "ALI"}

if uploaded_passport:
    st.success("✅ تم استلام بيانات الجواز")
    
    # 2. الخانات اليدوية (لإكمال النموذج)
    st.subheader("📝 إكمال بيانات النموذج الأصلي")
    col1, col2 = st.columns(2)
    with col1:
        mother_name = st.text_input("اسم الأم بالكامل")
        current_job = st.text_input("المهنة الحالية")
    with col2:
        passport_no = st.text_input("رقم الجواز", value=passport_data["PassportNo"] if "PassportNo" in passport_data else "")
        phone_no = st.text_input("رقم الهاتف")

    # 3. دمج البيانات بنظام "الطباعة الفوقية"
    if st.button(f"🚀 إصدار ملف {target_country} المطبوع"):
        try:
            # قراءة القالب الأصلي من GitHub
            existing_pdf = PdfReader(f"{target_country}.pdf")
            output = PdfWriter()

            # إنشاء طبقة شفافة للكتابة فوقها
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # ضبط أماكن النص (الإحداثيات) - يمكنك تعديل الأرقام لتناسب المربعات
            can.setFont("Helvetica", 10)
            can.drawString(100, 715, passport_data["Surname"]) # خانة اللقب
            can.drawString(100, 695, passport_data["FirstName"]) # خانة الاسم
            can.drawString(100, 675, mother_name) # خانة اسم الأم
            can.drawString(100, 655, current_job) # خانة المهنة
            can.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            
            # دمج الطبقة الجديدة مع الصفحة الأولى من النموذج
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

            # إضافة باقي الصفحات كما هي
            for i in range(1, len(existing_pdf.pages)):
                output.add_page(existing_pdf.pages[i])

            final_output = io.BytesIO()
            output.write(final_output)
            
            st.download_button(
                label=f"📥 تحميل نموذج {target_country} الجاهز للطباعة",
                data=final_output.getvalue(),
                file_name=f"Visa_{target_country}_Final.pdf",
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error(f"❌ لم نجد ملف '{target_country}.pdf' على GitHub.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")

# الإحصائيات (من صور فواتيرك السابقة)
st.sidebar.metric("مبيعاتك اليوم", "2850 د.ل")
