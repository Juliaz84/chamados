import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def conectar_bd():
    conexao = sqlite3.connect("chamados.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            problema TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL,
            tecnico TEXT
        )
    """)
    conexao.commit()
    return conexao


def carregar_chamados():
    for item in tree.get_children():
        tree.delete(item)

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM chamados")
    registros = cursor.fetchall()

    for linha in registros:
        tree.insert("", tk.END, values=linha)


def adicionar_chamado():
    cliente = entry_cliente.get()
    problema = entry_problema.get()
    prioridade = combo_prioridade.get()
    status = combo_status.get()
    tecnico = entry_tecnico.get()

    if not cliente or not problema:
        messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
        return

    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO chamados (cliente, problema, prioridade, status, tecnico)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente, problema, prioridade, status, tecnico))
    conexao.commit()

    limpar_campos()
    carregar_chamados()
    messagebox.showinfo("Sucesso", "Chamado cadastrado com sucesso!")


def selecionar_item(event):
    item = tree.focus()
    if not item:
        return

    valores = tree.item(item)["values"]

    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(tk.END, valores[0])
    entry_id.config(state="readonly")

    entry_cliente.delete(0, tk.END)
    entry_cliente.insert(tk.END, valores[1])

    entry_problema.delete(0, tk.END)
    entry_problema.insert(tk.END, valores[2])

    combo_prioridade.set(valores[3])
    combo_status.set(valores[4])

    entry_tecnico.delete(0, tk.END)
    entry_tecnico.insert(tk.END, valores[5])


def atualizar_chamado():
    id_chamado = entry_id.get()
    if not id_chamado:
        messagebox.showwarning("Aviso", "Selecione um chamado para atualizar.")
        return

    cliente = entry_cliente.get()
    problema = entry_problema.get()
    prioridade = combo_prioridade.get()
    status = combo_status.get()
    tecnico = entry_tecnico.get()

    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE chamados SET cliente=?, problema=?, prioridade=?, status=?, tecnico=?
        WHERE id=?
    """, (cliente, problema, prioridade, status, tecnico, id_chamado))
    conexao.commit()

    carregar_chamados()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Chamado atualizado!")


def excluir_chamado():
    id_chamado = entry_id.get()
    if not id_chamado:
        messagebox.showwarning("Aviso", "Selecione um chamado para excluir.")
        return

    cursor = conexao.cursor()
    cursor.execute("DELETE FROM chamados WHERE id=?", (id_chamado,))
    conexao.commit()

    carregar_chamados()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Chamado excluído!")


def limpar_campos():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="readonly")

    entry_cliente.delete(0, tk.END)
    entry_problema.delete(0, tk.END)
    combo_prioridade.set("Baixa")
    combo_status.set("Aberto")
    entry_tecnico.delete(0, tk.END)

def resetar_ids():
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM chamados")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='chamados'")
    conexao.commit()
    carregar_chamados()
    messagebox.showinfo("Pronto", "IDs resetados e tabela limpa!")




conexao = conectar_bd()

root = tk.Tk()
root.title("Sistema de Chamados")
root.geometry("1000x650")
root.configure(bg="#F5F7FA")


style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#FFFFFF",
                foreground="#000000",
                rowheight=28,
                fieldbackground="#FFFFFF",
                bordercolor="#D9D9D9",
                borderwidth=1)

style.map("Treeview", background=[("selected","#396459")])

style.configure("Treeview.Heading",
                background="#396459",
                foreground="white",
                font=("Arial", 11, "bold"))


frame_form = tk.LabelFrame(root, text=" Cadastro de Chamados ", bg="#F5F7FA",
                           fg="#333", font=("Arial", 12, "bold"), padx=15, pady=15)
frame_form.pack(fill="x", padx=20, pady=10)

label_font = ("Arial", 11)


tk.Label(frame_form, text="ID:", bg="#F5F7FA", font=label_font).grid(row=0, column=0, sticky="w")
entry_id = tk.Entry(frame_form, width=10)
entry_id.grid(row=0, column=1, padx=10, pady=5)
entry_id.config(state="readonly")

tk.Label(frame_form, text="Cliente:", bg="#F5F7FA", font=label_font).grid(row=0, column=2, sticky="w")
entry_cliente = tk.Entry(frame_form, width=40)
entry_cliente.grid(row=0, column=3, padx=10, pady=5)


tk.Label(frame_form, text="Problema:", bg="#F5F7FA", font=label_font).grid(row=1, column=0, sticky="w")
entry_problema = tk.Entry(frame_form, width=40)
entry_problema.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="we")


tk.Label(frame_form, text="Prioridade:", bg="#F5F7FA", font=label_font).grid(row=2, column=0, sticky="w")
combo_prioridade = ttk.Combobox(frame_form, values=["Baixa", "Média", "Alta", "Crítica"], width=15)
combo_prioridade.set("Baixa")
combo_prioridade.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Status:", bg="#F5F7FA", font=label_font).grid(row=2, column=2, sticky="w")
combo_status = ttk.Combobox(frame_form, values=["Aberto", "Em andamento", "Aguardando", "Fechado"], width=20)
combo_status.set("Aberto")
combo_status.grid(row=2, column=3, padx=10, pady=5)


tk.Label(frame_form, text="Técnico:", bg="#F5F7FA", font=label_font).grid(row=3, column=0, sticky="w")
entry_tecnico = tk.Entry(frame_form, width=40)
entry_tecnico.grid(row=3, column=1, padx=10, pady=5)

#botoes
frame_buttons = tk.Frame(root, bg="#F5F7FA")
frame_buttons.pack(pady=10)

botao_estilo = {
    "font": ("Arial", 11, "bold"),
    "width": 12,
    "height": 1,
    "bd": 0,
    "fg": "white",
    "padx": 5,
    "pady": 5,
}

btn_add = tk.Button(frame_buttons, text="Adicionar", bg="#40BD9D",
                    command=adicionar_chamado, **botao_estilo)
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(frame_buttons, text="Atualizar", bg="#14795F",
                       command=atualizar_chamado, **botao_estilo)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(frame_buttons, text="Excluir", bg="#8F1508",
                       command=excluir_chamado, **botao_estilo)
btn_delete.grid(row=0, column=2, padx=10)

btn_clear = tk.Button(frame_buttons, text="Limpar", bg="#7F8C8D",
                      command=limpar_campos, **botao_estilo)
btn_clear.grid(row=0, column=3, padx=10)

btn_reset = tk.Button(frame_buttons, text="Resetar IDs", bg="#8E44AD",
                      command=resetar_ids, **botao_estilo)
btn_reset.grid(row=0, column=4, padx=10)


#tabela
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame,
                    columns=("ID", "Cliente", "Problema", "Prioridade", "Status", "Tecnico"),
                    show="headings",
                    yscrollcommand=tree_scroll.set)
tree.pack(fill="both", expand=True)

tree_scroll.config(command=tree.yview)

colunas = ["ID", "Cliente", "Problema", "Prioridade", "Status", "Tecnico"]
titulos = ["ID", "Cliente", "Problema", "Prioridade", "Status", "Tecnico"]

for i, col in enumerate(colunas):
    tree.heading(col, text=titulos[i])
    tree.column(col, width=120)

tree.bind("<ButtonRelease-1>", selecionar_item)

carregar_chamados()

root.mainloop()