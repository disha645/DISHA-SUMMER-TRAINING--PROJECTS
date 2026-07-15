import streamlit as st
import pandas as pd
import pickle

def load_model():
    with open('decision_tree_model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

st.title("🫁 Lung Cancer Risk Predictor")
st.write("Enter the patient's details below to assess lung cancer risk.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    smoking_years = st.number_input("Smoking Years", min_value=0, max_value=100, value=5, step=1)
    cigarettes_per_day = st.number_input("Cigarettes per Day", min_value=0, max_value=100, value=10, step=1)

with col2:
    air_pollution_index = st.number_input("Air Pollution Index", min_value=0, max_value=500, value=60, step=1)
    exercise_hours = st.number_input("Exercise (Hours/Week)", min_value=0, max_value=50, value=3, step=1)

st.divider()

if st.button("Predict Risk", type="primary"):
    input_data = pd.DataFrame({
        'smoking_years': [smoking_years],
        'cigarettes_per_day': [cigarettes_per_day],
        'air_pollution_index': [air_pollution_index],
        'exercise_hours_per_week': [exercise_hours]
    })

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("### ⚠️ High Risk Detected")
        st.write("The model indicates a high risk of lung cancer based on these metrics.")
    else:
        st.success("### ✅ Low Risk Detected")
        st.write("The model indicates a lower risk of lung cancer. Keep up the healthy habits!")
