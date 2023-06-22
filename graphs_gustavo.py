from datacleaning import criar_dataset, coluna_vazia, limpar_coluna, contar_repeticoes
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
import pyproj

output_file("teste_gustavo.html")

df = pd.read_csv("prouni.csv") 

# Primeiro Gráfico : Quantidade de mulheres e homens por sexo por ano

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

# Segundo Gráfico : top 10 cursos mais frequêntes no ProUni

df2 = df.groupby(["NOME_CURSO_BOLSA"])["NOME_CURSO_BOLSA"].count().reset_index(name = "Bolsas")
df2 = df2.sort_values(['Bolsas'], ascending=False).head(10)

plot2 = figure(x_range=df2["NOME_CURSO_BOLSA"], width=1000, height=480, tools="box_zoom, pan, reset")
plot2.xaxis.axis_label = "Curso"
plot2.yaxis.axis_label = "Quantidade"
plot2.xaxis.major_label_orientation = 1
plot2.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

plot2.vbar(x=df2["NOME_CURSO_BOLSA"], top=df2["Bolsas"], width=0.4)
plot2.y_range.start = 0

#Gráfico 3: Mapa com municípios que já tiveram bolsa

#Lê os dados de municipios e deixa somente as colunas que nos importam (nome, latitude, longitude)
municipios = pd.read_csv("municipios.csv")
municipios = municipios[["nome", "latitude", "longitude"]]

#Remove acentos e letras maíusculas dos nomes dos municípios, já que este é o formato de nome que está no csv do ProUni
municipios["nome"] = municipios["nome"].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
municipios = municipios.rename(columns = {"nome": "MUNICIPIO_BENEFICIARIO_BOLSA"}) #coloca o mesmo nome para os dois df

#Cria um dataframe focado apenas nos municípios do csv do Prouni
df3 = df.groupby(["MUNICIPIO_BENEFICIARIO_BOLSA"])["MUNICIPIO_BENEFICIARIO_BOLSA"].count().reset_index(name = "quantidade")

#União dos dois csv com base nos valores da coluna MUNICIPIO_BENEFICIARIO_BOLSA, que tem nos dois dataframes
df3 = pd.merge(df3, municipios, how = 'inner', on = ["MUNICIPIO_BENEFICIARIO_BOLSA"])

#Define um tema pro mapa e o cria
tile_provider = get_provider(CARTODBPOSITRON)

p = figure(x_range=(-8500000, -3500000), y_range=(-1650000, -1000000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)

#Arruma o sistema de projeção de latitude e latitude dos nossos dados para o que o Bokeh entende, que é o Web Mercator
wgs84 = pyproj.CRS("EPSG:4326")
mercator = pyproj.CRS("EPSG:3857")
transformer = pyproj.Transformer.from_crs(wgs84, mercator, always_xy=True)

#Aplica a transformação nas coordenadas do dataframe
df3["longitude_mercator"], df3["latitude_mercator"] = transformer.transform(df3["longitude"].values, df3["latitude"].values)

dataSourceMapa = ColumnDataSource(data=df3[["longitude_mercator", "latitude_mercator"]])

p.circle(x="longitude_mercator", y="latitude_mercator", size=3, fill_color="blue", fill_alpha=1, source=dataSourceMapa)

show(p)

output_file("tile.html")