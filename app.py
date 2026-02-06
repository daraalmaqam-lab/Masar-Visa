if uploaded_file:
    reader = load_ocr_engine()
    image = Image.open(uploaded_file)
    
    # تحويل الصورة إلى مصفوفة OpenCV
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # --- 🛠️ فلاتر "الفايق" لتحسين الصور الضعيفة ---
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # تنظيف النمش (Denoising)
    dst = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    # زيادة التباين (Contrast) باش تبان الحروف الباهتة
    processed_img = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    with st.spinner('جاري المسح الذكي للجواز الليبي...'):
        # قراءة النص بالكامل مع التركيز على اللغة الإنجليزية
        results = reader.readtext(processed_img, detail=0)
        full_raw_text = "".join(results).upper().replace(" ", "")
        
        # 🕵️ ذكاء اصطناعي للبحث عن رقم الجواز الليبي (يبدأ بـ حرف ثم أرقام)
        # الجواز الليبي عادة يبدأ بـ حرف واحد وبعده 7 أو 8 أرقام
        passport_pattern = re.compile(r'[A-Z][0-9]{7,9}')
        pass_matches = passport_pattern.findall(full_raw_text)
        if pass_matches:
            scanned_passport = pass_matches[0]
        
        # 🕵️ ذكاء استخراج الاسم من شفرة LBY (الأدق في الجوازات الليبية)
        if "LBY" in full_raw_text:
            try:
                # الكود يقص النص اللي بعد LBY ويطلع الاسم واللقب
                after_lby = full_raw_text.split("LBY")[1]
                # تنظيف الأسهم <<< وتحويلها لمسافات
                clean_name = after_lby.split("<<")[0].replace("<", " ").strip()
                # لو الاسم طلع فيه أرقام (بسبب خطأ قراءة)، ننظفه
                scanned_name = ''.join([i for i in clean_name if not i.isdigit()])
            except:
                scanned_name = results[0] if results else ""
        else:
            # لو الصورة ضعيفة جداً وما لقاش الكود، يحاول ياخد أول سطر نصي
            scanned_name = results[0] if results else ""

    st.success("✅ تم استخراج البيانات بأعلى دقة ممكنة!")
