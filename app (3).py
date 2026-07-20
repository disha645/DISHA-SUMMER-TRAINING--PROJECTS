import streamlit as st
import pickle
import numpy as np

@st.cache_resource
def load_model():
    with open("Linearmodel.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("PM 2.5 Prediction App")
st.write("Enter the weather details below to predict the **PM 2.5** levels:")

col1, col2 = st.columns(2)

with col1:
    T = st.number_input("Temperature (T)", value=25.0, step=0.1)
    H = st.number_input("Humidity (H)", value=60.0, step=1.0)
    VV = st.number_input("Visibility (VV)", value=1.5, step=0.1)

with col2:
    SLP = st.number_input("Sea Level Pressure (SLP)", value=1013.0, step=0.1)
    VM = st.number_input("Maximum Sustained Wind Speed (VM)", value=10.0, step=0.1)

if st.button("Predict PM 2.5"):
    features = np.array([[T, H, VV, SLP, VM]])
    prediction = model.predict(features)

    st.success(f"Predicted PM 2.5: **{prediction[0]:.2f}**")
