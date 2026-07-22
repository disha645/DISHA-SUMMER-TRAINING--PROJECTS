import streamlit as st
import numpy as np
import pickle

# Set page layout
st.set_page_config(page_title="Smoker Predictor", layout="centered")

st.title("Smoker Prediction App")
st.write("Predict whether a person is a smoker using an **SVM Classifier**.")

def load_model():
    return pickle.load(open("SVM_model.pkl", "rb"))

model = load_model()

st.subheader("Enter Details:")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    sex = st.selectbox("Sex", options=[("Male", 0), ("Female", 1)], format_func=lambda x: x[0])[1]
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)

with col2:
    children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
    charges = st.number_input("Medical Charges ($)", min_value=0.0, value=5000.0, step=500.0)

if st.button("Predict Smoker Status", type="primary"):
    features = np.array([[age, sex, bmi, children, charges]])
    prediction = model.predict(features)[0]

    st.markdown("---")
    if prediction == 1:
        st.error("### Result: **SMOKER**")
    else:
        st.success("### Result: **NON-SMOKER**")
