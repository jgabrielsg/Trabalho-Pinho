# A2 - Introdução a Ciência de Dados

### João Gabriel, Gustavo Bianchi, Guilherme Buss e Vinicius Nascimento

---

O trabalho foi feito usando a biblioteca Bokeh do Python. Com a biblioteca criamos gráficos interativos e os colocamos em um site hospedado no Netfily. Cada um dos integrantes fez, no mínimo, 3 gráficos, com até 3 modelos diferentes, como gráficos de linha, histogramas, mapas, gráficos de área, etc.

Aqui estão os arquivos e pastas utilizados para hospedarmos o nosso Bokeh Server. Na pasta CSVs temos os CSVs utilizados, na pasta modulos temos os arquivos em python que geram os gráficos, separados para cada um dos integrantes, na pasta templates temos o index.html, que possui a página do Bokeh Server criada, junto com a stylesheet e o script em JS.

---

Arquivos e suas utilizações:

- `datacleaning.py`: Faz a extração dos dados a partir dos CSVs e possui funções de limpeza de dados utilizada para a formação dos gráficos.
- `main.py`: Roda o Bokeh Server localmente ao ser executado. Ele chama as funções que criam os gráficos nos módulos e adiciona-os no index.html, que é feito em Jinja2.
- `theme.yaml`: Tema utilizado em alguns dos gráficos. Esse tema pode ser adicionado diretamente nos gráficos, o que permite padronização.
- `graphs_joao.py`, `graphs_gustavo.py` e etc.: Criam os gráficos no Bokeh e estilizam-los. Os gráficos são colocados em funções para poderem ser chamados pela main.

