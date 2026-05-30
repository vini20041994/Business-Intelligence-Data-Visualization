import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# ===============================
# Configurações
# ===============================

DATABASE_PATH = "sqlite:///cesta_basica.db"

API_URL = (
    "https://api.bcb.gov.br/dados/serie/"
    "bcdata.sgs.433/dados?formato=json"
)

# ===============================
# Conectar ao banco
# ===============================

engine = create_engine(DATABASE_PATH)


# ===============================
# Função: extrair dados da API
# ===============================

def extrair_ipca():

    print("Consultando API do Banco Central...")

    response = requests.get(API_URL)

    if response.status_code != 200:
        raise Exception("Erro ao acessar API")

    dados = response.json()

    df = pd.DataFrame(dados)

    return df


# ===============================
# Função: transformar dados
# ===============================

def transformar_dados(df):

    print("Transformando dados...")

    df["data"] = pd.to_datetime(
        df["data"],
        format="%d/%m/%Y"
    )

    df["valor"] = df["valor"].astype(float)

    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month

    return df


# ===============================
# Função: carregar dados no SQLite
# ===============================

def salvar_no_banco(df):

    print("Salvando dados no banco...")

    with engine.begin() as conn:

        for _, linha in df.iterrows():

            conn.execute(
                text("""
                    INSERT OR IGNORE INTO ipca
                    (data, valor, ano, mes)
                    VALUES
                    (:data, :valor, :ano, :mes)
                """),
                {
                    "data": linha["data"],
                    "valor": linha["valor"],
                    "ano": linha["ano"],
                    "mes": linha["mes"],
                }
            )

    print("Dados inseridos com sucesso!")


# ===============================
# Pipeline ETL
# ===============================

def main():

    df = extrair_ipca()

    df = transformar_dados(df)

    salvar_no_banco(df)


if __name__ == "__main__":
    main()