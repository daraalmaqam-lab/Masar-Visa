import streamlit as st

# 1. إعدادات الصفحة - إلغاء السايدبار نهائياً لضمان نظافة الواجهة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# --- مكتبة الثيمات الـ 14 كاملة (ثابتة ولا تحذف) ---
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

# تهيئة حالة الجلسة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'bg_choice' not in st.session_state: st.session_state.bg_choice = "🌆 باريس"

# --- 🎨 الستايل المطور (تعديل الألوان وتناسق الخانات) ---
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

    /* العنوان الزجاجي النظيف - لون خط أبيض ناصع مع ظل خفيف ليتناسب مع كل الصور */
    .main-title {{
        background: rgba(255, 255, 255, 0.15); 
        backdrop-filter: blur(20px);
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        max-width: 550px;
        margin: 20px auto; 
        color: #FFFFFF; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-family: 'Cairo', sans-serif;
        font-size: 32px; 
        font-weight: 900; 
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* البطاقة الشفافة الموحدة - لون الخط داخلها يتناسب مع الخلفية */
    .glass-card {{
        background: rgba(0, 0, 0, 0.5); 
        backdrop-filter: blur(15px);
        padding: 40px; 
        border-radius: 25px; 
        max-width: 500px; 
        margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.2); 
        color: white;
    }}

    /* تنسيق الخانات (الاسم والرقم السري) - حجم متناسق ومريح للعين */
    div[data-baseweb="input"] {{
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }}

    input {{ 
        height: 50px !important; 
        font-size: 18px !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        border-radius: 10px !important; 
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #1e3a8a !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
    }}

    /* لون تسمية الخانات (Labels) ليكون متناسق مع كل ثيم */
    label {{
        color: white !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        font-size: 16px !important;
    }}

    /* تنسيق الزر الأزرق الكبير */
    .stButton > button {{
        width: 100% !important; 
        height: 55px !important; 
        font-size: 20px !important;
        font-weight: bold !important; 
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important; 
        border-radius: 12px !important; 
        border: none !important;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- منطق عرض الشاشات ---

if not st.session_state.auth:
    # --- 1. شاشة الدخول (المعدلة) ---
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # اختيار الثيم
        st.session_state.bg_choice = st.selectbox("🎨 اختر واجهة المنظومة:", list(WALLPAPERS.keys()))
        st.divider()
        # خانات الاسم والرقم السري بحجم متناسق
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
    # --- 2. شاشة العمل (ثابتة كما هي بدون تغيير) ---
    st.markdown('<div class="main-title">🌍 لوحة التحكم - المسار الذهبي</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 3, 1])
    with col_b:
        st.markdown('<div class="glass-card" style="max-width: 800px;">', unsafe_allow_html=True)
        st.subheader("📝 نموذج إدخال بيانات المسافر")
        
        c1, c2 = st.columns(2)
        c1.text_input("الاسم الأول")
        c1.text_input("اللقب")
        c2.text_input("رقم الجواز")
        c2.selectbox("دولة الوجهة", ["إيطاليا", "فرنسا", "ألمانيا", "بريطانيا", "أمريكا"])
        
        st.divider()
        col_btns = st.columns(2)
        if col_btns[0].button("✅ حفظ البيانات"):
            st.success("تم حفظ البيانات بنجاح!")
            
        if col_btns[1].button("🚪 تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
