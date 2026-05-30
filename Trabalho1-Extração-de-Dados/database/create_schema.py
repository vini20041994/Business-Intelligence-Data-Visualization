from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    Boolean,
    UniqueConstraint
)

# ===============================
# Conexão com banco SQLite
# ===============================

engine = create_engine("sqlite:///cesta_basica.db", echo=True)

metadata = MetaData()


# ===============================
# Tabela: ipca
# Série histórica mensal
# ===============================

ipca = Table(
    "ipca",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", Date, nullable=False),
    Column("valor", Float, nullable=False),
    Column("ano", Integer, nullable=False),
    Column("mes", Integer, nullable=False),
    UniqueConstraint("ano", "mes", name="uq_ipca_ano_mes")
)


# ===============================
# Tabela: produtos
# Produtos coletados via scraping
# ===============================

produtos = Table(
    "produtos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(150), nullable=False),
    Column("marca", String(100)),
    Column("categoria", String(50), nullable=False),
    Column("preco", Float, nullable=False),
    Column("peso", Float),
    Column("unidade", String(20)),
    Column("data_coleta", Date, nullable=False)
)


# ===============================
# Tabela: cesta_basica
# Define versões da cesta
# (mínima ou máxima)
# ===============================

cesta_basica = Table(
    "cesta_basica",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tipo", String(20), nullable=False),  # menor_valor / maior_valor
    Column("data_referencia", Date, nullable=False),
    Column("valor_total", Float)
)


# ===============================
# Tabela: itens_cesta
# Relação entre cesta e produtos
# ===============================

itens_cesta = Table(
    "itens_cesta",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cesta_id", Integer,
           ForeignKey("cesta_basica.id"),
           nullable=False),
    Column("produto_id", Integer,
           ForeignKey("produtos.id"),
           nullable=False),
    Column("quantidade", Float, nullable=False),
    Column("valor_unitario", Float, nullable=False),
    Column("valor_total_item", Float, nullable=False)
)


# ===============================
# Tabela: historico_cesta
# Valor estimado da cesta no passado
# corrigido por IPCA
# ===============================

historico_cesta = Table(
    "historico_cesta",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cesta_id", Integer,
           ForeignKey("cesta_basica.id"),
           nullable=False),
    Column("ano", Integer, nullable=False),
    Column("valor_estimado", Float, nullable=False),
    Column("corrigido_por_ipca", Boolean, default=True)
)


# ===============================
# Criar tabelas
# ===============================

metadata.create_all(engine)

print("Schema criado com sucesso!")