import requests 
from datetime import datetime

API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"

def extrair_ipca():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        dados = response.json()
             
        return dados

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return []
    except ValueError as e:
        print(f"Erro ao processar os dados: {e}")
        return []

def transformar_ipca(dados_brutos):
    
    dados_transformados = []

    for item in dados_brutos:
        try:
            data = datetime.strptime(item['data'], "%d/%m/%Y").date()  # Converte a string para um objeto date
            valor = float(item['valor'].replace(",", "."))  # Converte a string para float, substituindo a vírgula por ponto
            dados_transformados.append({"data": data, "valor": valor})

        except Exception as e:
            print(f"Erro ao transformar os dados: {e}")
            continue

    return dados_transformados

def carregar_ipca()
    dados_brutos = extrair_ipca()
    if not dados_brutos:
        print("Nenhum dado para carregar.")
        return []

    dados_transformados = transformar_ipca(dados_brutos)
    return dados_transformados

if __name__ == "__main__":
    dados = carregar_ipca()
    for item in dados:
        print(f"Data: {item['data']}, Valor: {item['valor']}")