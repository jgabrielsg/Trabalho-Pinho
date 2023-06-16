import pandas as pd

df = pd.read_csv("gas_prices.csv")

# Testando se os valores estão completos:

for coluna in df:
    coluna_vazia = df[coluna].isna().any() # Retorna um booleano que mostra ter ou não valores vazios em alguma célula de cada coluna
    print("A coluna '{}' tem algum valor vazio? {}".format(coluna, coluna_vazia))

print("\n"*3)
# Dataset completo!