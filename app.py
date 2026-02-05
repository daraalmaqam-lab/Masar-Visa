import streamlit as st
from docx import Document
import io, requests, subprocess, uuid

# --- 1. نظام الحماية الذكي المعتمد على البصمة ---
def get_secure_id():
    try:
        # المحاولة الأولى: بصمة الويندوز الأصلية
        cmd = 'wmic csproduct get uuid'
        result = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        if result and "0000" not in result: return result
    except: pass
    # المحاولة الثانية: بصمة العتاد (الهاردوير)
    return str(uuid.getnode())

# --- القائمة البيضاء: الأجهزة المسموح لها فقط ---
ALLOWED_DEVICES = [
    "4CDC17BF-BCD5-11E8-B386-F43909279CED", # جهاز الزبون
    "52792806964878"                         # جهازك أنت (المفتاح الفعلي)
]

current_id = get_secure_id()

# فحص الترخيص قبل تشغيل أي شيء
if current_id not in ALLOWED_DEVICES:
    st.title("🔐 نظام الحماية المركزية")
    st.error("عذراً، هذه النسخة غير مرخصة للعمل على هذا الجهاز.")
    st.info(f"بصمة الجهاز: {current_id}")
    st.stop()

# --- 2. واجهة المنظومة (شركة المسار الذهبي) ---
st.set_page_config(page_title="منظومة المسار الذهبي", layout="wide")

st.markdown(f"""
    <div style="background-color: #007bff; padding: 25px; border-radius: 15px; color: white; text-align: center; border: 3px solid #facc15;">
        <h1 style='margin:0;'>🏛️ منظومة الشنغن العالمية</h1>
        <p style='margin:5px;'>إصدار مرخص وحصري | شركة المسار الذهبي</p>
    </div>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state['data'] = {'f_name':"", 'l_name':"", 'p_num':"", 'b_date':"", 'nat':"", 'expiry':""}

# --- 3. محرك القراءة الآلي ---
st.subheader("📸 معالجة جواز السفر")
uploaded_file = st.file_uploader("ارفع صورة الجواز هنا", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    if st.button("🔍 سحب البيانات آلياً"):
        with st.spinner("جاري التحليل طبقاً للمعايير الدولية..."):
            files = {'file': ('img.jpg', uploaded_file.getvalue(), 'image/jpeg')}
            # محرك OCR العالمي
            r = requests.post('https://api.ocr.space/parse/image', files=files, data={'apikey': 'K88186596388957', 'OCREngine': 2}).json()
            if r.get("OCRExitCode") == 1:
                text = r["ParsedResults"][0]["ParsedText"]
                lines = [l.replace(" ", "").upper() for l in text.split('\n') if "<" in l and len(l) > 30]
                if len(lines) >= 2:
                    l1, l2 = lines[-2], lines[-1]
                    st.session_state['data']['l_name'] = l1[5:].split("<<")[0].replace("<", " ").strip()
                    st.session_state['data']['f_name'] = l1[5:].split("<<")[1].replace("<", " ").strip() if "<<" in l1 else ""
                    st.session_state['data']['p_num'] = l2[0:9].replace("<", "")
                    st.session_state['data']['nat'] = l1[2:5]
                    b = l2[13:19]
                    st.session_state['data']['b_date'] = f"{b[4:6]}/{b[2:4]}/19{b[0:2]}" if int(b[0:2]) > 30 else f"{b[4:6]}/{b[2:4]}/20{b[0:2]}"
                    e = l2[21:27]
                    st.session_state['data']['expiry'] = f"{e[4:6]}/{e[2:4]}/20{e[0:2]}"
                st.success("✅ تمت المعالجة بنجاح!")

# --- 4. عرض البيانات وإصدار الوورد ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    fn = st.text_input("الاسم الأول والوسط:", value=st.session_state['data']['f_name'])
    ln = st.text_input("اللقب:", value=st.session_state['data']['l_name'])
with col2:
    pn = st.text_input("رقم الجواز:", value=st.session_state['data']['p_num'])
    bd = st.text_input("تاريخ الميلاد:", value=st.session_state['data']['b_date'])

def create_doc():
    doc = Document()
    doc.add_heading('Schengen Visa Application Data', 0)
    table = doc.add_table(rows=4, cols=2); table.style = 'Table Grid'
    items = [("First Name", fn), ("Last Name", ln), ("Passport", pn), ("Date of Birth", bd)]
    for i, (k, v) in enumerate(items):
        table.cell(i, 0).text = k; table.cell(i, 1).text = str(v)
    buf = io.BytesIO(); doc.save(buf); buf.seek(0); return buf

if st.button("📄 توليد مستند الوورد"):
    st.download_button("⬇️ اضغط للتحميل", create_doc(), f"Visa_{fn}.docx")