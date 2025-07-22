import uuid
import pandas as pd
import os

DATA_FILE = "user_data.csv"

# Ensure the data file exists
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["User ID", "Name", "Email", "Phone", "Age", "Current Weight (kg)",
                                   "Target Weight (kg)", "Goal Duration (months)", "Daily Calorie Deficit"])
        df.to_csv(DATA_FILE, index=False)

# Generate a unique user ID
def generate_user_id():
    return str(uuid.uuid4())[:8]

# Check if a user already exists based on email or phone
def is_duplicate_user(email, phone):
    if not os.path.exists(DATA_FILE):
        return False
    df = pd.read_csv(DATA_FILE)
    return ((df["Email"] == email) | (df["Phone"] == phone)).any()

# Calculate daily calorie deficit
def calculate_daily_calorie_deficit(current_weight, target_weight, goal_months):
    if goal_months <= 0:
        return 0
    weight_loss = current_weight - target_weight
    if weight_loss <= 0:
        return 0
    total_calories_to_lose = weight_loss * 7700  # 7700 kcal = 1kg fat
    days = goal_months * 30
    return round(total_calories_to_lose / days, 2)

# Save user data to CSV
def save_user_data(user_data):
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
