from datacleaning import criar_dataset, coluna_vazia, limpar_coluna, contar_repeticoes
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure

output_file("teste_gustavo.html")

df = pd.read_csv("prouni.csv") 

# Primeiro Gráfico : Quantidade de pessoas por sexo por ano

df1 = df.groupby(["ANO_CONCESSAO_BOLSA", "SEXO_BENEFICIARIO_BOLSA"])["SEXO_BENEFICIARIO_BOLSA"].count().reset_index(name='Quantidade')

#Criando objeto do gráfico
plot1 = figure(width=1000, height=480, tools="box_zoom, pan, reset")
plot1.xaxis.axis_label = "Ano"
plot1.yaxis.axis_label = "Beneficiários"
plot1.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

dataSourceF = ColumnDataSource(df1[df1["SEXO_BENEFICIARIO_BOLSA"] == "F"])
dataSourceM = ColumnDataSource(df1[df1["SEXO_BENEFICIARIO_BOLSA"] == "M"])

plot1.line(x="ANO_CONCESSAO_BOLSA", y = "Quantidade", legend_label="Mulher", line_width=2, color = "red", source = dataSourceF)
plot1.line(x="ANO_CONCESSAO_BOLSA", y = "Quantidade", legend_label="Homem", line_width=2, color = "blue", source = dataSourceM)

plot1.legend.location = "top_left" #Tira a legenda da frente do gráfico


# Segundo Gráfico : Cursos mais frequêntes no ProUni

df2 = df.groupby(["NOME_CURSO_BOLSA"])["NOME_CURSO_BOLSA"].count().reset_index(name = "Bolsas")
df2 = df2.sort_values(['Bolsas'], ascending=False).head(10)

plot2 = figure(x_range=df2["NOME_CURSO_BOLSA"], width=1000, height=480, tools="box_zoom, pan, reset")
plot2.xaxis.axis_label = "Curso"
plot2.yaxis.axis_label = "Quantidade"
plot2.xaxis.major_label_orientation = 1
plot2.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

plot2.vbar(x=df2["NOME_CURSO_BOLSA"], top=df2["Bolsas"], width=0.4)
plot2.y_range.start = 0

show(plot2)