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


### 2. Geração de Gráficos

Esta função processa os dados filtrados e gera gráficos para visualização de falhas.

**O gráfico realiza as determinadas funções:**
* Identifica falhas nos testes com base nos limites máximo e mínimo.
* Agrupa os dados por "Channel" e exibe a quantidade de falhas por teste.
* Salva o gráfico na pasta de destino.

### 3. Interface Gráfica (Tkinter)

Cria uma interface gráfica para facilitar a seleção de arquivos e configurações de processamento.
 
**A interface gráfica possui:**
* Campos para seleção do arquivo CSV e da pasta de destino.
* Botães para navegação no sistema de arquivos.
* Opções de filtragem de dados por intervalo de tempo.
* Botão para iniciar o processamento do CSV.
