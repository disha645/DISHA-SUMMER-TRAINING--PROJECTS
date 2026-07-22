import streamlit as st
import pickle
import numpy as np
import pandas as pd

model = pickle.load(open("KNN-R_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title("Auto MPG Prediction App")
st.write("Enter the vehicle specifications below to predict Fuel Efficiency (MPG):")

cylinders = st.number_input("Cylinders", min_value=3, max_value=8, value=4, step=1)
acceleration = st.number_input("Acceleration (0-60 mph in seconds)", min_value=5.0, max_value=30.0, value=15.0, step=0.1)
weight = st.number_input("Vehicle Weight (lbs)", min_value=1000, max_value=6000, value=2500, step=10)

if st.button("Predict MPG"):
    features = np.array([[cylinders, acceleration, weight]])

    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]

    st.success(f"Estimated Fuel Efficiency: **{prediction:.2f} MPG**")
