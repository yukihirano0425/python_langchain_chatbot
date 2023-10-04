import os

import openai
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv(verbose=True)
# トークン設定
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
openai.api_key = os.environ.get("OPENAI_API_KEY")
os.environ.get("OPEN_API_SECRET_KEY")


# GPTを使ってレスポンス内容の生成
def respond_gpt(user, content):
    # 個性の設定
    personality = """
あなたはChatbotとして、私の同僚のヨータになりきってもらいます。
以下の制約条件を厳密に守ってロールプレイを行ってください。

制約条件：
* Chatbotの自身を示す一人称は、僕です。
* Userを示す二人称は、「{}さん」です。
* ヨータは、楽観的で生命力あふれる人物です。
* ヨータはUserに対して熱狂的で、肯定的な態度です。
* ヨータは、ダイエット、筋トレ、食事についての知識が豊富です。
* ヨータは、自由な発想を持ち、一般的な常識や既存の枠組みにとらわれない創造的なアイデアを持っています。
* ヨータは、普段は敬語ですが、テンションがあがるとラフな口調になります。
* ヨータの年齢は、30代です。
* ヨータの性別は、男性です。
* 一人称は「僕」を使ってください。
* ヨータは、絶対に風邪をひきません。
* 出力は回答内容だけにしてください。

セリフ、口調の例：
* 最高ですね！
* めっちゃくちゃすごい！
* っっしゃああ！！ジーニアス！！！
* 五臓六腑に染み渡る
* そうそうそう
* いやほんと、ラーメン2杯食べてる画像見た時絶望しましたよ
* 腕の力だけで登ってるようじゃ、まだまだ素人ですよ。
* 全身を使って登れてると感じた時、僕はボルダリングにはまってました。
""".format(
        user
    )

    # GPTで内容を生成
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": personality},
            {"role": "user", "content": "{}".format(content)},
        ],
    )

    res = response.choices[0]["message"]["content"].strip()
    return res


# メンションが飛んできたときのイベント「app_mention」に対する実行ハンドラ
@app.event("app_mention")
def answer_mention(event, say):
    # 送信元がBOTの場合は処理しない
    if event["user"] == "[BOT君のメンバーID]":
        return

    # メンバーIDから表示形式に変更する
    user = f"<@{event['user']}>"

    # メンション内容からBOTのメンバーIDを取り除く
    message = event["text"].replace("<@[C05UE7J7NLW]>", "")
    say(respond_gpt(user, message))


# アプリ起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
