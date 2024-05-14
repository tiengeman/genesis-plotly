from dash import html, dcc
from dash import dash_table
import locale
import dash.dash_table.FormatTemplate as FormatTemplate
from banco import *

# Paleta de cores
colors = {
    'background': '#EFEEEE',  # Cinza claro para o fundo da página
    'text': '#333333',        # Cor de texto principal em preto
    'orange': '#FF4E00',      # Laranja
    'white': '#FFFFFF',       # Branco
    'gray': '#CCCCCC'         # Cinza claro para elementos secundários
}

# Define a layout with a centered container
layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    html.H1(children='Performance Mensal por Competência', style={'color': '#616468', 'marginTop': '10px'}),
    html.Hr(style={'backgroundColor': colors['orange']}),  # Linha horizontal laranja
    html.Div(style={'marginTop': '20px'}),
    # Lista suspensa
    dcc.Dropdown(
        id='minha-lista-suspensa',
        options=back.competencias(),
        value=back.competencias()[-1],
        style={'fontFamily': 'Arial, sans-serif'}  # Definindo a fonte da lista suspensa
    ),
    html.Div(style={'marginTop': '20px'}),  # Espaçamento entre dropdown e tabela
    html.Div(id='tabela-container', style={'margin': '20px'}),  # Div para mostrar a tabela selecionada com margem
    html.Div(id='tabela2-container', style={'margin': '20px'})  # Div para mostrar a tabela selecionada com margem
])

def atualizar_tabela(selecao):
    if selecao:
        df_tabela = tabela(selecao)
        format_numeric_columns(df_tabela, ['(R) MEDIÇÃO', '(D) DESPESAS', '(R-D) LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL'])
        return create_datatable(df_tabela, colors)
    else:
        return html.P("Nenhuma tabela disponível para esta seleção.")

def atualizar_tabela2(selecao):
    if selecao:
        df_tabela = tabela_2(selecao)
        format_numeric_columns(df_tabela, ['(R) MEDIÇÃO', '(D) DESPESAS', '(R-D) LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL'])
        return create_datatable(df_tabela, colors)
    else:
        return html.P("Nenhuma tabela disponível para esta seleção.")

def format_numeric_columns(df, columns):
    for col in columns:
        # Aplica a formatação para cada valor na coluna
        df[col] = df[col].apply(lambda x: '{:,.2f}'.format(x).replace('.', '*').replace(',', '.').replace('*', ','))

def create_datatable(df, colors):
    return dash_table.DataTable(
        id='tabela',
        data=df.to_dict('records'),
        filter_action="native",
        columns=[
            {'name': 'LOCAL', 'id': 'LOCAL', 'type': 'text', "hideable": True},
            {'name': 'CONTRATO', 'id': 'CONTRATO', 'type': 'text'},
            {'name': 'CC', 'id': 'C.CUSTOS', 'type': 'text', "hideable": True},
            {'name': 'INATIVO', 'id': 'INATIVO', 'type': 'text', "hideable": True},
            {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'text', "hideable": True},
            {'name': 'MEDIÇÃO', 'id': '(R) MEDIÇÃO', 'type': 'numeric', "hideable": True},
            {'name': 'DESPESAS', 'id': '(D) DESPESAS', 'type': 'numeric', "hideable": True},
            {'name': 'LUCRO', 'id': '(R-D) LUCRO', 'type': 'numeric', "hideable": True},
            {'name': '%', 'id': '%', 'type': 'numeric', 'format': FormatTemplate.percentage(1), "hideable": True},
            {'name': 'MEDIÇÃO TOTAL', 'id': 'MEDIÇÃO TOTAL', 'type': 'numeric', "hideable": True},
            {'name': 'DESP. TOTAIS', 'id': 'DESPESAS TOTAIS', 'type': 'numeric', "hideable": True},
            {'name': 'LUCRO TOTAL', 'id': 'LUCRO TOTAL', 'type': 'numeric', "hideable": True},
            {'name': '%', 'id': '% TOTAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1), "hideable": True},
        ],
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
        style_cell_conditional = [
            {'if': {'column_id': 'LOCAL'}, 'width': '4%'},
            {'if': {'column_id': 'CONTRATO'}, 'width': '35%'},
            {'if': {'column_id': 'C.CUSTOS'}, 'width': '4%'},
            {'if': {'column_id': 'INATIVO'}, 'width': '4%'},
            {'if': {'column_id': 'FILIAL'}, 'width': '4%'},
            {'if': {'column_id': '(R) MEDIÇÃO'}, 'width': '6%', 'textAlign': 'right'},
            {'if': {'column_id': '(D) DESPESAS'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': '(R-D) LUCRO'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': '%'}, 'width': '4%', 'textAlign': 'right'},
            {'if': {'column_id': 'MEDIÇÃO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': 'DESPESAS TOTAIS'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': 'LUCRO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': '% TOTAL'}, 'width': '4%', 'textAlign': 'right'},
        ],
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#616468',
            'color': colors['white'],
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': colors['background'],
            },
            {
                'if': {
                    'filter_query': "{CONTRATO} = 'TOTAL OPERAÇÃO'",
                },
                'backgroundColor': colors['gray'],
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'filter_query': "{%} < 0",
                    'column_id': '%',
                },
                'backgroundColor': '#B22222',
                'color': 'white',
            },
            {
                'if': {
                    'filter_query': "{%} > 0.07",
                    'column_id': '%',
                },
                'backgroundColor': '#008000',
                'color': 'white',   
            },
            {
                'if': {
                    'filter_query': "{%} > 0 && {%} < 0.07",
                    'column_id': '%',
                },
                'backgroundColor': '#DAA520',
                'color': 'white',
            },
            {
                'if': {
                    'filter_query': "{% TOTAL} < 0",
                    'column_id': '% TOTAL',
                },
                'backgroundColor': '#B22222',
                'color': 'white',
            },
            {
                'if': {
                    'filter_query': "{% TOTAL} > 0.07",
                    'column_id': '% TOTAL',
                },
                'backgroundColor': '#008000',
                'color': 'white',   
            },
            {
                'if': {
                    'filter_query': "{% TOTAL} > 0 && {% TOTAL} < 0.07",
                    'column_id': '% TOTAL',
                },
                'backgroundColor': '#DAA520',
                'color': 'white',
            }
        ], 
    )