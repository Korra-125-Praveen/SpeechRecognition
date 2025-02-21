def analyze_keywords(text):
    scam_keywords = ["free money", "lottery", "urgent", "IRS", "bank details", "scam"]
    return [word for word in scam_keywords if word in text.lower()]

def analyze_emotion(audio_path):
    # Placeholder for future ML-based emotion analysis
    return "neutral"
