from flask import Flask,request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters ,CommandHandler

from PyDictionary import PyDictionary

bot_token="<token is hidden,contact admin>"

bot = telegram.Bot(token=bot_token)

app=Flask(__name__)

dictionary = PyDictionary()


@app.route("/webhook/chenlitw_bot",methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

dispatcher = Dispatcher(bot, None)

def echo_handler(bot,update):
    update.message.reply_text(update.message.text[6:])

def dict_handler(bot,update):
    update.message.reply_text(str(dictionary.meaning(str(update.message.text[6:]))))

dispatcher.add_handler(CommandHandler("echo", echo_handler))
dispatcher.add_handler(CommandHandler("dict", dict_handler))
#dispatcher.add_handler()

if __name__ == "__main__":
    app.run(port=5000)
