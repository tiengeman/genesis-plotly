import dash_bootstrap_components as dbc
from dash import html, dcc
from constants import *


# Definição do layout da página de registro
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1('Cadastro', className='text-center mt-5')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='nome', placeholder='Nome Completo', type='text', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='email', placeholder='E-mail', type='email', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='setor',
                    placeholder= 'Setor',
                    options=[
                        {'label': 'Financeiro', 'value': 'financeiro'},
                        {'label': 'Tecnologia e Informações', 'value': 'TI'},
                        {'label': 'Operações', 'value': 'operacoes'},
                    ],
                    # value='NaoPrestador', 
                    # clearable=False,
                    className='mb-3'
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='cargo', placeholder='Cargo/Função', type='text', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='senha', placeholder='Senha', type='password', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='confirmar-senha', placeholder='Confirmar senha', type='password', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('Cadastrar', id='register-button', n_clicks=0),
                width='50px',
                className='d-flex justify-content-center'
            )
        ),
        html.Div(children='''Ou ''', className='d-flex justify-content-center'),
        dbc.Row(
            dbc.Col(
                dbc.Button('Faça Login', id='fzlogin-button', style={'backgroundColor': colors['white'], 'color': colors['orange'], 'border-color': colors['orange']}, className='me-2', n_clicks=0),
                width= '20px',
                className='d-flex justify-content-center mb-2'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='output-message-cadastro', className='text-center mt-3')
            )
        ),

    ],
    fluid=True
)

# Função de callback para registrar o usuário
