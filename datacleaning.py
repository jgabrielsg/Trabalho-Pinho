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

df = criar_dataset("prouni.csv")
coluna_vazia(df)

print("-=-="*19)