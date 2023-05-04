from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('otXONelmYjey10XyTKIrTX7E/TVfGs9v7vzKtX/vWfSw+jPyW3RwYRbMIx0ybe718SoAZRZh45L4TfdNWfs82bzLwCtg0r7n4EWhLo3uI1DSYcsGua7wVXnm/ocBBY7NN+fg9hUpY sFNOuCkC5oi/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e47cdd0ecfed15fc78d8a36082f0d4bf')


@app.route("/")
def home():
    return "LINE BOT API Server is running"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()