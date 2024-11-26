import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_banco

class TelaConsultaProduto(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#000000")  # Cor de fundo preta

        # Título
        self.title_label = tk.Label(self, text="Consulta de Produtos", font=("Helvetica", 16, "bold"), fg="#003366", bg="white")
        self.title_label.pack(pady=20)

        # Configurando o estilo da tabela
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Helvetica", 10),
                        rowheight=25)
        style.configure("Treeview.Heading",
                        font=("Helvetica", 12, "bold"),
                        foreground="black", background="#003366")
        style.configure("Treeview.Cell", padding=5)

        # Treeview para exibição dos produtos
        self.tree = ttk.Treeview(self, columns=("ID", "Produto", "Loja", "Valor"), show='headings', height=10)
        self.tree.heading("ID", text="ID Produto", anchor="w")
        self.tree.heading("Produto", text="Produto", anchor="w")
        self.tree.heading("Loja", text="Loja Disponível", anchor="w")
        self.tree.heading("Valor", text="Valor Produto", anchor="w")

        # Definindo largura das colunas
        self.tree.column("ID", width=80, anchor="w")
        self.tree.column("Produto", width=200, anchor="w")
        self.tree.column("Loja", width=150, anchor="w")
        self.tree.column("Valor", width=120, anchor="e")

        # Adiciona a tabela na tela
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Barra de rolagem para a tabela
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.carregar_produtos()

    def carregar_produtos(self):
    # Limpando os dados antigos na tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

    # Carregando os produtos do banco de dados
        with conectar_banco() as conn:
            cursor = conn.cursor()
            query = """ 
                SELECT Produtos.ID_PRODUTO, Produtos.NOME_PRODUTO, Lojas.NOME_LOJA, Produtos.PRECO
                FROM Produtos
                LEFT JOIN Lojas ON Produtos.LOJA_DISPONIVEL = Lojas.ID_LOJA
            """
            for produto in cursor.execute(query):
                # Extrair cada valor individualmente da tupla retornada pelo cursor
                id_produto = produto[0]
                nome_produto = produto[1]
                nome_loja = produto[2]
                preco_produto = produto[3]

            # Insere os dados corretamente na tabela sem parênteses ou aspas extras
                self.tree.insert("", "end", values=(id_produto, nome_produto, nome_loja, preco_produto))
