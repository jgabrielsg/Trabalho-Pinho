import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Legend, DatetimeTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from datacleaning import criar_dataset
from bokeh.layouts import gridplot

output_file("Testes/teste_joao.html")  # Define o nome do arquivo de saída

DATA = 'CSVs/prouni.csv'

df = criar_dataset(DATA)

'''
Primeiro Gráfico: Divide por região a quantidade de bolsas por ano, mostrando a evolução de cada região
na quantidade de bolsas por ano. Foi feito um gráfico de linhas para cada região, com o eixo x sendo o ano.
'''

df_regiões = df.groupby(['ANO_CONCESSAO_BOLSA', 'REGIAO_BENEFICIARIO_BOLSA']).size().reset_index(name='QUANTIDADE POR ANO')

plot_região = figure(x_axis_type = "datetime", width = 1000, height = 480, x_range=(2005, 2020))

regiões = df_regiões['REGIAO_BENEFICIARIO_BOLSA'].unique()  # Obter a lista de regiões únicas
cores = ('#1957FF', '#0BD979', '#D4CB00', '#EB8100', '#E00913')

for i, região in enumerate(regiões):
    dados_regionais = df_regiões[df_regiões['REGIAO_BENEFICIARIO_BOLSA'] == região]
    plot_região.line(dados_regionais['ANO_CONCESSAO_BOLSA'], dados_regionais['QUANTIDADE POR ANO'], 
                     line_width=5, line_color=cores[i], legend_label=região)

plot_região.title.text = "QUANTIDADE DE BOLSAS POR REGIÃO"
plot_região.title.text_font = "Arial"
plot_região.title.text_font_size = "13pt"
plot_região.title.text_font_style = "bold"
plot_região.title.align = "center"

plot_região.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

show(plot_região)


'''
Gráfico 2: Quantidade de bolsas por região e por estado, mostrando a evolução de cada estado na quantidade de bolsas por ano.
'''

# Agrupar os dados por região, estado e calcular a quantidade de beneficiados
df_regiao_estado = df.groupby(['ANO_CONCESSAO_BOLSA', 'REGIAO_BENEFICIARIO_BOLSA', 'SIGLA_UF_BENEFICIARIO_BOLSA']).size().reset_index(name='QUANTIDADE DE BENEFICIADOS')
df_regiao_estado['ANO_CONCESSAO_BOLSA'] = pd.to_datetime(df_regiao_estado['ANO_CONCESSAO_BOLSA'], format="%Y")

# Definir as cores para cada estado
cores = ('#1957FF', '#0BD979', '#D4CB00', '#EB8100', '#E00913', '#1957FF', '#0BD979', '#D4CB00', '#EB8100', '#E00913')

# Obter a lista de regiões únicas
regioes_unicas = df_regiao_estado['REGIAO_BENEFICIARIO_BOLSA'].unique()

plots = []  # Lista para armazenar os gráficos individuais

for regiao in regioes_unicas:
    dados_regiao = df_regiao_estado[df_regiao_estado['REGIAO_BENEFICIARIO_BOLSA'] == regiao]
    plot_regiao = figure(x_axis_type="datetime", width=1200, height=400, x_range=(df_regiao_estado['ANO_CONCESSAO_BOLSA'].min(), df_regiao_estado['ANO_CONCESSAO_BOLSA'].max()))

    for i, estado in enumerate(dados_regiao['SIGLA_UF_BENEFICIARIO_BOLSA'].unique()):
        dados_estado = dados_regiao[dados_regiao['SIGLA_UF_BENEFICIARIO_BOLSA'] == estado]
        plot_regiao.line(dados_estado['ANO_CONCESSAO_BOLSA'], dados_estado['QUANTIDADE DE BENEFICIADOS'],
                                line_width=5, line_color=cores[i], legend_label=estado)

    plot_regiao.title.text = "QUANTIDADE DE BOLSAS POR ESTADO - REGIÃO {}".format(regiao)
    plot_regiao.title.text_font = "Arial"
    plot_regiao.title.text_font_size = "13pt"
    plot_regiao.title.text_font_style = "bold"
    plot_regiao.title.align = "center"

    plot_regiao.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

    plots.append(plot_regiao)  # Adiciona o gráfico à lista

