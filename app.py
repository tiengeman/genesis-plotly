import dash
from banco import *
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import back
import locale
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import dash.dash_table.FormatTemplate as FormatTemplate

app = dash.Dash(__name__)
server = app.server

# Paleta de cores
colors = {
    'background': '#F8F8F8',  # Cinza claro para o fundo da página
    'text': '#333333',        # Cor de texto principal em preto
    'orange': '#FF4E00',      # Laranja
    'white': '#FFFFFF',       # Branco
    'gray': '#CCCCCC'         # Cinza claro para elementos secundários
}

# Layout do aplicativo
app.layout = html.Div(style={'backgroundColor': colors['background'], 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H2(children='Performance Mensal por Competência', style={'color': colors['orange'], 'textAlign': 'center', 'marginBottom': '20px', 'fontSize': '2em'}),
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

# Callback para atualizar a tabela com base na seleção da lista suspensa
@app.callback(
    Output('tabela-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def atualizar_tabela(selecao):
    # Verifica se há uma seleção
    if selecao:
        # Obtém a tabela com base na seleção da lista suspensa
        df_tabela = tabela(selecao)
        
        # Formatar colunas numéricas para o estilo brasileiro
        for coluna in ['(R) MEDIÇÃO', '(D) DESPESAS', '(R-D) LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL']:
            df_tabela[coluna] = df_tabela[coluna].apply(lambda x: locale.format_string('%1.2f', x, grouping=True))
        
        # Cria DataTable a partir do DataFrame
        tabela_datatable = dash_table.DataTable(
            id='tabela',
            data=df_tabela.to_dict('records'),
            filter_action="native",
            columns=[
            {'name': 'LOCAL', 'id': 'LOCAL', 'type': 'text'},
            {'name': 'CONTRATO', 'id': 'CONTRATO', 'type': 'text'},
            {'name': 'C.CUSTOS', 'id': 'C.CUSTOS', 'type': 'text'},
            {'name': 'INATIVO', 'id': 'INATIVO', 'type': 'text'},
            {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'text'},
            {'name': '(R) MEDIÇÃO', 'id': '(R) MEDIÇÃO', 'type': 'numeric'},
            {'name': '(D) DESPESAS', 'id': '(D) DESPESAS', 'type': 'numeric'},
            {'name': '(R-D) LUCRO', 'id': '(R-D) LUCRO', 'type': 'numeric'},
            {'name': '%', 'id': '%', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'name': 'MEDIÇÃO TOTAL', 'id': 'MEDIÇÃO TOTAL', 'type': 'numeric'},
            {'name': 'DESPESAS TOTAIS', 'id': 'DESPESAS TOTAIS', 'type': 'numeric'},
            {'name': 'LUCRO TOTAL', 'id': 'LUCRO TOTAL', 'type': 'numeric'},
            {'name': '% TOTAL', 'id': '% TOTAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
        ],
            style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'right'
                } for c in ['(R) MEDIÇÃO', '(D) DESPESAS', '(R-D) LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL']
            ],
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': colors['orange'],
                'color': colors['white'],
            },
            style_data={
                'backgroundColor': colors['gray'],
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
        
        return tabela_datatable
    else:
        # Se não houver seleção, retorna uma mensagem indicando que nenhuma tabela está disponível
        return html.P("Nenhuma tabela disponível para esta seleção.")

# Callback para atualizar a tabela com base na seleção da lista suspensa
@app.callback(
    Output('tabela2-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def atualizar_tabela2(selecao):
    # Verifica se há uma seleção
    if selecao:
        # Obtém a tabela com base na seleção da lista suspensa
        df_tabela = tabela_2(selecao)
        
        # Formatar colunas numéricas para o estilo brasileiro
        for coluna in ['(R) MEDIÇÃO', '(D) DESPESAS', '(R-D) LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL']:
            df_tabela[coluna] = df_tabela[coluna].apply(lambda x: locale.format_string('%1.2f', x, grouping=True))
        
        # Cria DataTable a partir do DataFrame
        tabela_datatable = dash_table.DataTable(
            id='tabela',
            data=df_tabela.to_dict('records'),
            filter_action="native",
            columns=[
            {'name': 'LOCAL', 'id': 'LOCAL', 'type': 'text'},
            {'name': 'CONTRATO', 'id': 'CONTRATO', 'type': 'text'},
            {'name': 'C.CUSTOS', 'id': 'C.CUSTOS', 'type': 'text'},
            {'name': 'INATIVO', 'id': 'INATIVO', 'type': 'text'},
            {'name': 'FILIAL', 'id': 'FILIAL', 'type': 'text'},
            {'name': '(R) MEDIÇÃO', 'id': '(R) MEDIÇÃO', 'type': 'numeric'},
            {'name': '(D) DESPESAS', 'id': '(D) DESPESAS', 'type': 'numeric'},
            {'name': '(R-D) LUCRO', 'id': '(R-D) LUCRO', 'type': 'numeric'},
            {'name': '%', 'id': '%', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'name': 'MEDIÇÃO TOTAL', 'id': 'MEDIÇÃO TOTAL', 'type': 'numeric'},
            {'name': 'DESPESAS TOTAIS', 'id': 'DESPESAS TOTAIS', 'type': 'numeric'},
            {'name': 'LUCRO TOTAL', 'id': 'LUCRO TOTAL', 'type': 'numeric'},
            {'name': '% TOTAL', 'id': '% TOTAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
        ],
            style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': colors['white'], 'color': colors['text']},  # Ajustando o tamanho da fonte
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'right'
                } for c in ['(R) MEDIÇÃO', '(D) DESPESAS', '(R-D) LUCRO', 'MEDIÇÃO TOTAL', 'DESPESAS TOTAIS', 'LUCRO TOTAL']
            ],
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': colors['orange'],
                'color': colors['white'],
            },
            style_data={
                'backgroundColor': colors['gray'],
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
        
        return tabela_datatable
    else:
        # Se não houver seleção, retorna uma mensagem indicando que nenhuma tabela está disponível
        return html.P("Nenhuma tabela disponível para esta seleção.")

if __name__ == '__main__':
    app.run_server(debug=True)
