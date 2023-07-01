from bokeh.plotting import curdoc

from modulos import graphs_gustavo
from modulos import graphs_joao
from modulos import graphs_vinicius
from modulos import graphs_guilherme

from os.path import dirname, join #necessário pro bokeh achar os arquivos
import pandas as pd

from bokeh.command.bootstrap import main
#Função pra rodar o bokeh server diretamente do main.py
if __name__ == "__main__":
    main(["bokeh", "serve", "--show", "../Trabalho-Pinho"])

#Carrega o dataframe
df = pd.read_csv(join(dirname(__file__), 'CSVs', 'prouni.csv'))

Gustavo_plot1 = graphs_gustavo.Gustavo_plot1(df)
Gustavo_plot2 = graphs_gustavo.Gustavo_plot2(df)

#Carrega as informações adicionais necessárias para o mapa
municipios = pd.read_csv(join(dirname(__file__), 'CSVs', 'municipios.csv'))

Gustavo_plot3 = graphs_gustavo.Gustavo_plot3(df, municipios)

Joao_plot1 = graphs_joao.Joao_plot1(df)
Joao_plot2 = graphs_joao.Joao_plot2(df)
Joao_plot3 = graphs_joao.Joao_plot3(df)
Joao_plot4 = graphs_joao.Joao_plot4(df)

Vinicius_plot1 = graphs_vinicius.Vinicius_plot1(df)
Vinicius_plot2 = graphs_vinicius.Vinicius_plot2(df)
Vinicius_plot3 = graphs_vinicius.Vinicius_plot3(df)

Guilherme_plot1 = graphs_guilherme.Guilherme_plot1(df)
Guilherme_plot2, Guilherme_plot3 = graphs_guilherme.Guilherme_plot2(df)
Guilherme_plot4 = graphs_guilherme.Guilherme_plot3(df)


#permite que o index.html leia os gráficos
curdoc().add_root(Gustavo_plot1)
curdoc().add_root(Gustavo_plot2)
curdoc().add_root(Gustavo_plot3)

curdoc().add_root(Joao_plot1)
# curdoc().add_root(Joao_plot2)
curdoc().add_root(Joao_plot3)
curdoc().add_root(Joao_plot4)

curdoc().add_root(Vinicius_plot1)
curdoc().add_root(Vinicius_plot2)
curdoc().add_root(Vinicius_plot3)

curdoc().add_root(Guilherme_plot1)
curdoc().add_root(Guilherme_plot2)
curdoc().add_root(Guilherme_plot3)
curdoc().add_root(Guilherme_plot4)