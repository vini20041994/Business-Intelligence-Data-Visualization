import pandas as pd
import numpy as np

def get_sinteticos_distribuicao(serie: pd.Series, min, max) -> pd.Series:
    media, desvio_pd, total = (serie.mean(), serie.std(), serie.count())
    if pd.isna(media) or pd.isna(desvio_pd):
        print("NaN!")
    else:
        print(f"Media: {media}, std:{desvio_pd}")
    # Gera dados sintéticos com a mesma média e desvio padrão
    distr = np.random.normal(loc=media, scale=desvio_pd, size=total)
    return pd.Series(np.clip(distr, min, max), dtype='float64').astype('float64')

def extrai_dados_uc(df: pd.DataFrame):
    df = df.copy()
    # Primeira linha tem os pesos de cada prova
    pesos = df.iloc[0][1:]
    # Ids: Na 4ª  linha, a partir da 2ª coluna
    ids = df.iloc[3][1:]
    # As notas aparecem a partir da 5ª linha
    notas = df.iloc[4:].copy()
    # O cabeçalho das notas está na linha 3
    notas.columns = df.iloc[3].copy()
    # Transforma strings em float
    colunas = notas.columns[1:]
    for col in colunas:
        notas[col] = notas[col].str.replace(',','.',regex=True).astype(float)
    # .iloc[:, 1:].apply(lambda c: c.astype(float))
    # Substitui dados NaN com o valor 0
    notas.fillna(value=0, inplace=True)
    notas = notas.rename(columns={"Coluna 1": "nome"})

    return (pesos, notas)


def acopla_dados_sinteticos(df_notas: pd.DataFrame, nomes_sinteticos: list):
    # Todas as linhas, primeira coluna: substituo pelos nomes sintéticos
    df_notas.iloc[:, 0] = nomes_sinteticos[0 : len(df_notas)]
    # Para cada coluna de notas, gera dados sintéticos com a mesma distribuição
    df_notas.iloc[:, 1:] = df_notas.iloc[:, 1:].apply(
        get_sinteticos_distribuicao, args=(0, 10)
    )
    return df_notas.round(2)

def explode_dataframe(df_notas: pd.DataFrame, pesos: list) -> pd.DataFrame:
    id_notas = df_notas.iloc[:, 1:].columns
    if len(id_notas) != len(pesos):
        print("Número de notas difere do número de pesos!")
    # zip é um iterador que percorre 2 listas
    # Usamos dict para gerar um dicionário onde as chaves são as notas e os valores são os pesos
    dict_notas_pesos = dict(zip(id_notas, pesos))

    # Transforma um dataframe "largo" em um dataframe "longo"
    # Um DF largo apresenta uma linha por entidade e variáveis nas colunas (Uma tabela é um DF largo)
    #   No nosso caso, cada linha é um aluno e as colunas são suas notas
    # Um DF longo pode conter multiplas linhas por entidade, cada uma representando um datapoint específico.
    #   Após a conversão, cada linha representa uma nota específica do aluno, com seu peso associado
    # https://pandas.pydata.org/docs/reference/api/pandas.melt.html
    df_explodido = df_notas.melt(
        id_vars=["nome"],
        value_vars=id_notas,
        var_name="avaliacao",  # Os ids das colunas serão valores da nova coluna 'Avaliacao'
        value_name="nota",  # Os valores das colunas notas serão explodidos na coluna 'Nota'
    )

    # Agregamos o peso de cada avaliação ao dataframe final
    df_explodido["peso"] = df_explodido["avaliacao"].map(dict_notas_pesos)
    return df_explodido