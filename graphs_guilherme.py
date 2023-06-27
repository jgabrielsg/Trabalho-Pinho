import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

output_file("Testes/teste_guilherme.html")

DATA = 'CSVs/prouni.csv'

df = pd.read_csv(DATA)

#------Primeiro Gráfico: Relação entre região e acesso de Deficientes físicos a bolsas

#Filtra os dados para as linhas da coluna 'BENEFICIARIO_DEFICIENTE_FISICO' com valor igual a "sim".
df_filtrado = df[df['BENEFICIARIO_DEFICIENTE_FISICO'] == 'sim']

#Nos dados filtrados separamos todos os dados em grupos por região, e contamos a quantidade de dados em cada grupo.
df1 = df_filtrado.groupby("REGIAO_BENEFICIARIO_BOLSA").size().reset_index(name='Quantidade')

#Paleta de cores aleatórias
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

#EStrutura básica do gráfico
plot1 = figure(x_range=df1["REGIAO_BENEFICIARIO_BOLSA"], width=1000, height=480, tools="box_zoom, pan, reset")
plot1.xaxis.axis_label = "Região"
plot1.yaxis.axis_label = "Número de benificiados"
plot1.title.text = "Número de deficientes com acesso a bolsa por região"

#Gráfico de barras da região pela quantidade de bolsistas com deficiência física.
plot1.vbar(x="REGIAO_BENEFICIARIO_BOLSA", top="Quantidade", width=0.4, line_width=2,
           #Preenchendo as barras com uma cor para cada região.
           fill_color=factor_cmap("REGIAO_BENEFICIARIO_BOLSA", palette=colors, factors=df1["REGIAO_BENEFICIARIO_BOLSA"].unique()),source=df1)

plot1.y_range.start = 0

show(plot1)