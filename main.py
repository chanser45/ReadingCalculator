import streamlit as st
import datetime
import json
import os
import hashlib

st.set_page_config(page_title="Reading Tracker App", page_icon="📚")

# File paths
USERS_FILE = "users.json"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load and save user data
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def user_login():
    st.sidebar.header("🔐 Login / Register")
    tab = st.sidebar.radio("Choose an option:", ["Login", "Register"])
    users = load_users()

    if tab == "Register":
        new_user = st.sidebar.text_input("New username")
        new_pass = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Register"):
            if new_user in users:
                st.sidebar.warning("This username already exists.")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.sidebar.success("Registration successful! You can now log in.")

    if tab == "Login":
        user = st.sidebar.text_input("Username")
        pw = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if user in users and users[user] == hash_password(pw):
                st.session_state.user = user
                st.sidebar.success(f"Welcome, {user}!")
            else:
                st.sidebar.error("Incorrect username or password.")

if "user" not in st.session_state:
    user_login()
    st.stop()

# Continue after login
user_id = st.session_state.user
data_path = f"{DATA_DIR}/{user_id}.json"

# Load or initialize user data
if os.path.exists(data_path):
    with open(data_path, "r") as f:
        user_data = json.load(f)
else:
    user_data = {"log": {}}

# Daily input
today = str(datetime.date.today())
pages_read = st.number_input("How many pages did you read today?", min_value=0, step=1)

if st.button("Save"):
    user_data["log"][today] = user_data["log"].get(today, 0) + pages_read
    with open(data_path, "w") as f:
        json.dump(user_data, f)
    st.success(f"Added {pages_read} pages for {today}!")

# Stats calculations
reading_log = user_data.get("log", {})
total_pages = sum(reading_log.values())

days_active = len(reading_log)
avg_daily = total_pages / days_active if days_active > 0 else 0

yearly_estimate = avg_daily * 365
average_book_length = 300
books_per_year = yearly_estimate / average_book_length

st.header("📊 Your Reading Statistics")
st.write(f"Total pages read: **{total_pages}**")
st.write(f"Average pages per day: **{avg_daily:.2f}**")
st.write(f"At this pace, you'll read **{int(yearly_estimate)}** pages or about **{books_per_year:.1f}** books per year.")

# Global comparison
comparison_data = {
    "Average Person (Global)": 12,
    "CEO Average": 60,
    "Bill Gates": 50,
    "UK Average": 15,
    "India Average": 16,
    "Finland Average": 16,
    "France Average": 14,
    "US Average": 17
}

for person, average in comparison_data.items():
    if books_per_year > average:
        st.success(f"You're on track to read more books per year than **{person}**!")

# Motivational messages
if books_per_year >= 20:
    st.balloons()
    st.success("You're doing amazing! If you keep it up, you'll finish more than 20 books a year!")
elif books_per_year >= 10:
    st.info("You're doing well! Looks like you'll read at least 10 books this year.")
else:
    st.warning("Your pace is a bit low, but every page counts. Keep going! 💪")
