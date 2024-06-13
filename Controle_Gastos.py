import tkinter
import customtkinter
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import os
import pandas as pd
from tkinter.filedialog import asksaveasfilename

def add_contato():
    banco = banco_combobox.get()
    valor = valor_entry.get()
    parcela = parcela_entry.get()
    vencimento = vencimento_calendar.get_date()

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "O valor deve ser um número válido.")
        return
    
    descricao = descricao_entry.get("1.0", tkinter.END).strip().replace('\n', '\\n')

    # Construir o texto do item da Listbox
    item_text = f"Banco: {banco} - Valor: R$ {valor:.2f} - Parcela: {parcela} - Vencimento: {vencimento} - Descrição: {descricao}"
    
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
        carrega_lista_tamanho()  # Adiciona esta linha para ajustar a largura após a exclusão
    else:
        messagebox.showinfo("Aviso", "Selecione uma linha para excluir.")
    carrega_lista_tamanho()

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
            # Substitui caracteres especiais por quebras de linha
            item_text = item_text.replace('\\n', '\n')
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
                contacts_listbox.insert(tkinter.END, line.strip())
    except FileNotFoundError:
        pass

def carrega_lista_tamanho():
    # Calcula o comprimento máximo das linhas
    max_line_length = max(len(item) for item in contacts_listbox.get(0, tkinter.END))
    
    # Define a largura da Listbox com base no comprimento máximo das linhas
    font_width = tkinter.font.Font().measure("A")
    contacts_listbox.config(width=max_line_length + int(max_line_length * font_width / 10))
valor_filtro_entry_date = None  # Definindo a variável globalmente

def consulta_lancamentos():
    global valor_filtro_entry_date  # Importante para modificar a variável global

    # Criar uma nova janela para a consulta
    consulta_window = tkinter.Toplevel(window)
    consulta_window.title("Consulta de Lançamentos")

    # Criar um frame para os campos de filtro
    filtro_frame = tkinter.Frame(consulta_window)
    filtro_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    filtro_label = tkinter.Label(filtro_frame, text="Filtrar por:")
    filtro_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    filtro_combobox = ttk.Combobox(filtro_frame, values=["Banco", "Data"])
    filtro_combobox.grid(row=0, column=1, padx=10, pady=5)

    valor_filtro_entry = ttk.Combobox(filtro_frame, values=bancos, state="readonly")
    valor_filtro_entry.grid(row=0, column=2, padx=10, pady=5)
    valor_filtro_entry.set(bancos[0])  # Definir o primeiro banco como valor padrão

    valor_filtro_entry_date = tkinter.Entry(filtro_frame)
    valor_filtro_entry_date.grid(row=0, column=2, padx=10, pady=5)
    valor_filtro_entry_date.insert(0, "dd/mm/aaaa")
    valor_filtro_entry_date.grid_remove()

    # Função para atualizar o campo de entrada de acordo com o filtro selecionado
    def atualizar_campo():
        if filtro_combobox.get() == "Data":
            valor_filtro_entry.grid_forget()
            valor_filtro_entry_date.grid()
        else:
            valor_filtro_entry_date.grid_forget()
            valor_filtro_entry.grid()

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

        contacts_resultados_listbox.delete(0, tkinter.END)

        # Adicionar os resultados à Listbox
        for resultado in resultados:
            contacts_resultados_listbox.insert(tkinter.END, resultado)            

    # Adicionar botão para buscar os lançamentos
    buscar_button = tkinter.Button(filtro_frame, text="Buscar", command=buscar_lancamentos)
    buscar_button.grid(row=0, column=3, padx=10, pady=5, sticky="e")

    # Criar uma Listbox para exibir os resultados da consulta
    contacts_resultados_listbox = tkinter.Listbox(consulta_window, bg="#262626", fg="white")
    contacts_resultados_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    consulta_window.grid_rowconfigure(1, weight=1)
    consulta_window.grid_columnconfigure(0, weight=1)

