import streamlit as st
import pandas as pd
import uuid
from utils import calculate_calorie_deficit, save_user_data, user_exists

# Load existing data
try:
    user_data = pd.read_csv("user_data.csv")
except FileNotFoundError:
    user_data = pd.DataFrame(columns=["User ID", "Name", "Email", "Phone", "Current Weight", "Goal Weight", "Goal Months", "Calories to Burn"])

st.title("🏋️ Weight Goal Tracker")
st.subheader("Register to track your fitness journey")

with st.form("registration_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    weight_now = st.number_input("Current Weight (kg)", min_value=1.0, step=0.5)
    goal_weight = st.number_input("Goal Weight (kg)", min_value=1.0, step=0.5)
    months = st.number_input("Time to reach goal (in months)", min_value=1)

    submitted = st.form_submit_button("Register")

    if submitted:
        if user_exists(email, phone, user_data):
            st.error("🚫 A user with this email or phone already exists.")
        else:
            user_id = str(uuid.uuid4())[:8]
            calories_to_burn = calculate_calorie_deficit(weight_now, goal_weight)

            new_entry = {
                "User ID": user_id,
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Current Weight": weight_now,
                "Goal Weight": goal_weight,
                "Goal Months": months,
                "Calories to Burn": calories_to_burn
            }

            user_data = save_user_data(new_entry, user_data)
            st.success(f"✅ Registration successful! Your User ID is: {user_id}")
            st.info(f"To reach your goal, you need to burn approximately {calories_to_burn} kcal.")
