import dash_bootstrap_components as dbc
from dash import html, dcc


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
                dbc.Input(id='setor', placeholder='Setor', type='text', className='mb-3')
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
        dbc.Row(
            dbc.Col(
                html.Div(id='output-message-cadastro', className='text-center mt-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Button( 'Ou Faça Login', id='fzlogin-button', n_clicks=0)
            )
        )
    ],
    fluid=True
)

# Função de callback para registrar o usuário
