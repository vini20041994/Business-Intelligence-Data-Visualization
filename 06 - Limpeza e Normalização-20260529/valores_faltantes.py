import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_excel("bensimoveis-69cbc20141908.xlsx")
# Substituo String vazia por NA para incluir estes registros na contagem
# SE eu sei que existe um valor default (-1 por exemplo) para esses casos, posso substituir por NA também
data = data.replace("",pd.NA)

# Contagem de valores faltantes, ordenada menor->maior
heatmap = data.isna().sum().sort_values()

# Podemos também gerar um sumário, calculando a porcentagem de registros faltantes
relativa = data.isna().mean() * 100
print(relativa.sort_values(ascending=False))

# Visualização da distribuição de valores faltantes
plot = heatmap.plot.bar(x=heatmap.index)
plt.show()

# Análise pair-wise de características (Valores faltantes de acordo com o município)
por_municipio = data.isna().groupby(data['nmmunicipio']).sum()
relativa = data.isna().groupby(data['nmmunicipio']).mean() * 100

plt.figure(figsize=(12, 8))
plt.ticklabel_format(style='plain', axis='both')

# Filtrando apenas os 20 municípios com mais dados faltantes para não poluir o gráfico
top_missing = relativa.sum(axis=1).sort_values(ascending=False).head(20).index
ax = sns.heatmap(relativa.loc[top_missing], annot=True, cmap='YlOrRd')
                     
plt.title("Deficiência de Coleta de Dados por Município (%)")
plt.show()

plt.close('all')