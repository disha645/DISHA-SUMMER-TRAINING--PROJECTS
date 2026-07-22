import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Loan Prediction App", layout="centered")

st.title("🏦 Bank Loan Eligibility Predictor")
st.write("Enter the customer details below to predict whether they will apply for/take a loan.")

def load_model():
    with open('random_forest_model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

with st.form("prediction_form"):
    st.subheader("Customer Information")

    age = st.number_input("Age", min_value=18, max_value=100, value=35, step=1)
    balance = st.number_input("Account Balance ($)", value=1000, step=50)

    housing = st.selectbox(
        "Has Housing Loan?", 
        options=["No", "Yes"],
        index=0
    )

    deposit = st.selectbox(
        "Has Term Deposit?", 
        options=["No", "Yes"],
        index=0
    )

    submit_button = st.form_submit_button("Predict Loan Status")

housing_val = 1 if housing == "Yes" else 0
deposit_val = 1 if deposit == "Yes" else 0

if submit_button:
    input_data = pd.DataFrame([[balance, age, housing_val, deposit_val]], 
                              columns=['balance', 'age', 'housing', 'deposit'])

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.markdown("---")
    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("**High Likelihood:** Customer is likely to take a loan!")
    else:
        st.info("**Low Likelihood:** Customer is unlikely to take a loan.")
