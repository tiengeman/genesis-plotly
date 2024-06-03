from dash import html, dcc
from dash import html, dcc
from dash import dash_table
import dash.dash_table.FormatTemplate as FormatTemplate
import dash_bootstrap_components as dbc
from banco import *
from constants import *

# Layout com container centralizado e dois dropdowns
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Detalhamento', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
    html.Hr(style={'backgroundColor': colors['orange']}),  # Linha horizontal laranja
    html.Div(style={'marginTop': '20px'}),
    
    # dbc.Row contendo dois dropdowns
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='minha-lista-suspensa-1-detalhamento',
                options=back.competencias(),
                style={'fontFamily': 'Arial, sans-serif'}  # Definindo a fonte da lista suspensa
            ),
            width=6
        ),
        dbc.Col(
            dcc.Dropdown(
                id='minha-lista-suspensa-2',
                options=lista_contratos(),
                style={'fontFamily': 'Arial, sans-serif'}  # Definindo a fonte da lista suspensa
            ),
            width=6
        )
    ], justify='center'),
    
    html.Div(style={'marginTop': '20px'}),  # Espaçamento entre dropdown e tabela

    html.H3('Medição', style={'marginTop': '10px', 'color': colors['gray']}),
    html.Div(id='tabela-detalhamento-container-medicao', style={'margin': '20px'}),
    html.H3('Despesas', style={'marginTop': '10px', 'color': colors['gray']}),
    html.Div(id='tabela-detalhamento-container-despesa', style={'margin': '20px'}),
    
    html.Div(id='tabela-detalhamento-container', style={'margin': '20px'}),  # Div para mostrar a tabela selecionada com margem
])

#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela_despesa(selecao, contrato):
    df_tabela = detalha_despesas(selecao, contrato)
    return create_datatable_despesas(df_tabela, colors, "tabela-detalhamento-despesa")
    
#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela_medicao(selecao, contrato):
    df_tabela = detalha_receita(selecao, contrato)
    return create_datatable_medicao(df_tabela, colors, "tabela-detalhamento-medicao")
    
# função de criação de tabela
def create_datatable_despesas(df, colors, id):
    return dash_table.DataTable(
        id=id,
        data=df.to_dict('records'),
        filter_action="native",
        columns=[
            {'name': 'PROJETO-UNI', 'id': 'PROJETO-UNI', 'type': 'text'},
            {'name': 'DESCRIÇÃO', 'id': 'DESCRIÇÃO', 'type': 'text'},
            {'name': 'PROJETO-ORI', 'id': 'PROJETO-ORI', 'type': 'text'},
            {'name': 'DOCUMENTO', 'id': 'DOCUMENTO', 'type': 'text'},
            {'name': 'AGENTE', 'id': 'AGENTE', 'type': 'text'},
            {'name': 'DESC. AGENTE', 'id': 'DESC. AGENTE', 'type': 'text'},
            {'name': 'VALOR ORI', 'id': 'VALOR ORI', 'type': 'numeric'},
            {'name': 'VALOR INVEST.', 'id': 'VALOR INVEST.', 'type': 'numeric'},
            {'name': 'VALOR DESP', 'id': 'VALOR DESP', 'type': 'numeric'},
            {'name': 'COD. CLASSE', 'id': 'COD. CLASSE', 'type': 'text'},
            {'name': 'DESC. CLASSE', 'id': 'DESC. CLASSE', 'type': 'text'},
            {'name': 'DATA', 'id': 'DATA', 'type': 'datetime'},
            {'name': 'COMPETENCIA', 'id': 'COMPETENCIA', 'type': 'text'},
            {'name': 'OBSERVAÇÕES', 'id': 'OBSERVAÇÕES', 'type': 'text'},
            {'name': 'TIPO', 'id': 'TIPO', 'type': 'text'},
        ],
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
        # estilo do cabeçalho tabela
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#616468',
            'color': colors['white'],
        },
        # estiliza os dados das tabelas gerenciais
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': colors['background'],
            },

        ],
        style_table={'overflowX': 'auto', 'width': '100%'},  # Definindo o tamanho da tabela 
    )

# função de criação de tabela
def create_datatable_medicao(df, colors, id):
    return dash_table.DataTable(
        id=id,
        data=df.to_dict('records'),
        filter_action="native",
        columns=[
            {'name': 'PROJETO-UNI', 'id': 'PROJETO-UNI', 'type': 'text'},
            {'name': 'DESCRIÇÃO', 'id': 'DESCRIÇÃO', 'type': 'text'},
            {'name': 'PROJETO-ORI', 'id': 'PROJETO-ORI', 'type': 'text'},
            {'name': 'DOCUMENTO', 'id': 'DOCUMENTO', 'type': 'text'},
            {'name': 'CLIENTE', 'id': 'CLIENTE', 'type': 'text'},
            {'name': 'DATA', 'id': 'DATA', 'type': 'datetime'},
            {'name': 'VALOR', 'id': 'VALOR', 'type': 'numeric'},
            {'name': 'VALOR-RETENCAO', 'id': 'VALOR-RETENCAO', 'type': 'numeric'},
            {'name': 'VALOR-ADM', 'id': 'VALOR-ADM', 'type': 'numeric'},
            {'name': 'COMPETENCIA', 'id': 'COMPETENCIA', 'type': 'text'},
            {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'text'},
        ],
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
        # estilo do cabeçalho tabela
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#616468',
            'color': colors['white'],
        },
        # estiliza os dados das tabelas gerenciais
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': colors['background'],
            },

        ], 
        style_table={'overflowX': 'auto', 'width': '100%'},  # Definindo o tamanho da tabela 
    )