import dash
from banco import *
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go

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
