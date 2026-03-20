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
    'macarrão': 1.0,  # kg,
    'farinha': 1.0,  # kg,
    'sal': 1.0,  # kg
}

# ==============================
# CARREGAR DADOS DO BANCO DE DADOS
# ==============================

def carregar_dados():
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT p.nome AS Produto, p.categoria , pr.marca, m.nome AS mercado, pr.preco, pr.data_coleta
            FROM precos_produto pr
                JOIN produtos p ON pr.produto_id = p.id
                JOIN mercados m ON pr.mercado_id = m.id'''
    
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
    return menor_preco, custo_total_cesta

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
# CALCULAR CESTA BÁSICA
# ==============================

cesta_basica_mais_barata, custo_cesta_barata = montar_cesta_basica(df, CESTA_BASICA, tipo = 'barata')
cesta_basica_mais_cara, custo_cesta_cara = montar_cesta_basica(df, CESTA_BASICA, tipo = 'cara')

# ==============================
# CALCULAR CESTA BÁSICA COMPLEMENTO
# ==============================

cesta_complemento_mais_barata, custo_cesta_complemento_mais_barata = montar_cesta_basica(df, COMPLEMENTOS, tipo = 'barata')
cesta_complemento_mais_cara, custo_cesta_complemento_mais_cara = montar_cesta_basica(df, COMPLEMENTOS, tipo = 'cara')

# ==============================
# CALCULAR CESTA BÁSICA COMPLEMENTO + CESTA BÁSICA
# ==============================

total_cesta_complemento_mais_barata = custo_cesta_barata + custo_cesta_complemento_mais_barata
total_cesta_complemento_mais_cara = custo_cesta_cara + custo_cesta_complemento_mais_cara

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


