from dash import html, dcc
from dash import dash_table
import dash.dash_table.FormatTemplate as FormatTemplate
import dash_bootstrap_components as dbc
from banco import *
from constants import *
from filters import *

layout = dbc.Card(style={'fontFamily': 'Arial, sans-serif', 'textAlign': 'center'}, children=[
    dbc.CardHeader(
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Resumo', value='tab-1'),
            dcc.Tab(label='Detalhamento', value='tab-2'),
            dcc.Tab(label='Dashboards', value='tab-3'),
            dcc.Tab(label='Backlog', value='tab-4'),
            dcc.Tab(label='Ger. Geral', value='tab-5'),
            dcc.Tab(label='Ger. Contratos', value='tab-6'),
            dcc.Tab(label='Ger. Administrativa', value='tab-7'),
            dcc.Tab(label='Fluxo de Contratos', value='tab-8'),
        ])
    ),
    html.Div(id='tabs-content')
])

# ================================================== FUNÇÕES GERENCIAL ==================================================================

global df_medicao_gerencial
global df_despesa_gerencial
global lista_todos_contrato
global lista_todos_cc
global lista_todos_locais
lista_todos_contrato, lista_todos_cc, lista_todos_locais = back.pega_centro_custos()
lista_todos_contrato, lista_todos_cc, lista_todos_locais = ordenar_listas_locais(lista_todos_contrato, lista_todos_cc, lista_todos_locais)
df_medicao_gerencial = detalha_receita_sem_format()
df_medicao_gerencial = df_medicao_gerencial.fillna(0)
df_despesa_gerencial = detalha_despesas_sem_format()
df_despesa_gerencial = df_despesa_gerencial.fillna(0)

#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela(selecao):
    if selecao:
        lista_todos_contrato1 = lista_todos_contrato.copy()
        lista_todos_cc1 = lista_todos_cc.copy()
        lista_todos_locais1 = lista_todos_locais.copy()
        df_tabela = tabela(selecao, df_medicao_gerencial, df_despesa_gerencial, lista_todos_contrato1, lista_todos_cc1, lista_todos_locais1)
        format_numeric_columns(df_tabela, ['MEDIÇÃO', 'DESPESAS', 'LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL'])
        return create_datatable(df_tabela, colors, "tabela")
    else:
        return html.P("Nenhuma tabela disponível para esta seleção.")

#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela2(selecao):
    if selecao:
        df_tabela = tabela_2(selecao)
        format_numeric_columns(df_tabela, ['MEDIÇÃO', 'DESPESAS', 'LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL'])
        return create_datatable(df_tabela, colors, "tabela2")
    else:
        return html.P("Nenhuma tabela disponível para esta seleção.")

# função de criação de tabela
def create_datatable(df, colors, id):
    return dash_table.DataTable(
        id=id,
        data=df.to_dict('records'),
        filter_action="native",
        columns=[
            {'name': 'LOCAL', 'id': 'LOCAL', 'type': 'text', "hideable": True},
            {'name': 'CONTRATO', 'id': 'CONTRATO', 'type': 'text'},
            {'name': 'CC', 'id': 'C.CUSTOS', 'type': 'numeric', "hideable": True},
            {'name': 'INATIVO', 'id': 'INATIVO', 'type': 'text', "hideable": True},
            {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'text', "hideable": True},
            {'name': 'MEDIÇÃO', 'id': 'MEDIÇÃO', 'type': 'numeric', "hideable": True},
            {'name': 'DESPESAS', 'id': 'DESPESAS', 'type': 'numeric', "hideable": True},
            {'name': 'LUCRO', 'id': 'LUCRO', 'type': 'numeric', "hideable": True},
            {'name': '%', 'id': '%', 'type': 'numeric', 'format': FormatTemplate.percentage(1), "hideable": True},
            {'name': 'MEDIÇÃO TOTAL', 'id': 'MEDIÇÃO TOTAL', 'type': 'numeric', "hideable": True},
            {'name': 'DESP. TOTAIS', 'id': 'DESPESAS TOTAIS', 'type': 'numeric', "hideable": True},
            {'name': 'LUCRO TOTAL', 'id': 'LUCRO TOTAL', 'type': 'numeric', "hideable": True},
            {'name': '%', 'id': '% TOTAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1), "hideable": True},
        ],
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
        style_cell_conditional = [
            {'if': {'column_id': 'LOCAL'}, 'width': '4%'},
            {'if': {'column_id': 'CONTRATO'}, 'width': '25%'},
            {'if': {'column_id': 'C.CUSTOS'}, 'width': '4%'},
            {'if': {'column_id': 'INATIVO'}, 'width': '4%'},
            {'if': {'column_id': 'FILIAL'}, 'width': '4%'},
            {'if': {'column_id': 'MEDIÇÃO'}, 'width': '6%', 'textAlign': 'right'},
            {'if': {'column_id': 'DESPESAS'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': 'LUCRO'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': '%'}, 'width': '4%', 'textAlign': 'right'},
            {'if': {'column_id': 'MEDIÇÃO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': 'DESPESAS TOTAIS'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': 'LUCRO TOTAL'}, 'width': '7%', 'textAlign': 'right'},
            {'if': {'column_id': '% TOTAL'}, 'width': '4%', 'textAlign': 'right'},
        ],
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
            {
                'if': {
                    'filter_query': "{CONTRATO} = 'TOTAL OPERAÇÃO'",
                },
                'backgroundColor': colors['gray'],
                'color': 'white',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'filter_query': "{CONTRATO} = 'TOTAL OPERAÇÃO'",
                    'column_id': 'INATIVO',
                },
                'color': colors['gray'],
            },
                        {
                'if': {
                    'filter_query': "{CONTRATO} = 'TOTAL CAPEX'",
                },
                'backgroundColor': colors['gray'],
                'color': 'white',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'filter_query': "{CONTRATO} = 'TOTAL CAPEX'",
                    'column_id': 'INATIVO',
                },
                'color': colors['gray'],
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
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
    )

# ============================================= FUNÇÕES DETALHAMENTO ===================================================
global df_despesa
df_despesa = detalha_despesas()
global df_medicao
df_medicao = detalha_receita()

#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela_despesa(selecao, contrato):
    if selecao == None:
        selecao = []
    if contrato == None:
        contrato = []
    df_tabela = filtra_detalha(df_despesa, selecao, contrato)
    return create_datatable_despesas(df_tabela, colors, "tabela-detalhamento-despesa")
    
#função para atualizar a tabela, é chamada no callback quando uma competencia é selecionada
def atualizar_tabela_medicao(selecao, contrato):
    if selecao == None:
        selecao = []
    if contrato == None:
        contrato = []
    df_tabela = filtra_detalha(df_medicao, selecao, contrato)
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