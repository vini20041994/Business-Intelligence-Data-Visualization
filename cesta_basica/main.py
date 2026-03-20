from database.create_db import create_db
from etl.ipca_api import extrair_ipca, transformar_ipca, carregar_ipca
from processing.cesta_calculo import carregar_dados, cesta_basica_mais_barata, cesta_basica_mais_cara, ipca_acumulado_por_ano, estimativa_historica_custo_cesta
from etl.load_data import carregar_ipca_no_db
from etl.cesta_spider import CestaSpider

def main():
    # Criar o banco de dados e as tabelas
    create_db()

    # Carregar os dados do IPCA e inserir no banco de dados
    dados_ipca = carregar_ipca()
    carregar_ipca_no_db(dados_ipca)

    # Extrair, transformar e carregar os dados dos preços dos produtos
    spider = CestaSpider()
    spider.crawl()

    # Carregar os dados para análise
    df = carregar_dados()

    # Análise da cesta básica mais barata
    

    # Análise da cesta básica mais cara
    cesta_cara, custo_cesta_cara = cesta_basica_mais_cara(df)
    print("\nCesta Básica Mais Cara:")
    print(cesta_cara)
    print(f"Custo Total da Cesta Básica Mais Cara: R$ {custo_cesta_cara:.2f}")

    # Análise do IPCA acumulado por ano
    ipca_acumulado = ipca_acumulado_por_ano(df)
    print("\nIPCA Acumulado por Ano:")
    print(ipca_acumulado)

    # Estimativa do custo da cesta básica ajustada pelo IPCA

    historico_cesta_barata = estimativa_historica_custo_cesta(custo_cesta_barata, ipca_acumulado)
    print("\nEstimativa do Custo da Cesta Básica Mais Barata Ajustada pelo IPCA:")
    print(historico_cesta_barata)

    historico_cesta_cara = estimativa_historica_custo_cesta(custo_cesta_cara, ipca_acumulado)
    print("\nEstimativa do Custo da Cesta Básica Mais Cara Ajustada pelo IPCA:")
    print(historico_cesta_cara) 
