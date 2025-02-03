import tkinter as tk
from tkinter import filedialog
from processData import *
import config

def centralize_window(window):
    """Centraliza a janela na tela."""
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")


def show_home():
    """Exibe a janela inicial com as opções principais."""
    root = tk.Tk()
    root.title("Sistema de Teste - Home")

    # Botões para os modelos
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    tk.Label(frame, text="Selecione o módulo:", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

    tk.Button(frame, text="ATE", command=lambda: show_ate_interface(root), width=15).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, text="HiPot", command=lambda: show_hipot_interface(root), width=15).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(frame, text="Burn-in", command=lambda: show_burnin_interface(root), width=15).grid(row=1, column=2, padx=10, pady=10)

    # Centralizar janela
    centralize_window(root)

    root.mainloop()


def show_ate_interface(parent):
    """Exibe a interface do modelo ATE e fecha a janela principal."""
    parent.destroy()  # Fecha a janela inicial

    ate_window = tk.Tk()
    ate_window.title("ATE - Processador de CSV e Gerador de Gráficos")

    # Variáveis de Configuração
    config.csv_file_path = tk.StringVar()
    config.output_folder = tk.StringVar()
    config.apply_filter = tk.BooleanVar(value=False)
    config.start_hour = tk.StringVar(value="00")
    config.start_minute = tk.StringVar(value="00")
    config.start_second = tk.StringVar(value="00")
    config.end_hour = tk.StringVar(value="23")
    config.end_minute = tk.StringVar(value="00")
    config.end_second = tk.StringVar(value="00")
    config.selected_model = tk.StringVar(value=0)

    # Criar Frame Principal
    frame = tk.Frame(ate_window, padx=10, pady=10)
    frame.pack()

    # Seção de Arquivo
    tk.Label(frame, text="Selecione o arquivo CSV:").grid(row=0, column=0, sticky="w")
    tk.Entry(frame, textvariable=config.csv_file_path, width=40).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=lambda: config.csv_file_path.set(filedialog.askopenfilename())).grid(row=0, column=2)

    tk.Label(frame, text="Pasta de saída:").grid(row=1, column=0, sticky="w")
    tk.Entry(frame, textvariable=config.output_folder, width=40).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=lambda: config.output_folder.set(filedialog.askdirectory())).grid(row=1, column=2)

    # Checkbox
    tk.Checkbutton(frame, text="Aplicar filtro de horário", variable=config.apply_filter).grid(row=2, column=0, sticky="w")

    # Modelos
    radio_frame = tk.Frame(frame)
    radio_frame.grid(row=2, column=1, sticky="w", padx=10)
    tk.Radiobutton(radio_frame, text="Unicorn", variable=config.selected_model, value="Unicorn").pack(side="left")
    tk.Radiobutton(radio_frame, text="Napple", variable=config.selected_model, value="Napple").pack(side="left")

    # Intervalo de Tempo
    time_frame = tk.LabelFrame(frame, text="Intervalo de Tempo")
    time_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

    tk.Label(time_frame, text="Hora inicial:").grid(row=0, column=0, sticky="w")
    tk.Entry(time_frame, textvariable=config.start_hour, width=5).grid(row=0, column=1, padx=2)
    tk.Entry(time_frame, textvariable=config.start_minute, width=5).grid(row=0, column=2, padx=2)
    tk.Entry(time_frame, textvariable=config.start_second, width=5).grid(row=0, column=3, padx=2)

    tk.Label(time_frame, text="Hora final:").grid(row=1, column=0, sticky="w")
    tk.Entry(time_frame, textvariable=config.end_hour, width=5).grid(row=1, column=1, padx=2)
    tk.Entry(time_frame, textvariable=config.end_minute, width=5).grid(row=1, column=2, padx=2)
    tk.Entry(time_frame, textvariable=config.end_second, width=5).grid(row=1, column=3, padx=2)

    # Botão de Processar
    tk.Button(frame, text="Processar CSV", command=process_ATE).grid(row=4, column=0, columnspan=3, pady=10)

    # Botão Voltar
    tk.Button(frame, text="Voltar", command=lambda: return_to_home(ate_window)).grid(row=5, column=0, columnspan=3, pady=10)

    # Centralizar Janela
    centralize_window(ate_window)

    ate_window.mainloop()


def show_burnin_interface(parent):
    """Exibe a interface do modelo Dummy (HiPot ou Burn-in) e fecha a janela principal."""
    parent.destroy()  # Fecha a janela inicial

    burnin_window = tk.Tk()
    burnin_window.title("Burn-In - Processador de CSV e Gerador de Gráficos")

    # Variáveis de Configuração
    config.csv_file_path = tk.StringVar()
    config.output_folder = tk.StringVar()

    # Criar Frame Principal
    frame = tk.Frame(burnin_window, padx=10, pady=10)
    frame.pack()

    # Seção de Arquivo
    tk.Label(frame, text="Selecione o arquivo CSV:").grid(row=0, column=0, sticky="w")
    tk.Entry(frame, textvariable=config.csv_file_path, width=40).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=lambda: config.csv_file_path.set(filedialog.askopenfilename())).grid(row=0,
                                                                                                                 column=2)

    tk.Label(frame, text="Pasta de saída:").grid(row=1, column=0, sticky="w")
    tk.Entry(frame, textvariable=config.output_folder, width=40).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=lambda: config.output_folder.set(filedialog.askdirectory())).grid(row=1,
                                                                                                              column=2)
    # Botão de Processar
    tk.Button(frame, text="Processar CSV", command=process_BurnIn).grid(row=4, column=0, columnspan=3, pady=10)

    # Botão Voltar
    tk.Button(frame, text="Voltar", command=lambda: return_to_home(burnin_window)).grid(row=5, column=0, columnspan=3,
                                                                                     pady=10)

    # Centralizar Janela
    centralize_window(burnin_window)

    burnin_window.mainloop()

def show_hipot_interface(parent):
    """Exibe a interface do modelo Dummy (HiPot ou Burn-in) e fecha a janela principal."""
    parent.destroy()  # Fecha a janela inicial

    hipot_window = tk.Tk()
    hipot_window.title("Burn-In - Processador de CSV e Gerador de Gráficos")

    # Variáveis de Configuração
    config.csv_file_path = tk.StringVar()
    config.output_folder = tk.StringVar()

    # Criar Frame Principal
    frame = tk.Frame(hipot_window, padx=10, pady=10)
    frame.pack()

    # Seção de Arquivo
    tk.Label(frame, text="Selecione o arquivo CSV:").grid(row=0, column=0, sticky="w")
    tk.Entry(frame, textvariable=config.csv_file_path, width=40).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=lambda: config.csv_file_path.set(filedialog.askopenfilename())).grid(row=0,
                                                                                                                 column=2)

    tk.Label(frame, text="Pasta de saída:").grid(row=1, column=0, sticky="w")
    tk.Entry(frame, textvariable=config.output_folder, width=40).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=lambda: config.output_folder.set(filedialog.askdirectory())).grid(row=1,
                                                                                                              column=2)
    # Botão de Processar
    tk.Button(frame, text="Processar CSV", command=process_Hipot).grid(row=4, column=0, columnspan=3, pady=10)

    # Botão Voltar
    tk.Button(frame, text="Voltar", command=lambda: return_to_home(hipot_window)).grid(row=5, column=0, columnspan=3,
                                                                                     pady=10)

    # Centralizar Janela
    centralize_window(hipot_window)

    hipot_window.mainloop()

def return_to_home(current_window):
    """Fecha a janela atual e volta para a janela inicial."""
    current_window.destroy()
    show_home()


