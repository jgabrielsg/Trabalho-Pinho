from datacleaning import criar_dataset, contar_repeticoes_multiplas, coluna_vazia, contar_repeticoes_unitaria, limpar_coluna, valores_unicos
from bokeh.models import ColumnDataSource, NumeralTickFormatter, FactorRange, HoverTool
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Accent3, Category20
from bokeh.transform import dodge, factor_cmap
import pandas as pd

DATA = "CSVs/prouni.csv"

df = criar_dataset(DATA)

output_file("Testes/teste_vinicius.html")

"""

#---------------------------- Primeiro gráfico: quantidade de cada tipo de bolsa que foi fornecida através dos anos

# coluna_vazia(df)
# Nenhuma das colunas a serem usadas têm valores vazios, então não há a necessidade de limpar o dataset que vou usar

df_tipo_de_bolsa_por_ano = contar_repeticoes_multiplas(df, "TIPO_BOLSA", "ANO_CONCESSAO_BOLSA")

plot1 = figure(tools = "box_zoom, pan, reset, save, wheel_zoom", width = 800)

# Adicionando um tool em que ao passar o mouse em cima de uma barra, a quantidade de bolsas aparece
quantidade_de_bolsas_da_linha = HoverTool(tooltips = [("QUANTIDADE", "@QUANTIDADE")])
plot1.add_tools(quantidade_de_bolsas_da_linha)

# Configurando a estética dos parâmetros
plot1.toolbar.logo = None # Remove a logo no canto
plot1.toolbar.autohide = True # Apaga as ferramentas de longe e reaparece quando passa o mouse perto
plot1.toolbar_location = "below" # Escolhe onde colocar as ferramentas no gráfico

# Criando uma fonte de dados para cada tipo de bolsa
bolsas_tipo = {}
for tipo_bolsa in df_tipo_de_bolsa_por_ano["TIPO_BOLSA"].unique():
    # Criação de um dataset para cada tipo de bolsa
    tipo_bolsa_dados = df_tipo_de_bolsa_por_ano[df_tipo_de_bolsa_por_ano["TIPO_BOLSA"] == tipo_bolsa]
    bolsas_tipo[tipo_bolsa] = ColumnDataSource(tipo_bolsa_dados)

# Plotando uma linha para cada tipo de bolsa
for tipo_bolsa, cor in zip(df_tipo_de_bolsa_por_ano["TIPO_BOLSA"].unique(), Accent3):
    if tipo_bolsa == "BOLSA COMPLEMENTAR 25%":
        # Só teve "BOLSA COMPLEMENTAR 25%" no ano de 2008, então, para essa variável, vou plotar um ponto ao invés de um gráfico de linhas
        círculo = plot1.circle(x = "ANO_CONCESSAO_BOLSA", y = "QUANTIDADE", source=bolsas_tipo[tipo_bolsa], color = cor,
        legend_label = tipo_bolsa, width = 4)
    else:
        plot1.line(x = "ANO_CONCESSAO_BOLSA", y = "QUANTIDADE", source=bolsas_tipo[tipo_bolsa], line_color = cor,
        legend_label = tipo_bolsa, width = 2)

# Configurando o meu círculo
glyph_círculo = círculo.glyph
glyph_círculo.size = 10 # Tamanho do círculo
glyph_círculo.line_color = "darkgreen" # Borda do círculo
glyph_círculo.line_width = 2 # Largura da linha

# Configurando o título do gráfico
plot1.title.text = "QUANTIDADE DE CADA TIPO DE BOLSA POR ANO"
plot1.title.text_font = "Arial"
plot1.title.text_font_size = "13pt"
plot1.title.text_font_style = "bold"
plot1.title.align = "center"

# Configurando o eixo x
plot1.xaxis.axis_label = "ANO"
plot1.xaxis.axis_label_text_font = "Arial"
plot1.xaxis.axis_label_text_font_size = "13pt"
plot1.xaxis.axis_label_text_font_style = "bold"
plot1.xaxis.ticker = df_tipo_de_bolsa_por_ano["ANO_CONCESSAO_BOLSA"].unique()  # Mostra todos os anos

# Configurando o eixo y
plot1.yaxis.axis_label = "BOLSISTAS"
plot1.yaxis.axis_label_text_font = "Arial"
plot1.yaxis.axis_label_text_font_size = "13pt"
plot1.yaxis.axis_label_text_font_style = "bold"
plot1.yaxis.formatter = NumeralTickFormatter(format = "0,0") # Impede que os números apareçam em notação científica

# Configurando a legenda
plot1.legend.location = "top_left"
plot1.legend.title = "TIPO DE BOLSA:"
plot1.legend.title_text_font = "Arial"
plot1.legend.title_text_font_size = "11pt"
plot1.legend.title_text_font_style = "normal" # Para tirar o itálico horrível que vem por padrão
plot1.legend.label_text_font = "Arial"
plot1.legend.label_text_font_size = "10pt"

# Configurando a área de plotagem
plot1.border_fill_color = "white"
plot1.outline_line_color = "black"

# Exibindo o gráfico
show(plot1)

#---------------------------- Segundo gráfico: raça dos bolsistas por estado brasileiro

# coluna_vazia(df)
# A coluna "SIGLA_UF_BENEFICIARIO_BOLSA" tem valores vazios, então vou limpá-los

df_bolsa_por_estado = limpar_coluna(df, "SIGLA_UF_BENEFICIARIO_BOLSA")

# Usando a função "len" para contar as linhas, 402 colunas vazias foram tiradas do dataset

df_bolsa_por_estado = contar_repeticoes_multiplas(df, "SIGLA_UF_BENEFICIARIO_BOLSA", "RACA_BENEFICIARIO_BOLSA")

# Criando uma paleta de cores para as raças
raças_valores_unicos = df_bolsa_por_estado["RACA_BENEFICIARIO_BOLSA"].unique()
cores = Category20[6]

# Definindo alguns parâmetros do gráfico
plot2 = figure(x_range=df_bolsa_por_estado["SIGLA_UF_BENEFICIARIO_BOLSA"].unique(), width = 1200, 
               tools = "box_zoom, pan, reset, save, wheel_zoom")

# Adicionando um tool em que ao passar o mouse em cima de uma barra, a quantidade de bolsas aparece
quantidade_de_bolsas_da_barra = HoverTool(tooltips = [("QUANTIDADE", "@QUANTIDADE")])
plot2.add_tools(quantidade_de_bolsas_da_barra)

# Configurando a estética dos parâmetros
plot2.toolbar.logo = None # Remove a logo no canto
plot2.toolbar.autohide = True # Apaga as ferramentas de longe e reaparece quando passa o mouse perto
plot2.toolbar_location = "below" # Escolhe onde colocar as ferramentas no gráfico

# Criando uma fonte com ColumnDataSource para cada umas das raças
dicionario_fonte = {}
for raça in raças_valores_unicos:
    source = ColumnDataSource(df_bolsa_por_estado[df_bolsa_por_estado["RACA_BENEFICIARIO_BOLSA"] == raça])
    dicionario_fonte[raça] = source

# Criando o gráfico
for numero_da_linha, raça in enumerate(raças_valores_unicos):
    source = dicionario_fonte[raça]
    barra = plot2.vbar(x = dodge("SIGLA_UF_BENEFICIARIO_BOLSA", numero_da_linha/(len(raças_valores_unicos)+2), range = plot2.x_range),
                top="QUANTIDADE", width=0.2, source = source, color = cores[numero_da_linha], legend_label = raça)

# Configurando o título do gráfico
plot2.title.text = "QUANTIDADE DE BOLSAS POR RAÇA EM CADA ESTADO"
plot2.title.text_font = "Arial"
plot2.title.text_font_size = "13pt"
plot2.title.text_font_style = "bold"
plot2.title.align = "center"

# Configurando o eixo x
plot2.xaxis.axis_label = "ESTADOS"
plot2.xaxis.axis_label_text_font = "Arial"
plot2.xaxis.axis_label_text_font_size = "13pt"
plot2.xaxis.axis_label_text_font_style = "bold"

# Configurando o eixo y
plot2.yaxis.axis_label = "BOLSAS"
plot2.yaxis.axis_label_text_font = "Arial"
plot2.yaxis.axis_label_text_font_size = "13pt"
plot2.yaxis.axis_label_text_font_style = "bold"
plot2.yaxis.formatter = NumeralTickFormatter(format = "0,0") # Impede que os números apareçam em notação científica

# Configurando a legenda
plot2.legend.location = "top_left"
plot2.legend.title = "RAÇA DO BOLSISTA:"
plot2.legend.title_text_font = "Arial"
plot2.legend.title_text_font_size = "11pt"
plot2.legend.title_text_font_style = "normal" # Para tirar o itálico horrível que vem por padrão
plot2.legend.label_text_font = "Arial"
plot2.legend.label_text_font_size = "10pt"

# Configurando a área de plotagem
plot2.border_fill_color = "white"
plot2.outline_line_color = "black"

# Exibir o gráfico
show(plot2)

"""

#---------------------------- Terceiro gráfico: