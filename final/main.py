import streamlit as st
import bcrypt
import json
import os

st.set_page_config(page_title="EchoVerse - Login", page_icon="🎧", layout="centered")

USER_FILE = "users.json"

# Load or create users file
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

with open(USER_FILE, "r") as f:
    users = json.load(f)

st.title("🎧 EchoVerse")
st.subheader("Stories that speak, Emotions that echo")

tab_login, tab_signup = st.tabs(["Login", "Signup"])

with tab_login:
    username_login = st.text_input("Username")
    password_login = st.text_input("Password", type="password")
    if st.button("Login"):
        if username_login in users and bcrypt.checkpw(password_login.encode('utf-8'), users[username_login].encode('utf-8')):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_login
            st.switch_page("pages/echoverse.py")
        else:
            st.error("❌ Invalid username or password.")

with tab_signup:
    username_signup = st.text_input("Choose a username")
    password_signup = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Sign Up"):
        if password_signup != confirm_password:
            st.error("❌ Passwords do not match.")
        elif username_signup in users:
            st.warning("⚠ Username already exists.")
        else:
            hashed_pw = bcrypt.hashpw(password_signup.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            users[username_signup] = hashed_pw
            with open(USER_FILE, "w") as f:
                json.dump(users, f)
            st.success("✅ Account created! Please login now.")
