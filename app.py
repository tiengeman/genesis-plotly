import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
from pages.encargos import lista_encargos
import pages.gerencial as gerencial
import pages.home as home
import pages.diretoria as diretoria
import pages.relacao as relacao
import pages.cadastro_projetos as cadastro_projetos
import pages.impostos as impostos
import pages.encargos as encargos
import pages.detalhamento as detalhamento
from constants import *
from dash.exceptions import PreventUpdate
from banco import *
from back.inserts import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

#conteúdo dentro do menu
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Gerencial', href='/gerencial', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Diretoria', href='/diretoria', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Relação', href='/relacao', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Cadastro Projetos', href='/cadastro_projetos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Impostos', href='/impostos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Encargos', href='/encargos', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Detalhamento', href='/detalhamento', className='nav-link')),
    ],
    vertical=True,  # Make the nav items stack vertically
    pills=True,  # Make the nav items take up the full width of the sidebar
)

# botão para abrir o menu
offcanvas = html.Div(
    [
        dbc.Button(
            html.I(className="bi bi-list"),
            id="open-offcanvas",
            n_clicks=0,
            size="md", 
            color = '#FF4E00',
            style={"font-size": "1.60em"},
            className='btn-white',
        ),
        dbc.Offcanvas(
            sidebar,
            id="offcanvas",
            title="Menu",
            is_open=False,
        ),
    ]
)

# Top navigation bar
header = dbc.Navbar(
    dbc.Row(
        [
            dbc.Col(offcanvas),
            dbc.Col( #adicionar a imagem depois
                html.A(
                    html.Img(src=logo, height="60px"),
                    href="/home",
                    style={"textDecoration": "none"}  # Add this style to remove the default underline
                )
            ),
        ]
    ),
    color=colors['orange'],
    dark=True,
    className='justify-content-between', 
    style={'height': '50px'} 
)

# Div onde mostra o conteúdo de cada página
content_area = html.Div(id='content')

# Layout geral, caebçalho + content area
app.layout = html.Div([
    header,
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(content_area),
    ]),
])

#====================================================================== Callbacks ================================================================================================

#callback para mudar de página de acordo com o menu
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def update_content(pathname):
    if pathname == '/gerencial':
        return gerencial.layout
    elif pathname == '/diretoria':
        return diretoria.layout
    elif pathname == '/relacao':
        return relacao.layout
    elif pathname == '/cadastro_projetos':
        return cadastro_projetos.layout
    elif pathname == '/impostos':
        return impostos.layout
    elif pathname == '/encargos':
        return encargos.layout
    elif pathname == '/detalhamento':
        return detalhamento.layout
    else:
        return home.layout
    
# ================================================ UPDATE TABLE GERENCIAL ==========================================================

def update_table(output_id, value):
    if output_id == 'tabela-container':
        return gerencial.atualizar_tabela(value)
    elif output_id == 'tabela2-container':
        return gerencial.atualizar_tabela2(value)

