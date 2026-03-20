import scrapy
import w3lib.html

class CestaSpider(scrapy.Spider):
    name = "cesta_basica"
    start_urls = [
        'https://www.giassi.com.br/sitemap.xml'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Atraso entre as requisições para evitar sobrecarregar o servidor
        'RADOMIZE_DOWNLOAD_DELAY': True,  # Randomiza o atraso para parecer mais natural
        'CONCURRENT_REQUESTS' : 1,  # Limita a quantidade de requisições simultâneas
        'LOG_FILE': 'scrapay_output.log',  # Log das atividades do spider

        # CACHE SETTINGS
        'HTTPCACHE_ENABLED': True,  # Habilita o cache para evitar requisições repetidas
        'HTTPCACHE_EXPIRATION_SECS': 86400,  # Tempo de expiração do cache (24 horas)
        'HTTPCACHE_DIR': 'cache',  # Diretório onde o cache será armazenado
        'HTTPCACHE_IGNORE_HTTP_CODES': [404, 500, 502, 503],  # Ignora erros comuns para não armazenar respostas de erro
    }

    # ==============================
    # Função para processar o sitemap e extrair os links das páginas de produtos
    # ==============================

    def parse(self, response):
        response.selector.remove_namespaces()

        produtos = response.xpath(
            '//sitemap/loc[contains(text(),"/product")]/text()'
        )

        for url in produtos:
            yield response.follow(url.get(), self.parse_lista_produtos)
    
    # ==============================
    # Função para filtrar os dados dos produtos da cesta básica
    # ==============================

    def parse_lista_produtos(self, response):
        response.selector.remove_namespaces()

        urls = response.xpath('//url/loc/text()').getall()

        for url in urls:

            url_lower = url.lower()

            # FILTRO DA CESTA BÁSICA
            if any(prod in url_lower for prod in [
                "arroz", "feijao", "óleo", "oleo",
                "acucar", "açucar", "cafe"
            ]):
                yield response.follow(url, self.parse_info_produtos)

    # ==============================
    # Função para extrair as informações dos produtos da cesta básica
    # ==============================

    def parse_info_produtos(self, response):

        nome = response.xpath('//h1/text()').get()
        preco = response.xpath('//span[contains(@class,"price")]/text()').get()

        if preco:
            preco = preco.replace("R$", "").replace(",", ".").strip()

        yield {
            "nome": w3lib.html.remove_tags(nome).strip() if nome else None,
            "preco": float(preco) if preco else None,
            "url": response.url
        }

