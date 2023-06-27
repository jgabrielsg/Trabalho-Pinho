import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Legend, DatetimeTickFormatter
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from datacleaning import criar_dataset, contar_repeticoes_multiplas, coluna_vazia
from bokeh.palettes import Accent3
from bokeh.layouts import gridplot



df = criar_dataset("prouni.csv")

'''
Primeiro Gráfico: Divide por região a quantidade de bolsas por ano, mostrando a evolução de cada região
na quantidade de bolsas por ano. Foi feito um gráfico de linhas para cada região, com o eixo x sendo o ano.
'''

df["ANO_CONCESSAO_BOLSA"] = pd.to_datetime(df["ANO_CONCESSAO_BOLSA"], format = "%Y")

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

#show(plot_região)

'''
Simplesmente passei vergonha nesse primeiro gráfico, foi mal aí, galera, sou noob demais pra isso kkkkkk 
eis que eu não sei nem o que fazer com o dataset que eu criei: meme da menina do "sei lá, só sei que foi assim"
pelo menos o pai é o rei dos memes, né? admitam o pai é o rei dos memes :) eis que a SAM é braba demais
meu deus, eu não sei o que fazer, eu não sei o que fazer, eu não sei o que fazer, eu não sei o que fazer
por favor deus, eu vou ter que passar o zap pro guilherme, eu não sei o que fazer, eu não sei o que fazer
vsf quem é esse who desse guizinho10, noob demais, não sabe nem fazer um gráfico, que noob, que noob
'''

df_ead_presencial = df.groupby(['MODALIDADE_ENSINO_BOLSA', 'ANO_CONCESSAO_BOLSA']).size().reset_index(name='QUANTIDADE POR ANO')

plot_modalidade = figure(x_axis_type="datetime", width=1000, height=480, x_range=(2005, 2020))

modalidades = df_ead_presencial['MODALIDADE_ENSINO_BOLSA'].unique()  # Obter a lista de modalidades únicas
cores = ('#1957FF', '#0BD979')

for i, modalidade in enumerate(modalidades):
    dados_modalidade = df_ead_presencial[df_ead_presencial['MODALIDADE_ENSINO_BOLSA'] == modalidade]
    plot_modalidade.line(dados_modalidade['ANO_CONCESSAO_BOLSA'], dados_modalidade['QUANTIDADE POR ANO'],
                         line_width=5, line_color=cores[i], legend_label=modalidade)

plot_modalidade.title.text = 'QUANTIDADE DE BOLSAS POR MODALIDADE DE ENSINO'
plot_modalidade.title.text_font = "Arial"
plot_modalidade.title.text_font_size = "13pt"
plot_modalidade.title.text_font_style = "bold"
plot_modalidade.title.align = "center"

plot_modalidade.yaxis.formatter = NumeralTickFormatter(format='0,0')  # Impede que os números apareçam em notação científica

#show(plot_modalidade)

'''
Gráfico 3: eu simplesmente estou a busca do doce sabor da morte, pare de dizer que eu não sei fazer gráficos
talvez seja verdade, mas o que importa é que eu estou tentando, e isso é o que importa, não é mesmo?
e se você está lendo isso, saiba que eu te amo, e que eu te quero bem, e que eu quero que você seja feliz
aceite meu pedido de casamento, rawr, uwu, :3 vc é cute cuti, linda safada, gostosa, te amo
pq o copilot não para de se repetir? que noob, que noob, que noob, que noob, que noob, que noob, que noob
viu? ele fez de novo, meu deus, que noob, que noob, que noob, que noob, que noob, que noob, que noob
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

output_file("graficos.html")  # Define o nome do arquivo de saída
show(grid)  # Exibe o layout de grade com os gráficos