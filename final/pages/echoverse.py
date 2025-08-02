import streamlit as st
import os
from services.ibm_tts import synthesize_speech
from services.tone_rewrite import rewrite_text
import json
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="EchoVerse", page_icon="🎧", layout="centered")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #fbeaff 0%, #d8e8ff 100%);
}

/* Text inputs & textareas */
textarea, .stTextInput input {
    color: #333333 !important; 
    font-weight: 500;
    background-color: #ffffffee !important;
    border-radius: 8px;
    border: 1px solid #b8b8b8;
}

/* Labels */
label, .stTextInput label, .stTextArea label {
    color: #4D2D52 !important;
    font-weight: 600;
    font-size: 1rem;
}

/* Titles */
h1, h2, h3 {
    color: #4D2D52 !important;
    font-family: 'Georgia', serif;
    text-shadow: 0px 0px 2px #ffffffaa;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #e8b6ff 0%, #a6baff 100%);
    color: #2c2c2c;
    font-weight: bold;
    border-radius: 8px;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #d39cff 0%, #8ea6ff 100%);
}

/* Radio Label Text */
div[data-baseweb="radio"] > div {
    color: #4D2D52 !important;
    font-weight: 600;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center;'>EchoVerse</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#4D2D52;'>Stories that Speak, Emotions that Echo</h4>", unsafe_allow_html=True)

# ---------- USER DATA FILE ----------
if not os.path.exists("user_data.json"):
    with open("user_data.json", "w") as f:
        json.dump({}, f)

with open("user_data.json", "r") as f:
    user_data = json.load(f)

username = st.session_state.get("username", "guest")
if username not in user_data:
    user_data[username] = {"narrations": []}

# ---------- INPUT SECTION ----------
st.subheader("📥 Upload or Enter Your Story")
uploaded_file = st.file_uploader("Drag and drop a .txt file", type=["txt"])
user_text = ""
if uploaded_file:
    user_text = uploaded_file.read().decode("utf-8")
else:
    user_text = st.text_area("Or write/paste your text here:", height=150)

voice_gender = st.radio("Select Voice Gender", ["Female", "Male"])

voice_options = {
    "Female": ["Allison", "Lisa", "Olivia"],
    "Male": ["Michael", "James", "Henry"]
}
voice = st.selectbox("Choose Voice", voice_options[voice_gender])

tone = st.selectbox("Select Tone", [
    "Happy", "Sad", "Inspiring", "Dramatic", "Suspenseful", "Romantic", "Neutral"
])

include_soundscape = st.checkbox("Include a soundscape in audio?")
soundscape = st.selectbox("Choose Soundscape", [
    "None", "Rain", "Forest", "Seashore", "Piano", "Birds", "Fire"
])

# ---------- GENERATE AUDIO ----------
if st.button("🎧 Generate Audio"):
    if not user_text.strip():
        st.error("Please provide some text first!")
    else:
        with st.spinner("Rewriting and generating audio..."):
            # Rewrite text in selected tone
            rewritten = rewrite_text(user_text, tone=tone)

            # Combine text to ensure continuity in TTS
            final_text = (user_text.strip() + ". " + rewritten.strip()).replace("\n", ". ")

            # Generate audio
            audio_file = synthesize_speech(
                final_text,
                voice=voice,
                soundscape_name=(soundscape if include_soundscape and soundscape != "None" else None)
            )

            time.sleep(1)
            st.success("✅ Audio generated successfully!")

            # Display original & rewritten text side by side
            col1, col2 = st.columns(2)
            with col1:
                st.text_area("Original Text", user_text, height=200)
            with col2:
                st.text_area("Rewritten Text", rewritten, height=200)

            # Play audio
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

            # Download button
            st.download_button("⬇ Download MP3", data=audio_bytes, file_name="audiobook.mp3", mime="audio/mp3")

            # Save narration history
            user_data[username]["narrations"].append(user_text[:100] + "...")
            with open("user_data.json", "w") as f:
                json.dump(user_data, f)

# ---------- VIEW PAST NARRATIONS ----------
if st.button("📜 View Past Narrations"):
    st.subheader("Your Past Narrations:")
    narrations = user_data.get(username, {}).get("narrations", [])
    if narrations:
        for i, n in enumerate(narrations, 1):
            st.markdown(f"**{i}.** {n}")
    else:
        st.info("No past narrations yet!")
