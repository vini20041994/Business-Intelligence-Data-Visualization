#!/usr/bin/env python3
"""
Script para gerar PDF com as respostas das questões sobre Emendas Parlamentares.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys
from io import StringIO

# Suprimir warnings
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# 1. CARREGAR E PREPARAR DADOS
# ==============================================================================

p = Path('EmendasParlamentares.csv')
if not p.exists():
    p = Path('Aula 02 - Python para Processamento de Dados-20260220') / 'EmendasParlamentares.csv'

df = pd.read_csv(p, sep=';', encoding='latin-1', engine='python')
df.columns = [c.strip() for c in df.columns]

pd.options.display.float_format = '{:,.2f}'.format

def to_num(col):
    return pd.to_numeric(col.str.replace('.', '', regex=False).str.replace(',', '.', regex=False))

numeric_cols = ['Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 'Valor Restos A Pagar Cancelados']
for c in numeric_cols:
    df[c + ' Num'] = to_num(df[c])

# ==============================================================================
# 2. FUNÇÕES PARA CAPTURAR OUTPUT
# ==============================================================================

def capture_q1():
    total_pago_por_ano = df.groupby('Ano da Emenda')['Valor Pago Num'].sum().sort_index()
    print("Valor total pago em emendas por ano:")
    print(total_pago_por_ano)
    print(f"\nTotal geral: R$ {total_pago_por_ano.sum():,.2f}")

def capture_q2():
    q2_stats = df.groupby('Região')['Valor Empenhado Num'].agg(['mean', 'std', 'count', 'sum'])
    print("Média e desvio padrão dos valores empenhados por região:")
    print(q2_stats)

def capture_q3():
    q3_autores = df.groupby('Nome do Autor da Emenda')['Valor Empenhado Num'].sum().sort_values(ascending=False).head(10)
    print("Top 10 autores que mais destinaram recursos:")
    print(q3_autores)

def capture_q4():
    q4_sc = df[df['UF'] == 'SANTA CATARINA'].shape[0]
    q4_sc_valor = df[df['UF'] == 'SANTA CATARINA']['Valor Empenhado Num'].sum()
    print(f"Total de emendas: {q4_sc}")
    print(f"Valor total empenhado: R$ {q4_sc_valor:,.2f}")

def capture_q5():
    df_sc = df[df['UF'] == 'SANTA CATARINA']
    q5_municipios = df_sc.groupby(['Município', 'Tipo de Emenda'])['Valor Empenhado Num'].sum().sort_values(ascending=False).head(10)
    print("Top 10 - Municípios de SC por tipo de emenda:")
    print(q5_municipios)

def capture_q6():
    df['Diferença'] = abs(df['Valor Liquidado Num'] - df['Valor Pago Num'])
    diferenca_significativa = df[df['Diferença'] > 0]
    print(f"Total de emendas com diferença > 0: {len(diferenca_significativa)}")
    print(f"Percentual: {len(diferenca_significativa)/len(df)*100:.2f}%")
    print(f"\nTop 10 maiores diferenças:")
    print(diferenca_significativa.nlargest(10, 'Diferença')[['Ano da Emenda', 'Município', 'Valor Liquidado Num', 'Valor Pago Num', 'Diferença']])

def capture_q7():
    q7_percentual = (df.groupby('Ano da Emenda')['Valor Restos A Pagar Cancelados Num'].sum() / df.groupby('Ano da Emenda')['Valor Empenhado Num'].sum()) * 100
    print("Percentual de Restos a Pagar Cancelados por ano:")
    print(q7_percentual)

def capture_q8():
    q8_subfuncao = df.groupby('Região')['Nome Subfunção'].apply(lambda x: x.value_counts().index[0])
    print("Subfunção mais comum para cada Região:")
    print(q8_subfuncao)

def capture_q9():
    q9_ausentes = df[df['Código Município IBGE'].isna() | (df['Código Município IBGE'] == '')]
    q9_count = len(q9_ausentes)
    q9_pct = (q9_count / len(df)) * 100
    print(f"Total de linhas com código ausente: {q9_count}")
    print(f"Percentual: {q9_pct:.2f}%")
    if q9_count > 0:
        print(f"\nAmostra de linhas com código ausente:")
        print(q9_ausentes[['Ano da Emenda', 'Município', 'Código Município IBGE']].head(5))
    else:
        print("Nenhuma linha com código ausente encontrada.")

def capture_q10():
    municipios_unicos = df['Município'].unique()
    print(f"Total de nomes únicos de Município: {len(municipios_unicos)}")
    print(f"Total de registros: {len(df)}")
    sao_municipios = [m for m in municipios_unicos if 'São' in m or 'Sao' in m or 'SAO' in m]
    print(f"\nMunicípios com 'São' encontrados: {len(sao_municipios)}")
    if sao_municipios:
        print("Exemplos (primeiros 10):")
        for m in sao_municipios[:10]:
            print(f"  - {m}")

# Dicionário de questões
questoes = {
    'Q1': {
        'titulo': 'Qual o valor total pago em emendas por ano?',
        'codigo': """total_pago_por_ano = df.groupby('Ano da Emenda')['Valor Pago Num'].sum().sort_index()
