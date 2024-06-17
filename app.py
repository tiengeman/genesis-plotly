import dash
from flask import Flask, render_template, redirect, url_for, session, request, send_from_directory, sessions
from flask_session import Session
import uuid
import os
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
from pages.encargos import lista_encargos
import pages.gerencial as gerencial
import pages.home as home
import pages.diretoria as diretoria
import pages.relacao as relacao
import pages.cadastro_projetos as cadastro_projetos
import pages.impostos as impostos
import pages.encargos as encargos
import pages.detalhamento as detalhamento
import pages.cadastro as cadastro
import pages.login as login
import pages.perfil_user as perfil_user
from constants import *
from dash.exceptions import PreventUpdate
from banco import *
from back.inserts import *
from back.models import *
# from back.auth import login_required_dash
# from back.msal_login import initiate_microsoft_login

from pymongo import MongoClient
from passlib.hash import sha256_crypt
from msal import ConfidentialClientApplication, SerializableTokenCache
import webbrowser


server = Flask(__name__)
server.config['SECRET_KEY'] = '68f170cb6f230e030cd3353b48666511a7bdc74600576a03'
# server = app.server
# server.secret_key = os.getenv('SECRET_KEY', '68f170cb6f230e030cd3353b48666511a7bdc74600576a03')

# if not session.get('user_email'):
#     session['user_email'] = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

# @server.route('/login')
# def login_route():
#     return redirect('/login-page')


#conteúdo dentro do menu
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Gerencial', href='/gerencial', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Diretoria', href='/diretoria', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Relação', href='/relacao', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Cadastro Projetos', href='/cadastro_projetos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Impostos', href='/impostos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Encargos', href='/encargos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Detalhamento', href='/detalhamento', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Cadastro', href='/cadastro', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Login', href='/login', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Perfil', href='/perfil_user', className='nav-link')),
    ],
    vertical=True,  # Make the nav items stack vertically
    pills=True,  # Make the nav items take up the full width of the sidebar
)

