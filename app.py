import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(page_title="Fasting Blood Sugar Predictor", page_icon="🩺", layout="centered")

st.title("🩺 Fasting Blood Sugar Prediction App")
st.write("This app uses a Logistic Regression model to predict whether fasting blood sugar is > 120 mg/dl.")

def load_model():
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()

st.subheader("Enter Input Parameters:")

sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female (0)" if x == 0 else "Male (1)")
cp = st.selectbox("Chest Pain Type (cp)", options=[0, 1, 2, 3], help="0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic")
exang = st.selectbox("Exercise Induced Angina (exang)", options=[0, 1], format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")

if st.button("Predict", type="primary"):
    # Format input into 2D array
    features = np.array([[sex, cp, exang]])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    st.markdown("---")
    st.subheader("Prediction Result:")

    if prediction == 1:
        st.error(f"⚠️ Predicted FBS > 120 mg/dl (High Risk)")
    else:
        st.success(f"✅ Predicted FBS ≤ 120 mg/dl (Normal)")

    st.write(f"**Confidence / Probability Breakdown:**")
    st.write(f"- Class 0 (Normal): `{probabilities[0]*100:.2f}%`")
    st.write(f"- Class 1 (High FBS): `{probabilities[1]*100:.2f}%`")
