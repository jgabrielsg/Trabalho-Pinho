import pandas as pd
import numpy as np
from bokeh.models import NumeralTickFormatter, DatetimeTickFormatter, LabelSet, HoverTool
from bokeh.io import output_file, save, show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.themes import Theme

from datacleaning import criar_dataset, transforma_ColumnDataSource

import os

caminho_theme = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'theme.yaml')

curdoc().theme = Theme(filename=caminho_theme)


'''
Primeiro Gráfico: Divide por região a quantidade de bolsas por ano, mostrando a evolução de cada região
na quantidade de bolsas por ano. Foi feito um gráfico de linhas para cada região, com o eixo x sendo o ano.
'''

def Joao_plot1(df):
    df_regiões = df.groupby(['ANO_CONCESSAO_BOLSA', 'REGIAO_BENEFICIARIO_BOLSA']).size().reset_index(name='QUANTIDADE POR ANO') # Agrupar os dados por região e calcular a quantidade de beneficiados

    df_regiões['ANO_CONCESSAO_BOLSA'] = df_regiões['ANO_CONCESSAO_BOLSA'].astype(int)  # Converter a coluna de ano para inteiros

    plot_região = figure(width = 1000, height = 480, x_range=(2005, 2019), name = "Linhas_Joao")

    regiões = df_regiões['REGIAO_BENEFICIARIO_BOLSA'].unique()  # Obter a lista de regiões únicas
    cores = ('#1957FF', '#0BD979', '#D4CB00', '#EB8100', '#E00913')

    # Cria um gráfico de linhas para cada região
    for i, região in enumerate(regiões):
        dados_regionais = df_regiões[df_regiões['REGIAO_BENEFICIARIO_BOLSA'] == região]
        plot_região.line(dados_regionais['ANO_CONCESSAO_BOLSA'], dados_regionais['QUANTIDADE POR ANO'], 
                        line_width=5, line_color=cores[i], legend_label=região)

    # Configura a localização das ferramentas do gráfico
    plot_região.title.text = "QUANTIDADE DE BOLSAS POR REGIÃO"
    plot_região.title.align = 'center'
    plot_região.xaxis.axis_label = "Ano"
    plot_região.yaxis.axis_label = "Quantidade de Bolsas"

    plot_região.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

    return plot_região


'''
Gráfico 2: Quantidade de bolsas por região e por estado, mostrando a evolução de cada estado na quantidade de bolsas por ano.
'''

def Joao_plot2(df):
    # Agrupar os dados por região, estado e calcular a quantidade de beneficiados
    df_regiao_estado = df.groupby(['ANO_CONCESSAO_BOLSA', 'REGIAO_BENEFICIARIO_BOLSA', 'SIGLA_UF_BENEFICIARIO_BOLSA']).size().reset_index(name='QUANTIDADE DE BENEFICIADOS')
    df_regiao_estado['ANO_CONCESSAO_BOLSA'] = pd.to_datetime(df_regiao_estado['ANO_CONCESSAO_BOLSA'], format="%Y")

    # Definir as cores para cada estado
    cores = ('#1957FF', '#0BD979', '#D4CB00', '#EB8100', '#E00913', '#1957FF', '#0BD979', '#D4CB00', '#EB8100', '#E00913')

    # Obter a lista de regiões únicas
    regioes_unicas = df_regiao_estado['REGIAO_BENEFICIARIO_BOLSA'].unique()

    plots = []  # Lista para armazenar os gráficos individuais

    # Cria um gráfico de linhas para cada região
    for regiao in regioes_unicas:
        dados_regiao = df_regiao_estado[df_regiao_estado['REGIAO_BENEFICIARIO_BOLSA'] == regiao]
        plot_estados = figure(x_axis_type="datetime", width=1200, height=400, 
                            x_range=(df_regiao_estado['ANO_CONCESSAO_BOLSA'].min(), df_regiao_estado['ANO_CONCESSAO_BOLSA'].max()), name = "Região {}".format(regiao))

        # Cria um gráfico de linhas para cada estado
        for i, estado in enumerate(dados_regiao['SIGLA_UF_BENEFICIARIO_BOLSA'].unique()):
            dados_estado = dados_regiao[dados_regiao['SIGLA_UF_BENEFICIARIO_BOLSA'] == estado]
            plot_estados.line(dados_estado['ANO_CONCESSAO_BOLSA'], dados_estado['QUANTIDADE DE BENEFICIADOS'],
                                    line_width=5, line_color=cores[i], legend_label=estado)
            
        # Configuração do gráfico
        plot_estados.title.text = "QUANTIDADE DE BOLSAS POR ESTADO - REGIÃO {}".format(regiao)
        plot_estados.title.align = 'center'
        plot_estados.xaxis.axis_label = "Ano"
        plot_estados.yaxis.axis_label = "Quantidade de Bolsas"

        plot_estados.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

        plots.append(plot_estados)  # Adiciona o gráfico à lista

    # Cria um layout de grade com os gráficos
    grid = gridplot([[plot] for plot in plots], toolbar_location=None)

    return grid

