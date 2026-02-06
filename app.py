# --- القارئ الذكي المطور (تعديل المخ فقط) ---
if uploaded_file:
    reader = load_reader()
    image = Image.open(uploaded_file)
    # تحويل الصورة إلى مصفوفة ومعالجتها لتحسين الحروف
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # زيادة حدة الصورة (Sharpness) باش الحروف الصغيرة تبان
    processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    with st.spinner('جاري التحليل الذكي...'):
        # قراءة النص بالكامل
        results = reader.readtext(processed_img, detail=0)
        full_text = " ".join(results).upper().replace(" ", "")
        
        # 1. البحث عن رقم الجواز (نمط ذكي: حرف + 7 أو 8 أرقام)
        import re
        passport_match = re.search(r'[A-Z][0-9]{7,9}', full_text)
        if passport_match:
            pass_val = passport_match.group()
        
        # 2. البحث عن الاسم (المنظومة ذكية توا: تبحث عن الحروف اللي بعد كلمة P<LBY)
        # الجواز الليبي فيه كود P<LBY، الاسم يجي بعدها طول
        if "LBY" in full_text:
            name_part = full_text.split("LBY")[1]
            # تنظيف الاسم من الرموز الزايدة (<<<)
            name_val = name_part.split("<<")[0].replace("<", " ").strip()
        else:
            # لو ما لقاش الكود، ياخد أول سطرين كالعادة
            name_val = results[0] if len(results) > 0 else ""

    st.success("تمت القراءة بدقة!")
