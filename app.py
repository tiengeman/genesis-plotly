import dash
import dash_bootstrap_components as dbc
from dash import callback_context
from dash import html, dcc
from dash.dependencies import Input, Output, State
from pages.encargos import lista_encargos
import pages.gerencial as gerencial
import pages.home as home
import pages.diretoria as diretoria
import pages.relacao as relacao
import pages.cadastro_projetos as cadastro_projetos
import pages.impostos as impostos
import pages.encargos as encargos
import pages.cadastro as cadastro
import pages.login as login
from constants import *
from dash.exceptions import PreventUpdate
from banco import *
from back.inserts import *

# Imports para gerenciamento de logins e usuários
import os
from flask import Flask, render_template, redirect, url_for, session, request, send_from_directory, sessions, make_response, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session as FlaskSession
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
from werkzeug.middleware.proxy_fix import ProxyFix
import sendgrid 

server = Flask(__name__)
server.secret_key = os.getenv('SECRET_KEY', 'o68f170cb6f230e030cd3353b48666511a7bdc74600576a04')
FlaskSession(server)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

app.server.wsgi_app = ProxyFix(app.server.wsgi_app, x_for=1, x_host=1)

# Configuração do MongoDB para sessões
# mongo = PyMongo(server, uri="mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/Project")
# server.config['SESSION_TYPE'] = 'mongodb'
# server.config['SESSION_MONGODB'] = mongo.cx
# server.config['SESSION_MONGODB_DB'] = 'Project'
# server.config['SESSION_MONGODB_COLLECT'] = 'Sessão'
# server.config['SESSION_PERMANENT'] = True
# server.config['SESSION_USE_SIGNER'] = True

# Configuração de sessões em arquivos
server.config['SESSION_TYPE'] = 'filesystem'  
server.config['SESSION_PERMANENT'] = True

FlaskSession(server)

# Inicialização do MongoDB
client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
db_mongo = client['Project']
users_collection = db_mongo['Usuários']
#conteúdo dentro do menu
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', id='home-link', className='nav-link')),
        html.Div(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                dbc.NavLink('Gerencial', href='/gerencial', id='gerencial-link', className='nav-link'),
                                dbc.NavLink('Diretoria', href='/diretoria', id='diretoria-link', className='nav-link'),
                            ],
                            title='Relatórios',
                            item_id='accordion-item',
                            className='nav-link',
                        ),
                    ],
                    id='accordion-relatorios',
                    flush=True,
                    start_collapsed=True,
                ),
            ],
            className='nav-item',
        ),
        html.Div(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                dbc.NavLink('Cadastro Projetos', href='/cadastro_projetos', id='cadastro-projetos-link', className='nav-link'),
                                dbc.NavLink('Cadastro de Impostos', href='/impostos', id='impostos-link', className='nav-link'),
                                dbc.NavLink('Cadastro de Encargos', href='/encargos', id='encargos-link', className='nav-link'),
                                dbc.NavLink('Cadastro de Usuários', href='/cadastro', id='cadastro-link', className='nav-link'),
                                dbc.NavLink('Cadastro de Relacionamento', href='/relacao', id='relacao-link', className='nav-link'),
                            ],
                            title='Cadastros',
                            item_id='accordion-item',
                            className='nav-link',
                        ),
                    ],
                    id='accordion-cadastros',
                    flush=True,
                    start_collapsed=True,
                ),
            ],
            className='nav-item',
        ),
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
            scrollable=True
        ),
    ]
)

