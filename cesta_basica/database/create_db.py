import sqlite3

def create_db():
    try:
        # Conexão ao banco de dados (será criado se não existir)
        conn = sqlite3.connect('cesta.db')
        cursor = conn.cursor()

        # Ativar o suporte a chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON;")

        # ==============================
        # Criação da tabela 'produtos'
        # ==============================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL
            );
        ''')

        # ==============================
        # Criação da tabela 'mercados'
        # ==============================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mercados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cidade TEXT NOT NULL
            );
        ''')

        # ==============================
        # Criação da tabela 'precos'
        # ==============================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS precos_produto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                marca TEXT NOT NULL,
                mercado_id INTEGER NOT NULL,
                preco REAL NOT NULL CHECK (preco > 0),
                data_coleta DATE NOT NULL,

                FOREIGN KEY (produto_id) REFERENCES produtos(id),
                FOREIGN KEY (mercado_id) REFERENCES mercados(id)
            );
        ''')

        # ================================
        # Criação da tabela 'IPCA'
        # ================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ipca (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATE NOT NULL,
                valor REAL NOT NULL
            );
        ''')

        # ==============================
        # Indices para otimização de consultas
        # ==============================

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_produto_categoria ON produtos(categoria);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_preco_produto ON precos_produto(produto_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_preco_mercado ON precos_produto(mercado_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ipca_data ON ipca(data);")

        # Salvar as alterações 

        conn.commit()
        print("Banco de dados criado com sucesso!")

    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        conn.close()

