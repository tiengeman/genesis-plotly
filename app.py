import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pages.gerencial as gerencial
import pages.home as home
import pages.diretoria as diretoria
import pages.relacao as relacao
import pages.cadastro_projetos as cadastro_projetos
from constants import *
from dash.exceptions import PreventUpdate
from pages.cadastro_projetos import df as df_projetos
from banco import *

# Constants
# logo = 'https://i0.wp.com/engeman.net/wp-content/uploads/2024/04/LOGO_ENGEMAN_HORIZONTAL-e1714498268589.png?w=851&ssl=1'

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
                # html.A(
                #     html.Img(src=logo, height="60px"),
                #     href="/home",
                #     style={"textDecoration": "none"}  # Add this style to remove the default underline
                # )
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
    else:
        return home.layout

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

#callback para abrir o modal de cadastro dos impostos
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback para salvar itens do cadastro
@app.callback(
    Output("input-values", "children"),
    [Input("close-centered", "n_clicks")],
    [State("OS", "value"), State("TIPO", "value")], State("ENQUADRAMENTO", "value"), State("CLIENTE", "value"), State("DESCRIÇÃO", "value"), State("ICJ", "value"), State("SAP", "value"), State("INÍCIO", "value")
    , State("FIM", "value"), State("ADITIVOS", "value"), State("VALOR", "value"), State("PRAZOMES", "value"), State("PRAZODIAS", "value"), State("STATUS", "value"), State("RESPONSÁVEL", "value"), State("FILIAL", "value")
    , State("PROJETO", "value"), State("PROJETO SAPIENS", "value"), State("ISS", "value"), State("ADM CENTRAL", "value"), State("PIS", "value"), State("COFINS", "value"), State("CSLL", "value"), State("IRPJ", "value")
    , State("INVESTIMENTOS", "value"), State("ICMS", "value"), #adicionar todos os elementos aqui, pra poder retornar a lista
)
def get_input_values(n, os, tipo, enq, cliente, desc, icj, sap, inicio, fim, adt, valor, prazom, prazod, status, resp, filial, projeto, projsap, iss, admcentral, pis, cofins, csll, irpj, invest, icms):
    if n: #depois, jogar a função para mandar essas info para o back
        lista_input = [os,tipo,enq,cliente,desc,icj,sap,inicio,fim,adt,valor,prazom,prazod,status,resp,filial,projeto,projsap,iss,admcentral,pis,cofins,csll,irpj,invest,icms]

        return lista_input
    return ""

@app.callback(
    Output('tabela-impostos', 'columns'),
    Input('edit-switch', 'value')
)
def toggle_editability(value):
    columns = [{"name": i, "id": i, "editable": value} if i not in ["VALOR", "PRAZOMES", "PRAZODIAS"] else {"name": i, "id": i} for i in cad_contratos().columns]
    return columns

if __name__ == '__main__':
    app.run_server(debug=True)