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
        dbc.Row([dbc.Label("Receite Total", width=2),dbc.Col(dbc.Input(type="number", id="RECEITATOTAL", placeholder="Insira a receita total"))],className="mb-3"),
        dbc.Row([dbc.Label("PIS Retido", width=2),dbc.Col(dbc.Input(type="number", id="PISRETIDO", placeholder="Insira o PIS retido"))],className="mb-3"),
        dbc.Row([dbc.Label("PIS Pago", width=2),dbc.Col(dbc.Input(type="number", id="PISPAGO", placeholder="Insira o PIS pago"))],className="mb-3"),
        dbc.Row([dbc.Label("COFINS Retido", width=2),dbc.Col(dbc.Input(type="number", id="COFINSRETIDO", placeholder="Insira o COFINS retido"))],className="mb-3"),
        dbc.Row([dbc.Label("COFINS Pago", width=2),dbc.Col(dbc.Input(type="number", id="COFINSPAGO", placeholder="Insira o COFINS pago"))],className="mb-3"),
        dbc.Row([dbc.Label("Data Fechamento", width=2),dbc.Col(dbc.Input(type="date", id="DATAFECHAMENTO", placeholder="Insira a data de fechamento"))],className="mb-3"),
        dbc.Row([dbc.Label("Competência", width=2),dbc.Col(dbc.Input(type="text", id="COMPETENCIA", placeholder="Insira a competência"))],className="mb-3"),
    ]
)

# modelo do modal
modal = html.Div(
    [
        dbc.Button("Cadastrar", id="open-centered-impostos", style={'backgroundColor': colors['orange']}),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cadastro de Impostos"), close_button=True),
                dbc.ModalBody(form),
                dbc.ModalFooter(
                    dbc.Button(
                        "Submit",
                        id="close-centered-impostos",
                        style={'backgroundColor': colors['orange']},
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-centered-impostos",
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
                dbc.ModalHeader(id="message-modal-header-impostos"),
                dbc.ModalBody(id="message-modal-body-impostos"),
                dbc.ModalFooter(
                    dbc.Button("Fechar", id="close-message-modal-impostos", className="ml-auto")
                ),
            ],
            id="message-modal-impostos",
            centered=True,
            is_open=False,
        ),
    ]
)

# switch para edição da tabela
switch = html.Div([
    dbc.Switch(id="edit-switch-impostos", style={"color": colors['gray']}, value=False, label="Editar",
               input_style={"height": "20px", "background-color": colors['orange']})
], className="ms-auto")

# Adicione um botão que chama a função de callback para atualizar a tabela
refresh_button = html.Div([
    dbc.Button("Atualizar Tabela", id="refresh-button-impostos", style={'backgroundColor': colors['gray']})
])

# Define a layout with a centered container
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Cadastro de Impostos', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
    html.Hr(style={'backgroundColor': colors['orange']}),
    html.Div(style={'marginTop': '20px'}),
    html.Div(id='tabela-impostos-container', style={'margin': '20px'}, children=[
        dbc.Stack([
            modal,
            html.Div(style={'margin': '10px'}),
            refresh_button,
            switch
        ],
        direction="horizontal",
        ),
        html.Div(style={'marginTop': '20px'}),
        dash_table.DataTable(
            id='tabela-impostos',
            data=cad_impostos().to_dict('records'),
            filter_action="native",
            columns=[
                {'name': 'RECEITATOTAL', 'id': 'RECEITATOTAL', 'type': 'numeric'},
                {'name': 'PISRETIDO', 'id': 'PISRETIDO', 'type': 'numeric'},
                {'name': 'PISPAGO', 'id': 'PISPAGO', 'type': 'numeric'},
                {'name': 'COFINSRETIDO', 'id': 'COFINSRETIDO', 'type': 'numeric'},
                {'name': 'COFINSPAGO', 'id': 'COFINSPAGO', 'type': 'numeric'},
                {'name': 'DATA FECHAMENTO', 'id': 'DATAFECHAMENTO', 'type': 'datetime'},
                {'name': 'COMPETENCIA', 'id': 'COMPETENCIA', 'type': 'any'},
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
        ), 
    ]),
    message_modal  # Adicione o message_modal aqui
])