import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment

# Environment variables for IBM Watson
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")

# Initialize IBM TTS client
authenticator = IAMAuthenticator(IBM_TTS_APIKEY)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(IBM_TTS_URL)


def synthesize_speech(text, voice="Allison", soundscape_name=None):
    """
    Generate speech from text using IBM Watson TTS.
    Optionally mixes with a soundscape from soundscapes/ folder.
    """
    OUTPUT_FILE = "audiobook.mp3"

    # Clean text and prepare SSML (no pitch to avoid errors)
    clean_text = text.strip().replace("\n", ". ")
    ssml_text = f"<speak>{clean_text}</speak>"

    # Generate narration
    with open(OUTPUT_FILE, 'wb') as audio_file:
        audio_file.write(
            tts.synthesize(
                ssml_text,
                voice=f"en-US_{voice}V3Voice",  # Ensure correct IBM voice format
                accept='audio/mp3'
            ).get_result().content
        )

    # If no soundscape selected, return the generated audio
    if not soundscape_name or soundscape_name.lower() == "none":
        return OUTPUT_FILE

    # Mix with soundscape
    try:
        narration = AudioSegment.from_file(OUTPUT_FILE, format="mp3")
        soundscape_file = os.path.join("soundscapes", f"{soundscape_name.lower()}.mp3")

        if os.path.exists(soundscape_file):
            soundscape = AudioSegment.from_file(soundscape_file, format="mp3")
            # Loop soundscape to match narration length
            soundscape = soundscape * (len(narration) // len(soundscape) + 1)
            mixed = narration.overlay(soundscape - 15)  # Lower soundscape volume
            mixed.export(OUTPUT_FILE, format="mp3")
        else:
            print(f"⚠ Soundscape '{soundscape_name}' not found. Using narration only.")
    except Exception as e:
        print(f"Error mixing soundscape: {e}")

    return OUTPUT_FILE
