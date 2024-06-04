from flask import Flask, render_template, redirect, url_for, session, request
from msal import ConfidentialClientApplication
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

# Constants
# logo = 'https://i0.wp.com/engeman.net/wp-content/uploads/2024/04/LOGO_ENGEMAN_HORIZONTAL-e1714498268589.png?w=851&ssl=1'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

# Conteúdo dentro do menu
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Gerencial', href='/gerencial', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Diretoria', href='/diretoria', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Relação', href='/relacao', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Cadastro Projetos', href='/cadastro_projetos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Impostos', href='/impostos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Registro', href='/registro', className='nav-link'))
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
    else:
        return home.layout

def update_table(output_id, value):
    if output_id == 'tabela-container':
        return gerencial.atualizar_tabela(value)
    elif output_id == 'tabela2-container':
        return gerencial.atualizar_tabela2(value)

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

# Callback para redirecionar para a página de login quando o botão for clicado
@app.callback(
    Output('url', 'pathname'),
    Input('user-button', 'n_clicks')
)
def go_to_login(n_clicks):
    if n_clicks:
        return '/login'
    return dash.no_update


# CALBACKS DA TELA REGISTRO ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° °
# @app.callback(
#     Output('output-message', 'children'),
#     [Input('register-button', 'n_clicks')],
#     [State('nome', 'value'), State('email', 'value'), State('senha', 'value'), State('confirmar-senha', 'value'), State('setor', 'value')]

# )
# def register_user(n_clicks, nome, email, senha, confirmar_senha, setor):
#     if n_clicks > 0:
#         if not nome or not email or not senha or not confirmar_senha or not setor:
#             return 'Por favor, preencha todos os campos.'

#         if senha != confirmar_senha:
#             return 'As senhas não coincidem. Por favor, tente novamente.'

#         try:
#             client = MongoClient('mongodb+srv://ianfelipe:MateMatica16@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority')
#             db = client['Project']
#             collection = db['Usuários']
            
#             # Verificar se o email já está registrado
#             if collection.find_one({"email": email}):
#                 return 'Email já registrado. Por favor, faça o login.'

#             # Gerar hash da senha
#             hashed_senha = sha256_crypt.hash(senha) #Dê certo, pfv eu preciso largar

#             user_document = {
#                 'nome': nome,
#                 'email': email, 
#                 'senha': hashed_senha, #hash.senha
#                 'setor': setor
#             }
#             result = collection.insert_one(user_document)
#             print("Documento inserido:", result)
#             return 'Cadastro realizado com sucesso!'
#         except Exception as e:
#             return f'Erro ao realizar o cadastro: {e}'
#     return '', dash.no_update


#CALBACKS DA TELA LOGIN ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° °
@app.callback(
    Output('output-message', 'children'),
    [Input('login-button', 'n_clicks')],
    [Input('ms-button', 'n_clicks')],
    [State('email', 'value'), State('senha', 'value')]
)
def handle_login(n_clicks_login, n_clicks_ms, email, senha):
    ctx = dash.callback_context

    if not ctx.triggered:
        return '', dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'login-button':
        # Simulação de processamento de login
        if email and senha:
            return f'Login realizado com email: {email}'
        else:
            return 'Por favor, preencha os campos de email e senha'
    elif button_id == 'ms-button':
        # auth_url = initiate_microsoft_login()
        return 'http://localhost:5000/login', 'Redirecionado para login com Microsoft'
    return '', dash.no_update



if __name__ == '__main__':
    app.run_server(debug=True)