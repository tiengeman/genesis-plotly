# app.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pages.gerencial as gerencial
import pages.home as home
import pages.diretoria as diretoria
import pages.relacao as relacao

# Constants
logo = 'https://i0.wp.com/engeman.net/wp-content/uploads/2024/04/LOGO_ENGEMAN_HORIZONTAL-e1714498268589.png?w=851&ssl=1'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Gerencial', href='/gerencial', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Diretoria', href='/diretoria', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Relação', href='/relacao', className='nav-link')),
    ],
    vertical=True,  # Make the nav items stack vertically
    pills=True,  # Make the nav items take up the full width of the sidebar
)

offcanvas = html.Div(
    [
        dbc.Button(
            html.I(className="bi bi-list"),  # Use Bootstrap Icon
            id="open-offcanvas",
            n_clicks=0,
            size="md",  # Add a size to the button
            color = '#FF4E00',
            style={"font-size": "1.60em"},  # Set the background color to #FF4E00
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
    color='#FF4E00',
    dark=True,
    className='justify-content-between',  # Add this class to justify the content
    style={'height': '50px'}  # Reduce the height of the header
)

# Content area
content_area = html.Div(id='content')

app.layout = html.Div([
    header,
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(content_area),  # Make the content area take up 10 columns
    ]),
])

# Callbacks
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
    else:
        return home.layout

def update_table(output_id, value):
    if output_id == 'tabela-container':
        return gerencial.atualizar_tabela(value)
    elif output_id == 'tabela2-container':
        return gerencial.atualizar_tabela2(value)

@app.callback(
    Output('tabela-container', 'children'),
    Output('tabela2-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def update_tables(value):
    return update_table('tabela-container', value), update_table('tabela2-container', value)
    
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)