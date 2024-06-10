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
        dbc.Row([dbc.Label("OS", width=2),dbc.Col(dbc.Input(type="text", id="OS", placeholder="Insira a OS do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Tipo", width=2),dbc.Col(dbc.Input(type="text", id="TIPO", placeholder="Insira o tipo do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Enquadramento", width=2),dbc.Col(dbc.Input(type="text", id="ENQUADRAMENTO", placeholder="Insira o enquadramento do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Cliente", width=2),dbc.Col(dbc.Input(type="text", id="CLIENTE", placeholder="Insira o cliente"))],className="mb-3"),
        dbc.Row([dbc.Label("Descrição", width=2),dbc.Col(dbc.Input(type="text", id="DESCRIÇÃO", placeholder="Insira a descrição do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("ICJ", width=2),dbc.Col(dbc.Input(type="text", id="ICJ", placeholder="Insira o código ICJ do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("SAP", width=2),dbc.Col(dbc.Input(type="text", id="SAP", placeholder="Insira o código SAP do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Início", width=2),dbc.Col(dbc.Input(type="date", id="INÍCIO", placeholder="Insira a data de início do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Fim", width=2),dbc.Col(dbc.Input(type="date", id="FIM", placeholder="Insira a data de fim do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Aditivos", width=2),dbc.Col(dbc.Input(type="text", id="ADITIVOS", placeholder="Insira os aditivos do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Valor", width=2),dbc.Col(dbc.Input(type="number", id="VALOR", placeholder="Insira o valor do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Prazo Mês", width=2),dbc.Col(dbc.Input(type="number", id="PRAZOMES", placeholder="Insira o prazo do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Prazo Dias", width=2),dbc.Col(dbc.Input(type="number", id="PRAZODIAS", placeholder="Insira o prazo do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Status", width=2),dbc.Col(dbc.Input(type="text", id="STATUS", placeholder="Insira o status do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Responsável", width=2),dbc.Col(dbc.Input(type="text", id="RESPONSÁVEL", placeholder="Insira o resposnsável pelo projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Filial", width=2),dbc.Col(dbc.Input(type="number", id="FILIAL", placeholder="Insira a filial do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Projeto", width=2),dbc.Col(dbc.Input(type="number", id="PROJETO", placeholder="Insira o código do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Projeto Sapiens", width=2),dbc.Col(dbc.Input(type="number", id="PROJETO SAPIENS", placeholder="Insira o código sapiens do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("ISS", width=2),dbc.Col(dbc.Input(type="number", id="ISS", placeholder="Insira o ISS do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("ADM Central", width=2),dbc.Col(dbc.Input(type="number", id="ADM CENTRAL", placeholder="Insira o valor adm central do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("PIS", width=2),dbc.Col(dbc.Input(type="number", id="PIS", placeholder="Insira o PIS do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("COFINS", width=2),dbc.Col(dbc.Input(type="number", id="COFINS", placeholder="Insira o COFINS do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("CSLL", width=2),dbc.Col(dbc.Input(type="number", id="CSLL", placeholder="Insira o CSLL do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("IRPJ", width=2),dbc.Col(dbc.Input(type="number", id="IRPJ", placeholder="Insira o IRPJ do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Investimentos", width=2),dbc.Col(dbc.Input(type="number", id="INVESTIMENTOS", placeholder="Insira o investimento do projetos"))],className="mb-3"),
        dbc.Row([dbc.Label("ICMS", width=2),dbc.Col(dbc.Input(type="number", id="ICMS", placeholder="Insira o ICMS do projetos"))],className="mb-3"),
    ]
)

# modelo do modal
modal = html.Div(
    [
        dbc.Button("Cadastrar", id="open-centered-projetos", style={'backgroundColor': colors['orange']}),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cadastro de Projetos"), close_button=True),
                dbc.ModalBody(form),
                dbc.ModalFooter(
                    dbc.Button(
                        "Submit",
                        id="close-centered-projetos",
                        style={'backgroundColor': colors['orange']},
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-centered-projetos",
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
                dbc.ModalHeader(id="message-modal-header-projetos"),
                dbc.ModalBody(id="message-modal-body-projetos"),
                dbc.ModalFooter(
                    dbc.Button("Fechar", id="close-message-modal-projetos", className="ml-auto")
                ),
            ],
            id="message-modal-projetos",
            centered=True,
            is_open=False,
        ),
    ]
)

#formata a coluna que tem numeros
# format_numeric_columns(df, ["VALOR"])

# switch para edição da tabela
switch = html.Div([
    dbc.Switch(id="edit-switch-contratos", style={"color": colors['gray']}, value=False, label="Editar",
               input_style={"height": "20px", "background-color": colors['orange']})
], className="ms-auto")

# Adicione um botão que chama a função de callback para atualizar a tabela
refresh_button = html.Div([
    dbc.Button("Atualizar Tabela", id="refresh-button-contratos", style={'backgroundColor': colors['gray']})
])

# Define a layout with a centered container
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Cadastro de Projeto', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
    html.Hr(style={'backgroundColor': colors['orange']}),
    html.Div(style={'marginTop': '20px'}),
    html.Div(id='tabela-projetos-container', style={'margin': '20px'}, children=[
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
            id='tabela-projetos',
            data=cad_contratos().to_dict('records'),
            filter_action="native",
            columns=[
                {'name': 'OS', 'id': 'OS', 'type': 'text'},
                {'name': 'TIPO', 'id': 'TIPO', 'type': 'text'},
                {'name': 'ENQUADRAMENTO', 'id': 'ENQUADRAMENTO', 'type': 'text'},
                {'name': 'CLIENTE', 'id': 'CLIENTE', 'type': 'text'},
                {'name': 'DESC', 'id': 'DESC', 'type': 'text'},
                {'name': 'ICJ', 'id': 'ICJ', 'type': 'text'},
                {'name': 'SAP', 'id': 'SAP', 'type': 'text'},
                {'name': 'INICIO', 'id': 'INICIO', 'type': 'datetime'},
                {'name': 'FIM', 'id': 'FIM', 'type': 'datetime'},
                {'name': 'ADITIVOS', 'id': 'ADITIVOS', 'type': 'text'},
                {'name': 'VALOR', 'id': 'VALOR', 'type': 'numeric'},
                {'name': 'PRAZOMES', 'id': 'PRAZOMES', 'type': 'numeric'},
                {'name': 'PRAZODIAS', 'id': 'PRAZODIAS', 'type': 'numeric'},
                {'name': 'STATUS', 'id': 'STATUS', 'type': 'text'},
                {'name': 'RESPONSAVEL', 'id': 'RESPONSAVEL', 'type': 'text'},
                {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'numeric'},
                {'name': 'PROJETO', 'id': 'PROJETO', 'type': 'numeric'},
                {'name': 'PROJETOSAPIENS', 'id': 'PROJETOSAPIENS', 'type': 'numeric'},
                {'name': 'ISS', 'id': 'ISS', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'ADMCENTRAL', 'id': 'ADMCENTRAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'PIS', 'id': 'PIS', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'COFINS', 'id': 'COFINS', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'CSLL', 'id': 'CSLL', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'IRPJ', 'id': 'IRPJ', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'INVESTIMENTOS', 'id': 'INVESTIMENTOS', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'ICMS', 'id': 'ICMS', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},

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