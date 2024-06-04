from dash import html, dcc
from dash import dash_table
from dash import html
from back import *
from banco import *
import dash_bootstrap_components as dbc
from constants import *
import dash.dash_table.FormatTemplate as FormatTemplate

# modelo do formulário de cadastro de projeto
form = dbc.Form(
    [
        dbc.Row([dbc.Label("Código", width=2),dbc.Col(dbc.Input(type="number", id="CODIGO", placeholder="Insira a receita total"))],className="mb-3"),
        dbc.Row([dbc.Label("Nome", width=2),dbc.Col(dbc.Input(type="text", id="NOME", placeholder="Insira o PIS retido"))],className="mb-3"),
        dbc.Row([dbc.Label("CNPJ", width=2),dbc.Col(dbc.Input(type="text", id="CNPJ", placeholder="Insira o PIS pago"))],className="mb-3"),
        dbc.Row([dbc.Label("Percentual", width=2),dbc.Col(dbc.Input(type="number", id="PERCENTUAL", placeholder="Insira o COFINS retido"))],className="mb-3"),
        dbc.Row([dbc.Label("CPRB", width=2),dbc.Col(dbc.Input(type="number", id="CPRB", placeholder="Insira o COFINS pago"))],className="mb-3"),
        dbc.Row([dbc.Label("Início", width=2),dbc.Col(dbc.Input(type="date", id="INICIO", placeholder="Insira a data de fechamento"))],className="mb-3"),
        dbc.Row([dbc.Label("Fim", width=2),dbc.Col(dbc.Input(type="date", id="FIM", placeholder="Insira a competência"))],className="mb-3"),
    ]
)

# modelo do modal
modal = html.Div(
    [
        dbc.Button("Cadastrar", id="open-centered-encargos", style={'backgroundColor': colors['orange']}),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cadastro de Encargos"), close_button=True),
                dbc.ModalBody(form),
                dbc.ModalFooter(
                    dbc.Button(
                        "Submit",
                        id="close-centered-encargos",
                        style={'backgroundColor': colors['orange']},
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-centered-encargos",
            centered=True,
            is_open=False,
            className="modal-lg"
        ),
    ]
)

# Novo modal para exibir mensagens
message_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(id="message-modal-header-encargos"),
                dbc.ModalBody(id="message-modal-body-encargos"),
                dbc.ModalFooter(
                    dbc.Button("Fechar", id="close-message-modal-encargos", className="ml-auto")
                ),
            ],
            id="message-modal-encargos",
            centered=True,
            is_open=False,
        ),
    ]
)

# switch para edição da tabela
switch = html.Div([
    dbc.Switch(id="edit-switch-encargos", style={"color": colors['gray']}, value=False, label="Editar",
               input_style={"height": "20px", "background-color": colors['orange']})
], className="ms-auto")

# Adicione um botão que chama a função de callback para atualizar a tabela
refresh_button = html.Div([
    dbc.Button("Atualizar Tabela", id="refresh-button-encargos", style={'backgroundColor': colors['gray']})
])

lista_encargos = cad_encargos()

# Define a layout with a centered container
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Cadastro de Encargos', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
    html.Hr(style={'backgroundColor': colors['orange']}),
    html.Div(style={'marginTop': '20px'}),
    html.Div(id='tabela-encargos-container', style={'margin': '20px'}, children=[
        dbc.Stack([
            modal,
            html.Div(style={'margin': '10px'}),
            refresh_button,
            switch
        ],
        direction="horizontal",
        ),
        html.Div(style={'marginTop': '20px'}),
        # Criar uma tabela para cada lista dentro de lista_encargos
        *[dash_table.DataTable(
            id=f'tabela-encargos-{index}',
            data=encargos.to_dict('records'),
            columns=[
                {'name': 'CODIGO', 'id': 'CODIGO', 'type': 'numeric'},
                {'name': 'NOME', 'id': 'NOME', 'type': 'text'},
                {'name': 'CNPJ', 'id': 'CNPJ', 'type': 'text'},
                {'name': 'PERCENTUAL', 'id': 'PERCENTUAL', 'type': 'numeric'},
                {'name': 'CPRB', 'id': 'CPRB', 'type': 'numeric'},
                {'name': 'INICIO', 'id': 'INICIO', 'type': 'datetime'},
                {'name': 'FIM', 'id': 'FIM', 'type': 'datetime'},
            ],
            style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': colors['gray'],
                'color': colors['white'],
            },
            style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': colors['background'],
            },
            ],
            style_table={'overflowX': 'auto', 'width': '100%'},  # Definindo o tamanho da tabela
            editable=False  # Certifique-se de que a tabela é editável
        ) for index, encargos in enumerate(lista_encargos)]
    ]),
    message_modal  # Adicione o message_modal aqui
])
