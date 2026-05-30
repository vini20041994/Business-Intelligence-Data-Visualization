import scrapy
import w3lib.html


class CestaSpider(scrapy.Spider):

    name = "cesta_basica"

    start_urls = [
        "https://www.giassi.com.br/sitemap.xml",
    ]

    custom_settings = {

        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'LOG_FILE': 'scrapy_output.log',

        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 86400,
        'HTTPCACHE_DIR': 'cache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [404, 500, 502, 503]

    }

    def parse(self, response: scrapy.http.Response):

        # remove namespaces do XML
        response.selector.remove_namespaces()

        # pega sitemaps de produtos
        produtos = response.xpath(
            '//sitemap/loc[contains(text(),"/product")]/text()'
        )

        print('Products:')

        for url in produtos:

            if url is not None:

                print(url.get())

                yield response.follow(
                    url.get(),
                    self.parse_lista_produtos
                )

        return


    def parse_lista_produtos(self, response: scrapy.http.Response):

        response.selector.remove_namespaces()

        # itens obrigatórios da cesta básica
        lista_arroz = response.xpath(
            '//url/loc[contains(text(),"arroz")]/text()'
        )

        lista_feijao = response.xpath(
            '//url/loc[contains(text(),"feijao")]/text()'
        )

        lista_acucar = response.xpath(
            '//url/loc[contains(text(),"acucar")]/text()'
        )

        lista_oleo = response.xpath(
            '//url/loc[contains(text(),"oleo")]/text()'
        )

        lista_cafe = response.xpath(
            '//url/loc[contains(text(),"cafe")]/text()'
        )

        # complemento (bônus)
        lista_macarrao = response.xpath(
            '//url/loc[contains(text(),"macarrao")]/text()'
        )

        lista_farinha = response.xpath(
            '//url/loc[contains(text(),"farinha")]/text()'
        )

        lista_sal = response.xpath(
            '//url/loc[contains(text(),"sal")]/text()'
        )

        listas = (
            lista_arroz +
            lista_feijao +
            lista_acucar +
            lista_oleo +
            lista_cafe +
            lista_macarrao +
            lista_farinha +
            lista_sal
        )

        for produto_url in listas:

            yield response.follow(
                produto_url.get(),
                self.parse_info_produtos
            )


    def parse_info_produtos(self, response):

        from datetime import datetime
        import re

        nome = response.xpath('//h1/text()').get()

        preco = response.xpath(
            '//span[contains(@class,"price")]/text()'
        ).get()


        if preco:

            preco = preco.replace(
                "R$", ""
            ).replace(
                ",", "."
            ).strip()


        if nome and preco:

            nome_lower = nome.lower()

            categoria = self.definir_categoria(nome)

            # tentativa simples de extrair marca (primeira palavra normalmente)
            marca = nome.split()[0]

            # tentativa simples de extrair peso e unidade
            peso = None
            unidade = None

            match = re.search(r'(\d+[\.,]?\d*)\s?(kg|g|ml|l)', nome_lower)

            if match:

                peso = float(match.group(1).replace(",", "."))

                unidade = match.group(2)


            self.cursor.execute(

                """
                INSERT INTO produtos
                (nome, marca, categoria, preco, peso, unidade, data_coleta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,

                (

                    nome,
                    marca,
                    categoria,
                    float(preco),
                    peso,
                    unidade,
                    datetime.now().date()

                )

            )

            self.conn.commit()


        yield {

            "nome": nome,
            "preco": preco,
            "url": response.url

        }