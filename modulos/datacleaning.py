import pandas as pd
from bokeh.models import ColumnDataSource

# Função que, quando dado o nome do arquivo csv, retorna ele como um dataset em Pandas:
def criar_dataset(dataset):
    dataset_preparado = pd.read_csv(dataset)
    return dataset_preparado

# Confere se há valores vazios em alguma coluna:
def coluna_vazia(dataset):
    for coluna in dataset:
        valor_vazio = dataset[coluna].isna().any() # Retorna um booleano que mostra ter ou não valores vazios em alguma célula
        print("A coluna '{}' tem algum valor vazio? {}".format(coluna, valor_vazio))

# Limpa os valores vazios da coluna selecionada
def limpar_coluna(dataset, coluna):
    return dataset.dropna(subset = [coluna])

# Conta a quantidade de vezes que um valor se repete em relação a mais de uma coluna:
def contar_repeticoes_multiplas(dataset, *colunas):
    # A coluna que vai contar as repetições se chamará "QUANTIDADE"
    repetições = dataset.groupby(list(colunas)).size().reset_index(name = "QUANTIDADE")
    return repetições

# Mostra todos valores únicos de uma coluna do dataset:
def valores_unicos(dataset, coluna):
    lista_de_valores_unicos = []
    for unico in dataset[coluna].unique():
        lista_de_valores_unicos.append(unico)
    print(lista_de_valores_unicos)

#Transforma os dados em ColumnDataSource de acordo com a necessidade
def transforma_ColumnDataSource(df, coluna = None, igualA = None):
    if coluna != None and igualA != None:
        df = ColumnDataSource(df[df[coluna] == igualA])
    elif coluna != None:
        df = ColumnDataSource(df[coluna])
    else:
        df = ColumnDataSource(df)

    return df