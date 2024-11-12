from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_banco

class TelaCadastroLoja(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#000000")  # Cor de fundo preta

        tk.Label(self, text="Cadastro de Loja", font=("Helvetica", 16, "bold"), fg="#003366", bg="white").grid(row=0, columnspan=2, pady=20)
        self.grid(row=0, column=0, sticky="nsew")

        tk.Label(self, text="Nome da Loja", fg="white", bg="#000000").grid(row=1, column=0, pady=5)
        tk.Label(self, text="CNPJ da Loja", fg="white", bg="#000000").grid(row=2, column=0, pady=5)
        tk.Label(self, text="UF da Loja", fg="white", bg="#000000").grid(row=3, column=0, pady=5)
        tk.Label(self, text="Tipo de Loja", fg="white", bg="#000000").grid(row=4, column=0, pady=5)

        self.nome_loja = tk.Entry(self)
        self.cnpj_loja = tk.Entry(self)
        self.uf_loja = tk.Entry(self)
        self.tipo_loja = tk.Entry(self)

        self.nome_loja.grid(row=1, column=1)
        self.cnpj_loja.grid(row=2, column=1)
        self.uf_loja.grid(row=3, column=1)
        self.tipo_loja.grid(row=4, column=1)

        tk.Button(self, text="Cadastrar", command=self.cadastrar_loja, bg="#003366", fg="white").grid(row=5, columnspan=2, pady=20)

    def cadastrar_loja(self):
        with conectar_banco() as conn:
            cursor = conn.cursor()

            nome_loja = self.nome_loja.get()
            cnpj_loja = self.cnpj_loja.get()
            uf_loja = self.uf_loja.get()
            tipo_loja = self.tipo_loja.get()

            # Verificar se todos os campos foram preenchidos
            if not nome_loja or not cnpj_loja or not uf_loja or not tipo_loja:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return

            # Verificar se o CNPJ já existe
            cursor.execute("SELECT COUNT(*) FROM Lojas WHERE NU_CNPJ = ?", (cnpj_loja,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Erro", "Já existe uma loja com esse CNPJ.")
                return

            # Inserir dados da loja
            cursor.execute("""
            INSERT INTO Lojas (NOME_LOJA, NU_CNPJ, UF, TIPO_LOJA)
            VALUES (?, ?, ?, ?)""", (nome_loja, cnpj_loja, uf_loja, tipo_loja))

            conn.commit()
            messagebox.showinfo("Sucesso", "Loja cadastrada com sucesso!")


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
            if loja_id is None:
                messagebox.showerror("Erro", "Selecione uma loja válida.")
                return

            # Pegue os dados do produto a partir dos campos de entrada
            nome_produto = self.nome.get()
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
