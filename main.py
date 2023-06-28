
from bokeh.plotting import curdoc
from bokeh.models import Button
from bokeh.layouts import column

from modulos import graphs_gustavo
from modulos import graphs_joao


from os.path import dirname, join #necessário pro bokeh achar os arquivos
import pandas as pd

#Carrega o dataframe
df = pd.read_csv(join(dirname(__file__), 'CSVs', 'prouni.csv')) 

Gustavo_plot1 = graphs_gustavo.Gustavo_plot1(df)
Gustavo_plot2 = graphs_gustavo.Gustavo_plot2(df)

Joao_plot1 = graphs_joao.Joao_plot1(df)
Joao_plot2 = graphs_joao.Joao_plot2(df)
Joao_plot3 = graphs_joao.Joao_plot3(df)
Joao_plot4 = graphs_joao.Joao_plot4(df)

#Carrega as informações adicionais necessárias para o mapa
municipios = pd.read_csv(join(dirname(__file__), 'CSVs', 'municipios.csv'))

Gustavo_plot3 = graphs_gustavo.Gustavo_plot3(df, municipios)

#permite que o index.html leia os gráficos
curdoc().add_root(Gustavo_plot1)
curdoc().add_root(Gustavo_plot2)
curdoc().add_root(Gustavo_plot3)

curdoc().add_root(Joao_plot1)
# curdoc().add_root(Joao_plot2)
curdoc().add_root(Joao_plot3)
curdoc().add_root(Joao_plot4)