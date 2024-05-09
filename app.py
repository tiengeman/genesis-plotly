# app.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pages.pagina1 as pagina1

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/home', className='nav-link')),
        dbc.NavItem(dbc.NavLink('Page 1', href='/page1', className='nav-link')),
        #...
    ],
    vertical=True,  # Make the nav items stack vertically
    pills=True,  # Make the nav items take up the full width of the sidebar
    className='bg-light'  # Add a light background color to the sidebar
)

content_area = html.Div(id='content')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(sidebar, width=1, className='bg-light'),  # Make the sidebar take up 2 columns
        dbc.Col(content_area, width=10)  # Make the content area take up 10 columns
    ])
])

# Callbacks
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def update_content(pathname):
    if pathname == '/page1':
        return pagina1.layout
    else:
        return html.Div([
            html.H1('Home'),
            html.P('This is a simple text message.')
        ])

def update_table(output_id, value):
    if output_id == 'tabela-container':
        return pagina1.atualizar_tabela(value)
    elif output_id == 'tabela2-container':
        return pagina1.atualizar_tabela2(value)


@app.callback(
    Output('tabela-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def update_table1(value):
    return update_table('tabela-container', value)

@app.callback(
    Output('tabela2-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
def update_table2(value):
    return update_table('tabela2-container', value)

if __name__ == '__main__':
    app.run_server(debug=True)