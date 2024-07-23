import dash_bootstrap_components as dbc
from dash import html, dcc
from constants import *

layout = dbc.Container(
    [
        dcc.Location(id='url_login', refresh=True),
        dbc.Row(
            dbc.Col(html.H2("Faça login"), className='text-center mt-5', ),

        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='email', placeholder='E-mail', type='email', className='mb-3'),
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='senha', placeholder='Senha', type='password', className='mb-3'),
                width= '40px'
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('Login', id='login-button',style={'backgroundColor': colors['orange'], 'border':'None'}, className='me-2', n_clicks=0),
                width= '50px',
                className='d-flex justify-content-center mb-2'
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('  Entrar com Microsoft', id='ms-button', className='bi bi-microsoft', n_clicks=0),
                width='50px',
                className='d-flex justify-content-center'
            )
        ),
                html.Div(children='''Ou ''', className='d-flex justify-content-center'),
        dbc.Row(
            dbc.Col(
                html.A('Registre-se agora', href='/cadastro', id='fzcadastro-button', style={'backgroundColor': colors['white'], 'color': colors['orange'], 'border-color': colors['orange'], 'padding': '10px', 'border-radius': '5px', 'text-decoration': 'none'}),
                # dbc.Button('Faça Login', id='fzlogin-button', style={'backgroundColor': colors['white'], 'color': colors['orange'], 'border-color': colors['orange']}, className='me-2', n_clicks=0),
                width= '20px',
                className='d-flex justify-content-center mb-2'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='output-message-login', className='text-center mt-3'),
            )
        ),
    ],
    fluid=True,
    style={"maxWidth" :"500px", "margin": "auto", "padding-top": "80px"},
    className="mx-auto"
)

