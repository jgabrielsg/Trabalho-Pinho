import pathlib
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, Span, Label, Title, HoverTool
from bokeh.io import output_file, save, show, curdoc
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot
from bokeh.palettes import Category20
from datacleaning import criar_dataset
from bokeh.themes import Theme

import os

caminho_theme = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tema_gui.yaml')

curdoc().theme = Theme(filename=caminho_theme)

# output_file("Testes/teste_guilherme.html")

# DATA = 'CSVs/prouni.csv'

# df = criar_dataset(DATA)

#------Primeiro Gráfico: Relação entre região e acesso de Deficientes físicos a bolsas

def Guilherme_plot1(df):
    # Filtra os dados para o Sudeste.
    df_sudeste = df[df['BENEFICIARIO_DEFICIENTE_FISICO'] == 'sim']
    #Filtra então para bolsistas com deficiência física.
    df_deficientes_sudeste = df_sudeste[df_sudeste["REGIAO_BENEFICIARIO_BOLSA"] == 'SUDESTE']

    # Nos dados filtrados separamos todos os dados em grupos por estado e ano, e contamos a quantidade de dados em cada grupo.
    df_agrupado = df_deficientes_sudeste.groupby(["ANO_CONCESSAO_BOLSA", "SIGLA_UF_BENEFICIARIO_BOLSA"]).size().reset_index(name='Quantidade')

    # Contamos a quantidade de dados totais para fazer uma linha que represente o Sudeste como todo.
    df_deficientes_sudeste = df_deficientes_sudeste.groupby(["ANO_CONCESSAO_BOLSA"]).size().reset_index(name='Quantidade')

    # Estrutura básica do gráfico
    plot1 = figure(width=1000, height=480, tools="box_zoom, pan, reset", name = "linhas_guilherme")
    plot1.xaxis.axis_label = "Ano de Concessão da Bolsa"
    plot1.yaxis.axis_label = "Número de beneficiados"
    plot1.title.text = "Número de deficientes físicos com acesso a bolsa\nno Sudeste por ano"

    # Define o começo e o fim do eixo x.
    plot1.x_range.start = 2005
    plot1.x_range.end = 2019
    
    # Lista de cores para usar nas linhas.
    cores =  ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Remove o grid
    plot1.xgrid.grid_line_color = None
    plot1.ygrid.grid_line_color = None

    # Cria uma linha para cada região
    for i, row in df_agrupado.iterrows():
        # Armazena o nome da região atual.
        estado = row['SIGLA_UF_BENEFICIARIO_BOLSA']
        
        # Filtra os dados para a região atual.
        df_estado = df_agrupado[df_agrupado['SIGLA_UF_BENEFICIARIO_BOLSA'] == estado]
        
        # Obtém os valores de y (Total de bolsistas) por x (ano) para a região.
        eixo_x = df_estado['ANO_CONCESSAO_BOLSA']
        eixo_y = df_estado['Quantidade']
        
         # Cria a linha com essas informações e a nomeia com o nome armazenado.
        plot1.line(eixo_x, eixo_y, legend_label=estado, line_width = 3, line_color=cores[i % len(cores)], line_alpha = 0.5)

    # Cria a linha do Sudeste.
    plot1.line(df_deficientes_sudeste['ANO_CONCESSAO_BOLSA'], df_deficientes_sudeste['Quantidade'], line_width = 6, legend_label="Sudeste", line_color= 'black')

    # Adiciona a legenda ao gráfico
    plot1.legend.location = "top_left"
    plot1.legend.title = "Estado/região"
    plot1.legend.label_text_font_size = "10pt"

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

    #Paleta de cores, basicamente rgb, o quarto fator é o alpha/transparência
    destaque_SP = ['rgba(255, 127, 14, 0.5)', 'rgba(44, 160, 44, 0.5)', 'rgba(148, 103, 189, 0.5)', 'rgba(214, 39, 40, 1)']
    destaque_ES = ['rgba(255, 127, 14, 1)', 'rgba(44, 160, 44, 0.5)', 'rgba(148, 103, 189, 0.5)', 'rgba(214, 39, 40, 0.5)']


    #Estrutura básica do gráfico desproporcional
    plot_desproporcional = figure(x_range=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"], width=600, height=300, tools="box_zoom, pan, reset", name = "plot_desproporcional")
    plot_desproporcional.xaxis.axis_label = "Estado"
    plot_desproporcional.yaxis.axis_label = "Número de benificiados"
    plot_desproporcional.title.text = "Número de deficientes físicos com acesso a bolsa\npor estado da região sudeste"
    
    # Remove o grid
    plot_desproporcional.xgrid.grid_line_color = None
    plot_desproporcional.ygrid.grid_line_color = None

    #Gráfico de barras do estado pelo número de bolsistas com deficiência física.
    plot_desproporcional.vbar(x="SIGLA_UF_BENEFICIARIO_BOLSA", top="Quantidade", width=0.4, line_width=0,
            #Preenchendo as barras com uma cor para cada região.
            fill_color=factor_cmap("SIGLA_UF_BENEFICIARIO_BOLSA", palette=destaque_SP, factors=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"].unique()),
            source=df_deficientes_fisicos_sudeste)
    plot_desproporcional.y_range.start = 0

    #Estrutura básica do gráfico proporcional
    plot_proporcional = figure(x_range=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"], width=600, height=300, tools="box_zoom, pan, reset", name = "plot_proporcional")
    plot_proporcional.xaxis.axis_label = "Estado"
    plot_proporcional.yaxis.axis_label = "Porcentagem dentre os bolsistas"
    plot_proporcional.title.text = "Percentual de estudantes com deficiência física\nem relação ao total de bolsistas"
    plot_proporcional.yaxis.formatter = NumeralTickFormatter(format="0.0%")

    # Remove o grid
    plot_proporcional.xgrid.grid_line_color = None
    plot_proporcional.ygrid.grid_line_color = None

    #Gráfico de barras do estado pela proporção de bolsistas com deficiência física.
    plot_proporcional.vbar(x="SIGLA_UF_BENEFICIARIO_BOLSA", top="Proporcao", width=0.4, line_width=0,
            #Preenchendo as barras com uma cor para cada região.
            fill_color=factor_cmap("SIGLA_UF_BENEFICIARIO_BOLSA", palette=destaque_ES, factors=df_deficientes_fisicos_sudeste["SIGLA_UF_BENEFICIARIO_BOLSA"].unique()),source=df_deficientes_fisicos_sudeste)
    plot_proporcional.y_range.start = 0

    # Calcula a média
    media = df_deficientes_fisicos_sudeste['Proporcao'].mean()
    # Define a linha
    linha_media = Span(dimension='width', line_color='gray', line_dash='dashed', line_width=2)
    linha_media.location = media
    # Adiciona a linha ao gráfico
    plot_proporcional.add_layout(linha_media)

    # Adiciona um nome a linha e quanto vale a média.
    media_texto = Label(x=3, y=media, text=f"Média: {media:.2%}", text_font_size="10pt", text_color="gray")
    plot_proporcional.add_layout(media_texto)

    #Gera um gridplot com os dois gráficos.
    plot2 = gridplot([[plot_desproporcional, None],[plot_proporcional, None]])          

    return plot_proporcional, plot_desproporcional

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
    plot3 = figure(x_range=eixo_x, width =1000, height=400, tools="", name = "velas_guilherme")

    plot3.xaxis.axis_label = "Intervalo de anos"
    plot3.yaxis.axis_label = "Número de bolsistas"
    plot3.title.text = "Análise da variação de bolsistas entre os anos"
    plot3.yaxis[0].formatter = NumeralTickFormatter(format="0,")

    # Define o começo e o fim do eixo y.
    plot3.y_range.start = 90000
    plot3.y_range.end = 260000

    # Gera uma legenda para as cores verde e vermelho.
    plot3.rect([1], [1], width=1, height=1, fill_color='green', line_color='black', legend_label="Positiva")
    plot3.rect([1], [1], width=1, height=1, fill_color='red', line_color='black', legend_label="Negativa")

    # Adiciona a legenda ao gráfico
    plot3.legend.location = "top_left"
    plot3.legend.title = "Variação"
    plot3.legend.label_text_font_size = "10pt"

    # Cria duas listas, uma com as bases: o menor dos resultados, outra com os topos: o maior deles.
    bases_das_velas = []
    topos_das_velas = []
    for i in range(num_anos):
        bases_das_velas.append(min(dados_por_ano.iloc[i+1], dados_por_ano.iloc[i]))
        topos_das_velas.append(max(dados_por_ano.iloc[i+1], dados_por_ano.iloc[i]))

    # Checa-se a quantidade de bolsistas/dados está aumentando ou diminuindo, e adiciona a lista cores a cor verde ou vermelha respectivamente.
    cores = []
    for i in range(num_anos):
        if dados_por_ano.iloc[i+1] > dados_por_ano.iloc[i]:
            cores.append('green')
        else:
            cores.append('red')

    # Gera as linhas que cortam as velas.
    lista_y0 = []
    lista_y1 = []
    for i in range(num_anos):
        if 0 < i <num_anos-1:
            lista_y0.append((bases_das_velas[i-1] + bases_das_velas[i+1])/2)
            lista_y1.append((topos_das_velas[i-1] + topos_das_velas[i+1])/2)
    plot3.segment(x0=eixo_x[1:], x1=eixo_x[1:], y0=lista_y0, y1=lista_y1, color='black', line_width=2)

    # Configura o grid
    plot3.grid.visible = True
    plot3.grid.grid_line_color = 'gray'
    plot3.grid.grid_line_alpha = 0.2

    # Cria uma ColumnDataSource para as velas
    velas = ColumnDataSource(data=dict(
        eixo_x=eixo_x,
        bases_das_velas=bases_das_velas,
        topos_das_velas=topos_das_velas,
        cores = cores
    ))

    # Define a hover tool.
    hover_tool = HoverTool(
        tooltips=[
            ("Intervalo de anos", "@eixo_x"),
            ("Mínimo", "@bases_das_velas"),
            ("Máximo", "@topos_das_velas"),
        ],
        mode="vline",
    )
    # Adiciona a hover tool ao plot
    plot3.add_tools(hover_tool)

    # Gera as velas.
    plot3.vbar(x='eixo_x', width=0.7, bottom='bases_das_velas', top='topos_das_velas', fill_color='cores', line_color='black', source=velas)

    return plot3