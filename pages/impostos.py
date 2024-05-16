import dash
import dash_table
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from back import *
from banco import *
import dash_bootstrap_components as dbc

# Paleta de cores
colors = {
    'background': '#EFEEEE',  # Cinza claro para o fundo da página
    'text': '#333333',        # Cor de texto principal em preto
    'orange': '#FF4E00',      # Laranja
    'white': '#FFFFFF',       # Branco
    'gray': '#616468'         # Cinza claro para elementos secundários
}

data_impostos = back.impostos()

modal = html.Div(
    [
        dbc.Row(dbc.Col(dbc.Button("Cadastrar", id="open-centered"), width="auto")),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cadastro de Impostos"), close_button=True),
                dbc.ModalBody("This modal is vertically centered"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-centered",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-centered",
            centered=True,
            is_open=False,
        ),
    ]
)

# Define a layout with a centered container
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Impostos', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
    html.Hr(style={'backgroundColor': colors['orange']}),  # Linha horizontal laranja
    html.Div(style={'marginTop': '20px'}),  # Espaçamento entre dropdown e tabela
    html.Div(id='tabela-impostos-container', style={'margin': '20px'}, children=[
        dbc.Row(
            modal,
        ),
        html.Div(style={'marginTop': '20px'}),
        dash_table.DataTable(
            id='tabela-impostos',
            data=df_impostos().to_dict('records'),
            filter_action="native",
            columns=[{'name': 'CONTRATO', 'id': 'CONTRATO', 'type': 'text'},
                     {'name': 'IMPOSTO', 'id': 'IMPOSTO', 'type': 'numeric'},],
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
            ]
        ),
    ])
])