print("Valor total pago em emendas por ano:")
print(total_pago_por_ano)
print(f"\\nTotal geral: R$ {total_pago_por_ano.sum():,.2f}")""",
        'funcao': capture_q1
    },
    'Q2': {
        'titulo': 'Média e desvio padrão dos valores empenhados por região',
        'codigo': """q2_stats = df.groupby('Região')['Valor Empenhado Num'].agg(['mean', 'std', 'count', 'sum'])
print("Média e desvio padrão dos valores empenhados por região:")
print(q2_stats)""",
        'funcao': capture_q2
    },
    'Q3': {
        'titulo': 'Top 10 autores que mais destinaram recursos',
        'codigo': """q3_autores = df.groupby('Nome do Autor da Emenda')['Valor Empenhado Num'].sum().sort_values(ascending=False).head(10)
print("Top 10 autores que mais destinaram recursos:")
print(q3_autores)""",
        'funcao': capture_q3
    },
    'Q4': {
        'titulo': 'Emendas destinadas para Santa Catarina',
        'codigo': """q4_sc = df[df['UF'] == 'SANTA CATARINA'].shape[0]
q4_sc_valor = df[df['UF'] == 'SANTA CATARINA']['Valor Empenhado Num'].sum()
print(f"Total de emendas: {q4_sc}")
print(f"Valor total empenhado: R$ {q4_sc_valor:,.2f}")""",
        'funcao': capture_q4
    },
    'Q5': {
        'titulo': 'Top 10 - Municípios de SC por tipo de emenda',
        'codigo': """df_sc = df[df['UF'] == 'SANTA CATARINA']
q5_municipios = df_sc.groupby(['Município', 'Tipo de Emenda'])['Valor Empenhado Num'].sum().sort_values(ascending=False).head(10)
print("Top 10 - Municípios de SC por tipo de emenda:")
print(q5_municipios)""",
        'funcao': capture_q5
    },
    'Q6': {
        'titulo': 'Emendas com diferença entre Valor Liquidado e Valor Pago',
        'codigo': """df['Diferença'] = abs(df['Valor Liquidado Num'] - df['Valor Pago Num'])
diferenca_significativa = df[df['Diferença'] > 0]
print(f"Total de emendas com diferença > 0: {len(diferenca_significativa)}")
print(f"Percentual: {len(diferenca_significativa)/len(df)*100:.2f}%")
print(f"\\nTop 10 maiores diferenças:")
print(diferenca_significativa.nlargest(10, 'Diferença')[...])""",
        'funcao': capture_q6
    },
    'Q7': {
        'titulo': 'Percentual de Restos a Pagar Cancelados por ano',
        'codigo': """q7_percentual = (df.groupby('Ano da Emenda')['Valor Restos A Pagar Cancelados Num'].sum() / 
                     df.groupby('Ano da Emenda')['Valor Empenhado Num'].sum()) * 100
