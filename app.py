from flask import Flask, request
import requests

TOKEN = "8246279346:AAH1ElgTACfc-bBV21MsZPcjOEo-9mNEOmY"   # <-- yaha apna token daalo
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # --- Bot ka logic (simple echo) ---
        reply = f"👋 You said: {text}"

        # Reply bhejna
        requests.post(URL, json={"chat_id": chat_id, "text": reply})

    return "ok", 200


# Local testing ke liye (PythonAnywhere me zaroori nahi)
if __name__ == "__main__":
    app.run(debug=True)
