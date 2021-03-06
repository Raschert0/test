from functools import wraps
from flask import request, Response
from pymongo import MongoClient
from db import mclient
import jwt

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    db = mclient.flask_logins
    return db.users.find_one({"login":username,"pass":password})

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Token Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_token(token):
    """This function called to check if a auth token is valid"""
    db = mclient.flask_logins
    return db.users.find_one({'token':bytes(token,'utf-8')})

def forbidden():
    """Sends a 403 response"""
    return Response('403 Forbidden', 403)

def requires_token_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.args.get('auth-token')
        if not auth_token or not check_token(auth_token):
            return forbidden()
        return f(*args, **kwargs)
    return decorated
