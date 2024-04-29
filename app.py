import dash
from banco import *
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import back
import locale
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import dash.dash_table.FormatTemplate as FormatTemplate
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

# Layout do aplicativo
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9', 'color': '#333'}, children=[
    html.Div([
        html.H2(children='Performance Mensal por Contrato', style={'color': '#ff4e00', 'fontFamily': 'Arial Black', 'fontSize': '36px', 'textAlign': 'center', 'marginBottom': '20px'}),  # Título com cor laranja e estilo de fonte Arial Black
    ]),
    html.Hr(style={'borderColor': '#ff4e00', 'marginBottom': '20px'}),  # Linha horizontal com cor laranja e margem inferior
    dcc.Tabs(id='tabs', value='tab-tabela', children=[  # Tabs para separar as telas
        dcc.Tab(label='Tabela', value='tab-tabela', selected_style={'backgroundColor': '#ff4e00', 'color': '#fff','margin':"20px"}),  # Tab para exibir a tabela
        dcc.Tab(label='Gráfico e Informações', value='tab-grafico', selected_style={'backgroundColor': '#ff4e00', 'color': '#fff'}),  # Tab para exibir o gráfico e informações
    ]),
    
    html.Div(id='tabs-content')  # Div para mostrar o conteúdo da tab selecionada
])

# Callback para atualizar o conteúdo da tab
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-tabela':  # Se a tab selecionada for a de tabela
        # Lista suspensa
        lista_suspensa = dcc.Dropdown(
            id='minha-lista-suspensa',
            options=back.competencias(),
            value=back.competencias()[-1],
            style={'fontFamily': 'Arial, sans-serif', 'color': '#ff4e00', 'backgroundColor': '#f1f1f1'},  # Cores da lista suspensa
        )

        # Tabela de dados
        tabela_datatable = html.Div(id='tabela-selecionada')

        # Layout da tab de tabela
        tab_tabela = html.Div([
            lista_suspensa,
            html.Div(style={'margin-top': '20px'}),  # Espaçamento entre dropdown e tabela
            tabela_datatable
        ])

        return tab_tabela
    elif tab == 'tab-grafico':  # Se a tab selecionada for a de gráfico e informações
        # Lista suspensa
        lista_suspensa = dcc.Dropdown(
            id='minha-lista-suspensa-grafico',
            options=back.competencias(),
            value=back.competencias()[-1],
            style={'fontFamily': 'Arial, sans-serif', 'color': '#ff4e00', 'backgroundColor': '#f1f1f1'},  # Cores da lista suspensa
        )

        # Gráfico e informações
        grafico_info = html.Div(id='grafico-info')

        # Layout da tab de gráfico e informações
        tab_grafico = html.Div([
            lista_suspensa,
            html.Div(style={'margin-top': '20px'}),  # Espaçamento entre dropdown e gráfico
            grafico_info
        ])

        return tab_grafico

# Callback para atualizar o conteúdo da tabela
@app.callback(
    Output('tabela-selecionada', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def atualizar_tabela(selecao):
    # Verifica se há uma seleção
    if selecao:
        # Obtém a tabela com base na seleção da lista suspensa
        df_tabela = tabela(selecao)
        
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
                {'name': '(R) MEDIÇÃO', 'id': '(R) MEDIÇÃO', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': '(D) DESPESAS', 'id': '(D) DESPESAS', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': '(R-D) LUCRO', 'id': '(R-D) LUCRO', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': '%', 'id': '%', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
                {'name': 'MEDIÇÃO TOTAL', 'id': 'MEDIÇÃO TOTAL', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'DESPESAS TOTAIS', 'id': 'DESPESAS TOTAIS', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'LUCRO TOTAL', 'id': 'LUCRO TOTAL', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': '% TOTAL', 'id': '% TOTAL', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            ],
            style_cell={'textAlign': 'center', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '0.8em', 'backgroundColor': '#fff', 'color': '#333'},  # Ajustando o estilo das células da tabela
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'right'
                } for c in ['(R) MEDIÇÃO', 'MEDIÇÃO TOTAL']
            ],
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': '#ff4e00',
                'color': '#fff',
            },
             style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(245,245,245)',
                },
                {
                    'if': {
                        'filter_query': "{CONTRATO} = 'TOTAL OPERAÇÃO'",
                    },
                    'backgroundColor': 'rgb(220,220,220)',
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

# Callback para atualizar o conteúdo do gráfico e informações
@app.callback(
    Output('grafico-info', 'children'),
    [Input('minha-lista-suspensa-grafico', 'value')]
)
def atualizar_grafico_info(selecao):
    # Verifica se há uma seleção
    if selecao:
        # Obtém a tabela com base na seleção da lista suspensa
        df_tabela = tabela(selecao)
        
        # Cria um gráfico de barras 3D com os dados da coluna "(R) MEDIÇÃO"
        grafico_barras = go.Figure(
            data=[go.Bar(x=df_tabela['CONTRATO'], y=df_tabela['(R) MEDIÇÃO'], marker_color='#ff4e00')],
            layout=go.Layout(
                title='Gráfico de Barras - (R) MEDIÇÃO por CONTRATO',
                scene=dict(
                    xaxis=dict(title='CONTRATO'),
                    yaxis=dict(title='(R) MEDIÇÃO'),
                    zaxis=dict(title='Valor'),
                ),
                font=dict(family='Arial, sans-serif', size=12, color='#333'),  # Ajustando a fonte e o tamanho do texto
                paper_bgcolor='#f9f9f9',  # Cor de fundo do gráfico
            )
        )

        # Renderiza o gráfico
        grafico_barras_html = dcc.Graph(id='grafico-barras', figure=grafico_barras)

        # Informações adicionais
        informacoes_adicionais = html.Div([
            html.H3("Informações Adicionais", style={'color': '#ff4e00'}),
            html.P("."),
            html.P("."),
        ])

        # Renderiza o gráfico e informações adicionais
        return html.Div([grafico_barras_html, informacoes_adicionais])
    else:
        # Se não houver seleção, retorna uma mensagem indicando que nenhuma tabela está disponível
        return html.P("Nenhuma tabela disponível para esta seleção.") 

if __name__ == '__main__':
    app.run_server(debug=True)
