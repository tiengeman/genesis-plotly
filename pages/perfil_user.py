import dash_bootstrap_components as dbc
from dash import html, dcc
from constants import *

layout = html.Div([
    #     dcc.Tabs(id='tabs-user', value='tab-1', children=[
    #     dcc.Tab(label='Dados do usuário', value= 'tab-1'),
    #     dcc.Tab(label='Permissões', value='tab-2'),
    # ]),
    dbc.Row([
        dbc.Col([
            # Coluna esquerdaaa
            html.Img(
                id='profile-image', 
                src="https://th.bing.com/th/id/R.5db279e2c2b45c912f7b1ad811275985?rik=QaUgIIHBl1LHxQ&riu=http%3a%2f%2fwww.rwg.bz%2fprivate%2fhamster%2fHamsterusesmini-computer.jpg&ehk=RkZlS26KLyIW5TAPLOw4Nm03wK3LyLAoKkcqdBRiWsA%3d&risl=&pid=ImgRaw&r=0", 
                height=200, width=200, style={"border-radius": "50%"}, n_clicks=0,
            ),

            dbc.Input(id='nome', placeholder='Nome', type='text', className='mb-3', disabled=True),

            dbc.Input(id='email', placeholder='Email', type='email', className='mb-3', disabled=True),
            dbc.Input(id='cargo', placeholder='Cargo/Função', type='text', className='mb-3', disabled = True),
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
            dbc.Button("Salvar", id="salvar-button", color="primary", className="mt-2"),
        ], width=6),
        
        dbc.Col([
            # Coluna direita
            dbc.Input(id='senha', placeholder='Senha', type='password', className='mb-3', disabled=True),
            html.P("Cargo/Função:"),
            dbc.Button('Alterar dados', id='altdados-button', style={'backgroundColor': colors['orange'], 'border':'None'}, className='me-2', n_clicks=0),

            html.Div(id='output-message-perfil', className='text-center mt-3'),

            #dbc.Button("Logout", id="logout-button", color="danger", className="mt-2"),

        ], width=6),

        # botão sair da conta
        dbc.Col([
            dbc.Button('Sair', id='logout-button', style={'background': colors['white'], 'color': 'red', 'border-color': 'red'}, className='me-2', n_clicks=0)
        ])
    ])
],
    style={"maxWidth" :"80em", "margin": "auto", "padding-top": "50px"},
    className="mx-auto"
)


# layout = html.Div([
#     dcc.Tabs(id='tabs-user', value='tab-1', children=[
#         dcc.Tab(label='Dados do usuário', value= 'tab-1'),
#         dcc.Tab(label='Permissões', value='tab-2'),
#     ]),
#     dcc.Location(id='url-user'),
# html.Div(children=[
#         dcc.Location(id='url_login', refresh=True),
#         dbc.Row(
#             dbc.Col(html.H2("Dados do Usuário"), className='text-center mt-5', ),

#         ),
#         dbc.Row(
#             dbc.Col(
#                 # html.I(
#                 #     id='profile-image', 
#                 #     src="https://th.bing.com/th/id/R.5db279e2c2b45c912f7b1ad811275985?rik=QaUgIIHBl1LHxQ&riu=http%3a%2f%2fwww.rwg.bz%2fprivate%2fhamster%2fHamsterusesmini-computer.jpg&ehk=RkZlS26KLyIW5TAPLOw4Nm03wK3LyLAoKkcqdBRiWsA%3d&risl=&pid=ImgRaw&r=0", 
#                 #     height=200, width=200, style={"border-radius": "50%"}, n_clicks=0,
#                 # ),
#                 dbc.Button(
#                     html.I(className="bi bi-person-circle",style={"font-size": "1.60em", "color": colors['gray']}),
#                     id="profile-image",
#                     n_clicks=0,
#                     size="md",
#                     color='#FFFFFF',
#                     style={"font-size": "8em", "color": "#FFFFFF"},
#                     className='btn-white',
#                 ),
#                 id="profile-image-link",
#                 width="auto", 
#                 className="d-flex justify-content-center" 
#             ),
#         ),
#         # Adicionar o modal para exibir o componente dcc.Upload
#         dbc.Modal(
#             [
#                 dbc.ModalHeader("Alterar imagem de perfil"),
#                 dbc.ModalBody(
#                     dcc.Upload(
#                         id='profile-image-upload',
#                         children=html.Div([
#                             'Drag and Drop or ',
#                             html.A('Select Files')
#                         ]),
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
#                         # Ocultar o modal após o upload ser concluído
#                     )
#                 ),
#                 dbc.ModalFooter(
#                     dbc.Button("Fechar", id="close-profile-image-modal", color="secondary", className="me-auto", n_clicks=0)
#                 )
#             ],
#             id="profile-image-modal",
#             is_open=False,
#             backdrop="static",
#             keyboard=False
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Input(id='nome', placeholder='Nome', type='text', className='mb-3', disabled=True),
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Input(id='email', placeholder='Email', type='email', className='mb-3', disabled=True),
#             ),
#             justify="center"
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Input(id='data_nascimento', placeholder='Data de Nascimento', type='date', className='mb-3'),
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Input(id='telefone', placeholder='Telefone', type='number', className='mb-3'),
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Input(id='cargo', placeholder='Cargo/Função', type='text', className='mb-3', disabled = True),
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dcc.Dropdown(
#                     id='setor',
#                     placeholder= 'Setor',
#                     options=[
#                         {'label': 'Financeiro', 'value': 'financeiro'},
#                         {'label': 'Tecnologia e Informações', 'value': 'ti'},
#                         {'label': 'Operações', 'value': 'operacoes'},
#                     ],
#                     # value='NaoPrestador', 
#                     # clearable=False,
#                     className='mb-3'
#                     , disabled=True
#                 ),
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Input(id='senha', placeholder='Senha', type='password', className='mb-3', disabled=True),
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Button('Alterar dados', id='altdados-button', style={'backgroundColor': colors['orange'], 'border':'None'}, className='me-2', n_clicks=0),
#                 width= '50px',
#                 className='d-flex justify-content-center mb-2'
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Button('Salvar', id='save-button', style={'backgroundColor': colors['orange'], 'border':'None'}, className='me-2', n_clicks=0),
#                 width= '50px',
#                 className='d-flex justify-content-center mb-2'
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Button('Alterar Senha', id='altsenha-button', style={'backgroundColor': colors['white'], 'color': colors['orange'], 'border-color': colors['orange']}, className='me-2', n_clicks=0),
#                 width= '50px',
#                 className='d-flex justify-content-center mb-2'
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Button('Sair', id='logout-button', style={'background': colors['white'], 'color': 'red', 'border-color': 'red'}, className='me-2', n_clicks=0),
#                 width= '20px',
#                 className= 'd-flex right mb-2'
#             )
#         ),
#         dbc.Row(
#             dbc.Col(
#                 html.Div(id='output-message-perfil', className='text-center mt-3'),
#             )
#         ),

#         #consciderar depois
#         # dbc.Row(
#         #     dbc.Col(
#         #         # html.H3('Permissões'),
#         #         # dcc.Markdown('''
#         #         #     **Editar tabelas**
#         #         # '''),
#         #         dbc.Checklist(
#         #             {'label': 'Gerencial', 'value':'Gerencial'},
#         #             {'label': 'Detalhamento', 'value': 'Detalhamento'},
#         #             {'label': 'Encargos', 'value': 'Encargos'},
#         #             {'label': 'Impostos', 'value':'Impostos'}
#         #         )
#         #     )
#         # )
#     ]),
#     html.Div(id='output-data'),
# ]),



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