# Cria um layout de grade com os gráficos
grid = gridplot([[plot] for plot in plots], toolbar_location=None)

show(grid)  # Exibe o layout de grade com os gráficos

'''
Gráfico 3: Quantidade de bolsas por modalidade de ensino por ano, separando entre presencial e EAD
'''

df_ead_presencial = df.groupby(['MODALIDADE_ENSINO_BOLSA', 'ANO_CONCESSAO_BOLSA']).size().reset_index(name='QUANTIDADE POR ANO')
df_ead = df_ead_presencial[df_ead_presencial['MODALIDADE_ENSINO_BOLSA'] == 'EAD']
df_presencial = df_ead_presencial[df_ead_presencial['MODALIDADE_ENSINO_BOLSA'] == 'PRESENCIAL']


plot_modalidade = figure(x_axis_type="datetime", width=1000, height=480, x_range=(2005, 2020))

modalidades = df_ead_presencial['MODALIDADE_ENSINO_BOLSA'].unique() # Obter a lista de modalidades únicas
print(modalidades)
cores = ('#1957FF', '#0BD979')

source_ead_presencial = ColumnDataSource(data=dict(
    x = df_ead['ANO_CONCESSAO_BOLSA'].head(15),
    y1 = df_ead['QUANTIDADE POR ANO'].head(15),
    y2 = df_presencial['QUANTIDADE POR ANO'].head(15)
))

plot_modalidade.varea_stack(x='x', stackers=['y1', 'y2'], color=cores, source=source_ead_presencial, alpha=0.5)

plot_modalidade.title.text = 'QUANTIDADE DE BOLSAS POR MODALIDADE DE ENSINO'
plot_modalidade.title.text_font = "Arial"
plot_modalidade.title.text_font_size = "13pt"
plot_modalidade.title.text_font_style = "bold"
plot_modalidade.title.align = "center"

plot_modalidade.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

show(plot_modalidade)


'''
Gráfico 4: Histograma da quantidade de bolsas por faixa etária no ano de 2019, o mais recente no dataset.
'''
df['ANO_CONCESSAO_BOLSA'] = pd.to_datetime(df["ANO_CONCESSAO_BOLSA"], format='%Y') # Converter a coluna de ano para datetime

df_idade = df[df['ANO_CONCESSAO_BOLSA'] == '2019']  # Filtrar os dados para o ano de 2019

df_idade['idade'] = df_idade['idade'].astype(int)  # Converter a coluna de idade para inteiros

df_idade = df_idade.groupby('idade').size().reset_index(name='NÚMERO DE PESSOAS')

# Cria uma fonte de dados para o gráfico
source = ColumnDataSource(df_idade)

plot_idades = figure(x_range=(18, 80),width=1000, height=480)
plot_idades.title.text = "QUANTIDADE DE BOLSAS POR FAIXA ETÁRIA"
plot_idades.title.text_font = "Arial"
plot_idades.title.text_font_size = "13pt"
plot_idades.title.text_font_style = "bold"
plot_idades.title.align = "center"
plot_idades.xaxis.axis_label = "Idade"
plot_idades.yaxis.axis_label = "Número de pessoas"
plot_idades.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

# Usar a fonte de dados na criação das barras
plot_idades.vbar(x='idade', top='NÚMERO DE PESSOAS', width=0.7, line_width=1.5, source=source)
plot_idades.line(x='idade', y='NÚMERO DE PESSOAS', line_width=2, line_alpha=0.2, line_cap='round', source=source, line_color='black')

show(plot_idades)