from flask import Flask, redirect, url_for, session, request
from msal import ConfidentialClientApplication
import uuid

# Autenticação com Microsoft Oauth2
app = Flask(__name__)
app.secret_key = '68f170cb6f230e030cd3353b48666511a7bdc74600576a03'

CLIENT_ID = '67e2167c-bb04-48d3-a10f-e9d9d618ad9d'
CLIENT_SECRET = 's2a8Q~dCSTsX-oPuaZuQSUOcnGjtAIlwv9oyLbWb'
TENANT_ID = '751b9ffa-fe40-4f7f-90a6-e3276de42583'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
REDIRECT_PATH = '/getAToken'
SCOPE = ['User.Read']

@app.route('/')
def index():
    return 'Flask MSAL Example'

@app.route('/login')
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=SCOPE, state=session["state"])
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))

    if 'error' in request.args:
        return "Login failure: " + request.args['error_description']

    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=SCOPE,
            redirect_uri=url_for('authorized', _external=True))
        if "error" in result:
            return "Token failure: " + result["error_description"]
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("index"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

def _build_msal_app(cache=None, authority=None):
    return ConfidentialClientApplication(
        CLIENT_ID, authority=authority or AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for('authorized', _external=True))

def _load_cache():
    return msal.SerializableTokenCache()

def _save_cache(cache):
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5000)