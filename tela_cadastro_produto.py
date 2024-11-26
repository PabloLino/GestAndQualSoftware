import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva/principal')


from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_banco

class TelaCadastroProduto(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#000000")  # Cor de fundo preta

        tk.Label(self, text="Cadastro de Produto", font=("Helvetica", 16, "bold"), fg="#003366", bg="white").grid(row=0, columnspan=2, pady=20)

        tk.Label(self, text="Nome do Produto", fg="white", bg="#000000").grid(row=1, column=0, pady=5)
        tk.Label(self, text="Loja Disponível", fg="white", bg="#000000").grid(row=2, column=0, pady=5)
        tk.Label(self, text="Valor do Produto", fg="white", bg="#000000").grid(row=3, column=0, pady=5)
        tk.Label(self, text="Quantidade em Estoque", fg="white", bg="#000000").grid(row=4, column=0, pady=5)
        tk.Label(self, text="Categoria do Produto", fg="white", bg="#000000").grid(row=5, column=0, pady=5)

        self.nome = tk.Entry(self)
        self.valor = tk.Entry(self)
        self.qtd_estoque = tk.Entry(self)
        self.categoria = tk.Entry(self)

        self.loja_combobox = ttk.Combobox(self)
        self.carregar_lojas()

        self.nome.grid(row=1, column=1)
        self.loja_combobox.grid(row=2, column=1)
        self.valor.grid(row=3, column=1)
        self.qtd_estoque.grid(row=4, column=1)
        self.categoria.grid(row=5, column=1)

        tk.Button(self, text="Cadastrar", command=self.cadastrar_produto, bg="#003366", fg="white").grid(row=6, columnspan=2, pady=20)

    def carregar_lojas(self):
        with conectar_banco() as conn:
            cursor = conn.cursor()
            lojas = cursor.execute("SELECT ID_LOJA, NOME_LOJA, NU_CNPJ, UF, TIPO_LOJA FROM Lojas").fetchall()
            self.lojas_dict = {f"{loja[1]}": loja[0] for loja in lojas}
            self.loja_combobox['values'] = list(self.lojas_dict.keys())

    def cadastrar_produto(self):
        with conectar_banco() as conn:
            cursor = conn.cursor()

            # Acesse o ID da loja selecionada
            loja_nome = self.loja_combobox.get()  # Nome da loja selecionada no Combobox

            # Mapeamento entre o nome da loja e o ID da loja
            loja_id = self.lojas_dict.get(loja_nome)  # Obtém o ID_LOJA correspondente ao nome

            # Verifique se a loja foi encontrada
            if not loja_id:
                messagebox.showerror("Erro", "Selecione uma loja válida.")
                return

            # Pegue os dados do produto a partir dos campos de entrada
            nome_produto = self.nome.get()
            if nome_produto is None or nome_produto == "":
                messagebox.showerror("Erro", "O nome do produto é obrigatório.")
                return
            try:
                preco_produto = float(self.valor.get())  # Converte o valor do produto para float
            except ValueError:
                messagebox.showerror("Erro", "O valor do produto deve ser um número válido.")
                return
            try:
                qtd_estoque = int(self.qtd_estoque.get())  # Certifique-se de que a quantidade é um número inteiro
            except ValueError:
                messagebox.showerror("Erro", "A quantidade de estoque deve ser um número inteiro.")
                return

            categoria_produto = self.categoria.get()  # Obtém o valor da categoria
            if not categoria_produto:
                messagebox.showerror("Erro", "A categoria do produto é obrigatória.")
                return

            data_cadastro = datetime.today().strftime('%Y-%m-%d')  # Formato de data 'yyyy-mm-dd'

            # Insira o produto na tabela
            cursor.execute("""
            INSERT INTO Produtos (NOME_PRODUTO, PRECO, QTD_ESTOQUE, DATA_CADASTRO, LOJA_DISPONIVEL, ID_LOJA, CATEGORIA) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome_produto, preco_produto, qtd_estoque, data_cadastro, loja_id, loja_id, categoria_produto))

            conn.commit()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
