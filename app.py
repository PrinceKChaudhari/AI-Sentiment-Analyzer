from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re

app = Flask(__name__)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity        # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1

    # Sentiment label
    if polarity > 0.3:
        label = "Positive"
        emoji = "😊"
        color = "#00ff41"
    elif polarity < -0.3:
        label = "Negative"
        emoji = "😔"
        color = "#ff006e"
    else:
        label = "Neutral"
        emoji = "😐"
        color = "#ffd700"

    # Emotion detection (simple keyword based)
    text_lower = text.lower()
    if any(w in text_lower for w in ["love", "amazing", "fantastic", "awesome", "great"]):
        emotion = "Joy 🎉"
    elif any(w in text_lower for w in ["hate", "terrible", "awful", "horrible", "worst"]):
        emotion = "Anger 😡"
    elif any(w in text_lower for w in ["sad", "cry", "miss", "lonely", "depressed"]):
        emotion = "Sadness 😢"
    elif any(w in text_lower for w in ["scared", "fear", "afraid", "nervous", "anxious"]):
        emotion = "Fear 😨"
    elif any(w in text_lower for w in ["wow", "surprised", "unexpected", "omg", "unbelievable"]):
        emotion = "Surprise 😲"
    else:
        emotion = "Calm 😌"

    # Word count & sentence count
    word_count = len(text.split())
    sentence_count = len(blob.sentences)

    return {
        "label": label,
        "emoji": emoji,
        "color": color,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "polarity_pct": round((polarity + 1) / 2 * 100, 1),
        "subjectivity_pct": round(subjectivity * 100, 1),
        "emotion": emotion,
        "word_count": word_count,
        "sentence_count": sentence_count,
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = analyze_sentiment(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
