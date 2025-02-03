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
    os.makedirs(config.output_path, exist_ok=True)
    plt.savefig(os.path.join(output_path, 'falhas_por_channel.png'))
    plt.show()
    plt.close()

def plotbarBurnIn(data):

    # Exemplo de falhas por carrinho e posição
    fail_by_cart = data[data["Result"] == "FAIL"]["Número do Carrinho"].value_counts().sort_index()
    fail_by_position = data[data["Result"] == "FAIL"]["Posição do Carrinho"].value_counts().sort_index()
    # Filtrando os dados de falhas, com relação a "Número do Carrinho" e "Posição do Carrinho"
    fail_by_cart_position = data[data["Result"] == "FAIL"].groupby(
        ["Número do Carrinho", "Posição do Carrinho"]).size().unstack(fill_value=0)

    # Criar os primeiros dois gráficos
    fig, axes = plt.subplots(1, 2)

    # Gráfico 1: Número do Carrinho x Contagem de FAIL
    axes[0].bar(fail_by_cart.index.astype(str), fail_by_cart.values, color="red")  # Convertendo o índice para string
    axes[0].set_title("Falhas por Número do Carrinho")
    axes[0].set_xlabel("Número do Carrinho")
    axes[0].set_ylabel("Ocorrências de FAIL")
    axes[0].tick_params(axis='x', rotation=45)

    # Gráfico 2: Posição do Carrinho x Contagem de FAIL
    axes[1].bar(fail_by_position.index.astype(str), fail_by_position.values,
                color="blue")  # Convertendo o índice para string
    axes[1].set_title("Falhas por Posição do Carrinho")
    axes[1].set_xlabel("Posição do Carrinho")
    axes[1].set_ylabel("Ocorrências de FAIL")
    axes[1].tick_params(axis='x', rotation=45)

    # Ajustar layout para evitar sobreposição
    plt.tight_layout()
    plt.show()
    plt.close()

    # Criar o terceiro gráfico em uma nova janela
    fig, ax = plt.subplots()
    fail_by_cart_position.plot(kind='bar', stacked=True, ax=ax, cmap='tab20')  # Gráfico empilhado
    ax.set_title("Falhas por Número do Carrinho e Posição")
    ax.set_xlabel("Número do Carrinho")
    ax.set_ylabel("Ocorrências de FAIL")
    ax.tick_params(axis='x', rotation=45)

    # Ajustar layout para o gráfico 3
    plt.tight_layout()
    plt.show()
    plt.close()