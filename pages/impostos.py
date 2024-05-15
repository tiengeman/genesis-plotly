# impostos.py
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

# Define a constant for the fees data
FEES_DATA = pd.DataFrame({
    'ID': [1, 2, 3],
    'DESCRIPTION': ['Fee 1', 'Fee 2', 'Fee 3'],
    'AMOUNT': [10.0, 20.0, 30.0]
})

# Define a function to create the fees table
def create_fees_table(fees_data):
    return dash_table.DataTable(
        id='fees-table',
        data=fees_data.to_dict('records'),
        columns=[
            {'name': 'ID', 'id': 'ID', 'type': 'numeric'},
            {'name': 'DESCRIPTION', 'id': 'DESCRIPTION', 'type': 'text'},
            {'name': 'AMOUNT', 'id': 'AMOUNT', 'type': 'numeric'}
        ],
        style_cell={'textAlign': 'center', 'padding': '5px'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#616468', 'color': 'white'}
    )

# Define a function to add a new fee to the table
def add_fee(fees_data, new_fee):
    new_fee_id = max(fees_data['ID']) + 1
    new_fee_row = pd.DataFrame({'ID': [new_fee_id], 'DESCRIPTION': [new_fee['DESCRIPTION']], 'AMOUNT': [new_fee['AMOUNT']]})
    fees_data = pd.concat([fees_data, new_fee_row])
    return fees_data

# Create the Impostos page layout
layout = html.Div([
    html.H1('Impostos'),
    html.Hr(),
    create_fees_table(FEES_DATA),
    html.Button('Add New Fee', id='add-fee-button', n_clicks=0),
    dcc.Input(id='new-fee-description', type='text', placeholder='Description'),
    dcc.Input(id='new-fee-amount', type='number', placeholder='Amount')
])