# botão para abrir o menu
offcanvas = html.Div(
    [
        dbc.Button(
            html.I(className="bi bi-list"),
            id="open-offcanvas",
            n_clicks=0,
            size="md", 
            color = '#FF4E00',
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

# user_button = dbc.Button(  # ir para página de login ou perfil do usuário caso esteja logado
#     html.I(className="bi bi-person-circle"),
#     id="user-button",
#     n_clicks=0,
#     size="md",
#     color='#FFFFFF',
#     style={"font-size": "1.60em", "color": "#000000"},
#     className='btn-white',
# )

# Top navigation bar
header = dbc.Navbar(
    dbc.Row(
        [
            dbc.Col(offcanvas),
            dbc.Col( #adicionar a imagem depois
                html.A(
                    html.Img(src=logo, height="60px"),
                    href="/home",
                    style={"textDecoration": "none"}  # Add this style to remove the default underline
                )
            ),
            dbc.Col(dbc.Button(
                html.I(className="bi bi-person-circle"),
                id="user-button",
                n_clicks=0,
                size="md",
                color='#FFFFFF',
                style={"font-size": "1.60em", "color": "#FFFFFF"},
                className='btn-white',
                ),
            ),
        ]
    ),
    color=colors['orange'],
    dark=True,
    className='justify-content-between', 
    style={'height': '50px'} 
)

# Div onde mostra o conteúdo de cada página
content_area = html.Div(id='content')

# Layout geral, caebçalho + content area
app.layout = html.Div([
    header,
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(content_area),
    ]),
])

#====================================================================== Callbacks ================================================================================================

#callback para mudar de página de acordo com o menu
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
# #@login_required_dash
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
    elif pathname == '/encargos':
        return encargos.layout
    elif pathname == '/detalhamento':
        return detalhamento.layout
    elif pathname == '/cadastro':
        return cadastro.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/loginms':
        return loginms.layout
    elif pathname == '/perfil_user':
        return perfil_user.layout
        
    else:
        return home.layout
    
# ============================================== BOTÃO USUÁRIO ===========================================================
# Callback para redirecionar para a página de login quando o botão for clicado
@app.callback(
    Output('url', 'pathname'),
    Input('user-button', 'n_clicks')
)
def go_to_login(n_clicks):
    if n_clicks:
        return '/login'
    return None
  
    
# ================================================ UPDATE TABLE GERENCIAL ==========================================================

def update_table(output_id, value):
    if output_id == 'tabela-container':
        return gerencial.atualizar_tabela(value)
    elif output_id == 'tabela2-container':
        return gerencial.atualizar_tabela2(value)

#callback para atualizar as tabelas gerenciais de acordo com a competencia
@app.callback(
    Output('tabela-container', 'children'),
    Output('tabela2-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def update_tables(value):
    return update_table('tabela-container', value), update_table('tabela2-container', value)

# ================================================= UPDATE TABLE DETALHAMENTO ==========================================================

def update_table_detalhamento(output_id, value, contrato):
    if output_id == 'tabela-detalhamento-container-medicao':
        return detalhamento.atualizar_tabela_medicao(value, contrato)
    elif output_id == 'tabela-detalhamento-container-despesa':
        return detalhamento.atualizar_tabela_despesa(value, contrato)

#callback para atualizar as tabelas gerenciais de acordo com a competencia
@app.callback(
    Output('tabela-detalhamento-container-medicao', 'children'),
    Output('tabela-detalhamento-container-despesa', 'children'),
    [Input('minha-lista-suspensa-1-detalhamento', 'value'), Input('minha-lista-suspensa-2', 'value')]
)
def update_tables(value, contrato):

    print(f'{value} - {contrato}')
    return update_table_detalhamento('tabela-detalhamento-container-medicao', value, contrato), update_table_detalhamento('tabela-detalhamento-container-despesa', value, contrato)

    
#callback para abrir o menu
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# ============================================ MODAL CADASTRO ====================================================

#callback para abrir o modal de cadastro de projetos
@app.callback(
    Output("modal-centered-projetos", "is_open"),
    [Input("open-centered-projetos", "n_clicks"), Input("close-centered-projetos", "n_clicks")],
    [State("modal-centered-projetos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro
@app.callback(
    [
        Output("message-modal-projetos", "is_open"),
        Output("message-modal-header-projetos", "children"),
        Output("message-modal-body-projetos", "children"),
    ],
    [
        Input("close-centered-projetos", "n_clicks"),
        Input("close-message-modal-projetos", "n_clicks"),
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

    if triggered_id == "close-centered-projetos":
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
    elif triggered_id == "close-message-modal-projetos":
        return False, "", ""
    else:
        raise dash.exceptions.PreventUpdate
    
#callback para abrir o modal de cadastro de projetos
@app.callback(
    Output("modal-centered-impostos", "is_open"),
    [Input("open-centered-impostos", "n_clicks"), Input("close-centered-impostos", "n_clicks")],
    [State("modal-centered-impostos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro
@app.callback(
    [
        Output("message-modal-impostos", "is_open"),
        Output("message-modal-header-impostos", "children"),
        Output("message-modal-body-impostos", "children"),
    ],
    [
        Input("close-centered-impostos", "n_clicks"),
        Input("close-message-modal-impostos", "n_clicks"),
    ],
    [
        State("RECEITATOTAL", "value"), State("PISRETIDO", "value"), State("PISPAGO", "value"),
        State("COFINSRETIDO", "value"), State("COFINSPAGO", "value"), State("DATAFECHAMENTO", "value"),
        State("COMPETENCIA", "value"),
    ],
)
def update_message_modal(submit_clicks, close_clicks, receitatotal, pisretido, pispago, cofinsretido, cofinspago, datafechamento, competencia):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "close-centered-impostos":
        if submit_clicks:
            lista_input = [receitatotal, pisretido, pispago, cofinsretido, cofinspago, datafechamento, competencia]
            message = enviar_contratos(lista_input)
            if "sucesso" in message.lower():
                return True, "Sucesso!", message
            else:
                return True, "Erro!", message
        else:
            raise dash.exceptions.PreventUpdate
    elif triggered_id == "close-message-modal-impostos":
        return False, "", ""
    else:
        raise dash.exceptions.PreventUpdate

#========================================= SWITCH TABELA EDITÁVEL ====================================================

# callback para deixar apenas algumas colunas editáveis na tela de cadastro de projetos
@app.callback(
    Output('tabela-projetos', 'columns'),
    Input('edit-switch-contratos', 'value')
)
def toggle_editability(value):
    columns = [{"name": i, "id": i, "editable": value} if i not in ["VALOR", "PRAZOMES", "PRAZODIAS"] else {"name": i, "id": i} for i in cad_contratos().columns]
    return columns

# callback para deixar apenas algumas colunas editáveis na tela de cadastro de projetos
@app.callback(
    Output('tabela-impostos', 'columns'),
    Input('edit-switch-impostos', 'value')
)
def toggle_editability(value):
    columns = [{"name": i, "id": i, "editable": value} if i not in [] else {"name": i, "id": i} for i in cad_impostos().columns]
    return columns


# Atualizar a propriedade editable das tabelas quando o switch é acionado
@app.callback(
    [Output(f'tabela-encargos-{index}', 'editable') for index in range(len(lista_encargos))],
    [Input('edit-switch-encargos', 'value')]
)
def update_editable(edit_value):
    return [edit_value] * len(lista_encargos)

# ============================================== BOTÃO ATUALIZAR ===========================================================

# Crie a callback para atualizar a tabela quando o botão for clicado
@app.callback(
    Output('tabela-projetos', 'data'),
    [Input('refresh-button-contratos', 'n_clicks')]
)
def refresh_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_contratos = cad_contratos()
        # Retorne os dados atualizados da tabela
        return df_contratos.to_dict('records')
    
# Crie a callback para atualizar a tabela de impostos quando o botão for clicado
@app.callback(
    Output('tabela-impostos', 'data'),
    [Input('refresh-button-impostos', 'n_clicks')]
)
def refresh_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_impostos = cad_impostos()
        # Retorne os dados atualizados da tabela
        return df_impostos.to_dict('records')
    
# Crie a callback para atualizar a tabela de impostos quando o botão for clicado
@app.callback(
    [Output(f'tabela-encargos-{index}', 'data') for index in range(len(lista_encargos))],
    [Input('refresh-button-encargos', 'n_clicks')]
)
def refresh_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_impostos = cad_impostos()
        # Retorne os dados atualizados da tabela
        return df_impostos.to_dict('records')

    
@app.callback(
    Output('row-info-container', 'children'),
    Input('tabela', 'active_cell'),
    Input('tabela2', 'active_cell'),
    State('tabela', 'data'),
    State('tabela', 'columns'),
    State('tabela2', 'data'),
    State('tabela2', 'columns')
)
def show_row_info(active_cell1, active_cell2, data1, columns1, data2, columns2):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    if ctx.triggered[0]['prop_id'].split('.')[0] == 'tabela':
        active_cell = active_cell1
        data = data1
        columns = columns1
    else:
        active_cell = active_cell2
        data = data2
        columns = columns2

    if active_cell is None:
        raise PreventUpdate

    column_id = columns[active_cell['column']]['id']
    if column_id!= 'MEDIÇÃO':
        raise PreventUpdate

    row_index = active_cell['row']
    row_data = data[row_index]
    # Create a new table or a div to show the row information
    info_table = html.Div([
        html.H5(f"Row {row_index} Information:"),
        html.Table([
            html.Tr([html.Th(key), html.Td(value)]) for key, value in row_data.items()
        ])
    ])
    return info_table

@app.callback(
    Output('detalhamento-container', 'children'),
    Input('detalhamento-button', 'n_clicks')
)
def update_detalhamento_container(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return detalhamento.layout
    else:
        return html.P("Nenhum detalhamento disponível.")


# ============================================== CALLBACKS DA TELA CADASTRO =========================================================== 
@app.callback(
    Output('output-message-cadastro', 'children'),
#    Output('url', 'pathname'),
    [Input('register-button', 'n_clicks')], # [Input('fzlogin-button', 'n_clicks_fz')],
    [State('nome', 'value'), State('email', 'value'), State('senha', 'value'), State('confirmar-senha', 'value'), State('setor', 'value'), State('cargo', 'value')]

)
def register_user(n_clicks, nome, email, senha, confirmar_senha, setor, cargo):
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
                'setor': setor,
                'cargo': cargo,

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



# # ============================================== CALLBACKS DA TELA LOGIN ===========================================================

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


# #============================================== PERFIL DE USUÁRIO ===========================================================
@app.callback(
    Output('nome', 'value'),
    Output('email', 'value'),
    Output('data_nascimento', 'value'),
    Output('telefone', 'value'),
    Output('setor', 'value'),
    Input('register-button', 'n_clicks')
)

def get_user_data(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        email = session.get('user_email')
        client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
        db = client['Project']
        users_collection = db['Usuários']
        user_data = users_collection.find_one({'email': email})
        if user_data:
            return(
                user_data['nome'],
                user_data['email'],
                user_data['data_nascimento'],
                user_data['telefone'],
                user_data['setor'],
                user_data['cargo']
            )
        else:
            return ('', '', '', '', '', '')
    raise PreventUpdate

# def update_user_data(pathname):
#     email = pathname.split('/')[-1]
#     user_data = get_user_data(email)
#     if user_data:
#         return (
#             user_data['nome'],
#             user_data['email'],
#             user_data['data_nascimento'],
#             user_data['telefone'],
#             user_data['setor'],
#             user_data['cargo']
#         )
#     else:
#         return ('', '', '', '', '')

if __name__ == '__main__':
    app.run_server(debug=True)