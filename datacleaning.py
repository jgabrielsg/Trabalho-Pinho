import pandas as pd

# Função que, quando dado o nome do arquivo csv, te retorna ele como um dataset em Pandas:
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
    return dataset.dropna(subset=[coluna])

# Conta a quantidade de vezes que um valor se repete em determinada coluna
def contar_repeticoes(dataset, coluna):
    repetições = dataset[coluna].value_counts().reset_index()
    return repetições