import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout da página de usuário
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1('Dados do Usuário', className='text-center mt-5')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='user-data', className='mt-3')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='profile-picture-container', children=[
                    html.Img(id='profile-picture', className='profile-picture', src='/assets/default-profile.png'),
                    dcc.Upload(
                        id='upload-image',
                        children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        multiple=False
                    )
                ], className='text-center mt-3')
            )
        ),
    ],
    fluid=True
)
