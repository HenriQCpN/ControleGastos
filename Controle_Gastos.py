import tkinter
import customtkinter
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import os

def add_contato():
    banco = banco_combobox.get()
    valor = valor_entry.get()
    parcela = parcela_entry.get()
    descricao = descricao_entry.get()
    
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "O valor deve ser um número válido.")
        return
    
    vencimento = vencimento_calendar.get_date()

    # Se houver quebras de linha na descrição, dividir em várias linhas
    descricao_lines = descricao.split('\n')
    
    # Construir o texto do item da Listbox
    item_text = f"Banco: {banco} - Valor: R$ {valor:.2f} - Parcela: {parcela} - Vencimento: {vencimento} - Descrição:"
    for line in descricao_lines:
        item_text += f"\n  {line}"
    
    # Inserir o item na Listbox
    contacts_listbox.insert(tkinter.END, item_text)

    # Atualizar a largura da Listbox
    carrega_lista_tamanho()
    salva_contato()

def deleta_contato():
    selected_index = contacts_listbox.curselection()
    if selected_index:  # Verifica se uma linha está selecionada
        contacts_listbox.delete(selected_index)
        salva_contato()  
    else:
        messagebox.showinfo("Aviso", "Selecione uma linha para excluir.")
    carrega_lista_tamanho()

def carrega_lista_tamanho():
    if contacts_listbox.size() > 0:
        max_width = max(len(item) for item in contacts_listbox.get(0, tkinter.END))
    else:
        max_width = 60  # Largura padrão se a Listbox estiver vazia
    contacts_listbox.config(width=max_width)

def abr_calendario():
    vencimento_calendar.selection_set(datetime.today())
    abr_calendario_button.grid_remove()
    fch_calendario_button.grid(row=2, column=1, pady=5)
    vencimento_calendar.grid(row=3, column=1, padx=7, pady=10)

def fch_calendario():
    vencimento_calendar.grid_remove()
    fch_calendario_button.grid_remove()
    abr_calendario_button.grid()

def salva_contato():
    desktop_path = get_desktop_path()
    file_path = os.path.join(desktop_path, 'contacts.txt')
    with open(file_path, "w") as file:
        for index in range(contacts_listbox.size()):
            item_text = contacts_listbox.get(index)
            print("Item a ser gravado:", item_text)  # Adiciona essa linha para ver o que está sendo gravado
            file.write(item_text + '\n')

    print("Contatos salvos com sucesso!")

def get_desktop_path():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'TrabalhoFacul')
    os.makedirs(desktop_path, exist_ok=True)  # Cria o diretório se não existir
    return desktop_path

def on_closing():
    salva_contato()
    window.destroy()

def carrega_contatos():
    desktop_path = get_desktop_path()
    file_path = os.path.join(desktop_path, 'contacts.txt')
    try:
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                
                # Verificar se a linha possui pelo menos cinco partes
                if len(parts) >= 5:
                    banco, valor, parcela, vencimento, descricao = parts[:5]
                    contacts_listbox.insert(tkinter.END, f"{banco} - Valor: R$ {valor} - Parcela: {parcela} - Vencimento: {vencimento} - Descrição: {descricao}")
                else:
                    print("Aviso: Uma linha no arquivo de contatos está incompleta:", parts)
    except FileNotFoundError:
        pass

valor_filtro_entry_date = None  # Definindo a variável globalmente

def consulta_lancamentos():
    global valor_filtro_entry_date  # Importante para modificar a variável global

    # Criar uma nova janela para a consulta
    consulta_window = tkinter.Toplevel(window)
    consulta_window.title("Consulta de Lançamentos")

    # Configurar o peso das linhas e colunas para o layout responsivo
    consulta_window.grid_columnconfigure(1, weight=1)
    consulta_window.grid_rowconfigure(1, weight=1)

    # Criar e posicionar os widgets para seleção do filtro
    filtro_label = tkinter.Label(consulta_window, text="Filtrar por:")
    filtro_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    filtro_combobox = ttk.Combobox(consulta_window, values=["Banco", "Data"])
    filtro_combobox.grid(row=0, column=1, padx=10, pady=5)

    valor_filtro_entry = ttk.Combobox(consulta_window, values=bancos, state="readonly")
    valor_filtro_entry.grid(row=0, column=2, padx=10, pady=5)
    valor_filtro_entry.set(bancos[0])  # Definir o primeiro banco como valor padrão

    # Função para atualizar o campo de entrada de acordo com o filtro selecionado
    def atualizar_campo():
        global valor_filtro_entry_date  # Importante para modificar a variável global
        if filtro_combobox.get() == "Data":
            # Remover o combobox de bancos
            valor_filtro_entry.grid_forget()
            # Adicionar campo de entrada para a data
            valor_filtro_entry_date = tkinter.Entry(consulta_window)
            valor_filtro_entry_date.grid(row=0, column=2, padx=10, pady=5)
            valor_filtro_entry_date.insert(0, "dd/mm/aaaa")  # Texto padrão
        else:
            # Remover o campo de entrada de data
            valor_filtro_entry_date.grid_forget()
            # Adicionar o combobox de bancos
            valor_filtro_entry.grid(row=0, column=2, padx=10, pady=5)

    # Chamar a função para atualizar o campo sempre que o filtro for alterado
    filtro_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_campo())

    # Definir função para buscar os lançamentos de acordo com o filtro selecionado
    def buscar_lancamentos():
        filtro = filtro_combobox.get()

        if filtro == "Banco":
            valor_filtro = valor_filtro_entry.get()
            # Buscar os lançamentos pelo banco selecionado
            resultados = [item for item in contacts_listbox.get(0, tkinter.END) if f"Banco: {valor_filtro}" in item]
        elif filtro == "Data":
            valor_filtro = valor_filtro_entry_date.get()
            # Buscar os lançamentos pela data inserida
            resultados = [item for item in contacts_listbox.get(0, tkinter.END) if f"Vencimento: {valor_filtro}" in item]
        else:
            messagebox.showerror("Erro", "Selecione um filtro válido.")
            return

        # Limpar a Listbox de resultados antes de exibir os novos resultados
        contacts_resultados_listbox.delete(0, tkinter.END)

        # Adicionar os resultados à Listbox
        for resultado in resultados:
            contacts_resultados_listbox.insert(tkinter.END, resultado)

    # Adicionar botão para buscar os lançamentos
    buscar_button = tkinter.Button(consulta_window, text="Buscar", command=buscar_lancamentos)
    buscar_button.grid(row=0, column=3, padx=10, pady=5, sticky="e")

    # Criar uma Listbox para exibir os resultados da consulta
    contacts_resultados_listbox = tkinter.Listbox(consulta_window, bg="#262626", fg="white")
    contacts_resultados_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

    # Configurar o peso da Listbox para expandir conforme necessário
    consulta_window.grid_rowconfigure(1, weight=1)
    consulta_window.grid_columnconfigure(0, weight=1)


