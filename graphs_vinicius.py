from datacleaning import criar_dataset, contar_repeticoes_multiplas, coluna_vazia, contar_repeticoes_unitaria, limpar_coluna
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Accent3

df = criar_dataset("prouni.csv")

output_file("teste_vinicius.html")

"""
# Primeiro gráfico: quantidade de cada tipo de bolsa que foi fornecida através dos anos

# coluna_vazia(df)
# Nenhuma das colunas a serem usadas têm valores vazios, então não há a necessidade de limpar o dataset que vou usar

df_tipo_de_bolsa_por_ano = contar_repeticoes_multiplas(df, "TIPO_BOLSA", "ANO_CONCESSAO_BOLSA")

plot1 = figure()

# Criando uma fonte de dados para cada tipo de bolsa
bolsas_tipo = {}
for tipo_bolsa in df_tipo_de_bolsa_por_ano["TIPO_BOLSA"].unique():
    # Criação de um dataset para cada tipo de bolsa
    tipo_bolsa_dados = df_tipo_de_bolsa_por_ano[df_tipo_de_bolsa_por_ano["TIPO_BOLSA"] == tipo_bolsa]
    bolsas_tipo[tipo_bolsa] = ColumnDataSource(tipo_bolsa_dados)

# Plotando uma linha para cada tipo de bolsa
for tipo_bolsa, color in zip(df_tipo_de_bolsa_por_ano["TIPO_BOLSA"].unique(), Accent3):
    if tipo_bolsa == "BOLSA COMPLEMENTAR 25%":
        # Só teve "BOLSA COMPLEMENTAR 25%" no ano de 2008, então, para essa variável, vou plotar um ponto ao invés de um gráfico de linhas
        plot1.circle(x = "ANO_CONCESSAO_BOLSA", y = "QUANTIDADE", source=bolsas_tipo[tipo_bolsa], color = color, legend_label = tipo_bolsa, width = 4)
    else:
        plot1.line(x = "ANO_CONCESSAO_BOLSA", y = "QUANTIDADE", source=bolsas_tipo[tipo_bolsa], line_color = color, legend_label = tipo_bolsa, width = 2)

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
plot1.xaxis.major_label_orientation = 1
plot1.xaxis.ticker = df_tipo_de_bolsa_por_ano["ANO_CONCESSAO_BOLSA"].unique()  # Mostra todos os anos

# Configurando o eixo y
plot1.yaxis.axis_label = "QUANTIDADE"
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
"""

# Segundo gráfico: densidade de bolsas por estado brasileiro

# coluna_vazia(df)
# A coluna "SIGLA_UF_BENEFICIARIO_BOLSA" tem valores vazios, então vou limpá-los

df_bolsa_por_estado = limpar_coluna(df, "SIGLA_UF_BENEFICIARIO_BOLSA")

# Usando a função "len" para contar as linhas, 402 colunas vazias foram tiradas do dataset

df_bolsa_por_estado = contar_repeticoes_multiplas(df, "SIGLA_UF_BENEFICIARIO_BOLSA", "ANO_CONCESSAO_BOLSA")