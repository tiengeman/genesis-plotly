from banco import *
from shiny import ui, render, App, reactive
from shiny.express import ui

ui.h2("Simple Interactive Table")
with ui.sidebar(open="closed", bg="#4972FF"):
        ui.input_selectize(
        "var", "Select variable",
        ["1", "2", "3", "4", "5"]
    )

df = tabela()
@render.data_frame  
def data_df():
    return render.DataGrid(df, summary=False, row_selection_mode="single")