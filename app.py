import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. تحميل الموديل المتجمد (تأكد أن الاسم مطابق للاسم اللي حفظت بيه في النوت بوك)
model = joblib.load('animal_age_model.pkl')

# 2. إعدادات الصفحة والعناوين بالـ English
st.set_page_config(page_title="Possum Age Predictor", page_icon="🐼", layout="centered")

st.title("🐼 Possum Age Predictor App")
st.write("Enter the physical measurements and sex of the possum below to predict its age.")

st.markdown("---") # خط فاصل للشياكة

# تقسيم المدخلات على عمودين عشان التصميم يكون متناسق ومتوازن
col1, col2 = st.columns(2)

with col1:
    hdlngth = st.number_input("Head Length (mm):", min_value=0.0, value=94.1, step=0.1)
    skullw = st.number_input("Skull Width (mm):", min_value=0.0, value=60.0, step=0.1)
    totlngth = st.number_input("Total Length (cm):", min_value=0.0, value=89.0, step=0.1)
    taill = st.number_input("Tail Length (cm):", min_value=0.0, value=36.0, step=0.1)

with col2:
    chest = st.number_input("Chest Girth (cm):", min_value=0.0, value=28.5, step=0.1)
    belly = st.number_input("Belly Girth (cm):", min_value=0.0, value=33.0, step=0.1)
    # اختيار الجنس (الخيارات هتروح للموديل كـ m أو f والبايبلاين هيعملها Encoding)
    sex = st.selectbox("Sex:", options=['m', 'f'], format_func=lambda x: "Male" if x=='m' else "Female")

st.markdown("---")

# 3. زرار التوقع وتشغيل الموديل
if st.button("🔮 Predict Age", use_container_width=True):
    
    # تجميع البيانات في DataFrame بنفس أسماء العواميد اللي الموديل اتدرب عليها بالظبط
    input_data = pd.DataFrame({
        'hdlngth': [hdlngth],
        'skullw': [skullw],
        'totlngth': [totlngth],
        'taill': [taill],
        'chest': [chest],
        'belly': [belly],
        'sex': [sex]
    })
    
    # تشغيل الموديل وعرض النتيجة
    try:
        prediction = model.predict(input_data)
        predicted_age = prediction[0]
        
        # عرض النتيجة بالـ English في مربع أخضر شيك
        st.success(f"🎯 Predicted Age: **{predicted_age:.1f} Years**")
    except Exception as e:
        # عرض خطأ بالـ English لو حصلت مشكلة في المسار أو الموديل
        st.error(f"An error occurred during prediction: {e}")