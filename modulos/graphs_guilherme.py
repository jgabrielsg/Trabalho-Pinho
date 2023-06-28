import pandas as pd
import numpy as np

from datacleaning import criar_dataset
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot

output_file("Testes/teste_guilherme.html")

DATA = 'CSVs/prouni.csv'

df = criar_dataset(DATA)

#------Primeiro Gráfico: Relação entre região e acesso de Deficientes físicos a bolsas

def guilherme_plot1(df):
    #Filtra os dados para as linhas da coluna 'BENEFICIARIO_DEFICIENTE_FISICO' com valor igual a "sim".
    df_filtrado = df[df['BENEFICIARIO_DEFICIENTE_FISICO'] == 'sim']

    #Nos dados filtrados separamos todos os dados em grupos por região, e contamos a quantidade de dados em cada grupo.
    df1 = df_filtrado.groupby("REGIAO_BENEFICIARIO_BOLSA").size().reset_index(name='Quantidade')

    #Paleta de cores aleatórias
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    #Estrutura básica do gráfico
    plot1 = figure(x_range=df1["REGIAO_BENEFICIARIO_BOLSA"], width=1000, height=480, tools="box_zoom, pan, reset")
    plot1.xaxis.axis_label = "Região"
    plot1.yaxis.axis_label = "Número de benificiados"
    plot1.title.text = "Número de deficientes físicos com acesso a bolsa por região"

    #Gráfico de barras da região pela quantidade de bolsistas com deficiência física.
    plot1.vbar(x="REGIAO_BENEFICIARIO_BOLSA", top="Quantidade", width=0.4, line_width=2,
            #Preenchendo as barras com uma cor para cada região.
            fill_color=factor_cmap("REGIAO_BENEFICIARIO_BOLSA", palette=colors, factors=df1["REGIAO_BENEFICIARIO_BOLSA"].unique()),source=df1)

    plot1.y_range.start = 0

    return plot1

#------Segundo Gráfico: Relação entre Estado e Munícipio com o acesso de Deficientes físicos a bolsas no Sudeste brasileiro

def guilherme_plot2(df):
    #Filtrando os dados para a região sudeste.
    df_sudeste = df[df['REGIAO_BENEFICIARIO_BOLSA'] == 'SUDESTE']
    #Separando em grupos por estado e medidindo a quantidade de bolsistas.
    df_sudeste = df_sudeste.groupby("SIGLA_UF_BENEFICIARIO_BOLSA").size().reset_index(name='Quantidade_total')

    #Filtrando os dados para bolsistas com deficiência física do sudeste.
    df_deficientes_fisicos_sudeste =df.loc[(df['REGIAO_BENEFICIARIO_BOLSA'] == 'SUDESTE') & (df['BENEFICIARIO_DEFICIENTE_FISICO'] == 'sim')]
    #Medidindo a quantidade de bolsistas específicos.
    df_deficientes_fisicos_sudeste = df_deficientes_fisicos_sudeste.groupby("SIGLA_UF_BENEFICIARIO_BOLSA").size().reset_index(name='Quantidade')

    #Calcula a proporção dos bolsistas com deficiência física com o total de bolsistas por estado.
    df_deficientes_fisicos_sudeste['Proporcao'] = df_deficientes_fisicos_sudeste['Quantidade']/df_sudeste['Quantidade_total']

    #Paleta de cores aleatórias
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    #Estrutura básica do gráfico proporcional
    plot_proporcional = figure(x_range=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"], width=600, height=300, tools="box_zoom, pan, reset")
    plot_proporcional.xaxis.axis_label = "Estado"
    plot_proporcional.yaxis.axis_label = "Proporção de benificiados"
    plot_proporcional.title.text = "Proporção de deficientes físicos com acesso a bolsa em relação ao total de bolsistas\npor estado da região sudeste"
    plot_proporcional.yaxis.formatter = NumeralTickFormatter(format="0.0%")

    #Gráfico de barras do estado pela proporção de bolsistas com deficiência física.
    plot_proporcional.vbar(x="SIGLA_UF_BENEFICIARIO_BOLSA", top="Proporcao", width=0.4, line_width=0,
            #Preenchendo as barras com uma cor para cada região.
            fill_color=factor_cmap("SIGLA_UF_BENEFICIARIO_BOLSA", palette=colors, factors=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"].unique()),source=df_deficientes_fisicos_sudeste)
    plot_proporcional.y_range.start = 0

    #Estrutura básica do gráfico desproporcional
    plot_desproporcional = figure(x_range=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"], width=600, height=300, tools="box_zoom, pan, reset")
    plot_desproporcional.xaxis.axis_label = "Estado"
    plot_desproporcional.yaxis.axis_label = "Número de benificiados"
    plot_desproporcional.title.text = "Número de deficientes físicos com acesso a bolsa\npor estado da região sudeste"

    #Gráfico de barras do estado pelo número de bolsistas com deficiência física.
    plot_desproporcional.vbar(x="SIGLA_UF_BENEFICIARIO_BOLSA", top="Quantidade", width=0.4, line_width=0,
            #Preenchendo as barras com uma cor para cada região.
            fill_color=factor_cmap("SIGLA_UF_BENEFICIARIO_BOLSA", palette=colors, factors=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"].unique()),source=df_deficientes_fisicos_sudeste)
    plot_desproporcional.y_range.start = 0

    #Gera um gridplot com os dois gráficos.
    plot2 = gridplot([[plot_desproporcional, None],[plot_proporcional, None]])          

    return plot2

show(guilherme_plot2(df))
# print(df.columns)