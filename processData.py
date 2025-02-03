from tkinter import messagebox
import pandas as pd
from datetime import time
from plottingGraph import plotbarATE, plotbarBurnIn
import config

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
        else:
            messagebox.showerror("Erro", "Nenhum modelo foi selecionado.")
            return
        # Converter a coluna 'Test Time' para datetime
        if 'Test Time' not in data.columns:
            messagebox.showerror("Erro", "A coluna 'Test Time' não foi encontrada no arquivo.")
            return
        data['Test Time'] = pd.to_datetime(data['Test Time'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        # Aplicar filtro de horário, se necessário
        if config.apply_filter.get():
            start_time = time(hour=int(config.start_hour.get()), minute=int(config.start_minute.get()),
                              second=int(config.start_second.get()))
            end_time = time(hour=int(config.end_hour.get()),
                            minute=int(config.end_minute.get()),
                            second=int(config.end_second.get()))
            data['Time'] = data['Test Time'].dt.time
            filtered_data = data[(data['Time'] >= start_time) & (data['Time'] <= end_time)]
            if filtered_data.empty:
                messagebox.showinfo("Informação", "Nenhum dado encontrado no intervalo de tempo selecionado.")
                return
        else:
            filtered_data = data
        # Processar os dados e gerar gráficos
        plotbarATE(filtered_data, data, config.output_folder.get(), colunas_selecionadas)
        messagebox.showinfo("Sucesso", "Gráficos gerados e salvos na pasta destino.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def process_BurnIn():
    try:
        # Verificar se o arquivo foi selecionado
        if not config.csv_file_path.get():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV.")
            return
        # Verificar se o caminho de destino foi fornecido
        if not config.output_folder.get():
            messagebox.showerror("Erro", "Por favor, insira um caminho de pasta destino.")
            return
        data = pd.read_csv(config.csv_file_path.get())
        data.rename(columns={
            'ID': 'Número do Carrinho',
            'Slot': 'Posição do Carrinho'
        }, inplace=True)
        colunas_selecionadas = ['Número do Carrinho','Posição do Carrinho', 'Result']
        # Processar os dados e gerar gráficos
        plotbarBurnIn(data)
        messagebox.showinfo("Sucesso", "Gráficos gerados e salvos na pasta destino.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


