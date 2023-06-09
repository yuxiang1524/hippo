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

line_bot_api = LineBotApi('OVUCwM09c6V1691pfl4XBK0lXwpZKsrv281DKWT39hajiKyVEol83W51QpVnVLqv8SoAZRZh45L4TfdNWfs82bzLwCtg0r7n4EWhLo3uI1DA4K6iqk2hRUwt+rUyhdXrZCdguEp3jSL/ukg42+a6igdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('e47cdd0ecfed15fc78d8a36082f0d4bf')


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
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()