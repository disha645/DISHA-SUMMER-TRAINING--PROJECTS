import streamlit as st
import joblib
import pandas as pd

model = joblib.load("fraudmodel.pkl")
joblib.dump(model, "fraudmodel.pkl")  # Save the model to a fil

st.set_page_config(
    page_title="credit card fraud detection",
    layout="centered"
)
st.title("Credit Card Fraud Detection")
st.write("Enter the transaction details")

V1 = st.number_input(
    "V1",
    min_value=-10.0,
    max_value=10.0,
    value=0.0
)
V2 = st.number_input(
    "V2",
    min_value=-10.0,
    max_value=10.0,
    value=0.0
)
V3 = st.number_input(
    "V3",
    min_value=-10.0,
    max_value=10.0,
    value=0.0
)
V4 = st.number_input(
    "V4",
    min_value=-10.0,
    max_value=10.0,
    value=0.0
)
if st.button("Predict"):
    input_data = pd.DataFrame(
        [[
            V1,
            V2,
            V3,
            V4
        ]],
        columns=[
            "V1",
            "V2",
            "V3",
            "V4"
        ]
    )
    input_data = {
        'V1': [V1],
        'V2': [V2],
        'V3': [V3],
        'V4': [V4]
    }
    prediction = model.predict(input_data)
    if prediction[0] == 0:
        st.success("The transaction is not fraudulent.")
    else:
        st.error("The transaction is fraudulent.")
