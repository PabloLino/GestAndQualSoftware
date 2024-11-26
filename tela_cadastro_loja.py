import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva/principal')


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
            result = cursor.fetchone()
            if result[0] > 0:
                messagebox.showerror("Erro", "Já existe uma loja com esse CNPJ.")
                return

            # Inserir dados da loja
            cursor.execute("""
            INSERT INTO Lojas (NOME_LOJA, NU_CNPJ, UF, TIPO_LOJA)
            VALUES (?, ?, ?, ?)""", (nome_loja, cnpj_loja, uf_loja, tipo_loja))

            conn.commit()
            messagebox.showinfo("Sucesso", "Loja cadastrada com sucesso!")
