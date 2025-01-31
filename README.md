# BEZ - Gráfico de Falhas 


# Documentação do Software de Processamento de CSV e Geração de Gráficos

## Visão Geral

Este software foi desenvolvido para processar arquivos CSV e gerar gráficos com base nos dados de diferentes modelos de testes. Ele utiliza a biblioteca Tkinter para a interface gráfica, Pandas para manipulação de dados, e Matplotlib para visualização gráfica.

## Requisitos

* Python 3.x

## Bibliotecas necessárias:

* tkinter

* pandas

* matplotlib

* datetime

* os 

## Funcionalidades Principais

### Seleção de Arquivo CSV: 
O usuário pode selecionar um arquivo CSV contendo os dados.

### Escolha do Modelo de Teste: 
Três modelos diferentes são suportados (Unicorn, Napple, Roma). Cada modelo tem um conjunto específico de colunas a serem analisadas.

### Filtragem por Intervalo de Tempo: 
O usuário pode definir um intervalo de tempo para filtrar os dados.

### Geração de Gráficos: 
O software gera gráficos de barras e de linha para análise dos dados processados.

### Exportação de Resultados: 
Os gráficos são salvos na pasta especificada pelo usuário.

## Estrutura do Código

### 1. Processamento do Arquivo CSV

Esta função lê o arquivo CSV selecionado e executa a normalização dos dados, incluindo a renomeação 
de colunas conforme o modelo escolhido.

**O processamento é realizado pela função process_csv(), que:**
* Verifica se os arquivos necessários foram fornecidos.
* Carrega os dados conforme o modelo selecionado.
* Renomeia as colunas conforme as necessidades de cada modelo.
* Converte a coluna de tempo para o formato correto.
* Aplica filtros, caso solicitado pelo usuário.

```python
def process_ATE():
    try:
        # Verificar se o arquivo foi selecionado
        if not config.csv_file_path.get():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV.")
            return
        # Verificar se o caminho de destino foi fornecido
        if not config.output_folder.get():
            messagebox.showerror("Erro", "Por favor, insira um caminho de pasta destino.")
            return
        modelo = config.selected_model.get()
        if modelo == "Unicorn":
            # Ler o CSV
            data = pd.read_csv(config.csv_file_path.get(), header=2, usecols=range(0, 23))
            # Renomear colunas
            data.rename(columns={
                'Output voltage(V)': 'Static Test 9V-90V',
                'Output Ripple(mV)': 'Ripple Test 9V-90V',
                'Output voltage(V).1': 'Static Test 9V-264V',
                'Average efficiency(%)': 'Average Efficiency (%) 9V-230V',
                'Output voltage(V).2': 'Static Test 5V-90V',
                'Output Ripple(mV).1': 'Ripple Test 5V-90V',
                'Average efficiency(%).1': 'Average Efficiency (%) 5V-230V',
                'Standby power(W)': 'Standby Power 230V'
            }, inplace=True)
            # Seleciona as colunas dos testes
            colunas_selecionadas = ['Static Test 9V-90V',
                                    'Ripple Test 9V-90V',
                                    'Static Test 9V-264V',
                                    'Average Efficiency (%) 9V-230V',
                                    'Static Test 5V-90V',
                                    'Ripple Test 5V-90V',
                                    'Average Efficiency (%) 5V-230V',
                                    'Standby Power 230V']
            print(data.index)
        elif modelo == "Napple":
            data = pd.read_excel(config.csv_file_path.get(), header=3, usecols=range(0, 17))
            data.rename(columns={
                'Output voltage(V)': 'Static Test 5V-90V-0A',
                'Output voltage(V).1': 'Static Test 5V-90V-3A',
                'OCP current(A)': 'OCP(5v)',
                'Efficiency Specifications(%)': 'Average Efficiency(5V)',
                'Output voltage(V).2': 'Static Test(PD9V)',
                'OCP current(A).1': 'OCP(9v)',
                'Output Ripple(mV)': 'Ripple(PD9V)',
                'Output voltage(V).3': 'Static Test(PD9V)',
                'Efficiency Specifications(%).1': 'Average Efficiency(9V)',
                'Input power(W)': 'Standby Power 230V',
                'Output voltage(V).4': 'Static Test(PD9V)'
            }, inplace=True)
            colunas_selecionadas = ['Static Test 5V-90V-0A',
                                    'Static Test 5V-90V-3A',
                                    'OCP(5v)',
                                    'Average Efficiency(5V)',
                                    'Static Test(PD9V)',
                                    'OCP(9v)',
                                    'Ripple(PD9V)',
                                    'Static Test(PD9V)',
                                    'Average Efficiency(9V)',
                                    'Standby Power 230V',
                                    'Static Test(PD9V)']
```

### 2. Geração de Gráficos

Esta função processa os dados filtrados e gera gráficos para visualização de falhas.

**O gráfico realiza as determinadas funções:**
* Identifica falhas nos testes com base nos limites máximo e mínimo.
* Agrupa os dados por "Channel" e exibe a quantidade de falhas por teste.
* Salva o gráfico na pasta de destino.

```python
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
```

### 3. Interface Gráfica (Tkinter)

Cria uma interface gráfica para facilitar a seleção de arquivos e configurações de processamento.
 
**A interface gráfica possui:**
* Campos para seleção do arquivo CSV e da pasta de destino.
* Botães para navegação no sistema de arquivos.
* Opções de filtragem de dados por intervalo de tempo.
* Botão para iniciar o processamento do CSV.

```python
 root = tk.Tk()
 root.title("Processador de CSV e Gerador de Gráficos")

 frame = tk.Frame(root, padx=10, pady=10)
 frame.pack()

 file_label = tk.Label(frame, text="Selecione o arquivo CSV:")
 file_label.grid(row=0, column=0, sticky="w")

 file_entry = tk.Entry(frame, textvariable=csv_file_path, width=40)
 file_entry.grid(row=0, column=1, padx=5, pady=5)

 file_button = tk.Button(frame, text="Browse", command=lambda: csv_file_path.set(filedialog.askopenfilename()))
 file_button.grid(row=0, column=2)

 process_button = tk.Button(frame, text="Processar CSV", command=process_csv)
 process_button.grid(row=4, column=0, columnspan=3, pady=10)

 root.mainloop()
 ```