from flask import request

from tg_bot import app
from tg_bot.handlers.message_handler import *
from tg_bot.handlers.callback_handler import *


@app.route('/', methods=["POST"])
def hello():
    if message := request.json.get('message'):
        handler = MessageHandler(message)
    elif callback := request.json.get('callback_query'):
        handler = CallbackHandler(callback)
    handler.handle()
    return 'ok'
