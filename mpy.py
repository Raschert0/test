from flask import Flask, request
from auth import requires_auth, requires_token_auth
from pymongo import MongoClient
import jwt
from datetime import datetime

app = Flask(__name__)

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
    cl = MongoClient()
    db = cl.flask_logins
    db.users.update({'login':user,'pass':pwd},
                    {"$set" :
                     {'token':ret,
                      'last_request_date':datetime.now()}})
    return ret

@app.route('/time', methods=['POST'])
@requires_token_auth
def ctime():
    return datetime.now().strftime("%a (%d) %b %Y : %H-%M-%S")

