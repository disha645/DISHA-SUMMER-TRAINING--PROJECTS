import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="Walmart Holiday Predictor",
    layout="centered"
)

def load_models():
    model = pickle.load(open("KNN-C_model.pkl", "rb"))
    scaler = pickle.load(open("sc_model.pkl", "rb"))
    return model, scaler

try:
    clf, sc = load_models()

    st.title("Walmart Holiday Predictor")
    st.markdown(
        "Predict whether a given week is a **Holiday Week** based on `Weekly_Sales`, `Temperature`, and `CPI`."
    )
    st.divider()

    # Input Form
    st.subheader("Input Features")

    weekly_sales = st.number_input(
        "Weekly Sales ($)", 
        min_value=0.0, 
        value=1600000.0, 
        step=10000.0
    )
    temperature = st.number_input(
        "Temperature (°F)", 
        min_value=-20.0, 
        max_value=120.0, 
        value=42.0, 
        step=0.5
    )
    cpi = st.number_input(
        "Consumer Price Index (CPI)", 
        min_value=0.0, 
        value=211.0, 
        step=0.1
    )

    st.divider()

    if st.button("Predict Holiday Status", type="primary", use_container_width=True):
        input_data = np.array([[weekly_sales, temperature, cpi]])

        scaled_data = sc.transform(input_data)

        prediction = clf.predict(scaled_data)[0]
        prediction_proba = clf.predict_proba(scaled_data)[0]

        if prediction == 1:
            st.success("**Holiday Week** (Holiday Flag = 1)")
        else:
            st.info("**Regular Week** (Holiday Flag = 0)")

except FileNotFoundError:
    st.error("KNN-C_model.pkl` or `sc_model.pkl` missing! Make sure to run the pickle dump cell first.")
