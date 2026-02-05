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

# --- 🎨 الستايل النهائي المعتمد (ثابت ولا يحذف) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء كل مسببات الكلمات الغريبة والزوائد */
    header, footer, .stAppDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    .stApp {{
        background-image: url("{WALLPAPERS[st.session_state.bg_choice]}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* العنوان الزجاجي النظيف */
    .main-title {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        padding: 20px; border-radius: 15px; text-align: center; max-width: 550px;
        margin: 20px auto; color: white; font-family: 'Cairo', sans-serif;
        font-size: 30px; font-weight: 900; border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    /* البطاقة الشفافة الموحدة */
    .glass-card {{
        background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px);
        padding: 40px; border-radius: 25px; max-width: 500px; margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.1); color: white;
    }}

    /* تنسيق الخانات الكبيرة والخط الواضح */
    input {{ 
        height: 55px !important; font-size: 20px !important; text-align: center !important; 
        font-weight: bold !important; border-radius: 12px !important; background-color: white !important;
    }}

    /* تنسيق الزر الأزرق */
    .stButton > button {{
        width: 100% !important; height: 55px !important; font-size: 20px !important;
        font-weight: bold !important; background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: white !important; border-radius: 12px !important; border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- منطق عرض الشاشات (فصل كامل) ---

if not st.session_state.auth:
    # --- 1. شاشة الدخول فقط ---
    st.markdown('<div class="main-title">🏛️ بوابة المسار الذهبي</div>', unsafe_allow_html=True)
    col1, col_mid, col2 = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.session_state.bg_choice = st.selectbox("🎨 اختر واجهة المنظومة:", list(WALLPAPERS.keys()))
        st.divider()
        user_input = st.text_input("اسم المستخدم").upper()
        pass_input = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            # التحقق من بياناتك المحفوظة
            if (user_input == "ALI FETORY" or user_input == "ALI") and pass_input == "0925843353":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة!")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- 2. شاشة العمل (تظهر فقط بعد نجاح الدخول) ---
    st.markdown('<div class="main-title">🌍 لوحة التحكم - المسار الذهبي</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 3, 1])
    with col_b:
        st.markdown('<div class="glass-card" style="max-width: 800px;">', unsafe_allow_html=True)
        st.subheader("📝 نموذج إدخال البيانات")
        
        c1, c2 = st.columns(2)
        c1.text_input("الاسم الأول")
        c1.text_input("اللقب")
        c2.text_input("رقم الجواز")
        c2.selectbox("دولة الوجهة", ["إيطاليا", "فرنسا", "ألمانيا", "بريطانيا"])
        
        st.divider()
        col_btns = st.columns(2)
        if col_btns[0].button("✅ حفظ البيانات"):
            st.success("تم حفظ بيانات المسافر بنجاح!")
            
        if col_btns[1].button("🚪 تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