#callback para atualizar as tabelas gerenciais de acordo com a competencia
@app.callback(
    Output('tabela-container', 'children'),
    Output('tabela2-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def update_tables(value):
    return update_table('tabela-container', value), update_table('tabela2-container', value)

# ================================================= UPDATE TABLE DETALHAMENTO ==========================================================

def update_table_detalhamento(output_id, value, contrato):
    if output_id == 'tabela-detalhamento-container-medicao':
        return detalhamento.atualizar_tabela_medicao(value, contrato)
    elif output_id == 'tabela-detalhamento-container-despesa':
        return detalhamento.atualizar_tabela_despesa(value, contrato)

#callback para atualizar as tabelas gerenciais de acordo com a competencia
@app.callback(
    Output('tabela-detalhamento-container-medicao', 'children'),
    Output('tabela-detalhamento-container-despesa', 'children'),
    [Input('minha-lista-suspensa-1-detalhamento', 'value'), Input('minha-lista-suspensa-2', 'value')]
)
def update_tables(value, contrato):
    print(f'{value} - {contrato}')
    return update_table_detalhamento('tabela-detalhamento-container-medicao', value, contrato), update_table_detalhamento('tabela-detalhamento-container-despesa', value, contrato)

    
#callback para abrir o menu
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# ============================================ MODAL CADASTRO ====================================================

#callback para abrir o modal de cadastro de projetos
@app.callback(
    Output("modal-centered-projetos", "is_open"),
    [Input("open-centered-projetos", "n_clicks"), Input("close-centered-projetos", "n_clicks")],
    [State("modal-centered-projetos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro
@app.callback(
    [
        Output("message-modal-projetos", "is_open"),
        Output("message-modal-header-projetos", "children"),
        Output("message-modal-body-projetos", "children"),
    ],
    [
        Input("close-centered-projetos", "n_clicks"),
        Input("close-message-modal-projetos", "n_clicks"),
    ],
    [
        State("OS", "value"), State("TIPO", "value"), State("ENQUADRAMENTO", "value"),
        State("CLIENTE", "value"), State("DESCRIÇÃO", "value"), State("ICJ", "value"),
        State("SAP", "value"), State("INÍCIO", "value"), State("FIM", "value"),
        State("ADITIVOS", "value"), State("VALOR", "value"), State("PRAZOMES", "value"),
        State("PRAZODIAS", "value"), State("STATUS", "value"), State("RESPONSÁVEL", "value"),
        State("FILIAL", "value"), State("PROJETO", "value"), State("PROJETO SAPIENS", "value"),
        State("ISS", "value"), State("ADM CENTRAL", "value"), State("PIS", "value"),
        State("COFINS", "value"), State("CSLL", "value"), State("IRPJ", "value"),
        State("INVESTIMENTOS", "value"), State("ICMS", "value"),
    ],
)
def update_message_modal(submit_clicks, close_clicks, os, tipo, enq, cliente, desc, icj, sap, inicio, fim, adt, valor, prazom,
                         prazod, status, resp, filial, projeto, projsap, iss, admcentral, pis,
                         cofins, csll, irpj, invest, icms):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "close-centered-projetos":
        if submit_clicks:
            lista_input = [os, tipo, enq, cliente, desc, icj, sap, inicio, fim, adt, valor, prazom,
                           prazod, status, resp, filial, projeto, projsap, iss, admcentral, pis,
                           cofins, csll, irpj, invest, icms]
            message = enviar_contratos(lista_input)
            if "sucesso" in message.lower():
                return True, "Sucesso!", message
            else:
                return True, "Erro!", message
        else:
            raise dash.exceptions.PreventUpdate
    elif triggered_id == "close-message-modal-projetos":
        return False, "", ""
    else:
        raise dash.exceptions.PreventUpdate
    
#callback para abrir o modal de cadastro de impostos
@app.callback(
    Output("modal-centered-impostos", "is_open"),
    [Input("open-centered-impostos", "n_clicks"), Input("close-centered-impostos", "n_clicks")],
    [State("modal-centered-impostos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro de impostos
@app.callback(
    [
        Output("message-modal-impostos", "is_open"),
        Output("message-modal-header-impostos", "children"),
        Output("message-modal-body-impostos", "children"),
    ],
    [
        Input("close-centered-impostos", "n_clicks"),
        Input("close-message-modal-impostos", "n_clicks"),
    ],
    [
        State("RECEITATOTAL", "value"), State("PISRETIDO", "value"), State("PISPAGO", "value"),
        State("COFINSRETIDO", "value"), State("COFINSPAGO", "value"), State("DATAFECHAMENTO", "value"),
        State("COMPETENCIA", "value"),
    ],
)
def update_message_modal(submit_clicks, close_clicks, receitatotal, pisretido, pispago, cofinsretido, cofinspago, datafechamento, competencia):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "close-centered-impostos":
        if submit_clicks:
            lista_input = [receitatotal, pisretido, pispago, cofinsretido, cofinspago, datafechamento, competencia]
            message = enviar_contratos(lista_input)
            if "sucesso" in message.lower():
                return True, "Sucesso!", message
            else:
                return True, "Erro!", message
        else:
            raise dash.exceptions.PreventUpdate
    elif triggered_id == "close-message-modal-impostos":
        return False, "", ""
    else:
        raise dash.exceptions.PreventUpdate
    
#callback para abrir o modal de cadastro de encargos
@app.callback(
    Output("modal-centered-encargos", "is_open"),
    [Input("open-centered-encargos", "n_clicks"), Input("close-centered-encargos", "n_clicks")],
    [State("modal-centered-encargos", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro de encargos
@app.callback(
    [
        Output("message-modal-encargos", "is_open"),
        Output("message-modal-header-encargos", "children"),
        Output("message-modal-body-encargos", "children"),
    ],
    [
        Input("close-centered-encargos", "n_clicks"),
        Input("close-message-modal-encargos", "n_clicks"),
    ],
    [
        State("CODIGO", "value"), State("NOME", "value"), State("CNPJ", "value"),
        State("PERCENTUAL", "value"), State("CPRB", "value"), State("INICIO", "value"),
        State("FIM", "value"),
    ],
)
def update_message_modal(submit_clicks, close_clicks, codigo, nome, cnpj, percentual, cprb, inicio, fim):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "close-centered-encargos":
        if submit_clicks:
            lista_input = [close_clicks, codigo, nome, cnpj, percentual, cprb, inicio, fim]
            message = enviar_contratos(lista_input)
            if "sucesso" in message.lower():
                return True, "Sucesso!", message
            else:
                return True, "Erro!", message
        else:
            raise dash.exceptions.PreventUpdate
    elif triggered_id == "close-message-modal-encargos":
        return False, "", ""
    else:
        raise dash.exceptions.PreventUpdate

#========================================= SWITCH TABELA EDITÁVEL ====================================================

# callback para deixar apenas algumas colunas editáveis na tela de cadastro de projetos
@app.callback(
    Output('tabela-projetos', 'columns'),
    Input('edit-switch-contratos', 'value')
)
def toggle_editability(value):
    columns = [{"name": i, "id": i, "editable": value} if i not in ["VALOR", "PRAZOMES", "PRAZODIAS"] else {"name": i, "id": i} for i in cad_contratos().columns]
    return columns

# callback para deixar apenas algumas colunas editáveis na tela de cadastro de projetos
@app.callback(
    Output('tabela-impostos', 'columns'),
    Input('edit-switch-impostos', 'value')
)
def toggle_editability(value):
    columns = [{"name": i, "id": i, "editable": value} if i not in [] else {"name": i, "id": i} for i in cad_impostos().columns]
    return columns


# Atualizar a propriedade editable das tabelas quando o switch é acionado
@app.callback(
    [Output(f'tabela-encargos-{index}', 'editable') for index in range(len(lista_encargos))],
    [Input('edit-switch-encargos', 'value')]
)
def update_editable(edit_value):
    return [edit_value] * len(lista_encargos)

# ============================================== BOTÃO ATUALIZAR ===========================================================

# Crie a callback para atualizar a tabela de projetos quando o botão for clicado
@app.callback(
    Output('tabela-projetos', 'data'),
    [Input('refresh-button-contratos', 'n_clicks')]
)
def refresh_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_contratos = cad_contratos()
        # Retorne os dados atualizados da tabela
        return df_contratos.to_dict('records')
    
# Crie a callback para atualizar a tabela de impostos quando o botão for clicado
@app.callback(
    Output('tabela-impostos', 'data'),
    [Input('refresh-button-impostos', 'n_clicks')]
)
def refresh_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_impostos = cad_impostos()
        # Retorne os dados atualizados da tabela
        return df_impostos.to_dict('records')
    
# Crie a callback para atualizar a tabela de encargos quando o botão for clicado
@app.callback(
    [Output(f'tabela-encargos-{index}', 'data') for index in range(len(lista_encargos))],
    [Input('refresh-button-encargos', 'n_clicks')]
)
def refresh_table(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Atualize o dataframe df chamando a função cad_contratos() novamente
        df_impostos = cad_impostos()
        # Retorne os dados atualizados da tabela
        return df_impostos.to_dict('records')
    
# @app.callback(
#     Output('row-info-container', 'children'),
#     Input('tabela', 'active_cell'),
#     Input('tabela2', 'active_cell'),
#     State('tabela', 'data'),
#     State('tabela', 'columns'),
#     State('tabela2', 'data'),
#     State('tabela2', 'columns')
# )
# def show_row_info(active_cell1, active_cell2, data1, columns1, data2, columns2):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         raise PreventUpdate

#     if ctx.triggered[0]['prop_id'].split('.')[0] == 'tabela':
#         active_cell = active_cell1
#         data = data1
#         columns = columns1
#     else:
#         active_cell = active_cell2
#         data = data2
#         columns = columns2

#     if active_cell is None:
#         raise PreventUpdate

#     column_id = columns[active_cell['column']]['id']
#     if column_id!= 'MEDIÇÃO':
#         raise PreventUpdate

#     row_index = active_cell['row']
#     row_data = data[row_index]
#     # Create a new table or a div to show the row information
#     info_table = html.Div([
#         html.H5(f"Row {row_index} Information:"),
#         html.Table([
#             html.Tr([html.Th(key), html.Td(value)]) for key, value in row_data.items()
#         ])
#     ])
#     return info_table

# @app.callback(
#     Output('detalhamento-container', 'children'),
#     Input('detalhamento-button', 'n_clicks')
# )
# def update_detalhamento_container(n_clicks):
#     if n_clicks is not None and n_clicks > 0:
#         return detalhamento.layout
#     else:
#         return html.P("Nenhum detalhamento disponível.")

if __name__ == '__main__':
    app.run_server(debug=True)