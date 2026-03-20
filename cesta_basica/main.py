from database.create_db import create_db
from etl.ipca_api import extrair_ipca, transformar_ipca, carregar_ipca
import processing.cesta_calculo as cesta_calculo
from etl.load_data import carregar_ipca_no_db
from etl.cesta_spider import CestaSpider
from scrapy.crawler import CrawlerProcess

def main():
    # Criar o banco de dados e as tabelas
    create_db()

    # Carregar os dados do IPCA e inserir no banco de dados
    dados_ipca = carregar_ipca()
    carregar_ipca_no_db(dados_ipca)

    # Extrair, transformar e carregar os dados dos preços dos produtos
    process = CrawlerProcess()
    process.crawl(CestaSpider)
    process.start()

    # Carregar os dados para análise
    df = cesta_calculo.carregar_dados()

    # Análise da cesta básica mais barata
    print("\nCesta Básica Mais Barata:")
    print(cesta_calculo.cesta_basica_mais_barata(df)[0][['categoria', 'Produto', 'preco', 'quantidade', 'custo_total']])
    print(f"Custo Total da Cesta Básica Mais Barata: R$ {cesta_calculo.cesta_basica_mais_barata(df)[1]:.2f}")
    print(f"Custo Total do complemento mais barato: R$ {cesta_calculo.cesta_basica_mais_barata(df)[2]:.2f}")
    print(f"Total da Cesta Básica + Complementos Mais Barata: R$ {cesta_calculo.cesta_basica_mais_barata(df)[3]:.2f}")

    # Análise da cesta básica mais cara
    print("\nCesta Básica Mais Cara:")
    print(cesta_calculo.cesta_basica_mais_cara(df)[0][['categoria', 'Produto', 'preco', 'quantidade', 'custo_total']])
    print(f"Custo Total da Cesta Básica Mais Cara: R$ {cesta_calculo.cesta_basica_mais_cara(df)[1]:.2f}")
    print(f"Custo Total do complemento mais caro: R$ {cesta_calculo.cesta_basica_mais_cara(df)[2]:.2f}")
    print(f"Total da Cesta Básica + Complementos Mais Cara: R$ {cesta_calculo.cesta_basica_mais_cara(df)[3]:.2f}")

    # Análise do IPCA acumulado por ano
    ipca_acumulado = cesta_calculo.ipca_acumulado_por_ano(df)
    print("\nIPCA Acumulado por Ano:")
    print(ipca_acumulado)

    # Estimativa do custo da cesta básica ajustada pelo IPCA

    historico_cesta_barata = cesta_calculo.estimativa_historica_custo_cesta(cesta_calculo.cesta_basica_mais_barata(df)[1], ipca_acumulado)
    print("\nEstimativa do Custo da Cesta Básica Mais Barata Ajustada pelo IPCA:")
    print(historico_cesta_barata)

    historico_cesta_cara = cesta_calculo.estimativa_historica_custo_cesta(cesta_calculo.cesta_basica_mais_cara(df)[1], ipca_acumulado)
    print("\nEstimativa do Custo da Cesta Básica Mais Cara Ajustada pelo IPCA:")
    print(historico_cesta_cara)

if __name__ == "__main__":
    main() 
