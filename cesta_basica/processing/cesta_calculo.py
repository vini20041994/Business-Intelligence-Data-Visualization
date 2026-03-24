import sqlite3
import pandas as pd

DB_NAME = 'cesta.db'

# ==============================
# CONFIGURAÇÕES DA CESTA BÁSICA
# ==============================

CESTA_BASICA = {
    'Arroz': 5.0,  # kg,
    'Feijão': 2.0,  # kg,
    'Óleo de Soja': 0.9,  # litro,
    'Açúcar': 1.0,  # kg,
    'Café': 0.5,  # kg,
}

COMPLEMENTOS = {
    'Macarrão': 1.0,  # kg,
    'Farinha': 0.5,  # kg,
    'Sal': 1.0,  # kg
}

# ==============================
# CARREGAR DADOS DO BANCO DE DADOS
# ==============================

def carregar_dados():
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT p.nome AS Produto, p.categoria, pr.marca, pr.preco, pr.data_coleta
            FROM precos_produto pr
                JOIN produtos p ON pr.produto_id = p.id'''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ==============================
# CESTA BÁSICA - MAIS BARATA
# ==============================

def cesta_basica_mais_barata(df):
    menor_preco = df.loc[df.groupby('categoria')['preco'].idxmin()]

    menor_preco['quantidade'] = menor_preco['categoria'].map(CESTA_BASICA)
    menor_preco['custo_total'] = menor_preco['preco'] * menor_preco['quantidade']

    custo_total_cesta = menor_preco['custo_total'].sum()

    # Complementos mais baratos
    menor_preco_complemento = df.loc[df.groupby('categoria')['preco'].idxmin()]
    menor_preco_complemento = menor_preco_complemento[menor_preco_complemento['categoria'].isin(COMPLEMENTOS.keys())].copy()
    menor_preco_complemento['quantidade'] = menor_preco_complemento['categoria'].map(COMPLEMENTOS)
    menor_preco_complemento['custo_total'] = menor_preco_complemento['preco'] * menor_preco_complemento['quantidade']
    custo_total_complemento = menor_preco_complemento['custo_total'].sum()

    total_cesta_complemento = custo_total_cesta + custo_total_complemento

    return menor_preco, custo_total_cesta, custo_total_complemento, total_cesta_complemento

# ==============================
# CESTA BÁSICA - MAIS CARA
# ==============================

def cesta_basica_mais_cara(df):
    maior_preco = df.loc[df.groupby('categoria')['preco'].idxmax()]

    maior_preco['quantidade'] = maior_preco['categoria'].map(CESTA_BASICA)
    maior_preco['custo_total'] = maior_preco['preco'] * maior_preco['quantidade']

    custo_total_cesta = maior_preco['custo_total'].sum()

    # Complementos mais caros
    maior_preco_complemento = df.loc[df.groupby('categoria')['preco'].idxmax()]
    maior_preco_complemento = maior_preco_complemento[maior_preco_complemento['categoria'].isin(COMPLEMENTOS.keys())].copy()
    maior_preco_complemento['quantidade'] = maior_preco_complemento['categoria'].map(COMPLEMENTOS)
    maior_preco_complemento['custo_total'] = maior_preco_complemento['preco'] * maior_preco_complemento['quantidade']
    custo_total_complemento = maior_preco_complemento['custo_total'].sum()

    total_cesta_complemento = custo_total_cesta + custo_total_complemento

    return maior_preco, custo_total_cesta, custo_total_complemento, total_cesta_complemento

# ==============================
# MONTAR CESTA BÁSICA 
# ==============================

def montar_cesta_basica(df, item, tipo = 'barata'):
    if tipo == 'barata':
        cesta = df.loc[df.groupby('categoria')['preco'].idxmin()]
    else:
        cesta = df.loc[df.groupby('categoria')['preco'].idxmax()]

    # Filtrar apenas os produtos da cesta básica
    cesta = cesta[cesta['categoria'].isin(item.keys())].copy()

    cesta['quantidade'] = cesta['categoria'].map(item)
    cesta['custo_total'] = cesta['preco'] * cesta['quantidade']

    total_cesta = cesta['custo_total'].sum()

    return cesta, total_cesta

# ==============================
# IPCA ACUMULADO POR ANO
# ==============================

def ipca_acumulado_por_ano(df):
    conn = sqlite3.connect(DB_NAME)
    
    df = pd.read_sql_query('SELECT data, valor FROM ipca', conn)
    conn.close()

    df['data'] = pd.to_datetime(df['data'])
    df['ano'] = df['data'].dt.year

    # Calcular o IPCA acumulado por ano
    df['fator'] = 1 + (df['valor'] / 100)

    ipca_acumulado = df.groupby('ano')['fator'].prod() - 1

    return ipca_acumulado.reset_index(name = 'ipca_acumulado')

# ==============================
# ESTIMATIVA HISTÓRICA DO CUSTO DA CESTA BÁSICA (DEFLAÇÃO)
# ==============================

def estimativa_historica_custo_cesta(valor_atual, ipca_acumulado):
    resultados = []
    for _, row in ipca_acumulado.iterrows():
        ano = row['ano']
        ipca = row['ipca_acumulado']
        valor_estimado = valor_atual / (1 + ipca)
        resultados.append({'ano': ano, 'valor_estimado': valor_estimado})

    return pd.DataFrame(resultados)


