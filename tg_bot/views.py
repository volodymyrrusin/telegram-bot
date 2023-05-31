from tg_bot import app
from .handlers import *


@app.route('/', methods=["POST"])
def hello():
    if message := request.json.get('message'):
        handler = MessageHandler(message)
    elif callback := request.json.get('callback_query'):
        handler = CallbackHandler(callback)
    handler.handle()
    return 'ok'
