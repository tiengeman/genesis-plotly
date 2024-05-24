import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import webbrowser


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
        )
    ],
    fluid=True,
    className='p-5'
)

@dash.callback(
    Output('output-message', 'children'),
    [Input('login-button', 'n_clicks')],
    [Input('ms-button', 'n_clicks')],
    [State('email', 'value'), State('senha', 'value')]
)
def handle_login(n_clicks_login, n_clicks_ms, email, senha):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ''
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'login-button':
        # Simulação de processamento de login
        if email and senha:
            return f'Login realizado com email: {email}'
        else:
            return 'Por favor, preencha os campos de email e senha'
    elif button_id == 'ms-button':
        webbrowser.open("http://localhost:5000/login")
        return 'Redirecionado para login com Microsoft'
    return ''
