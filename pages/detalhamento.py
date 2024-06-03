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
                value=back.competencias()[-1],
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
    if selecao:
        df_tabela = detalha_despesas(selecao, contrato)
        return create_datatable_despesas(df_tabela, colors, "tabela-detalhamento-despesa")
    else:
        return html.P("Nenhuma tabela disponível para esta seleção.")
    
#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela_medicao(selecao, contrato):
    if selecao:
        df_tabela = tabela(selecao)
        format_numeric_columns(df_tabela, ['MEDIÇÃO', 'DESPESAS', 'LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL'])
        return create_datatable(df_tabela, colors, "tabela-detalhamento-medicao")
    else:
        return html.P("Nenhuma tabela disponível para esta seleção.")
    
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
        # style_cell_conditional = [
        #     {'if': {'column_id': 'LOCAL'}, 'width': '4%'},
        #     {'if': {'column_id': 'CONTRATO'}, 'width': '35%'},
        #     {'if': {'column_id': 'C.CUSTOS'}, 'width': '4%'},
        #     {'if': {'column_id': 'INATIVO'}, 'width': '4%'},
        #     {'if': {'column_id': 'FILIAL'}, 'width': '4%'},
        #     {'if': {'column_id': 'MEDIÇÃO'}, 'width': '6%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'DESPESAS'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'LUCRO'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': '%'}, 'width': '4%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'MEDIÇÃO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'DESPESAS TOTAIS'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'LUCRO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': '% TOTAL'}, 'width': '4%', 'textAlign': 'right'},
        # ],
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
    )

# função de criação de tabela
def create_datatable(df, colors, id):
    return dash_table.DataTable(
        id=id,
        data=df.to_dict('records'),
        filter_action="native",
        columns=[
            {'name': 'LOCAL', 'id': 'LOCAL', 'type': 'text'},
            {'name': 'CONTRATO', 'id': 'CONTRATO', 'type': 'text'},
            {'name': 'CC', 'id': 'C.CUSTOS', 'type': 'text'},
            {'name': 'INATIVO', 'id': 'INATIVO', 'type': 'text'},
            {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'text'},
            {'name': 'MEDIÇÃO', 'id': 'MEDIÇÃO', 'type': 'numeric'},
            {'name': 'DESPESAS', 'id': 'DESPESAS', 'type': 'numeric'},
            {'name': 'LUCRO', 'id': 'LUCRO', 'type': 'numeric'},
            {'name': '%', 'id': '%', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'name': 'MEDIÇÃO TOTAL', 'id': 'MEDIÇÃO TOTAL', 'type': 'numeric'},
            {'name': 'DESP. TOTAIS', 'id': 'DESPESAS TOTAIS', 'type': 'numeric'},
            {'name': 'LUCRO TOTAL', 'id': 'LUCRO TOTAL', 'type': 'numeric'},
            {'name': '%', 'id': '% TOTAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
        ],
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
        # style_cell_conditional = [
        #     {'if': {'column_id': 'LOCAL'}, 'width': '4%'},
        #     {'if': {'column_id': 'CONTRATO'}, 'width': '35%'},
        #     {'if': {'column_id': 'C.CUSTOS'}, 'width': '4%'},
        #     {'if': {'column_id': 'INATIVO'}, 'width': '4%'},
        #     {'if': {'column_id': 'FILIAL'}, 'width': '4%'},
        #     {'if': {'column_id': 'MEDIÇÃO'}, 'width': '6%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'DESPESAS'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'LUCRO'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': '%'}, 'width': '4%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'MEDIÇÃO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'DESPESAS TOTAIS'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': 'LUCRO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
        #     {'if': {'column_id': '% TOTAL'}, 'width': '4%', 'textAlign': 'right'},
        # ],
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
    )