from flask import Flask,request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters ,CommandHandler

from PyDictionary import PyDictionary
from gtts import gTTS

#from langdetect import detect

from os import remove

file_id=int(0)

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

def say_handler(bot,update):
    if len(str(update.message.text[5:]))>200:
        update.message.reply_text("文字太長(上限為200字)")
        return
    global file_id
    file_path='./'+str(file_id)+'.mp3'
    file_id+=1;
    engine = gTTS(text=str(update.message.text[5:]),lang='zh-tw')#lang=detect(str(update.message.text[5:])))
    engine.save(file_path)
    update.message.reply_audio(audio=open(file_path,'rb'))
    remove(file_path)

dispatcher.add_handler(CommandHandler("echo", echo_handler))
dispatcher.add_handler(CommandHandler("dict", dict_handler))
dispatcher.add_handler(CommandHandler("say", say_handler))
#dispatcher.add_handler()

if __name__ == "__main__":
    app.run(port=5000)

