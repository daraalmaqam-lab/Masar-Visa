import streamlit as st

# 1. إعدادات الصفحة (ثبات كامل)
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل (عزل احترافي لضمان عدم التغير)
# =========================================================
if not st.session_state.auth:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .stApp { 
            background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
            background-size: cover; background-position: center; 
        }
        [data-testid="stVerticalBlock"] {
            position: absolute !important; top: 50% !important; left: 50% !important;
            transform: translate(-50%, -50%) !important; width: 100% !important;
            max-width: 450px !important; display: flex !important;
            flex-direction: column !important; align-items: center !important;
        }
        .main-title { text-align: center; color: #fbbf24; font-family: 'Cairo'; font-size: 50px; font-weight: 900; text-shadow: 3px 3px 6px black; margin-bottom: 20px; }
        .custom-label { color: white; font-family: 'Cairo'; font-size: 20px; font-weight: 700; text-align: center; width: 100%; margin-bottom: 5px; text-shadow: 2px 2px 4px black; }
        div[data-baseweb="input"] { height: 45px !important; width: 320px !important; margin: 0 auto !important; background-color: white !important; border-radius: 10px !important; border: 2px solid #fbbf24 !important; }
        input { text-align: center !important; color: black !important; font-size: 18px !important; }
        .stButton button { height: 50px !important; width: 200px !important; background-color: #fbbf24 !important; color: black !important; font-weight: bold; border-radius: 12px !important; margin-top: 20px !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; display: block !important; }
        .stApp { background-image: none !important; background-color: #f8f9fa !important; }
        .booking-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-right: 8px solid #fbbf24; direction: rtl; }
        h1, h3 { font-family: 'Cairo' !important; }
        </style>
        """, unsafe_allow_html=True)

# =========================================================
# 🏠 المحتوى
# =========================================================
if not st.session_state.auth:
    # شاشة الدخول الثابتة
    st.markdown('<div class="main-title">طيران المسار الذهبي</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-label">اسم المستخدم</div>', unsafe_allow_html=True)
    u = st.text_input("u", label_visibility="collapsed", key="u_login").upper()
    st.markdown('<div class="custom-label">كلمة المرور</div>', unsafe_allow_html=True)
    p = st.text_input("p", type="password", label_visibility="collapsed", key="p_login")
    
    if st.button("دخول للنظام"):
        if (u == "ALI" or u == "ALI FETORY") and p == "0925843353":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات خاطئة")
else:
    # لوحة التحكم: نموذج الحجز المبدئي (نظيفة وسريعة)
    st.markdown("<h1 style='text-align:center; color:#2c3e50;'>📋 إصدار نموذج حجز مبدئي</h1>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 4, 1])
    
    with center_col:
        st.markdown('<div class="booking-card">', unsafe_allow_html=True)
        st.markdown("### 📝 بيانات المسافر والرحلة")
        
        col_a, col_b = st.columns(2)
        with col_a:
            p_name = st.text_input("اسم المسافر بالكامل (كما في الجواز)")
            p_no = st.text_input("رقم جواز السفر")
            p_nation = st.text_input("الجنسية", value="Libyan")
        with col_b:
            b_type = st.selectbox("نوع الحجز المبدئي", ["حجز طيران", "حجز فندقي", "حجز طيران + فندق"])
            dest = st.text_input("الوجهة (من - إلى)")
            b_date = st.date_input("تاريخ السفر")

        st.write("---")
        notes = st.text_area("ملاحظات إضافية")

        if st.button("✅ حفظ وإصدار النموذج"):
            st.success(f"تم تسجيل الحجز المبدئي بنجاح لـ {p_name}")
            st.balloons()
            
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
