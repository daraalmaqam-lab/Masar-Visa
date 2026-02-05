import streamlit as st
import pandas as pd
from docx import Document
import io

# --- 1. إعدادات الهوية والأمان ---
ADMIN_USER = "ALI FETORY"
ADMIN_PASS = "0925843353"

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

# --- 2. نظام اللغات المدمج ---
texts = {
    "العربية": {
        "title": "منظومة المسار الذهبي للتأشيرات",
        "user": "اسم المستخدم", "pass": "الرقم السري", "login": "دخول",
        "dash": "لوحة الإحصائيات", "visa": "معالج تأشيرة شنغن", 
        "upload": "ارفع صورة الجواز لسحب البيانات", "result": "البيانات المستخرجة",
        "download": "تحميل النموذج الرسمي"
    },
    "English": {
        "title": "Masar Gold Visa System",
        "user": "Username", "pass": "Password", "login": "Login",
        "dash": "Dashboard", "visa": "Schengen Processor", 
        "upload": "Upload Passport Scan", "result": "Extracted Data",
        "download": "Download Official Form"
    }
}

# قائمة تغيير اللغة في الجانب
st.session_state.lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
T = texts[st.session_state.lang]

# --- 3. بوابة الدخول الذكية (خانتين) ---
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align: center;'>{T['title']}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u_name = st.text_input(T["user"]).strip().upper()
        u_pass = st.text_input(T["pass"], type="password").strip()
        if st.button(T["login"], use_container_width=True):
            if u_name == ADMIN_USER.upper() and u_pass == ADMIN_PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("❌ بيانات خاطئة" if st.session_state.lang == "العربية" else "❌ Invalid Data")
    st.stop()

# --- 4. الواجهة الرئيسية (بعد الدخول الناجح) ---
st.sidebar.success(f"Welcome: {ADMIN_USER}")
tab1, tab2 = st.tabs([T["dash"], T["visa"]])

with tab1:
    st.title("📊 Invoice Dashboard")
    # عرض البيانات التاريخية التي ظهرت في صورك
    st.info("أعلى إحصائية مسجلة: 2025-05-03 بمبلغ 2850")
    chart_data = pd.DataFrame({"المبالغ": [2400, 800, 2850]}, index=["أبريل", "مايو 1", "مايو 3"])
    st.bar_chart(chart_data)

with tab2:
    st.title(f"🇪🇺 {T['visa']}")
    country = st.selectbox("اختر دولة الاتحاد الأوروبي:", ["إيطاليا", "فرنسا", "ألمانيا", "إسبانيا", "هولندا"])
    
    uploaded_file = st.file_uploader(T["upload"], type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        st.divider()
        st.subheader(T["result"])
        # هنا يعمل محرك الـ OCR لسحب البيانات آلياً
        # بيانات توضيحية لما يتم سحبه من الجواز
        passport_info = {
            "Surname": "AL-FETORY", "Given Names": "ALI", 
            "Passport No": "P0012345", "Birth Date": "1985-01-01",
            "Expiry Date": "2030-10-10", "Nationality": "LBY"
        }
        st.table(pd.DataFrame([passport_info]))
        
        # تحويل البيانات لملف Word يحاكي النموذج الرسمي
        if st.button(T["download"]):
            doc = Document()
            doc.add_heading(f'Schengen Visa Application Form - {country}', 0)
            for key, val in passport_info.items():
                doc.add_paragraph(f"{key}: {val}")
            
            buffer = io.BytesIO()
            doc.save(buffer)
            st.download_button(
                label="💾 اضغط هنا للحصول على الملف",
                data=buffer.getvalue(),
                file_name=f"Schengen_{country}_{passport_info['Surname']}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if st.sidebar.button("Logout / خروج"):
    st.session_state.auth = False
    st.rerun()