window = tkinter.Tk()
window.configure(bg='#262626')
window.title("Contact List")
window.protocol("WM_deleta_janela", on_closing)

frame = tkinter.Frame(window, background='#262626')
frame.pack()

banco_label = customtkinter.CTkLabel(
    master=frame,
    text="Banco:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8)
banco_label.grid(row=0, column=0, padx=7, pady=10)

valor_label = customtkinter.CTkLabel(
    master=frame,
    text="Valor:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8)
valor_label.grid(row=1, column=0)

parcela_label = customtkinter.CTkLabel(
    master=frame,
    text="Parcela:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8)
parcela_label.grid(row=2, column=0)

vencimento_label = customtkinter.CTkLabel(
    master=frame,
    text="Vencimento:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8)
vencimento_label.grid(row=3, column=0)

descricao_label = customtkinter.CTkLabel(
    master=frame,
    text="Descrição:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8)
descricao_label.grid(row=4, column=0)

bancos = ["Nubank", "Itaú", "Santander", "C6", "Caixa"]

banco_combobox = ttk.Combobox(frame, values=bancos, state="readonly")
banco_combobox.grid(row=0, column=1, padx=7, pady=10)

valor_entry = customtkinter.CTkEntry(
    master=frame,
    text_color="white",
    border_width=2,
    border_color="#d3d3d3",
    bg_color="#262626",
    fg_color="#262626",
    corner_radius=5)
valor_entry.grid(row=1, column=1, padx=7, pady=10)

parcela_entry = customtkinter.CTkEntry(
    master=frame,
    text_color="white",
    border_width=2,
    border_color="#d3d3d3",
    bg_color="#262626",
    fg_color="#262626",
    corner_radius=5)
parcela_entry.grid(row=2, column=1, padx=7, pady=10)

vencimento_calendar = Calendar(frame, selectmode="day", date_pattern="dd/mm/yyyy")

descricao_entry = customtkinter.CTkEntry(
    master=frame,
    text_color="white",
    border_width=2,
    border_color="#d3d3d3",
    bg_color="#262626",
    fg_color="#262626",
    corner_radius=5)
descricao_entry.grid(row=4, column=1, padx=7, pady=10)

abr_calendario_button = customtkinter.CTkButton(
    master=frame,
    command=abr_calendario,
    text="Selecionar Data",
    text_color="white",
    hover=True,
    hover_color="Blue",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
abr_calendario_button.grid(row=3, column=1, pady=15)

fch_calendario_button = tkinter.Button(
    master=frame,
    text="X",
    command=fch_calendario,
    bg="#262626",
    fg="white",
    relief="flat",
    font=("Arial", 10, "bold"),
)
fch_calendario_button.grid(row=3, column=1, pady=5, sticky=tkinter.E)
fch_calendario_button.grid_remove()

contacts_listbox = tkinter.Listbox(window, bg="#262626", fg="white", width=60, height=10)
contacts_listbox.pack()

add_button = customtkinter.CTkButton(
    master=frame,
    command=add_contato,
    text="Adicionar",
    text_color="white",
    hover=True,
    hover_color="green",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
add_button.grid(row=5, column=0, padx=5, pady=15)

delete_button = customtkinter.CTkButton(
    master=frame,
    command=deleta_contato,
    text="Excluir",
    text_color="white",
    hover=True,
    hover_color="red",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
delete_button.grid(row=5, column=1, padx=5, pady=15)

consulta_button = customtkinter.CTkButton(
    master=frame,
    command=consulta_lancamentos,
    text="Consulta",
    text_color="white",
    hover=True,
    hover_color="blue",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
consulta_button.grid(row=5, column=2, padx=5, pady=15)

carrega_contatos()
carrega_lista_tamanho()

window.mainloop()
