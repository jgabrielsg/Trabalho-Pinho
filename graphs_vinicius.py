from datacleaning import criar_dataset, contar_repeticoes_multiplas, coluna_vazia
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Accent3

df = criar_dataset("prouni.csv")

output_file("teste_vinicius.html")

# Primeiro gráfico: quantidade de cada tipo de bolsa que foi fornecida através dos anos

# coluna_vazia(df)
# Nenhuma das colunas a serem usadas têm valores vazios, então não há a necessidade de limpar o dataset que vou usar

df_tipo_de_bolsa_por_ano = contar_repeticoes_multiplas(df, 'TIPO_BOLSA', 'ANO_CONCESSAO_BOLSA')

plot = figure()

# Criando uma fonte de dados para cada tipo de bolsa
bolsas = {}
for tipo_bolsa in df_tipo_de_bolsa_por_ano['TIPO_BOLSA'].unique():
    tipo_bolsa_dados = df_tipo_de_bolsa_por_ano[df_tipo_de_bolsa_por_ano['TIPO_BOLSA'] == tipo_bolsa]
    bolsas[tipo_bolsa] = ColumnDataSource(tipo_bolsa_dados)

# Plotando uma linha para cada tipo de bolsa
for tipo_bolsa, color in zip(df_tipo_de_bolsa_por_ano['TIPO_BOLSA'].unique(), Accent3):
    if tipo_bolsa == 'BOLSA COMPLEMENTAR 25%':
        # Só teve 'BOLSA COMPLEMENTAR 25%' no ano de 2008, então, para essa variável, vou plotar um ponto ao invés de um gráfico de linhas
        plot.circle(x = 'ANO_CONCESSAO_BOLSA', y = 'QUANTIDADE', source=bolsas[tipo_bolsa], color = color, legend_label = tipo_bolsa, width = 4)
    else:
        plot.line(x = 'ANO_CONCESSAO_BOLSA', y = 'QUANTIDADE', source=bolsas[tipo_bolsa], line_color = color, legend_label = tipo_bolsa, width = 2)

# Adicionando a legenda
plot.legend.location = 'top_left'
plot.legend.title = 'TIPO DE BOLSA'

# Configurar o eixo x
plot.xaxis.axis_label = 'ANO'
plot.xaxis.major_label_orientation = 1.2

# Configurar o eixo y
plot.yaxis.axis_label = 'QUANTIDADE'
plot.yaxis.formatter = NumeralTickFormatter(format = '0,0') # Impede que os números apareçam em notação científica

# Exibindo o gráfico
show(plot)