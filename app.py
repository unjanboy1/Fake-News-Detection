from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("models/fake_news_model.joblib")
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    user_msg = data.get("message", "")

    if not user_msg.strip():
        return jsonify({"error": "Please enter some text!"})

    if len(user_msg.split()) < 20:
        return jsonify({"error": "⚠️ Minimum 20 words required for deep analysis."})

    # Preprocessing (same as training)
    clean_msg = user_msg.lower().replace('\n', ' ')

    vec = vectorizer.transform([clean_msg])

    proba = model.predict_proba(vec)[0]

    def smooth(p):
        p = max(min(p, 0.95), 0.05)
        return round(p * 100, 2)

    fake_conf = smooth(proba[0])
    real_conf = smooth(proba[1])

    # Smart threshold
    if proba[0] >= 0.85:
        label = "FAKE NEWS 🟥"
    elif proba[1] >= 0.85:
        label = "REAL NEWS 🟩"
    else:
        label = "⚠️ UNCERTAIN / MIXED"

    return jsonify({
        "label": label,
        "fake": fake_conf,
        "real": real_conf
    })


if __name__ == "__main__":
    app.run(debug=True)