def mostrar_grafico():
    grafico_window = tkinter.Toplevel(window)
    grafico_window.title("Gráfico de Gastos")

    # Calcula o valor total cadastrado
    total_valor = 0
    gastos_por_banco = {banco: 0 for banco in bancos}
    vencimentos = []

    # Determina o início do dia atual
    inicio_do_dia_atual = datetime.combine(datetime.today(), datetime.min.time())

    for item in contacts_listbox.get(0, tkinter.END):
        parts = item.split(" - ")
        valor_part = next(part for part in parts if part.startswith("Valor:")).split(": ")[1]
        banco_part = next(part for part in parts if part.startswith("Banco:")).split(": ")[1]
        vencimento_part = next(part for part in parts if part.startswith("Vencimento:")).split(": ")[1]

        valor = float(valor_part.replace("R$", "").strip())
        total_valor += valor
        gastos_por_banco[banco_part] += valor

        vencimento_date = datetime.strptime(vencimento_part, "%d/%m/%Y")

        # Verifica se o vencimento é hoje ou em datas futuras
        if vencimento_date >= inicio_do_dia_atual:
            vencimentos.append((vencimento_date, item))

    vencimentos.sort(key=lambda x: x[0])

    # Retorna o banco com mais gastos
    banco_mais_gastos = max(gastos_por_banco, key=gastos_por_banco.get)
    total_banco_mais_gastos = gastos_por_banco[banco_mais_gastos]

    # mostra as informações na janela de gráfico
    ttk.Label(grafico_window, text=f"Valor Total Cadastrado: R$ {total_valor:.2f}").pack(pady=10)
    ttk.Label(grafico_window, text=f"Banco com Mais Gastos: {banco_mais_gastos} (R$ {total_banco_mais_gastos:.2f})").pack(pady=10)

    ttk.Label(grafico_window, text="Próximos Itens a Vencer:").pack(pady=10)

    # cria uma Listbox para exibir os próximos itens a vencer
    vencimentos_listbox = tkinter.Listbox(grafico_window, bg="#262626", fg="white")
    vencimentos_listbox.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

    for vencimento_date, item in vencimentos:
        vencimentos_listbox.insert(tkinter.END, item)

    # Ajustar a largura da Listbox de acordo com o tamanho máximo de linha dos itens
    max_line_length = max(len(item) for item in vencimentos_listbox.get(0, tkinter.END))
    vencimentos_listbox.config(width=max_line_length)


def gerar_relatorio():
    relatorio_window = tkinter.Toplevel(window)
    relatorio_window.title("Gerar Relatório")

    # Layout da nova janela
    relatorio_window.grid_columnconfigure(1, weight=1)
    relatorio_window.grid_rowconfigure(1, weight=1)

    filtro_label = tkinter.Label(relatorio_window, text="Filtrar por:")
    filtro_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    filtro_combobox = ttk.Combobox(relatorio_window, values=["Banco", "Data", "Todos"])
    filtro_combobox.grid(row=0, column=1, padx=10, pady=5)

    valor_filtro_entry = ttk.Combobox(relatorio_window, values=bancos, state="readonly")
    valor_filtro_entry.grid(row=0, column=2, padx=10, pady=5)
    valor_filtro_entry.set(bancos[0])

    valor_filtro_entry_date = tkinter.Entry(relatorio_window)
    valor_filtro_entry_date.grid(row=0, column=2, padx=10, pady=5)
    valor_filtro_entry_date.insert(0, "dd/mm/aaaa")
    valor_filtro_entry_date.grid_remove()

    def atualizar_campo():
        if filtro_combobox.get() == "Data":
            valor_filtro_entry.grid_remove()
            valor_filtro_entry_date.grid()
        elif filtro_combobox.get() == "Banco":
            valor_filtro_entry_date.grid_remove()
            valor_filtro_entry.grid()
        else:
            valor_filtro_entry_date.grid_remove()
            valor_filtro_entry.grid_remove()

    filtro_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_campo())

    def salvar_relatorio():
        filtro = filtro_combobox.get()
        if filtro == "Banco":
            valor_filtro = valor_filtro_entry.get()
            resultados = [item for item in contacts_listbox.get(0, tkinter.END) if f"Banco: {valor_filtro}" in item]
        elif filtro == "Data":
            valor_filtro = valor_filtro_entry_date.get()
            resultados = [item for item in contacts_listbox.get(0, tkinter.END) if f"Vencimento: {valor_filtro}" in item]
        else:
            resultados = contacts_listbox.get(0, tkinter.END)

        if not resultados:
            messagebox.showinfo("Sem resultados", "Nenhum resultado encontrado para o filtro selecionado.")
            return

        # Convertendo os resultados para um DataFrame do pandas
        data = []
        for resultado in resultados:
            parts = resultado.split(" - ")
            banco = parts[0].split(": ")[1]
            valor = parts[1].split(": ")[1]
            parcela = parts[2].split(": ")[1]
            vencimento = parts[3].split(": ")[1]
            descricao = parts[4].split(": ")[1]
            data.append([banco, valor, parcela, vencimento, descricao])

        df = pd.DataFrame(data, columns=["Banco", "Valor", "Parcela", "Vencimento", "Descrição"])

        # Pedir para o usuário salvar o arquivo
        file_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Relatório salvo", f"Relatório salvo com sucesso em: {file_path}")

    gerar_button = tkinter.Button(relatorio_window, text="Gerar Relatório", command=salvar_relatorio)
    gerar_button.grid(row=0, column=3, padx=10, pady=5, sticky="e")

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

