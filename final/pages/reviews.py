import streamlit as st
import json, os, datetime

DATA_FILE = "data/storage.json"
with open(DATA_FILE, "r") as f:
    data = json.load(f)

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please log in first.")
    st.stop()

username = st.session_state["username"]
user_data = data["users"][username]

st.title("📝 Your Reviews & Past Narrations")
st.markdown("<hr>", unsafe_allow_html=True)

# Past Narrations
st.subheader("🎙 Past Narrations")
if user_data["narrations"]:
    for i, n in enumerate(user_data["narrations"], 1):
        st.markdown(f"**{i}.** {n}")
else:
    st.info("No narrations yet.")

# Submit Review
st.subheader("💬 Leave a Review")
review = st.text_area("Write your feedback", height=150)

if st.button("Submit Review"):
    if review.strip():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        user_data["reviews"].append({"review": review.strip(), "timestamp": timestamp})
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        st.success("Thanks for your review! 💖")
    else:
        st.warning("Please write something before submitting.")

# Show Reviews
st.subheader("🗒 Your Reviews")
if user_data["reviews"]:
    for r in user_data["reviews"]:
        st.markdown(f"- *{r['review']}*  _(submitted on {r['timestamp']})_")
else:
    st.info("No reviews yet.")
