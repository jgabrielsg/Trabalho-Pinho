from datacleaning import criar_dataset, coluna_vazia, limpar_coluna, contar_repeticoes
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Range1d
from bokeh.io import output_file, show
from bokeh.plotting import figure

df = criar_dataset("prouni.csv")

output_file("teste_vinicius.html")

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