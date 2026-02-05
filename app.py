import streamlit as st

# 1. إعدادات الصفحة (إخفاء السايدبار تماماً لقتل كلمة keyboard_double)
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الثيمات ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974"
}

if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل (تنظيف شامل) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء كل مسببات الكلمات الغريبة والزوائد */
    [data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"],
    header, footer, .stAppDeployButton, .st-emotion-cache-6qob1r, .st-emotion-cache-1kyx738 {{
        display: none !important;
        visibility: hidden !important;
    }}

    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: rtl; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* المربع الزجاجي للعنوان */
    .glass-header {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center; max-width: 600px;
        margin: 30px auto; color: white;
        font-size: 28px; font-weight: 900;
    }}

    /* البطاقة الشفافة */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        padding: 35px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 450px; margin: 0 auto; color: white;
    }}

    input {{ 
        background-color: white !important; color: black !important; 
        border-radius: 8px !important; text-align: center; font-weight: bold !important;
        height: 45px !important;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important; font-weight: bold !important; height: 50px !important;
        border-radius: 10px !important; border: none !important; margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- شاشة الدخول (بدون المربع الأسود المزعج) ---
if not st.session_state.auth:
    st.markdown('<div class="glass-header">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # تم حذف مربع اختيار الثيم من هنا بناءً على طلبك
        user = st.text_input("اسم المستخدم").upper()
        passw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول النظام", use_container_width=True):
            if user == "ALI FETORY" and passw == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- واجهة العمل (تظهر بعد الدخول فقط) ---
st.markdown('<div class="glass-header">🌍 بوابة المسار الذهبي</div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 4, 1])
with col_b:
    st.markdown('<div class="glass-card" style="max-width: 1000px;">', unsafe_allow_html=True)
    
    # الثيمات تظهر هنا فقط بعد الدخول لضمان نظافة الواجهة الأولى
    st.session_state.bg_choice = st.selectbox("🎨 تغيير الثيم:", list(WALLPAPERS.keys()))
    
    st.divider()
    c1, c2 = st.columns(2)
    c1.text_input("اللقب")
    c1.text_input("الاسم")
    c2.text_input("رقم الجواز")
    
    if st.button("🚪 خروج", use_container_width=True):
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
