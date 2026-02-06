# ... (باقي الكود العلوي وشاشة الدخول كما هو بدون تغيير) ...

# ================== 4. شاشة لوحة التحكم (التعديل هنا) ==================
else:
    # ستايل خاص بلوحة التحكم باش يخلي كل شيء في النص
    st.markdown("""
    <style>
    /* تنسيق حاوية لوحة التحكم */
    .dashboard-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        margin-top: 50px;
    }
    
    .dashboard-title {
        color: #fbbf24;
        font-family: 'Cairo', sans-serif;
        font-size: 50px;
        font-weight: 900;
        text-shadow: 3px 3px 10px black;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    # وضع المحتوى داخل الحاوية المركزية
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-title">🌍 لوحة التحكم الذكية</div>', unsafe_allow_html=True)
    
    # هنا تقدر تضيف أزرار أو عمليات وتلقائياً حتجي في النص
    st.write("---")
    
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
