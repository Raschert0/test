import eventlet
eventlet.monkey_patch()

from requests import Session

from flask import Flask, request, render_template
from flask_socketio import SocketIO, send
from auth import requires_auth, requires_token_auth, forbidden
from datetime import datetime
from sec import sec_levels, sec_phrases, pool
from db import mclient
from bot import bot, API_TOKEN, logger
import jwt
import os
import logging
import telebot
import random
import mglobals

HOST = '18.196.4.151'
URL_LISTEN = '0.0.0.0'
PORT_LISTEN = 8443

WEBHOOK_URL_BASE = "https://%s:%s" % (HOST, PORT_LISTEN)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger.setLevel(logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
@requires_auth
def login():
    user = request.authorization.username
    pwd = request.authorization.password
    #S for Security
    ret = jwt.encode({'login':user,
                      'pass':pwd},
                     'secret', algorithm='HS256')
    db = mclient.flask_logins
    db.users.update({'login':user,'pass':pwd},
                    {"$set" :
                     {'token':ret,
                      'last_request_date':datetime.now()}})
    return ret

@app.route('/admin', methods=['GET'])
@requires_token_auth
def admin():
    print (mglobals.sec_level)
    return render_template('admin.html', sec_level=mglobals.sec_level)

@app.route('/time', methods=['POST'])
@requires_token_auth
def ctime():
    return datetime.now().strftime("%a (%d) %b %Y : %H-%M-%S")

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return forbidden()

@socketio.on('message')
def handle_message(message):
    print ('received message: ' + message)
    if(message == 'NextSecLevel'):
        mglobals.sec_level = next(pool)
        print(mglobals.sec_level)
        send(mglobals.sec_level, broadcast=True)

def randPhrase():
    print(mglobals.sec_level)
    max_r = 5
    if mglobals.sec_level == sec_levels[1]:
        max_r = 8
    elif mglobals.sec_level == sec_levels[2]:
        max_r = 11

    r = random.randint(1, max_r - 1)
    print (r)
    return sec_phrases[r]
        
if __name__ == '__main__':
    print (WEBHOOK_URL_PATH)
    mglobals.sec_level = next(pool)
    random.seed();

    keys_dir = os.path.join(os.getcwd(), 'keys')
    key = os.path.join(keys_dir, 'private.key')
    cert = os.path.join(keys_dir, 'cert.pem')

    socketio.run(app, log_output=True, host='0.0.0.0', port=8443, keyfile = key, certfile = cert)
