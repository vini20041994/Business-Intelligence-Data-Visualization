# Atividade em Sala - Mercado de Entretenimento

Este projeto entrega um dashboard em Dash para analisar o mercado de entretenimento com base no arquivo `mercado_entretenimento.csv`.

## O que a aplicação faz

O material foi separado em três partes, seguindo o enunciado da atividade:

1. Parte 1 mostra a evolução da bilheteria de cinema por gênero ao longo dos anos, com destaque visual para 2020 e anotação do impacto mais forte.
2. Parte 2 traz um painel interativo com dropdown para escolher a região e identificar o ponto em que o streaming ultrapassa o cinema.
3. Parte 3 monta um grid com a tendência de churn das plataformas e três mini gráficos com a participação regional atual de cada player.

O arquivo [reproduce.py](reproduce.py) centraliza a reprodução da entrega e também abre o dashboard.

## Estrutura do projeto

- [part1.py](part1.py): lógica e exportação da Parte 1.
- [part2.py](part2.py): lógica do painel interativo e criação do app Dash.
- [part3.py](part3.py): lógica e exportação da Parte 3.
- [shared.py](shared.py): funções compartilhadas para carga de dados, estilo e conversão de figuras.
- [reproduce.py](reproduce.py): script único para gerar os três artefatos e executar a aplicação.
- [requirements.txt](requirements.txt): dependências do projeto.

## Como executar

1. Instale as dependências.

    /usr/bin/python -m pip install --user -r requirements.txt

2. Execute o script de reprodução para gerar os três gráficos estáticos e abrir o dashboard.

    /usr/bin/python reproduce.py

3. Se quiser apenas gerar os gráficos estáticos, rode este snippet no diretório do projeto.

    /usr/bin/python - <<'PY'
    from reproduce import build_all_assets

    build_all_assets()
    PY

## Saídas geradas

Ao executar o script de reprodução, o projeto gera os seguintes arquivos na pasta do projeto:

- part1.png
- part2.png
- part3.png

Esses arquivos podem ser reutilizados fora do dashboard, caso seja necessário apresentar a entrega em formato estático.

## Observações

- O dashboard usa o dataset local [mercado_entretenimento.csv](mercado_entretenimento.csv).
- A Parte 2 calcula programaticamente o ponto de interseção entre Cinema e Streaming para cada região.
- A atividade foi organizada para facilitar a reprodução da entrega em sala e a apresentação final do grupo.