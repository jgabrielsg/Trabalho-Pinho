import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot
from bokeh.palettes import Category20
from datacleaning import criar_dataset

output_file("Testes/teste_guilherme.html")

DATA = 'CSVs/prouni.csv'

df = criar_dataset(DATA)

#------Primeiro Gráfico: Relação entre região e acesso de Deficientes físicos a bolsas

def Guilherme_plot1(df):
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

def Guilherme_plot2(df):
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

#------Terceiro Gráfico: fazer um gráfico da quantidade de registros por ano no estilo gráfico de velas

def Guilherme_plot3(df):
    # Separa os dados por ano e mede a quantidade de bolsistas.
    dados_por_ano = df.groupby(['ANO_CONCESSAO_BOLSA']).size()

    # Gera uma lista com os anos.
    anos = dados_por_ano.index.tolist()
    # Conta o número de anos.
    num_anos = len(dados_por_ano)-1

    # Define o eixo x, para ser YYYY-YYYY, já que para fazer as "velas" precisamos de dois valores(dois anos).
    eixo_x = []
    for i in range(num_anos):
        eixo_x.append(str(anos[i]) + '-' + str(anos[i+1]))

    # Cria o gráfico.
    plot3 = figure(x_range=eixo_x, height=400, title="Variação de bolsistas por ano")

    # Cria duas listas, uma com as bases: o menor dos resultados, outra com os topos: o maior deles.
    bases_das_velas = []
    topos_das_velas = []
    for i in range(num_anos):
        bases_das_velas.append(min(dados_por_ano.iloc[i+1], dados_por_ano.iloc[i]))
        topos_das_velas.append(max(dados_por_ano.iloc[i+1], dados_por_ano.iloc[i]))

    # Checa se a quantidade de bolsistas/dados está aumentando ou diminuindo, e adiciona a lista cores a cor verde ou vermelha respectivamente.
    cores = []
    for i in range(num_anos):
        if dados_por_ano.iloc[i+1] > dados_por_ano.iloc[i]:
            cores.append('green')
        else:
            cores.append('red')

    # Gera as linhas que cortam as velas.
    for i in range(num_anos):
        if num_anos > i > 0:
            plot3.segment(x0=eixo_x[i], x1=eixo_x[i], y0=bases_das_velas[i-1]-bases_das_velas[i+1], y1=topos_das_velas[i-1]-topos_das_velas[i+1], color='black', line_width=2)
        else:
            break
    # plot3.segment(x0=eixo_x, x1=eixo_x, y0=bases_das_velas, y1=topos_das_velas, color='black', line_width=2)

    # Gera as velas.
    plot3.vbar(x=eixo_x, width=0.7, bottom=bases_das_velas, top=topos_das_velas, fill_color=cores, line_color='black')

    return plot3

show(Guilherme_plot3(df))
# print(df.columns)