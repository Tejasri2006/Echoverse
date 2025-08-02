import random

def rewrite_text(original_text, tone="Neutral"):
    tone_prompts = {
        "Happy": [
            "Joy dances in every word, lifting the story with warmth and light.",
            "Each moment feels alive, like the world is smiling with you."
        ],
        "Sad": [
            "The air feels heavy, carrying a soft ache in every sentence.",
            "Every line drips with quiet sorrow, like rain on glass."
        ],
        "Inspiring": [
            "A spark ignites in the heart, pushing every moment to soar.",
            "The story breathes hope, lifting its reader beyond the ordinary."
        ],
        "Dramatic": [
            "Each word lands with the weight of destiny, echoing in silence.",
            "Moments collide with intensity, demanding the world’s attention."
        ],
        "Suspenseful": [
            "Every pause feels alive, as though the shadows themselves are listening.",
            "A quiet tension coils in the air, daring you to read the next word."
        ],
        "Romantic": [
            "The air hums with unspoken feelings, soft and magnetic.",
            "Every glance lingers, draped in warmth and longing."
        ],
        "Neutral": [
            "The words flow with clarity, steady and unadorned.",
            "A calm, balanced narration carries the story forward."
        ]
    }

    chosen_line = random.choice(tone_prompts.get(tone, tone_prompts["Neutral"]))
    return f"{chosen_line}"
