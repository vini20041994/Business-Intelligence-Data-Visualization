import sqlite3
from .ipca_api import carregar_ipca

DB_NAME = 'cesta.db'

def carregar_ipca_no_db(dados):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inseridos = 0

    for item in dados:
        data = item['data']
        valor = item['valor']

        # Verificar se o registro já existe para evitar duplicidade
        cursor.execute("SELECT id FROM ipca WHERE data = ?", (data,))
        existing = cursor.fetchone()
        if existing is None:
            cursor.execute("INSERT INTO ipca (data, valor) VALUES (?, ?)", (data, valor))
            inseridos += 1

    conn.commit()
    conn.close()

    print(f"{inseridos} registros de IPCA inseridos no banco de dados.")

