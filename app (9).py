import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Customer Segmentation App", layout="centered")

st.title("Customer Cluster Predictor")
st.write("Enter the customer details below to predict their cluster assignment.")
def load_models():
    with open('kmeans_model.pkl', 'rb') as f:
        kmeans = pickle.load(f)
    with open('sr.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return kmeans, scaler

try:
    kmeans, scaler = load_models()

    st.subheader("Customer Details")

    genre = st.selectbox("Gender", options=["Female", "Male"])
    age = st.slider("Age", min_value=18, max_value=100, value=30)
    income = st.number_input("Annual Income (k$)", min_value=0, max_value=200, value=50)

    genre_val = 1 if genre == "Female" else 0

    if st.button("Predict Cluster", type="primary"):
        input_data = pd.DataFrame([[genre_val, age, income]], 
                                  columns=['Genre', 'Age', 'Annual Income (k$)'])

        scaled_data = scaler.transform(input_data)
        cluster = kmeans.predict(scaled_data)[0]

        st.success(f"### Predicted Cluster: **Cluster {cluster}**")

        st.info(f"Customer profile: **{genre}**, **{age} years old**, making **${income}k/year**.")

except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.warning("Make sure 'kmeans_model.pkl' and 'sr.pkl' are saved in the current directory.")
