import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- 🌆 مكتبة الثيمات (روابط مباشرة تفتح فوراً) ---
WALLPAPERS = {
    "طرابلس - المدينة القديمة": "https://p4.wallpaperbetter.com/wallpaper/705/170/364/libya-tripoli-castle-wallpaper-preview.jpg",
    "لبدة الكبرى": "https://p4.wallpaperbetter.com/wallpaper/408/382/1000/leptis-magna-libya-wallpaper-preview.jpg",
    "جنوب ليبيا - أوباري": "https://p4.wallpaperbetter.com/wallpaper/137/954/337/dunes-lake-libya-palm-trees-wallpaper-preview.jpg",
    "باريس": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073", 
    "روما": "https://images.unsplash.com/photo-1529260830199-42c24126f198?q=80&w=2076", 
    "دبي": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070", 
    "لندن": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=2070"
}

# تهيئة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "طرابلس - المدينة القديمة"

# وظيفة التحديث الفوري
def update_bg():
    st.session_state.bg_choice = st.session_state.new_bg

# --- 🎨 الستايل (الخانات 50% والزر 85% ثابتة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed;
    }}

    .main-title {{
        background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 15px; text-align: center; max-width: 500px;
        margin: 15px auto; color: white; font-family: 'Cairo'; font-size: 28px; font-weight: 900;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    .glass-card {{
        background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(15px);
        padding: 35px; border-radius: 25px; max-width: 500px; margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.2); color: white;
        display: flex; flex-direction: column; align-items: center;
    }}

    [data-testid="stTextInput"], [data-testid="stSelectbox"] {{
        width: 50% !important; 
        margin: 0 auto !important;
    }}

    input {{
        height: 42px !important; font-size: 16px !important; text-align: center !important;
        border-radius: 8px !important; background-color: white !important; color: black !important;
    }}

    label {{
        color: white !important; font-weight: bold !important; font-size: 14px !important;
        text-align: center !important; width: 50% !important; display: block !important; margin: 5px auto !important;
    }}

    .stButton > button {{
        width: 85% !important; 
        height: 55px !important; 
        font-size: 22px !important;
        font-weight: 900 !important; 
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important; 
        border-radius: 15px !important; 
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        display: block !important; 
        margin: 30px auto !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # اختيار الثيم وتحديث فوري
        st.selectbox("🎨 اختر واجهة المنظومة:", list(WALLPAPERS.keys()), 
                     index=0, key="new_bg", on_change=update_bg)
        
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
    # شاشة العمل
    st.markdown('<div class="main-title">🌍 لوحة التحكم - المسار الذهبي</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 3, 1])
    with col_b:
        st.markdown('<div class="glass-card" style="max-width: 800px;">', unsafe_allow_html=True)
        st.subheader("📝 نموذج إدخال بيانات المسافر")
        c1, c2 = st.columns(2)
        c1.text_input("الاسم الأول")
        c1.text_input("اللقب")
        c2.text_input("رقم الجواز")
        c2.selectbox("دولة الوجهة", ["إيطاليا", "فرنسا", "ألمانيا"])
        st.divider()
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
