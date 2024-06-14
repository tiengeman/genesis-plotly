import dash_bootstrap_components as dbc
from dash import html, dcc
from constants import *

layout = html.Div([
    dcc.Tabs(id='tabs-user', value='tab-1', children=[
        dcc.Tab(label='Dados do usuário', value= 'tab-1'),
        dcc.Tab(label='Permissões', value='tab-2'),
    ]),
    dcc.Location(id='url-user'),
    html.Div(children=[
        dcc.Location(id='url_login', refresh=True),
        dbc.Row(
            dbc.Col(html.H2("Dados do Usuário"), className='text-center mt-5', ),

        ),
        dbc.Row(
            dbc.Col(
                html.Img(src="https://th.bing.com/th/id/R.5db279e2c2b45c912f7b1ad811275985?rik=QaUgIIHBl1LHxQ&riu=http%3a%2f%2fwww.rwg.bz%2fprivate%2fhamster%2fHamsterusesmini-computer.jpg&ehk=RkZlS26KLyIW5TAPLOw4Nm03wK3LyLAoKkcqdBRiWsA%3d&risl=&pid=ImgRaw&r=0", 
                         height=100, width=100, style={"border-radius": "50%"}),
                width="auto", 
                className="d-flex justify-content-center" 
            ),
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='nome', placeholder='Nome', type='text', className='mb-3', disabled=True),
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='email', placeholder='Email', type='email', className='mb-3', disabled=True),
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='data_nascimento', placeholder='Data de Nascimento', type='date', className='mb-3'),
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id='telefone', placeholder='Telefone', type='tel', className='mb-3'),
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='setor',
                    placeholder= 'Setor',
                    options=[
                        {'label': 'Financeiro', 'value': 'financeiro'},
                        {'label': 'Tecnologia e Informações', 'value': 'ti'},
                        {'label': 'Operações', 'value': 'operacoes'},
                    ],
                    # value='NaoPrestador', 
                    # clearable=False,
                    className='mb-3'
                    , disabled=True
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('Salvar', id='salvar-button', style={'backgroundColor': colors['orange'], 'border':'None'}, className='me-2', n_clicks=0),
                width= '50px',
                className='d-flex justify-content-center mb-2'
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('Alterar Senha', id='altsenha-button', style={'backgroundColor': colors['orange'], 'border':'None'}, className='me-2', n_clicks=0),
                width= '50px',
                className='d-flex justify-content-center mb-2'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='output-message-perfil', className='text-center mt-3'),
            )
        ),
    ]),
    html.Div(id='output-data'),
])



# import dash_bootstrap_components as dbc
# from dash import html, dcc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # não sei pra que serve, mas se faz o código funcionar tpá tudo certo

# layout = dbc.Container(
#     [
#         dbc.Row(
#             dbc.Col(
#                 html.H1('Dados do Usuário', className='text-center mt-5')
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 html.Div(id='user-data', className='mt-3')
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 html.Div(id='profile-picture-container', children=[
#                     html.Img(id='profile-picture', className='profile-picture', src='/assets/default-profile.png'),
#                     dcc.Upload(
#                         id='upload-image',
#                         children=html.Div(['Arraste e solte ou ', html.A('Selecione o arquivo')]),
#                         style={
#                             'width': '100%',
#                             'height': '60px',
#                             'lineHeight': '60px',
#                             'borderWidth': '1px',
#                             'borderStyle': 'dashed',
#                             'borderRadius': '5px',
#                             'textAlign': 'center',
#                             'margin': '10px'
#                         },
#                         multiple=False #pode selecionar mais de um arquivo
#                     ),
#                     html.Div(id='output-image-upload'),
#                 ], className='text-center mt-3')
#             )
#         ),
#     ],
#     fluid=True
# )