bancos = ["Santander", "Nubank", "Itaú", "Caixa Econômica", "Bradesco", "Banco do Brasil"]

window = customtkinter.CTk()
window.title("Controle de Gastos")
window.geometry("800x600")
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(5, weight=1)

frame = customtkinter.CTkFrame(window, corner_radius=10)
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
frame.grid_rowconfigure(6, weight=1)

title_label = customtkinter.CTkLabel(frame, text="Cadastramento de Gastos", font=("Arial", 20))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

banco_label = customtkinter.CTkLabel(frame, text="Banco:")
banco_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
banco_combobox = customtkinter.CTkComboBox(frame, values=bancos)
banco_combobox.grid(row=1, column=1, padx=10, pady=5)
banco_combobox.set(bancos[0])

valor_label = customtkinter.CTkLabel(frame, text="Valor:")
valor_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
valor_entry = customtkinter.CTkEntry(frame)
valor_entry.grid(row=2, column=1, padx=10, pady=5)

parcela_label = customtkinter.CTkLabel(frame, text="Parcela:")
parcela_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
parcela_entry = customtkinter.CTkEntry(frame)
parcela_entry.grid(row=3, column=1, padx=10, pady=5)

vencimento_label = customtkinter.CTkLabel(frame, text="Vencimento:")
vencimento_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
vencimento_calendar = Calendar(frame, selectmode="day", date_pattern="dd/mm/yyyy")
abr_calendario_button = customtkinter.CTkButton(frame, text="Abrir Calendário", command=abr_calendario)
abr_calendario_button.grid(row=4, column=1, pady=5)
fch_calendario_button = customtkinter.CTkButton(frame, text="Fechar Calendário", command=fch_calendario)

descricao_label = customtkinter.CTkLabel(frame, text="Descrição:")
descricao_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
descricao_entry = customtkinter.CTkTextbox(frame, height=100)
descricao_entry.grid(row=5, column=1, padx=10, pady=5)

contacts_listbox = tkinter.Listbox(window, bg="#262626", fg="white")
contacts_listbox.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

add_button = customtkinter.CTkButton(frame, text="Adicionar", command=add_contato)
add_button.grid(row=6, column=1, padx=10, pady=10)

delete_button = customtkinter.CTkButton(frame, text="Excluir", command=deleta_contato)
delete_button.grid(row=7, column=1, padx=10, pady=10, sticky="s")

menubar = tkinter.Menu(window)
opcoes_menu = tkinter.Menu(menubar, tearoff=0)
opcoes_menu.add_command(label="Consultar", command=consulta_lancamentos)
opcoes_menu.add_command(label="Gráfico", command=mostrar_grafico)
opcoes_menu.add_command(label="Relatório", command=gerar_relatorio)
menubar.add_cascade(label="Opções", menu=opcoes_menu)
window.config(menu=menubar)

carrega_contatos()
carrega_lista_tamanho()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