print("Percentual de Restos a Pagar Cancelados por ano:")
print(q7_percentual)""",
        'funcao': capture_q7
    },
    'Q8': {
        'titulo': 'Subfunção mais comum para cada Região',
        'codigo': """q8_subfuncao = df.groupby('Região')['Nome Subfunção'].apply(lambda x: x.value_counts().index[0])
print("Subfunção mais comum para cada Região:")
print(q8_subfuncao)""",
        'funcao': capture_q8
    },
    'Q9': {
        'titulo': 'Linhas com Código Município IBGE ausente',
        'codigo': """q9_ausentes = df[df['Código Município IBGE'].isna() | (df['Código Município IBGE'] == '')]
q9_count = len(q9_ausentes)
q9_pct = (q9_count / len(df)) * 100
print(f"Total de linhas com código ausente: {q9_count}")
print(f"Percentual: {q9_pct:.2f}%")""",
        'funcao': capture_q9
    },
    'Q10': {
        'titulo': 'Análise de duplicatas de Município com grafias diferentes',
        'codigo': """municipios_unicos = df['Município'].unique()
print(f"Total de nomes únicos: {len(municipios_unicos)}")
sao_municipios = [m for m in municipios_unicos if 'São' in m or 'Sao' in m]
print(f"Municípios com 'São': {len(sao_municipios)}")""",
        'funcao': capture_q10
    }
}

# ==============================================================================
# 3. GERAR PDF
# ==============================================================================

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError:
    print("Instalando reportlab...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Criar PDF
output_file = Path('Respostas_Emendas_Parlamentares.pdf')
doc = SimpleDocTemplate(str(output_file), pagesize=A4)

styles = getSampleStyleSheet()

# Definir estilos customizados
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor='#1f4788',
    spaceAfter=12,
    alignment=TA_CENTER
)

question_style = ParagraphStyle(
    'QuestionStyle',
    parent=styles['Heading2'],
    fontSize=12,
    textColor='#2563eb',
    spaceAfter=6,
    spaceBefore=12
)

code_style = ParagraphStyle(
    'CodeStyle',
    parent=styles['Normal'],
    fontSize=8,
    fontName='Courier',
    textColor='#333333',
    spaceAfter=6
)

# Construir conteúdo do PDF
story = []

# Título
story.append(Paragraph('Exercícios: Análise de Emendas Parlamentares', title_style))
story.append(Paragraph('Respostas e Código', styles['Heading3']))
story.append(Paragraph(f'<i>Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}</i>', styles['Normal']))
story.append(Spacer(1, 0.3 * inch))

# Adicionar cada questão
for q_num in sorted(questoes.keys(), key=lambda x: int(x[1:])):
    q = questoes[q_num]
    
    # Título da questão
    story.append(Paragraph(f'<b>{q_num}: {q["titulo"]}</b>', question_style))
    
    # Código
    story.append(Paragraph('<b>Código utilizado:</b>', styles['Normal']))
    code_text = q['codigo'].replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
    story.append(Preformatted(code_text, code_style))
    
    # Resposta
    story.append(Paragraph('<b>Resposta:</b>', styles['Normal']))
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        q['funcao']()
        output = mystdout.getvalue().strip()
    except Exception as e:
        output = f"Erro ao executar: {str(e)}"
    finally:
        sys.stdout = old_stdout
    
    output_text = output.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
    story.append(Preformatted(output_text, code_style))
    
    story.append(Spacer(1, 0.2 * inch))

# Rodapé
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph(
    '<i>Documento gerado automaticamente a partir do notebook de análise de Emendas Parlamentares.</i>',
    styles['Normal']
))

# Gerar PDF
doc.build(story)
print(f"\n✅ PDF gerado com sucesso: {output_file}")
print(f"   Localização: {output_file.absolute()}")
