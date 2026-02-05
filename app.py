import streamlit as st

# إعدادات الصفحة - إلغاء السايدبار نهائياً لمنع الكلمات الغريبة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الثيمات الـ 14 ---
WALLPAPERS = {
    "🌆 باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073",
    "🏛️ روما": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996",
    "🏙️ دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070",
    "🗼 طوكيو": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1974",
    "🎡 لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070",
    "🕌 اسطنبول": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2071",
    "🏖️ المالديف": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=1965",
    "⛰️ سويسرا": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=2070",
    "🗽 نيويورك": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=2070",
    "🏜️ الأهرامات": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?q=80&w=2070",
    "🏮 سور الصين": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?q=80&w=2070",
    "🕌 مراكش": "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?q=80&w=2071",
    "🌊 سانتوريني": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2022",
    "🌉 سان فرانسيسكو": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?q=80&w=2070"
}

if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 🎨 الستايل (تنظيف المسافات وإلغاء المربعات الفاضية) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف المربع الفاضي فوق وأي زوائد تقنية */
    [data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"],
    header, footer, .stAppDeployButton, .st-emotion-cache-6qob1r, .st-emotion-cache-1kyx738,
    .st-emotion-cache-18ni73i, .st-emotion-cache-z5fcl4 {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* إلغاء الفراغ العلوي الميت */
    .block-container {{ padding-top: 0rem !important; }}

    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; direction: rtl; }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* مربع العنوان (محدد ونظيف) */
    .main-title {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 15px; border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center; max-width: 500px;
        margin: 20px auto; color: white;
        font-size: 26px; font-weight: 900;
    }}

    /* بطاقة العمل الشفافة */
    .glass-card {{
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 500px; margin: 0 auto; color: white;
    }}

    input {{ 
        background-color: white !important; color: black !important; 
        border-radius: 8px !important; text-align: center; font-weight: bold !important;
        height: 45px !important;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important; font-weight: bold !important; height: 45px !important;
        border-radius: 10px !important; margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.session_state.bg_choice = st.selectbox("🎨 اختر الثيم:", list(WALLPAPERS.keys()))
        st.divider()
        user = st.text_input("اسم المستخدم").upper()
        passw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول النظام", use_container_width=True):
            if user == "ALI FETORY" and passw == "0925843353":
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- واجهة العمل ---
st.markdown('<div class="main-title">🌍 بوابة المسار الذهبي</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="glass-card" style="max-width: 800px;">', unsafe_allow_html=True)
    st.session_state.bg_choice = st.selectbox("🎨 تغيير الثيم:", list(WALLPAPERS.keys()), key="main_bg")
    st.divider()
    st.subheader("📋 البيانات المطلوبة")
    st.text_input("الاسم واللقب")
    if st.button("خروج", use_container_width=True):
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
