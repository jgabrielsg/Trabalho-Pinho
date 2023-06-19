from datacleaning import df
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Range1d
from bokeh.io import output_file, show
from bokeh.plotting import figure

output_file("teste_vinicius.html")

# Primeiro gráfico: quantidade de bolsistas por ano

contagem_por_ano = df['ANO_CONCESSAO_BOLSA'].value_counts().reset_index() # Dataframe só com o ano e a quantidade de vezes que ele aparece
contagem_por_ano.columns = ['ANO', 'QUANTIDADE'] # Redefinindo o nome das colunas

source = ColumnDataSource(contagem_por_ano)

# Criando o gráfico
plot = figure()
plot.vbar(x='ANO', top='QUANTIDADE', source=source, width=0.8)

# Configurar o eixo x
plot.xaxis.axis_label = 'Ano'
plot.xaxis.major_label_orientation = 1.2

# Configurar o eixo y
plot.yaxis.axis_label = 'Quantidade'
plot.yaxis.formatter = NumeralTickFormatter(format='0,0') # Impede que os números apareçam em notação científica

# Exibir o gráfico
show(plot)