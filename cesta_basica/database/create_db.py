import sqlite3


def create_db():

    try:

        # Conexão ao banco (cria se não existir)
        conn = sqlite3.connect("cesta.db")

        cursor = conn.cursor()

        # Ativar suporte a FK
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Remover tabela de mercado e colunas dependentes, se existir
        cursor.execute("DROP TABLE IF EXISTS mercados;")

        # ==============================
        # TABELA PRODUTOS
        # ==============================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL UNIQUE,

                categoria TEXT NOT NULL

            );
        """)


        # ==============================
        # TABELA PREÇOS
        # ==============================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS precos_produto (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                produto_id INTEGER NOT NULL,

                marca TEXT NOT NULL,

                preco REAL NOT NULL CHECK(preco > 0),

                data_coleta DATE NOT NULL,

                FOREIGN KEY(produto_id)
                REFERENCES produtos(id)

            );
        """)


        # ==============================
        # TABELA IPCA
        # ==============================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ipca (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                data DATE NOT NULL,

                valor REAL NOT NULL

            );
        """)


        # ==============================
        # ÍNDICES (OTIMIZAÇÃO)
        # ==============================

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_produto_categoria
            ON produtos(categoria);
        """)


        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_preco_produto
            ON precos_produto(produto_id);
        """)


        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_ipca_data
            ON ipca(data);
        """)


        conn.commit()

        print("Banco criado com sucesso!")

    except Exception as e:

        print("Erro ao criar banco:", e)


    finally:

        conn.close()