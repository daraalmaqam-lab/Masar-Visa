import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🌆 مكتبة الثيمات العالمية ---
WALLPAPERS = {
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076", 
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070", 
    "لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070",
    "اسطنبول": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2071"
}

if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "باريس"

def update_bg():
    st.session_state.bg_choice = st.session_state.new_bg

# --- 🎨 الستايل (ضبط اليمين والخط 23) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl !important;
    }}

    .main-title {{
        background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 15px; text-align: center; max-width: 500px;
        margin: 20px auto; color: white; font-family: 'Cairo' !important; font-size: 28px !important; font-weight: 900 !important;
        border: 2px solid rgba(255, 255, 255, 0.4);
    }}

    .glass-card {{
        background: rgba(0, 0, 0, 0.65); backdrop-filter: blur(15px);
        padding: 40px; border-radius: 30px; max-width: 550px; margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.2); color: white;
        text-align: right !important; /* إجبار المحاذاة لليمين */
    }}

    /* تعديل العناوين: حجم 23، يمين، سطر واحد */
    [data-testid="stWidgetLabel"] p {{
        font-size: 23px !important;
        font-family: 'Cairo' !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: right !important;
        direction: rtl !important;
        width: 100% !important;
        display: block !important;
        white-space: nowrap !important;
        margin-bottom: 8px !important;
    }}

    /* محاذاة حاويات الإدخال لليمين */
    [data-testid="stTextInput"], [data-testid="stSelectbox"], .stSelectbox {{
        width: 80% !important; 
        margin-right: 0 !important; /* الالتصاق باليمين */
        margin-left: auto !important;
        text-align: right !important;
    }}

    input {{
        height: 45px !important; font-size: 18px !important; text-align: center !important;
        border-radius: 8px !important;
    }}

    .stButton > button {{
        width: 100% !important; 
        height: 60px !important; 
        font-size: 22px !important;
        font-weight: 900 !important; 
        font-family: 'Cairo' !important;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        color: black !important; border-radius: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    st.markdown('<div class="main-title">🛂 طيران المسار الذهبي ✈️</div>', unsafe_allow_html=True)
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # التأكد من الترتيب من اليمين
        st.selectbox("ثيمات", list(WALLPAPERS.keys()), index=0, key="new_bg", on_change=update_bg)
        user_input = st.text_input("اسم المستخدم").upper()
        pass_input = st.text_input("كلمة المرور", type="password")
        
        if st.button("دخول للنظام"):
            if (user_input == "ALI FETORY" or user_input == "ALI") and pass_input == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-title">🌍 لوحة التحكم - المسار الذهبي</div>', unsafe_allow_html=True)
    # كود الصفحة الداخلية...
