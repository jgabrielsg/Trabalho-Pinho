import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot
from bokeh.palettes import Category20

import sys
sys.path.append('modulos/')

from datacleaning import criar_dataset

output_file("Testes/teste_guilherme.html")

DATA = 'CSVs/prouni.csv'

df = criar_dataset(DATA)

#------Primeiro Gráfico: Relação entre região e acesso de Deficientes físicos a bolsas

from bokeh.plotting import figure

def guilherme_plot1(df):
    # Filtra os dados para bolsistas com deficiência física.
    df_filtrado = df[df['BENEFICIARIO_DEFICIENTE_FISICO'] == 'sim']

    # Nos dados filtrados separamos todos os dados em grupos por região e ano, e contamos a quantidade de dados em cada grupo.
    df_agrupado = df_filtrado.groupby(["ANO_CONCESSAO_BOLSA", "REGIAO_BENEFICIARIO_BOLSA"]).size().reset_index(name='Quantidade')

    # Estrutura básica do gráfico
    plot1 = figure(width=1000, height=480, tools="box_zoom, pan, reset")
    plot1.xaxis.axis_label = "Ano de Concessão da Bolsa"
    plot1.yaxis.axis_label = "Número de beneficiados"
    plot1.title.text = "Número de deficientes físicos com acesso a bolsa\npor região por ano"

    # Cria uma linha para cada região
    for i, row in df_agrupado.iterrows():
        # Armazena o nome da região atual.
        regiao = row['REGIAO_BENEFICIARIO_BOLSA']
        
        # Filtra os dados para a região atual.
        df_regiao = df_agrupado[df_agrupado['REGIAO_BENEFICIARIO_BOLSA'] == regiao]
        
        # Obtém os valores de y (Total de bolsistas) por x (ano) para a região.
        eixo_x = df_regiao['ANO_CONCESSAO_BOLSA']
        eixo_y = df_regiao['Quantidade']
        
        # Cria a linha com essas informações e a nomeia com o nome armazenado.
        plot1.line(eixo_x, eixo_y, legend_label=regiao)

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