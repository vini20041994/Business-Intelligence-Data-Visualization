import pandas as pd
import numpy as np
import random
import os
import sys
import plot
import parse_functions

PLOT_HISTO = False
if len(sys.argv) > 1:
    PLOT_HISTO = sys.argv[1] == 'PLOT'


dir_normal = "csv_notas"
dir_explodido = "csv_notas_explode"

# Cria os diretórios para gravar os arquivos processados
os.makedirs(dir_normal, exist_ok=True)
os.makedirs(dir_explodido, exist_ok=True)
# Carrega o csv e remove as colunas não utilizadas
df = pd.read_csv("Cadastro_alunos.csv")

# Gerando um conjunto semi aleatório de nomes + sobrenomes para criar dados de ilustração
prim_nome = [
    "João",
    "José",
    "Maria",
    "Virgínia",
    "Pedro",
    "Paula",
    "Juliete",
    "Fern",
    "Stark",
    "Alphonse",
    "Edward",
    "Casca",
    "Farnese",
    "Puck",
]
sobrenome = [
    "Exemplo",
    "Hipótese",
    "Talvez",
    "Padrão",
    "Amostra",
    "Ilustração",
    "Cdia",
    "UniSenai",
    "Molde",
    "Arquétipo",
    "Vivência",
    "Aprendizado",
]

# Gera anos de nascimento aleatórios, entre 1990 e 2009
df["Nascimento"] = parse_functions.get_sinteticos_distribuicao(df["Nascimento"], 1990, 2009)
df["Nascimento"] = df["Nascimento"].round(0).astype(int)

df.to_csv("Cadastro_alunos_anonimizado.csv")

# Lista de N x N nomes
nomes = [(nm + " " + sb) for nm in prim_nome for sb in sobrenome]
# Embaralha a lista, para que a ordem dos nomes seja aleatória
random.shuffle(nomes)

# Substitui o nome pelos nomes aleatórios
df["Aluno"] = nomes[0 : len(df)]

df = (
    df.drop("Escola", axis=1)
    .drop("Cidade", axis=1)
    .drop("E-mail", axis=1)
    .drop("Ano de Conclusão", axis=1)
)
df = df.drop("Matrícula", axis=1).drop("Idade", axis=1)
# Converte True para 1 e False para 0
df["Regular?"] = (df["Regular?"] == True).astype(int)
df = df.drop("Coluna 1", axis=1)

# Renomeando as colunas para o padrão do banco
df = df.rename(
    columns={
        "Aluno": "nome",
        "Modalidade": "modalidade_ensino_medio",
        "Nascimento": "ano_nascimento",
        "Regular?": "regular",
    }
)
# Schema dos alunos
# CREATE TABLE alunos (
#     matricula int primary key AUTOINCREMENT,
#     nome VARCHAR(300) not null,
#     modalidade_ensino_medio VARCHAR(10) CHECK (modalidade_ensino_medio IN ('publica','privada','n/a')),
#     ano_nascimento int,
#     regular INT CHECK (regular IN (0,1)) DEFAULT 0
# )


# Usando o próprio índice do df como matrícula para omitir os dados originais
df.index.name = "matricula"

df.to_csv(dir_normal + "/alunos.csv")
df.to_csv(dir_explodido + "/alunos.csv")

###### Parse de notas

df_bd = pd.read_csv("notas_banco_dados1.csv", header=None)
# Schema das notas
# CREATE TABLE alunos_notas(
# id int primary key AUTOINCREMENT,
# matricula int not null,
# nota float not null DEAFAULT 0,
# id_uc int not null,
# nome VARCHAR(30),
# peso NUMERIC(5,4) CHECK(peso >=0.1 AND peso <= 1.0),

if PLOT_HISTO:
    series = (parse_functions.extrai_dados_uc(df_bd)[1]).iloc[:,1:]
    # Substitui dados NaN com o valor 0
    series.fillna(value=0, inplace=True)
    plot.plot_histo(series,'N1','Nota')


closure = lambda df_tp: (df_tp[0], parse_functions.acopla_dados_sinteticos(df_tp[1], nomes))
# closure = lambda df_tp : (df_tp[0],df_tp[1])

(pesos_bd, df_bd) = closure(parse_functions.extrai_dados_uc(df_bd))

print(df_bd.head()) 
print(df_bd.dtypes)

# Temos os pesos separados das notas. Podemos reformatar esse dataframe para agregar os dados
if PLOT_HISTO:
    plot.plot_histo(df_bd.iloc[:,1:],'N1S','Nota')
    
df_bd.to_csv(dir_normal + "/notas_banco_dados1.csv", float_format='%.2f')

df_bd = parse_functions.explode_dataframe(df_bd, pesos_bd)

df_bd.to_csv(dir_explodido + "/notas_banco_dados1.csv")
