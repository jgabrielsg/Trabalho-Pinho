import pandas as pd
import numpy as np
from datacleaning import df
from bokeh.models import ColumnDataSource
from bokeh.io import output_file, save, show
from bokeh.plotting import figure

# Primeiro Gráfico : Preço médio por região ao longo do tempo

#Agrupamento dos dados por data e região pela média dos dados agrupados em um novo dataframe.
df1 = df.groupby(["DATA INICIAL", "REGIÃO"])["PREÇO MÉDIO REVENDA"].mean().reset_index(name='MÉDIA')
df1["DATA INICIAL"] = pd.to_datetime(df1["DATA INICIAL"]) #Converte a coluna em data

#Criaçao do objeto do gráfico
plot = figure(width=640, height=480, tools="box_zoom, pan, reset")
plot.xaxis.axis_label = "Data"
plot.yaxis.axis_label = "Preço de revenda"

#Criação de lista para a realização de um loop já que o código de plotagem é o mesmo.
Regiões = ["CENTRO OESTE", "NORDESTE", "NORTE", "SUDESTE", "SUL"]
Cores = ["Blue", "Orange", "DarkGreen", "Purple", "Red"]

for regiao, cor in zip(Regiões, Cores):
    dataSource = ColumnDataSource(df1[df1["REGIÃO"] == regiao])
    plot.line(x="DATA INICIAL", y = "MÉDIA", legend_label=regiao, line_width=2, color = cor, source = dataSource)

show(plot)

output_file("teste1.html")