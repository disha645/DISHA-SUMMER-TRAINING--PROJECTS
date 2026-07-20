import streamlit as st
import pickle
import numpy as np

with open('decision_tree_classifier_model.pkl', 'rb') as file:
    clf = pickle.load(file)

st.title("Titanic Survival Prediction App")
st.write("Enter passenger details below to predict survival probability.")

pclass = st.selectbox("Passenger Class (Pclass)", options=[1, 2, 3], index=2)
sex_label = st.radio("Sex", options=["Male", "Female"])
age = st.slider("Age", min_value=0, max_value=80, value=28)
sex = 1 if sex_label == "Female" else 0

if st.button("Predict Survival"):
    input_data = np.array([[pclass, sex, age]])
    prediction = clf.predict(input_data)[0]

    if prediction == 1:
        st.success("Outcome: **Survived**")
    else:
        st.error("Outcome: **Did Not Survive**")
