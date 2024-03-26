import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App, reactive
from banco import lista_centro_custo, medidofaturado
import pandas as pd

lista_cc = lista_centro_custo()

# Part 1: ui ----
app_ui = ui.page_fluid(
    ui.h2("Medido X Faturado"),
    #lista suspensa
    ui.input_selectize("x1", "Selecione o CC", lista_cc),
    #plot do gráfico
    ui.output_plot("bar_plot"),
    ui.output_data_frame("txtcc"),
)

# Part 2: server ----
def server(input, output, session):
    @reactive.Calc
    #pega o valor do CC pela lista suspensa
    def centro_custo():
        cc = input.x1()
        return cc
    @reactive.Calc
    #chama a função do banco.py pra retornar o df completo
    def df_cc():
        cc = centro_custo()
        print(cc)
        df = medidofaturado(str(cc))
        return df
    
    @output
    #reenderiza o df
    @render.data_frame
    def txtcc():
        df = df_cc()
        return df
    
# Combine into a shiny app.
# Note that the variable must be "app".
app = App(app_ui, server)