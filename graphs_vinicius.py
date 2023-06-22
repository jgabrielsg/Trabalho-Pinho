from datacleaning import criar_dataset, coluna_vazia, limpar_coluna, contar_repeticoes
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Range1d
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Category10_10

df = criar_dataset("prouni.csv")

output_file("teste_vinicius.html")

"""
# Primeiro gráfico: quantidade de bolsistas por ano

contagem_por_ano = contar_repeticoes(df, 'ANO_CONCESSAO_BOLSA') # Dataframe só com o ano e a quantidade de vezes que ele aparece
contagem_por_ano.columns = ['ANO', 'QUANTIDADE'] # Redefinindo o nome das colunas
contagem_por_ano = contagem_por_ano.sort_values('ANO', ascending=True) #  Deixando o ano por ordem crescente para conseguir fazer gráfico de linha

source = ColumnDataSource(contagem_por_ano)

# Criando o gráfico
plot = figure()
plot.line(x='ANO', y='QUANTIDADE', source=source, width=1.5)

# Configurar o eixo x
plot.xaxis.axis_label = 'Ano'
plot.xaxis.major_label_orientation = 1.2

# Configurar o eixo y
plot.yaxis.axis_label = 'Quantidade'
plot.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

# Exibir o gráfico
show(plot)
"""

tipo_por_ano = df.groupby(['TIPO_BOLSA', 'ANO_CONCESSAO_BOLSA']).size().reset_index(name='QUANTIDADE')

# Apenas em 1 ano teve bolsas de 25% e esse valor único não está sendo plotado no gráfico, então vou tirar para não atrapalhar
tipo_por_ano = tipo_por_ano.drop(tipo_por_ano[tipo_por_ano['TIPO_BOLSA'] == 'BOLSA COMPLEMENTAR 25%'].index)

plot = figure()

# Criando uma fonte de dados para cada tipo de bolsa
bolsas = {}
for tipo_bolsa in tipo_por_ano['TIPO_BOLSA'].unique():
    tipo_bolsa_data = tipo_por_ano[tipo_por_ano['TIPO_BOLSA'] == tipo_bolsa]
    bolsas[tipo_bolsa] = ColumnDataSource(tipo_bolsa_data)

# Plotando as linhas
for tipo_bolsa, color in zip(tipo_por_ano['TIPO_BOLSA'].unique(), Category10_10):
    plot.line(x='ANO_CONCESSAO_BOLSA', y='QUANTIDADE', source=bolsas[tipo_bolsa], line_color=color, legend_label=tipo_bolsa, width=2)

# Adicionando a legenda
plot.legend.location = 'top_left'
plot.legend.title = 'TIPO DE BOLSA'
plot.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

# Exibindo o gráfico
show(plot)