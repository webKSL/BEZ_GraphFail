import matplotlib.pyplot as plt
import os
from processData import *


def plotbarATE(filtered_data, data, output_path, colunas_selecionadas):
    testes_valores = filtered_data[colunas_selecionadas].iloc[2:, :]  # Filtrando as linhas relevantes do filtered_data
    valores_maximo = data[colunas_selecionadas].iloc[:1, :]  # Apenas a primeira linha
    valores_minimo = data[colunas_selecionadas].iloc[1:2, :]  # Apenas a segunda linha
    coluna_channel = filtered_data.dropna()['Channel']

    # Converter para numérico
    testes_valores = testes_valores.apply(pd.to_numeric, errors='coerce')
    valores_maximo = valores_maximo.apply(pd.to_numeric, errors='coerce')
    valores_minimo = valores_minimo.apply(pd.to_numeric, errors='coerce')

    # Expandir os limites máximos e mínimos
    valores_maximo_expanded = pd.DataFrame(
        valores_maximo.values.repeat(len(testes_valores), axis=0),
        columns=testes_valores.columns,
        index=testes_valores.index
    )
    valores_minimo_expanded = pd.DataFrame(
        valores_minimo.values.repeat(len(testes_valores), axis=0),
        columns=testes_valores.columns,
        index=testes_valores.index
    )

    # Identificar falhas
    falhas_detectadas = (testes_valores > valores_maximo_expanded) | (testes_valores < valores_minimo_expanded)

    # Gráfico de barras
    falhas_por_channel_testes = pd.DataFrame(index=coluna_channel.unique())
    for i, coluna in enumerate(testes_valores.columns):
        falhas = falhas_detectadas.iloc[:, i].groupby(coluna_channel).sum()
        falhas_por_channel_testes[f'Falhas {coluna}'] = falhas

    falhas_por_channel_testes = falhas_por_channel_testes.dropna()
    falhas_por_channel_total = falhas_por_channel_testes.sum(axis=1)
    falhas = falhas_por_channel_total.sort_values(ascending=False).head(16)
    falhas_data = falhas_por_channel_testes.loc[falhas.index]
    fig, ax = plt.subplots()
    falhas_data.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Channel')
    ax.set_ylabel('Quantidade de Falhas')
    plt.tight_layout()
    os.makedirs(output_path, exist_ok=True)
    plt.savefig(os.path.join(output_path, 'falhas_por_channel.png'))
    plt.show()
    plt.close()

