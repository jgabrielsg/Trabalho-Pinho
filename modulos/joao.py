from graphs_joao import * 
from bokeh.layouts import column
from bokeh.models import Select

# Obter a lista de regiões únicas
regioes_unicas = df_regiao_estado['REGIAO_BENEFICIARIO_BOLSA'].unique()
regioes_unicas = regioes_unicas.tolist()

# Criar um widget Select para a escolha da região
select_regiao = Select(title="Escolha a região:", options=regioes_unicas)

# Função de callback para atualizar o gráfico quando uma nova região for selecionada
def update_plot(attrname, old, new):
    regiao_selecionada = select_regiao.value
    plot_estados = None
    
    for plot in plots:
        if plot.title.text.endswith(regiao_selecionada):
            plot_estados = plot
            break

    if plot_estados:
        layout.children = [select_regiao, plot_estados]

# Adicionar a função de callback ao widget Select
select_regiao.on_change('value', update_plot)

# Definir o gráfico inicial para a primeira região
plot_estados = plots[0]

# Criar o layout inicial com o filtro e o gráfico
layout = column(select_regiao, plot_estados)

# Exibir o layout
curdoc().add_root(layout)

# Exibir o layout
show(layout)