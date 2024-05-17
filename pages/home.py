from dash import html, dcc
import dash_bootstrap_components as dbc
from constants import colors

carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "assets\Banner-40-anos2-jpg.webp"},
        {"key": "2", "src": "assets\Banner-CQTE.png"},
        {"key": "3", "src": "assets\Banner-institucional2-jpg.webp"},
        {"key": "4", "src": "assets\Banner-Premiacao-PB.png"},
        {"key": "5", "src": "assets\Banner-Re22-jpg.webp"},
    ],
    controls=True,
    indicators=True,
    interval=7000,
    ride="carousel",
    # style={"width": "500px"}
)

layout = html.Div([
            html.H1('Genesis', style={'marginTop': '10px', 'color': colors['gray'], 'fontWeight': 'bold'}),
            html.P('Sistema de Dashboards Engeman', style={'color': colors['gray']}),
            html.Hr(style={'backgroundColor': colors['orange']}),  # Linha horizontal laranj
            carousel
        ],
        style={'margin': '20px'})