import logging
import time
import datetime
import flask
import telebot
#from parser import url
from config import token
import schedule
import threading
#import db_question

url='https://d4a82955d0f6.ngrok.io'
API_TOKEN = token
WEBHOOK_URL_BASE = url                                                      #https://6dc3bd5fa35c.ngrok.io
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)                                     #/1131808189:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])              #WEBHOOK_URL_PATH='/xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx/'
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(content_types=['text'])
def send_text(message):
    pass


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(1)
# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# Start flask server
app.run(debug=True)
