import os

import openai
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv(verbose=True)
OPEN_API_SECRET_KEY = os.environ.get("OPEN_API_SECRET_KEY")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SIGNIN_SECRET = os.environ.get("SIGNIN_SECRET")
VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN")

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

print("アプリの起動")
app = App(token=SLACK_BOT_TOKEN, signing_secret=SIGNIN_SECRET)
print("アプリの成功")


@app.event("app_mention")
def chatgpt_reply(event, say):
    input_text = event["text"]
    channel = event["channel"]
    print("prompt: " + input_text)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": input_text},
        ],
    )
    text = response["choices"][0]["message"]["content"]
    print("ChatGPT: " + text)

    say(text=text, channel=channel)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
