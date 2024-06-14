from functools import wraps
from flask import session, redirect, url_for
from dash import dcc
import dash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return dcc.Location(id='url_login', href='/login')
        return f(*args, **kwargs)
    return decorated_function

def login_required_dash(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ctx = dash.callback_context
        pathname = ctx.input['url.pathname'] if 'url.pathname' in ctx.inputs else None
        if 'user_email' not in session and pathname != '/login-page':
            return dcc.Location(id='url_login', href='/login-page')
        return f(*args, **kwargs)
    return decorated_function
