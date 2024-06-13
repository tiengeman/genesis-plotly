import base64
import os
from flask import Flask, render_template, redirect, url_for, session, request,send_from_directory
from msal import ConfidentialClientApplication, SerializableTokenCache
import uuid
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pages.gerencial as gerencial
import pages.home as home
import pages.diretoria as diretoria
import pages.relacao as relacao
import pages.cadastro_projetos as cadastro_projetos
import pages.impostos as impostos
import pages.login as login
import pages.registro as registro
import pages.user as user
from constants import *
from dash.exceptions import PreventUpdate
import dash
import dash_bootstrap_components as dbc
from banco import *
from back.inserts import *
from back.msal_login import *
from back.models import *
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from flask import send_from_directory
import datetime

# Constants
# logo = 'https://i0.wp.com/engeman.net/wp-content/uploads/2024/04/LOGO_ENGEMAN_HORIZONTAL-e1714498268589.png?w=851&ssl=1'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

#  UPLOAD_DIRECTORY = os.environ.get('UPLOAD_DIRECTORY', 'uploaded_images')


CLIENT_ID = '67e2167c-bb04-48d3-a10f-e9d9d618ad9d'
CLIENT_SECRET = 's2a8Q~dCSTsX-oPuaZuQSUOcnGjtAIlwv9oyLbWb'
TENANT_ID = '751b9ffa-fe40-4f7f-90a6-e3276de42583'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
REDIRECT_PATH = '/getAToken'
SCOPE = ['User.Read']

# Conteúdo dentro do menu
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Gerencial', href='/gerencial', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Diretoria', href='/diretoria', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Relação', href='/relacao', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Cadastro Projetos', href='/cadastro_projetos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Impostos', href='/impostos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Registro', href='/registro', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Usuário', href='/user', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Login', href='/login', className='nav-link')),
    ],
    vertical=True,
    pills=True,
)

# Botão para abrir o menu
offcanvas = html.Div(
    [
        dbc.Button(
            html.I(className="bi bi-list"),
            id="open-offcanvas",
            n_clicks=0,
            size="md",
            color='#FF4E00',
            style={"font-size": "1.60em"},
            className='btn-white',
        ),
        dbc.Offcanvas(
            sidebar,
            id="offcanvas",
            title="Menu",
            is_open=False,
        ),
    ]
)

user_button = dbc.Button(  # ir para página de login
    html.I(className="bi bi-person-circle"),
    id="user-button",
    n_clicks=0,
    size="md",
    color='#FFFFFF',
    style={"font-size": "1.60em", "color": "#FFFFFF"},
    className='btn-white',
)

# Top navigation bar
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(offcanvas, width="auto"),
                    dbc.Col(
                        # html.A(
                        #     html.Img(src=logo, height="60px"),
                        #     href="/home",
                        #     style={"textDecoration": "none"}
                        # ),
                        width="auto"
                    ),
                ],
                align="center",
                className="g-0",
            ),
            dbc.Row(
                dbc.Col(user_button, width="auto", className="ml-auto"),
                align="center",
                className="g-0"
            )
        ],
        fluid=True,
    ),
    color=colors['orange'],
    dark=True,
    className='justify-content-between',
    style={'height': '50px'}
)

# Div onde mostra o conteúdo de cada página
content_area = html.Div(id='content')

# Layout geral, cabeçalho + content area
app.layout = html.Div([
    header,
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(content_area),
    ]),
])

# Rotas de autenticação Microsoft
@server.route('/loginms')
def login_ms():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=SCOPE, state=session["state"])
    return redirect(auth_url)

@server.route(REDIRECT_PATH)
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

        email = result["id_token_claims"]["unique_name"]
        username = email.split("@")[0]
        user = get_user(email)
        if user:
            session["user"] = result.get("id_token_claims")
            _save_cache(cache)
        else:
            create_user(email, username, "", "Microsoft")
            session["user"] = result.get("id_token_claims")
            _save_cache(cache)
        
    return redirect(url_for("index"))

@server.route('/logout')
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
    cache = SerializableTokenCache()
    if session.get('token_cache'):
        cache.deserialize(session['token_cache'])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session['token_cache'] = cache.serialize()

## Função para obter URL de autenticação na página de login
def initiate_microsoft_login():
    with server.test_request_context():
        session["state"] = str(uuid.uuid4())
        auth_url = _build_auth_url(scopes=SCOPE, state=session["state"])
        return auth_url



#====================================================================== Callbacks ================================================================================================

