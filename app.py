from banco import *
from shiny import render, reactive
from shiny.express import input, ui

ui.page_opts(title="Performance Mensal por Competencia")
ui.page_opts(fillable = True)
with ui.sidebar(open="closed", bg="#FF4500"):  
    "teste"

ui.input_selectize(
        "var", "Selecione a competencia:",
        ["dezembro/2023","janeiro/2024", "fevereiro/2024", "março/2024", "abril/2024"]
    )

@render.data_frame  
def data_df():
    df = tabela(input.var())
    return render.DataGrid(df, summary=False, row_selection_mode="single", width="2000px", height="3550px")

@render.data_frame  
def data_df_2():
    #passa o valor do input na função tabela input.var()
    df_2 = tabela_2()
    return render.DataGrid(df_2, summary=False, row_selection_mode="single", width="2000px", height="300px")