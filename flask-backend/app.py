import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

load_dotenv(verbose=True)
OPEN_API_SECRET_KEY = os.environ.get("OPEN_API_SECRET_KEY")
BOT_TOKEN = os.environ.get("OAuth_Access_Token")
SLACK_SIGNIN_SECRET = os.environ.get("CLIENT_SECRET")

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)
slack_app = App(token=BOT_TOKEN, signing_secret=SLACK_SIGNIN_SECRET)
handler = SlackRequestHandler(slack_app)


@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"Key": "text_1", "Value": [1, 2, 3]}

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