# Callback para mudar de página de acordo com o menu
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def update_content(pathname):
    if pathname == '/gerencial':
        return gerencial.layout
    elif pathname == '/diretoria':
        return diretoria.layout
    elif pathname == '/relacao':
        return relacao.layout
    elif pathname == '/cadastro_projetos':
        return cadastro_projetos.layout
    elif pathname == '/impostos':
        return impostos.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/registro':
        return registro.layout
    elif pathname == '/user':
        return user.layout
    else:
        return home.layout

def update_table(output_id, value):
    if output_id == 'tabela-container':
        return gerencial.atualizar_tabela(value)
    elif output_id == 'tabela2-container':
        return gerencial.atualizar_tabela2(value)
    
# Callback para redirecionar para a página de login quando o botão for clicado
@app.callback(
    Output('url', 'pathname'),
    Input('user-button', 'n_clicks')
)
def go_to_login(n_clicks):
    if n_clicks:
        return '/login'
    return None

# Callback para atualizar as tabelas gerenciais de acordo com a competência
@app.callback(
    Output('tabela-container', 'children'),
    Output('tabela2-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def update_tables(value):
    return update_table('tabela-container', value), update_table('tabela2-container', value)

# Callback para abrir o menu
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Callback para abrir o modal de cadastro de projetos
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback para salvar itens do cadastro
@app.callback(
    [
        Output("message-modal", "is_open"),
        Output("message-modal-header", "children"),
        Output("message-modal-body", "children"),
    ],
    [
        Input("close-centered", "n_clicks"),
        Input("close-message-modal", "n_clicks"),
    ],
    [
        State("OS", "value"), State("TIPO", "value"), State("ENQUADRAMENTO", "value"),
        State("CLIENTE", "value"), State("DESCRIÇÃO", "value"), State("ICJ", "value"),
        State("SAP", "value"), State("INÍCIO", "value"), State("FIM", "value"),
        State("ADITIVOS", "value"), State("VALOR", "value"), State("PRAZOMES", "value"),
        State("PRAZODIAS", "value"), State("STATUS", "value"), State("RESPONSÁVEL", "value"),
        State("FILIAL", "value"), State("PROJETO", "value"), State("PROJETO SAPIENS", "value"),
        State("ISS", "value"), State("ADM CENTRAL", "value"), State("PIS", "value"),
        State("COFINS", "value"), State("CSLL", "value"), State("IRPJ", "value"),
        State("INVESTIMENTOS", "value"), State("ICMS", "value"),
    ],
)
def update_message_modal(submit_clicks, close_clicks, os, tipo, enq, cliente, desc, icj, sap, inicio, fim, adt, valor, prazom,
                         prazod, status, resp, filial, projeto, projsap, iss, admcentral, pis,
                         cofins, csll, irpj, invest, icms):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "close-centered":
        if submit_clicks:
            lista_input = [os, tipo, enq, cliente, desc, icj, sap, inicio, fim, adt, valor, prazom,
                           prazod, status, resp, filial, projeto, projsap, iss, admcentral, pis,
                           cofins, csll, irpj, invest, icms]
            message = enviar_contratos(lista_input)
            if "sucesso" in message.lower():
                return True, "Sucesso!", message
            else:
                return True, "Erro!", message
        else:
            raise dash.exceptions.PreventUpdate
    elif triggered_id == "close-message-modal":
        return False, "", ""
    else:
        raise dash.exceptions.PreventUpdate

# Callback para deixar apenas algumas colunas editáveis na tela de cadastro de projetos
@app.callback(
    Output('tabela-projetos', 'columns'),
    Input('edit-switch', 'value')
)
def toggle_editability(value):
    columns = [{"name": i, "id": i, "editable": value} if i not in ["VALOR", "PRAZOMES", "PRAZODIAS"] else {"name": i, "id": i} for i in cad_contratos().columns]
    return columns

# Callback para atualizar a tabela quando o botão for clicado
@app.callback(
    Output('tabela-projetos', 'data'),
    [Input('refresh-button-contratos', 'n_clicks')]
)
def update_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_contratos = cad_contratos()
        # Retorne os dados atualizados da tabela
        return df_contratos.to_dict('records')

# Callback para atualizar a tabela de impostos quando o botão for clicado
@app.callback(
    Output('tabela-impostos', 'data'),
    [Input('refresh-button-impostos', 'n_clicks')]
)
def update_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_impostos = cad_impostos()
        # Retorne os dados atualizados da tabela
        return df_impostos.to_dict('records')


# ============================================== CALLBACKS DA TELA CADASTRO =========================================================== 
@app.callback(
    Output('output-message-cadastro', 'children'),
#    Output('url', 'pathname'),
    [Input('register-button', 'n_clicks')], # [Input('fzlogin-button', 'n_clicks_fz')],
    [State('nome', 'value'), State('email', 'value'), State('senha', 'value'), State('confirmar-senha', 'value'), State('setor', 'value')]

)
def register_user(n_clicks, nome, email, senha, confirmar_senha, setor):
    if n_clicks > 0:
        if not nome or not email or not senha or not confirmar_senha or not setor:
            return 'Por favor, preencha todos os campos.'

        if senha != confirmar_senha:
            return 'As senhas não coincidem. Por favor, tente novamente.'

        try:
            client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
            db = client['Project']
            users_collection = db['Usuários']
            
            # Verificar se o email já está registrado
            if users_collection.find_one({"email": email}):
                return 'Email já registrado. Por favor, faça o login.'

            # Gerar hash da senha
            hashed_senha = sha256_crypt.hash(senha) #Dê certo, pfv eu preciso largar

            user_document = {
                'nome': nome,
                'email': email, 
                'senha': hashed_senha, #hash.senha
                'setor': setor
            }
            result = users_collection.insert_one(user_document)
            print("Documento inserido:", result)
            return '/home' #, 'Cadastro realizado com sucesso!' #redireciona para a página inicial com sessão ativa
        except Exception as e:
            return f'Erro ao realizar o cadastro: {e}'
        
    raise PreventUpdate
    # return '', None

# def fzlogin_button(n_clicks_fz):
#     if n_clicks_fz:
#         return '/login'
#     return None


# CALLBACK DA TELA DE PERFIL DO USUÁRIO ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° 
@app.callback(
    Output('user-data', 'children'),
    [Input('url', 'pathname')]
)
def load_user_data(pathname):
 
    if pathname == '/user' and 'user_email' in session:
        client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
        db = client['Project']
        collection = db['Usuários']
        user = collection.find_one({"email": session['user_email']})
        
        if user:
            profile_pic = user.get('profile_pic', None)
            profile_pic_div = html.Div()
            if profile_pic:
                profile_pic_div = html.Img(src=profile_pic, style={'border-radius': '50%', 'width': '150px', 'height': '150px'})

            return html.Div([
                profile_pic_div,
                html.P(f"Nome: {user['nome']}"),
                html.P(f"Email: {user['email']}"),
                html.P(f"Setor: {user['setor']}")
            ])
        return None
# CALLBACK PARA UPLOAD DA IMAGEM 

external_stylessheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

@app.callback(
    Output('output-image-upload','children'),
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename')]
)

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
# def upload_output(content, filename):
#     if content is not None:
#         data = content.encode("utf8").split(b";base64,")[1]
#         file_path = os.path.join(UPLOAD_DIRECTORY, filename)

#         with open(file_path, "wb") as fh:
#             fh.write(base64.decodebytes(data))

#         client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
#         db = client['Project']
#         collection = db['Usuários']
#         profile_pic = f'/uploaded_images/{filename}'
#         collection.update_one({'email': session['user_email']}, {'$set': {'profile_pic': profile_pic}})

#         return html.Div([
#             html.Img(src=profile_pic, style={'border-radius': '50%', 'width': '150px', 'height': '150px'})
#         ])
#     return None

# @server.route('/uploaded_images/<filename>')
# def uploaded_images(filename):
#     return send_from_directory(UPLOAD_DIRECTORY, filename)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# @app.callback(
#     Output('output-image-upload','children'),
#     [Input('upload-image', 'contents')],
#     [State('upload-image', 'filename'), State('profile_pic', 'children')]
# )

# def upload_output(content, filename, profile_pic):
#      if content is not None:
#         data = content.encode("utf8").split(b";base64,")[1]
#         file_path = os.path.join(UPLOAD_DIRECTORY, filename)

#         with open(file_path, "wb") as fh:
#             fh.write(base64.decodebytes(data))

#         client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
#         db = client['Project']
#         collection = db['Usuários']
#         profile_pic = f'/uploaded_images/{filename}'
#         collection.update_one({'email': session['user_email']}, {'$set': {'profile_pic': profile_pic}})
        
#         # return html.Div([
#         #     html.Img(src=content, style={'border-radius': '50%', 'width': '150px', 'height': '150px'}),
#         # ])
#         if profile_pic:
#             return html.Div([
#             html.Img(src=profile_pic, style={'border-radius': '50%', 'width': '150px', 'height': '150px'})
#     ])
     

# @server.route('/uploaded_images/<filename>')
# def uploaded_images(filename):
#     return send_from_directory(UPLOAD_DIRECTORY, filename)


# CALLBACKS DA TELA LOGIN ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° °
@app.callback(
#    Output('url', 'href'),
    Output('output-message-login', 'children'),
    [Input('login-button', 'n_clicks'), Input('ms-button', 'n_clicks')],
    [State('email', 'value'), State('senha', 'value')],
    prevent_initial_call=True, ##########
)
def handle_login(n_clicks_login, n_clicks_ms, email, senha):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate#return '', None #dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'login-button':
        if email and senha:

            client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
            db = client['Project']
            users_collection = db['Usuários']
            user = users_collection.find_one({"email": email})

            if user and sha256_crypt.verify(senha, user['senha']):
                session['user_email'] = email
                return 'Login realizado com sucesso!' ,'/home' #f'Login realizado com email: {email}'
            else:
                return 'Credenciais inválidas. Por favor, tente novamente.'
        else:
            return 'Por favor, preencha os campos de email e senha'
    elif button_id == 'ms-button':
        return '/loginms'    #Redirecionar para o MS login endpoint
        #webbrowser.open('https://login.microsoftonline.com/{TENANT_ID}')
        # return url_for('/loginms'), ''
    return 'Erro desconhecido. Por favor, tente novamente.'
        # return redirect(url_for('loginms'))

    
#        print ('Redirecionado para login com Microsoft')
#    return 'Erro desconhecido. Por favor, tente novamente.'

# @app.callback(
#     Output('url', 'href'),
#     [Input('redirect-store', 'data')],    
#     prevent_initial_call=True
    
# )

# def redirect_to(data):
#     if data:
#         return data.get('url')
#     return '', None #dash.no_update





# #============================================== LOGIN COM MICROSOFT ===========================================================

# # Configuração do aplicativo no azure
CLIENT_ID = '67e2167c-bb04-48d3-a10f-e9d9d618ad9d'
CLIENT_SECRET = 's2a8Q~dCSTsX-oPuaZuQSUOcnGjtAIlwv9oyLbWb'
TENANT_ID = '751b9ffa-fe40-4f7f-90a6-e3276de42583'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
REDIRECT_PATH = '/getAToken'
SCOPE = ['User.Read']

# Função para obter URL de autenticação na página de login
# def initiate_microsoft_login():
#     with server.test_request_context():
#         session["state"] = str(uuid.uuid4())
#         auth_url = _build_auth_url(scopes=SCOPE, state=session["state"])
#         return auth_url

# def _build_msal_app(cache=None, authority=None):
#     return ConfidentialClientApplication(
#         CLIENT_ID, authority=authority or AUTHORITY,
#         client_credential=CLIENT_SECRET, token_cache=cache)

# def _build_auth_url(authority=None, scopes=None, state=None):
#     return _build_msal_app(authority=authority).get_authorization_request_url(
#         scopes or [],
#         state=state or str(uuid.uuid4()),
#         redirect_uri=url_for('authorized', _external=True))

# def _load_cache():
#     cache = SerializableTokenCache()
#     if session.get('token_cache'):
#         cache.deserialize(session['token_cache'])
#     return cache

# def _save_cache(cache):
#     if cache.has_state_changed:
#         session['token_cache'] = cache.serialize()


# # - - - - - - - - - - - - - - - - - - - - - - - - - - 
# # Precisa de uma rota principal mas não faz nada
# @app.routes('/')
# def index():
#     return 'Flask MSAL'

msal_client = ConfidentialClientApplication(
    CLIENT_ID, 
    authority=AUTHORITY, 
    client_credential=CLIENT_SECRET,
    token_cache=SerializableTokenCache()
)

@server.route('/loginms')
def loginms():
    session["state"] = str(uuid.uuid4())
    auth_url = msal_client.get_authorization_request_url(
        SCOPE, 
        state=session["state"], 
        redirect_uri=url_for("authorized", _external=True)
    )
    return redirect(auth_url)


@server.route(REDIRECT_PATH)
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))

    if "error" in request.args:
        return f"Login failed: {request.args['error']} - {request.args.get('error_description')}", 403  #erro 403

    if request.args.get('code'):
#        cache = msal_client.token_cache
        result = msal_client.acquire_token_by_authorization_code(
            request.args['code'], 
            scopes=SCOPE, 
            redirect_uri=url_for("authorized", _external=True)
        )
        if "error" in result:
            return f"Error in token acquisition: {result['error']} - {result.get('error_description')}"
        session["user"] = result.get("id_token_claims")
        return redirect(url_for("home"))
    return "Authorization failed."

@server.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run_server(debug=True)