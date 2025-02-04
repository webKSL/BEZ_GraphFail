# **BEZ - GraphFail**

## **Introdução**

BEZ - GraphFail é um software desenvolvido para análise de testes de estresse e envelhecimento em cabeças de carregador. O programa processa os logs gerados pela máquina de testes e exibe gráficos para facilitar a interpretação dos resultados. A interface inicial apresenta um menu onde o operador pode selecionar entre três testes distintos, cada um com sua própria lógica de funcionamento.

## **Tecnologias Utilizadas**

### O projeto utiliza as seguintes bibliotecas do Python:

- **Tkinter**: Interface gráfica para a seleção de testes e parâmetros.
- **Pandas**: Manipulação e processamento dos logs de teste.
- **Matplotlib**: Geração de gráficos para visualização dos resultados.
- **Datetime**: Gerenciamento de datas e horários para filtragem de dados.
- **OS**: Interação com arquivos do sistema para carregamento dos logs.

## **Estrutura e Funcionalidades**

### **Menu Inicial**

Ao iniciar o programa, o operador acessa um menu onde pode escolher entre três testes de estresse e envelhecimento:

1. **Teste ATE**
    - Garante que dispositivos eletrônicos funcionem corretamente e sejam seguros.
    - Possui componentes de medição, estímulo e comutação controlados por computador.
    - Testa dispositivos em diferentes níveis, fornecendo dados para análise da funcionalidade.
    - No software, é possível selecionar entre três modelos de carregador e aplicar um filtro de horário.
2. **Teste Hipot**
    - Também conhecido como teste de resistência dielétrica, avalia a integridade do isolamento elétrico do dispositivo.
    - Submete o equipamento a alta tensão para verificar se o isolamento suporta a tensão especificada sem falhas.
    - Utilizado em uma ampla variedade de dispositivos, desde equipamentos de baixa tensão até alta tensão.
    - No software, os logs desse teste são carregados e analisados automaticamente.
3. **Teste Burn-In**
    - Descobre defeitos iniciais aplicando cargas de temperatura e voltagem a semicondutores.
    - Utiliza placas de burn-in para segurar os semicondutores durante o teste.
    - Exposição prolongada a condições extremas para identificar falhas precoces.
    - No software, os logs do teste são lidos e os dados são apresentados em gráficos para análise.

## **Geração de Gráficos**

O programa permite visualizar os dados através de diferentes tipos de gráficos:

- **Gráficos de Barras** para comparação entre diferentes testes.
- **Histogramas** para análise da distribuição dos dados.

## **Estrutura do Projeto**
```
BEZ_GraphFail/

│── config.py # Configurações do programa

│── main.py # Ponto de entrada da aplicação

│── plottingGraph.py # Geração de gráficos a partir dos logs

│── processData.py # Processamento e análise dos logs de teste

│── ui.py # Interface gráfica e menu de seleção de testes
```
## **Instalação e Execução**

1. **Instale o Python 3.x**

```- Certifique-se de que o Python está instalado no seu sistema.```
2. **Instale as bibliotecas necessárias**

```pip install pandas matplotlib tkinter```

3. **Execute a aplicação**

```python main.py```

## **Como Usar**

1. Abra a aplicação e selecione um dos testes disponíveis no menu inicial.
2. No caso do Teste ATE, selecione o modelo de carregador e, se necessário, aplique o filtro de horário.
3. Aguarde o processamento dos logs.
4. Visualize os gráficos gerados para análise.
5. Caso necessário, exporte os gráficos para documentação.