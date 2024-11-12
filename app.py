import tkinter as tk
from telas import TelaCadastroLoja, TelaCadastroProduto, TelaConsultaProduto

class SistemaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro")
        self.geometry("800x600")
        self.configure(bg="#000000")  # Cor de fundo preta

        # Configurar a grade para garantir que os frames ocupem o espaço da janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu principal
        menu = tk.Menu(self, bg="#003366", fg="white")
        self.config(menu=menu)

        cadastro_menu = tk.Menu(menu, bg="#003366", fg="white")
        menu.add_cascade(label="Cadastro", menu=cadastro_menu)
        cadastro_menu.add_command(label="Loja", command=self.exibir_cadastro_loja)
        cadastro_menu.add_command(label="Produto", command=self.exibir_cadastro_produto)
        
        menu.add_command(label="Consultar Produtos", command=self.exibir_consulta_produto)

        # Inicializando frames
        self.frames = {}
        self.criar_frames()

        # Mostra a tela de consulta como padrão
        self.exibir_frame("TelaConsultaProduto")

    def criar_frames(self):
        # Criar e armazenar os frames
        self.frames["TelaCadastroLoja"] = TelaCadastroLoja(self)
        self.frames["TelaCadastroProduto"] = TelaCadastroProduto(self)
        self.frames["TelaConsultaProduto"] = TelaConsultaProduto(self)

        for frame in self.frames.values():
            # Ajustar para os frames ficarem centralizados
            frame.grid(row=0, column=0, sticky="nsew")

    def exibir_frame(self, nome_frame):
        # Esconder todos os frames e mostrar apenas o selecionado
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[nome_frame].grid(row=0, column=0, sticky="nsew")

    def exibir_cadastro_loja(self):
        self.exibir_frame("TelaCadastroLoja")

    def exibir_cadastro_produto(self):
        self.exibir_frame("TelaCadastroProduto")

    def exibir_consulta_produto(self):
        self.exibir_frame("TelaConsultaProduto")

if __name__ == "__main__":
    app = SistemaApp()
    app.mainloop()