# Top navigation bar
header = dbc.Navbar(
    dbc.Row(
        [
            dbc.Col(
                offcanvas,
                width="auto",
            ),
            dbc.Col( #adicionar a imagem depois
                html.A(
                    html.Img(src=logo, height="60px"),
                    href="/home",
                    style={"textDecoration": "none"}  # Add this style to remove the default underline
                ),
                width="auto",
            ),
            dbc.Col(
                html.Div(
                    style={"flex": "1"},
                ),
            ),
            dbc.Col( # botão de login/profile
                dbc.Button(
                    html.I(className="bi bi-person-circle"),
                    id="user-button",
                    n_clicks=0,
                    size="md",
                    color='#FFFFFF',
                    style={"font-size": "1.60em", "color": "#FFFFFF"},
                    className='btn-white'
                ),
                width="auto"
            ),
        ],
        align="center",
        className="w-100"
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

# CONFIGURAÇÃO BANCO MONGO USUÁRIOS
client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
db = client['Project']
users_collection = db['Usuários']

#====================================================================== Callbacks ================================================================================================

#callback para mudar de página de acordo com o menu
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
    elif pathname == '/encargos':
        return encargos.layout
    # elif pathname == '/detalhamento':
    #     return detalhamento.layout
    elif pathname == '/cadastro':
        return cadastro.layout
    elif pathname == '/login':
        return login.layout
    else:
        return home.layout
    

# ============================================== BOTÃO USUÁRIO ===========================================================
# Callback para redirecionar para a página de login ou para o perfil de usuário quando já logado
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

def update_table_detalhamento(output_id, value, contrato, categoria):
    if output_id == 'tabela-detalhamento-container-medicao':
        return gerencial.atualizar_tabela_medicao(value, contrato)
    elif output_id == 'tabela-detalhamento-container-despesa':
        return gerencial.atualizar_tabela_despesa(value, contrato, categoria)

#callback para atualizar as tabelas gerenciais de acordo com a competencia
@app.callback(
    Output('tabela-detalhamento-container-medicao', 'children'),
    Output('tabela-detalhamento-container-despesa', 'children'),
    [Input('minha-lista-suspensa-1-detalhamento', 'value'), Input('minha-lista-suspensa-2', 'value'), Input('minha-lista-suspensa-3', 'value')]
)
def update_tables(value, contrato, categoria):
    return update_table_detalhamento('tabela-detalhamento-container-medicao', value, contrato, categoria), update_table_detalhamento('tabela-detalhamento-container-despesa', value, contrato, categoria)

# ============================================================MENU=========================================
#callback para abrir o menu
@app.callback(
    Output("offcanvas", "is_open"),
    [Input("open-offcanvas", "n_clicks")] +
    [Input(link_id, "n_clicks") for link_id in ["home-link", "gerencial-link", "diretoria-link", "cadastro-projetos-link", "impostos-link", "encargos-link", "cadastro-link", "relacao-link"]],
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(*args):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "open-offcanvas":
        return not args[-1]
    else:
        return False

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
    
#callback para abrir o modal de cadastro de impostos
@app.callback(
    Output("modal-centered-impostos", "is_open"),
    [Input("open-centered-impostos", "n_clicks"), Input("close-centered-impostos", "n_clicks")],
    [State("modal-centered-impostos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro de impostos
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
    
#callback para abrir o modal de cadastro de encargos
@app.callback(
    Output("modal-centered-encargos", "is_open"),
    [Input("open-centered-encargos", "n_clicks"), Input("close-centered-encargos", "n_clicks")],
    [State("modal-centered-encargos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro de encargos
@app.callback(
    [
        Output("message-modal-encargos", "is_open"),
        Output("message-modal-header-encargos", "children"),
        Output("message-modal-body-encargos", "children"),
    ],
    [
        Input("close-centered-encargos", "n_clicks"),
        Input("close-message-modal-encargos", "n_clicks"),
    ],
    [
        State("CODIGO", "value"), State("NOME", "value"), State("CNPJ", "value"),
        State("PERCENTUAL", "value"), State("CPRB", "value"), State("INICIO", "value"),
        State("FIM", "value"),
    ],
)
def update_message_modal(submit_clicks, close_clicks, codigo, nome, cnpj, percentual, cprb, inicio, fim):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "close-centered-encargos":
        if submit_clicks:
            lista_input = [close_clicks, codigo, nome, cnpj, percentual, cprb, inicio, fim]
            message = enviar_contratos(lista_input)
            if "sucesso" in message.lower():
                return True, "Sucesso!", message
            else:
                return True, "Erro!", message
        else:
            raise dash.exceptions.PreventUpdate
    elif triggered_id == "close-message-modal-encargos":
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

# Crie a callback para atualizar a tabela de projetos quando o botão for clicado
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
    
# Crie a callback para atualizar a tabela de encargos quando o botão for clicado
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
    
# @app.callback(
#     Output('row-info-container', 'children'),
#     Input('tabela', 'active_cell'),
#     Input('tabela2', 'active_cell'),
#     State('tabela', 'data'),
#     State('tabela', 'columns'),
#     State('tabela2', 'data'),
#     State('tabela2', 'columns')
# )
# def show_row_info(active_cell1, active_cell2, data1, columns1, data2, columns2):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         raise PreventUpdate

#     if ctx.triggered[0]['prop_id'].split('.')[0] == 'tabela':
#         active_cell = active_cell1
#         data = data1
#         columns = columns1
#     else:
#         active_cell = active_cell2
#         data = data2
#         columns = columns2

#     if active_cell is None:
#         raise PreventUpdate

#     column_id = columns[active_cell['column']]['id']
#     if column_id!= 'MEDIÇÃO':
#         raise PreventUpdate

#     row_index = active_cell['row']
#     row_data = data[row_index]
#     # Create a new table or a div to show the row information
#     info_table = html.Div([
#         html.H5(f"Row {row_index} Information:"),
#         html.Table([
#             html.Tr([html.Th(key), html.Td(value)]) for key, value in row_data.items()
#         ])
#     ])
#     return info_table

# @app.callback(
#     Output('detalhamento-container', 'children'),
#     Input('detalhamento-button', 'n_clicks')
# )
# def update_detalhamento_container(n_clicks):
#     if n_clicks is not None and n_clicks > 0:
#         return detalhamento.layout
#     else:
#         return html.P("Nenhum detalhamento disponível.")


# ============================================== CALLBACKS DA TELA CADASTRO ===========================================================
@app.callback(
    Output('output-message-cadastro', 'children'),
    [Input('register-button', 'n_clicks')],
    [State('nome', 'value'), State('email', 'value'), State('senha', 'value'), State('confirmar-senha', 'value'), State('setor', 'value'), State('cargo', 'value')]

)
def register_user(n_clicks, nome, email, senha, confirmar_senha, setor, cargo):
    if n_clicks > 0:
        if not nome or not email or not senha or not confirmar_senha or not setor:
            return 'Por favor, preencha todos os campos.'

        if senha != confirmar_senha:
            return 'As senhas não coincidem. Por favor, tente novamente.'
        
        if not email.endswith('@engeman.net'):
            return 'Utilize seu email corporativo Engeman. Por favor, tente novamente!'

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
            flash ('Cadastro realizado com sucesso!', category='sucess')
            return redirect(url_for('login'))
        except Exception as e:
            return f'Erro ao realizar o cadastro: {e}'
    raise PreventUpdate

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self.email = user_data.get('email')
        self.nome = user_data.get('nome')

@app.callback(
    Output('output-message-login', 'children'),
    [Input('login-button', 'n_clicks'), Input('ms-button', 'n_clicks')],
    [State('email', 'value'), State('senha', 'value')]
)
def handle_login(n_clicks_login, n_clicks_ms, email, senha):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'login-button':
        user = users_collection.find_one({"email": email})
        if user:
            if sha256_crypt.verify(senha, user['senha']):
                user_obj = User(user)
                login_user(user_obj, remember=True)
                return "Logado com sucesso!"
            else:
                return "Credenciais inválidas. Por favor, tente novamente."
        else:
            return "Usuário não encontrado. Por favor, tente novamente."
    elif button_id == 'ms-button':
        return dcc.Location(href='/loginms', id='someid_doesnt_matter')
    return "Redirecionando para login com a Microsoft..."


# Callbacks to update the content of each tab dynamically
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_tab_content(tab):
    if tab == 'tab-1':
        return [
            html.H1(children='Performance Mensal por Competência', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Hr(style={'backgroundColor': colors['orange']}),  # Linha horizontal laranja
            html.Div(style={'marginTop': '20px'}),
            dcc.Dropdown(
                id='minha-lista-suspensa',
                options=back.competencias(),
                value=back.competencias()[-1],
                style={'fontFamily': 'Arial, sans-serif'}  # Definindo a fonte da lista suspensa
            ),
            html.Div(style={'marginTop': '20px'}),  # Espaçamento entre dropdown e tabela
            html.Div(id='tabela-container', style={'margin': '20px'}),  # Div para mostrar a tabela selecionada com margem
            html.Div(id='tabela2-container', style={'margin': '20px'}),  # Div para mostrar a tabela selecionada com margem
            html.Div(id='row-info-container', style={'margin': '20px'})  # Add this Div to display row information
        ]
    elif tab == 'tab-2':
        return [
            html.H1(children='Detalhamento', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Hr(style={'backgroundColor': colors['orange']}),  # Linha horizontal laranja
            html.Div(style={'marginTop': '20px'}),
            
            # dbc.Row contendo dois dropdowns
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='minha-lista-suspensa-1-detalhamento',
                        placeholder = 'Competência',
                        options=back.competencias(),
                        style={'fontFamily': 'Arial, sans-serif'},  # Definindo a fonte da lista suspensa
                        multi=True,
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='minha-lista-suspensa-2',
                        placeholder = 'Contrato',
                        options=lista_contratos(),
                        style={'fontFamily': 'Arial, sans-serif'},  # Definindo a fonte da lista suspensa
                        multi=True,
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='minha-lista-suspensa-3',
                        placeholder = 'Categoria',
                        options=retorna_categorias(),
                        style={'fontFamily': 'Arial, sans-serif'},  # Definindo a fonte da lista suspensa
                        multi=True,
                    ),
                ),
            ], justify='center'),
            
            html.Div(style={'marginTop': '20px'}),  # Espaçamento entre dropdown e tabela

            html.H3('Medição', style={'marginTop': '10px', 'color': colors['gray']}),
            html.Div(id='tabela-detalhamento-container-medicao', style={'margin': '20px'}),
            html.H3('Despesas', style={'marginTop': '10px', 'color': colors['gray']}),
            html.Div(id='tabela-detalhamento-container-despesa', style={'margin': '20px'}),
            
            html.Div(id='tabela-detalhamento-container', style={'margin': '20px'})  # Div para mostrar a tabela selecionada com margem
        ]
    elif tab == 'tab-3':
        return [
            html.H1(children='Dashboards', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Div(style={'marginTop': '20px'}),
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[
                dcc.Dropdown(
                    id='dropdown-contratos-dashboards',
                    options=[{'label': i, 'value': i} for i in ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5']],
                    value=['Option 1', 'Option 3'],  # default selected options
                    multi=True,  # allow multiple selections
                    style={'fontFamily': 'Arial, sans-serif', 'width': '100%'}  # Definindo a fonte e largura da lista suspensa
                ),
                dcc.Dropdown(
                    id='dropdown-competencia-dashboards',
                    options=[{'label': i, 'value': i} for i in ['Option A', 'Option B', 'Option C', 'Option D', 'Option E']],
                    value='Option A',  # default selected option
                    style={'fontFamily': 'Arial, sans-serif', 'width': '100%'}  # Definindo a fonte e largura da lista suspensa
                ),
            ]),
        ]
    elif tab == 'tab-4':
        return [
            html.H1(children='Backlog', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Div(style={'marginTop': '20px'}),
        ]
    elif tab == 'tab-5':
        return [
            html.H1(children='Gerência Geral', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Div(style={'marginTop': '20px'}),
        ]
    elif tab == 'tab-6':
        return [
            html.H1(children='Gerência Contratos', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Div(style={'marginTop': '20px'}),
        ]
    elif tab == 'tab-7':
        return [
            html.H1(children='Gerência Administrativa', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Div(style={'marginTop': '20px'}),
        ]
    elif tab == 'tab-8':
        return [
            html.H1(children='Fluxo de Contratos', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.Div(style={'marginTop': '20px'}),
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
