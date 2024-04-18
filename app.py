from banco import *
from shiny import render, reactive
from shiny.express import input, ui

ui.page_opts(title="Performance Mensal por Competencia")
ui.page_opts(fillable = True)
with ui.sidebar(open="closed", bg="#FF4500"):  
    "teste"

ui.input_selectize(
        "var", "Selecione a competencia:",
        ["01/2024", "02/2024", "03/2024", "04/2024", "05/2024"]
    )

# with ui.card(full_screen=True):
@render.data_frame  
def data_df():
    #passa o valor do input na função tabela input.var()
    df = tabela()
    return render.DataGrid(df, summary=False, row_selection_mode="single", width="2000px", height="3550px")

@render.data_frame  
def data_df_2():
    #passa o valor do input na função tabela input.var()
    df_2 = tabela_2()
    return render.DataGrid(df_2, summary=False, row_selection_mode="single", width="2000px", height="300px")