'''
Gráfico 3: Quantidade de bolsas por modalidade de ensino por ano, separando entre presencial e EAD
'''

def Joao_plot3(df):
    df_ead_presencial = df.groupby(['MODALIDADE_ENSINO_BOLSA', 'ANO_CONCESSAO_BOLSA']).size().reset_index(name='QUANTIDADE POR ANO') # Agrupar os dados por modalidade de ensino e calcular a quantidade de beneficiados
    df_ead = df_ead_presencial[df_ead_presencial['MODALIDADE_ENSINO_BOLSA'] == 'EAD'] # Filtrar os dados para a modalidade EAD
    df_presencial = df_ead_presencial[df_ead_presencial['MODALIDADE_ENSINO_BOLSA'] == 'PRESENCIAL'] # Filtrar os dados para a modalidade PRESENCIAL

    plot_modalidade = figure(width=1000, height=480, x_range=(2005, 2019), name = "Area_Joao")

    cores = ('#1957FF', '#0BD979') # Definir as cores para cada modalidade

    # Cria um ColumnDataSource para o gráfico
    source_ead_presencial = transforma_ColumnDataSource(data=dict(
        x = df_ead['ANO_CONCESSAO_BOLSA'].head(15),
        y1 = df_ead['QUANTIDADE POR ANO'].head(15),
        y2 = df_presencial['QUANTIDADE POR ANO'].head(15)
    ))

    # Adiciona a ferramenta de hover
    hover = HoverTool(tooltips=[
    ("Ano", "@x"),
    ("Quantidade EAD", "@y1"),
    ("Quantidade Presencial", "@y2")
    ])

    plot_modalidade.add_tools(hover)

    plot_modalidade.varea_stack(x='x', stackers=['y1', 'y2'], color=cores, source=source_ead_presencial,
                                legend_label=['EAD', 'PRESENCIAL'], alpha=0.5)

    # Crie um ColumnDataSource para os rótulos
    labels = LabelSet(x='x', y='y', text='y', level='glyph', text_font_size='10pt',
                    x_offset=0, y_offset=8, source=source_ead_presencial)

    # Adicione os rótulos ao gráfico
    plot_modalidade.add_layout(labels)

    # Configuração do Gráfico
    plot_modalidade.title.text = 'QUANTIDADE DE BOLSAS POR MODALIDADE DE ENSINO'
    plot_modalidade.title.align = 'center'
    plot_modalidade.xaxis.axis_label = 'Ano'
    plot_modalidade.yaxis.axis_label = 'Quantidade de Bolsas'

    plot_modalidade.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

    return plot_modalidade


'''
Gráfico 4: Histograma da quantidade de bolsas por faixa etária no ano de 2019, o mais recente no dataset.
'''

def Joao_plot4(df):
    df['ANO_CONCESSAO_BOLSA'] = pd.to_datetime(df["ANO_CONCESSAO_BOLSA"], format='%Y') # Converter a coluna de ano para datetime

    df_idade = df[df['ANO_CONCESSAO_BOLSA'] == '2019']  # Filtrar os dados para o ano de 2019

    df_idade = df_idade.groupby('idade').size().reset_index(name='PESSOAS') # Agrupar os dados por idade e calcular a quantidade de beneficiados

    # Cria uma fonte de dados para o gráfico
    source = transforma_ColumnDataSource(df_idade)

    plot_idades = figure(x_range=(18, 80),width=1000, height=480, tools = "box_zoom, pan, reset, save, wheel_zoom", name = "Histograma_Joao")

    hovertool_idades = HoverTool(tooltips = [("QUANTIDADE", "@PESSOAS")]) # Mostra a quantidade ao passar o mouse em cima da coluna
    plot_idades.add_tools(hovertool_idades)

    # Configuração do Gráfico
    plot_idades.title.text = "QUANTIDADE DE BOLSAS POR FAIXA ETÁRIA"
    plot_idades.title.align = 'center'
    plot_idades.xaxis.axis_label = "Idade"
    plot_idades.yaxis.axis_label = "Número de pessoas"

    plot_idades.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

    # Usar a fonte de dados na criação das barras
    plot_idades.vbar(x='idade', top='PESSOAS', width=0.7, line_width=1.5, source=source)
    plot_idades.line(x='idade', y='PESSOAS', line_width=2, line_alpha=0.2, line_cap='round', source=source, line_color='black')

    return plot_idades