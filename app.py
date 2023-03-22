from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai

app = Flask(__name__)

# LINE Messaging APIのチャネルアクセストークンとチャネルシークレットを環境変数から取得する
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

# APIキーをセットアップする
openai.api_key = os.environ["OPENAI_API_KEY"]

# LINE Messaging APIからのメッセージを受け取るエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# テキストメッセージが送信されたときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #ユーザーから送られてきた文章
    line_event_message=event.message.text
    # line_event_message=line_event_message.replace("\n","")
    # line_event_message=line_event_message.replace(" ","")

    # GPT-3に対するプロンプトを作成する
    prompt_message='''\
    #命令
    後述の条件を必ず守った上で、入力された文章に改行を入れて出力して下さい。

    #条件(優先順)
    1位：文章が読みやすい。
    2位：1行あたりの文字数が必ず16文字以下である。
    3位：品詞と品詞の間で改行する。
    4位：1行あたりの文字数が10文字以上である。

    #入力
    {text}

    #出力
    '''.format(text=line_event_message)

    # GPT-3に対してテキスト生成をリクエストする
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_message,
        temperature=0, # ランダム性の制御[0-1]
        max_tokens=2000, # 返ってくるレスポンストークンの最大数
        top_p=1.0, # 多様性の制御[0-1]
        frequency_penalty=0.0, # 周波数制御[0-2]：高いと同じ話題を繰り返さなくなる
        presence_penalty=0.0 # 新規トピック制御[0-2]：高いと新規のトピックが出現しやすくなる
    )

    # LINE Messaging APIに送信するテキストメッセージを作成する 
    reply_text = response.choices[0].text.replace(" ", "")
    reply_message = TextSendMessage(text=reply_text)

    # LINE Messaging APIにメッセージを送信する
    line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run(port=8888)
