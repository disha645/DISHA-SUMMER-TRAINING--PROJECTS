import streamlit as st
import pickle
import pandas as pd

@st.cache_resource # This caches the model so it doesn't reload on every interaction
def load_model():
    with open('rf_model.pkl', 'rb') as file:
        return pickle.load(file)

try:
    model = load_model()
except FileNotFoundError:
    st.error("Error: 'rf_model.pkl' not found. Make sure the model file is in the same directory as this script.")
    st.stop()

st.title("🏋️‍♂️ Body Fat Percentage Predictor")
st.write("Enter your physical details and workout habits to estimate your body fat percentage using our Random Forest model.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    height = st.number_input("Height (in meters)", min_value=1.00, max_value=2.50, value=1.70, step=0.01)
    weight = st.number_input("Weight (in kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)

with col2:
    workout_freq = st.number_input("Workout Frequency (days/week)", min_value=0, max_value=7, value=3, step=1)

st.divider()

if st.button("Predict Fat Percentage", type="primary"):
    # Streamlit inputs must be formatted into a DataFrame with the exact column 
    # names that the model saw during training (from cell [35])
    input_data = pd.DataFrame({
        'Height (m)': [height],
        'Weight (kg)': [weight],
        'Workout_Frequency (days/week)': [workout_freq]
    })

    # Generate prediction
    prediction = model.predict(input_data)[0]

    # Display the result beautifully
    st.success(f"### Estimated Fat Percentage: {prediction:.2f}%")
    st.balloons() # Adds a fun animation on success!



