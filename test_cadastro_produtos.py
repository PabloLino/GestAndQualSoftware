#Meu python estava dando problema para importação, tive que usar isso
import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')

import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_cadastro_produto import TelaCadastroProduto

nome_loja_para_teste = "Loja do lucas"

@pytest.fixture
def setup_tela():
    root = tk.Tk()
    tela = TelaCadastroProduto(master=root)
    return tela

@patch('principal.telas.tela_cadastro_produto.conectar_banco')  # Mockando a conexão com o banco de dados
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')  # Mockando a exibição de mensagens de erro
def test_nome_produto_nao_preenchidos(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    # Simulando o clique no botão de cadastro
    tela.nome.insert(0, "")  # Campo vazio
    tela.valor.insert(0, "100")
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.set(nome_loja_para_teste)
    tela.qtd_estoque.insert(0, "10")
    tela.categoria.insert(0, "Categoria Teste")

    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "O nome do produto é obrigatório.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_valor_produto_invalido(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.insert(0, "Produto Teste")
    tela.valor.insert(0, "abc")  # Valor inválido
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.set(nome_loja_para_teste)
    tela.qtd_estoque.insert(0, "10")
    tela.categoria.insert(0, "Categoria Teste")
    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "O valor do produto deve ser um número válido.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_loja_invalida(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.insert(0, "Produto Teste")
    tela.valor.insert(0, "200")  # Valor válido
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.set("Loja Errada")  # Loja inválida
    tela.qtd_estoque.insert(0, "10")
    tela.categoria.insert(0, "Categoria Teste")
    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "Selecione uma loja válida.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_quantidade_invalida(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.insert(0, "Produto Teste")
    tela.valor.insert(0, "200")
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.set(nome_loja_para_teste)
    tela.qtd_estoque.insert(0, "10.0")  # Quantidade inválida (não inteiro)
    tela.categoria.insert(0, "Categoria Teste")
    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "A quantidade de estoque deve ser um número inteiro.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showerror')
def test_categoria_invalida(mock_showerror, mock_conectar, setup_tela):
    tela = setup_tela

    tela.nome.insert(0, "Produto Teste")
    tela.valor.insert(0, "200")
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.set(nome_loja_para_teste)
    tela.qtd_estoque.insert(0, "10")
    tela.categoria.insert(0, "")  # Campo de categoria vazio
    tela.cadastrar_produto()

    # Verifica se a mensagem de erro é exibida
    mock_showerror.assert_called_with("Erro", "A categoria do produto é obrigatória.")

@patch('principal.telas.tela_cadastro_produto.conectar_banco')
@patch('principal.telas.tela_cadastro_produto.messagebox.showinfo')
def test_cadastro_correto(mock_showinfo, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.return_value = [(1, nome_loja_para_teste, '789562', 'PR', 'Geral')]

    tela = setup_tela

    tela.nome.insert(0, "Produto Teste")
    tela.valor.insert(0, "200")  # Valor válido
    tela.lojas_dict = {f"{nome_loja_para_teste}": {"id": 1}}
    tela.loja_combobox.set(nome_loja_para_teste)
    tela.qtd_estoque.insert(0, "10")
    tela.categoria.insert(0, "Categoria Teste")
    tela.cadastrar_produto()

    # Verifica se a mensagem de sucesso é exibida
    mock_showinfo.assert_called_with("Sucesso", "Produto cadastrado com sucesso!")
