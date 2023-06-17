import pandas as pd
import numpy as np
from datacleaning import df
from bokeh.models import ColumnDataSource
from bokeh.io import output_file, save, show
from bokeh.plotting import figure

output_file("teste_vinicius.html")

# Converter a coluna "DATA INICIAL" para o tipo datetime
df["DATA INICIAL"] = pd.to_datetime(df["DATA INICIAL"])

# Extrair o ano da coluna "DATA INICIAL"
df["ANO"] = df["DATA INICIAL"].dt.year

# Contar a quantidade de ocorrências de cada produto por ano
contagem_produtos = df.groupby(["ANO", "PRODUTO"]).size().reset_index(name="QUANTIDADE")

# Lista de produtos desejados
produtos_selecionados = ["ETANOL HIDRATADO", "GASOLINA COMUM", "GLP", "GNV", "ÓLEO DIESEL",
                        "ÓLEO DIESEL S10", "OLEO DIESEL", "OLEO DIESEL S10", "GASOLINA ADITIVADA"]

# Lista de cores para atribuir a cada produto
cores = ["blue", "red", "green", "purple", "orange", "gray", "cyan", "magenta", "brown"]

# Criação do objeto do gráfico
plot = figure(width=640, height=480, x_axis_type='datetime', tools="box_zoom, pan, reset")
plot.xaxis.axis_label = "Ano"
plot.yaxis.axis_label = "Quantidade de Produtos"

# Loop para adicionar uma linha para cada produto
for produto, cor in zip(produtos_selecionados, cores):
    data_produto = contagem_produtos[contagem_produtos["PRODUTO"] == produto]
    plot.line(x=data_produto["ANO"], y=data_produto["QUANTIDADE"], legend_label=produto, line_width=2, color=cor)

show(plot)