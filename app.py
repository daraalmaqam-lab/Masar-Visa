import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Golden Path", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🎨 الستايل الذهبي (توسيط احترافي وعزل كامل)
# =========================================================
if not st.session_state.auth:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        
        /* إخفاء الزوائد */
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .stApp { 
            background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070"); 
            background-size: cover; background-position: center; background-attachment: fixed;
        }

        /* 🎯 حاوية التوسيط المطلق */
        [data-testid="stVerticalBlock"] {
            position: absolute !important;
            top: 50% !important; left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 100% !important;
            max-width: 450px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
        }

        .main-title {
            text-align: center; color: #fbbf24; font-family: 'Cairo'; 
            font-size: 55px; font-weight: 900; text-shadow: 4px 4px 10px black;
            margin-bottom: 30px; width: 100%;
        }

        /* 🏷️ تنسيق العناوين (اسم المستخدم / كلمة المرور) */
        .custom-label {
            color: white; font-family: 'Cairo'; font-size: 24px; font-weight: 700;
            text-align: center; width: 100%; margin-bottom: 8px; margin-top: 15px;
            text-shadow: 2px 2px 5px black;
        }

        /* ✍️ تنسيق المربعات (لضمان بقائها في المنتصف) */
        div[data-baseweb="input"] {
            height: 45px !important; width: 320px !important; 
            margin: 0 auto !important; background-color: rgba(255, 255, 255, 0.9) !important; 
            border-radius: 12px !important; border: 2px solid #fbbf24 !important;
        }
        
        input { text-align: center !important; color: #333 !important; font-size: 18px !important; font-weight: bold !important; }

        /* 🔘 زر الدخول */
        .stButton button {
            height: 55px !important; width: 220px !important; 
            background-color: #fbbf24 !important; color: black !important; 
            font-weight: bold !important; font-family: 'Cairo' !important;
            font-size: 22px !important; margin-top: 35px !important;
            border-radius: 15px !important; box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
        }
        </style>
        """, unsafe_allow_html=True)
else:
    # تنسيق لوحة التحكم (نظيف وعملي)
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] { position: static !important; transform: none !important; width: 100% !important; max-width: 100% !important; display: block !important; }
        .stApp { background-image: none !important; background-color: #f4f7f6 !important; }
        .booking-card { background: white; padding: 30px; border-radius: 15px; border-top: 5px solid #fbbf24; box-shadow: 0 4px 15px rgba(0,0,0,0.1); direction: rtl; }
        </style>
        """, unsafe_allow_html=True)

# =========================================================
# 🏠 محتوى التطبيق
# =========================================================

if not st.session_state.auth:
    # الشاشة الرئيسية
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
            st.error("البيانات غير صحيحة")
else:
    # لوحة التحكم - نموذج الحجز
    st.markdown("<h1 style='text-align:center; font-family:Cairo; color:#2c3e50;'>🌍 منظومة الحجز المبدئي</h1>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<div class="booking-card">', unsafe_allow_html=True)
        st.write("### 📝 نموذج حجز طيران وفندق")
        
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("اسم المسافر (بالإنجليزي كما في الجواز)")
            p_no = st.text_input("رقم الجواز")
        with c2:
            dest = st.text_input("الوجهة")
            b_date = st.date_input("تاريخ السفر")
        
        st.write("---")
        if st.button("✅ إصدار نموذج الحجز"):
            st.success(f"تم حجز طلب مبدئي لـ {p_name}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
