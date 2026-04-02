"""
SignAI — ASL Avatar Generator
==============================
Flask backend that converts English text to sign language gloss
and serves the avatar UI.

Usage:
    python app.py
    → Open http://localhost:5000
"""

import os
import sys
from flask import Flask, render_template, request, jsonify

# Import the gloss pipeline (no mediapipe needed)
from isl_english_only import text_to_gloss, BVH_MAP

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/translate", methods=["POST"])
def translate():
    """Accept English text, return ISL gloss tokens."""
    data = request.get_json(silent=True)
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    gloss = text_to_gloss(text)

    return jsonify({
        "original_text": text,
        "gloss": gloss,
        "has_sign": {token: token in BVH_MAP for token in gloss},
    })


@app.route("/api/vocabulary")
def vocabulary():
    """Return the full list of supported sign words."""
    return jsonify({"words": sorted(BVH_MAP.keys())})


if __name__ == "__main__":
    print("\n[SignAI] Avatar Generator")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
