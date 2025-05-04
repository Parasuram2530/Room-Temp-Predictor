import pandas as pd
import pickle
import streamlit as st

scalar = pickle.load(open('scaler.pkl', 'rb'))
ridge_model = pickle.load(open('ridge.pkl', 'rb'))
feature_columns = pickle.load(open('featureColumns.pkl', 'rb'))

st.title("Room Temperature Predictor")
st.write("Predict room temperature based on environmental features")


st.header("Input Parameters")
time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
outside_temp = st.slider("Outside Temperature (°C)", 10.0, 50.0, 25.0)
num_people = st.slider("Number of People in Room", 0, 10, 2)
fan_on = st.checkbox("Fan On", value=True)
ac_on = st.checkbox("AC On", value=False)
window_open = st.checkbox("Window Open", value=False)
room_size = st.selectbox("Room Size", ["Small", "Medium", "Large"])

input_dict = {
    'time_of_day': time_of_day,
    'outside_temp': outside_temp,
    'num_of_people_in_room': num_people,
    'fan_on': 1 if fan_on else 0,
    'ac_on': 1 if ac_on else 0,
    'window_open': 1 if window_open else 0,
    'room_size': room_size
}

if st.button("Predict Room Temperasture"):
    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df)
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[feature_columns]
    scaled_input = scalar.transform(input_df)
    prediction = ridge_model.predict(scaled_input)
    if prediction[0]>35:
        st.warning(f"Predicted Room Temperature : {prediction[0]:.1f} °C")
    else:
        st.success(f"Predicted Room Temperature : {prediction[0]:.1f} °C")

    st.subheader("Interpretation")
    if prediction[0] > 30:
        st.warning("Room temperature is high! Consider turning on AC or opening windows.")
    elif prediction[0] < 20:
        st.info("Room temperature is low. You might want to turn off cooling devices.")
    else:
        st.success("Comfortable room temperature detected!")