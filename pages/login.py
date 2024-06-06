import dash_bootstrap_components as dbc
from dash import html, dcc


# Definição do layout da página de login
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H2("Login"), className='text-center mt-5')
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='email', placeholder='E-mail', type='email', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='senha', placeholder='Senha', type='password', className='mb-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('Login', id='login-button', color='orange', className='me-2'),
                width='auto',
                className='d-flex justify-content-center mb-2'
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('  Entrar com Microsoft', id='ms-button', className='bi bi-microsoft'),
                width='auto',
                className='d-flex justify-content-center'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='output-message', className='text-center mt-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div([
                    dcc.Link("Ou Registre-se", id='reg-button', href="/registro"),
                    dcc.Location(id='url', refresh=False)
                ])
            )
        )
    ],
)

