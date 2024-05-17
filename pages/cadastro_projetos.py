from dash import dash_table
from dash import html
from back import *
from banco import *
import dash_bootstrap_components as dbc
from constants import *

# modelo do formulário de cadastro de projeto
form = dbc.Form(
    [
        dbc.Row([dbc.Label("Projeto", width=2),dbc.Col(dbc.Input(type="text", id="projeto", placeholder="Insira o nome do projeto"))],className="mb-3"),
        dbc.Row([dbc.Label("Imposto", width=2),dbc.Col(dbc.Input(type="number", id="imposto", placeholder="Insira o valor do imposto"))],className="mb-3")
    ]
)

# modelo do modal
modal = html.Div(
    [
        dbc.Button("Cadastrar", id="open-centered", style={'backgroundColor': colors['orange']}),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cadastro de Projetos"), close_button=True),
                dbc.ModalBody(form),
                dbc.ModalFooter(
                    dbc.Button(
                        "Submit",
                        id="close-centered",
                        style={'backgroundColor': colors['orange']},
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

# busca info no banco
df = df_impostos()
#formata a coluna que tem numeros
# format_numeric_columns(df, ["IMPOSTO"])

#div para mostrar os valores adicionados
input_values = html.Div(id="input-values")

# switch para edição da tabela
switch = html.Div([
    dbc.Switch(id="edit-switch", style={"color": colors['gray']}, value=False, label="Editar",
               input_style={"height": "20px", "background-color": colors['orange']})
], className="ms-auto")

# Define a layout with a centered container
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Cadastro de Projeto', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
    html.Hr(style={'backgroundColor': colors['orange']}),
    html.Div(style={'marginTop': '20px'}),
    html.Div(id='tabela-impostos-container', style={'margin': '20px'}, children=[
        dbc.Stack([
            modal, switch
        ],
        direction="horizontal",
        ),
        html.Div(style={'marginTop': '20px'}),
        input_values,  # Add the input_values div here
        dash_table.DataTable(
            id='tabela-impostos',
            data=df.to_dict('records'),
            filter_action="native",
            columns=[{"name": i, "id": i} for i in df.columns],
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