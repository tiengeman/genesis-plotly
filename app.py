from banco import *
from shiny import render, reactive
from shiny.express import input, ui

ui.h2("Simple Interactive Table")
with ui.sidebar(open="closed", bg="#FF4500"):
        ui.input_selectize(
        "var", "Selecione a competência",
        ["01/2024", "02/2024", "03/2024", "04/2024", "05/2024"]
    )

@render.text
def comp():
      return f'competência: {input.var()}'

# @reactive.cal
# def df():
#       return tabela(input.var())

@render.data_frame  
def data_df():
    #passa o valor do input na função tabela input.var()
    df = tabela()
    return render.DataGrid(df, summary=False, row_selection_mode="single")