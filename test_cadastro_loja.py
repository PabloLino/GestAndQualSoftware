#Meu python estava dando problema para importação, tive que usar isso
import sys
sys.path.append(r'D:/Documents/codigos/a3qualidade/definitiva')

import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
from principal.telas.tela_cadastro_loja import TelaCadastroLoja

@pytest.fixture
def setup_tela():    
    root = tk.Tk()
    tela = TelaCadastroLoja(master=root)
    return tela


# @patch('principal.telas.tela_cadastro_loja.conectar_banco')
# @patch('principal.telas.tela_cadastro_loja.messagebox.showinfo')
# def test_cadastro_loja_correto(mock_showinfo, mock_conectar, setup_tela):
#     # Configuração do mock para a conexão e cursor do banco de dados
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor = mock_conn.cursor.return_value
#     mock_conectar.return_value = mock_conn  # Mock da função conectar_banco
#     mock_cursor.fetchone.return_value = (0,)

#     # Configura os campos da tela para o teste
#     tela = setup_tela
#     tela.nome_loja.insert(0, "Loja do Teste")
#     tela.cnpj_loja.insert(0, "84548")  # CNPJ válido para o teste
#     tela.uf_loja.insert(0, "SC")
#     tela.tipo_loja.insert(0, "Geral")

#     # Chama o método para cadastrar a loja
#     tela.cadastrar_loja()

#     # Verifica se a mensagem de sucesso foi chamada
#     mock_showinfo.assert_called_with("Sucesso", "Loja cadastrada com sucesso!")

#     # Verifica se o commit foi chamado, ou seja, a transação foi efetivada
#     mock_conn.commit.assert_called_once()

#     # Verifica se a execução do comando de inserção foi realizada corretamente
#     mock_cursor.execute.assert_any_call(
#         "INSERT INTO Lojas (NOME_LOJA, NU_CNPJ, UF, TIPO_LOJA) VALUES (?, ?, ?, ?)",
#         ("Loja do Teste", "12345678000195", "SC", "Geral")
#     )


@patch('principal.telas.tela_cadastro_loja.conectar_banco')  # Mockando a conexão com o banco de dados
@patch('principal.telas.tela_cadastro_loja.messagebox.showerror')  # Mockando a exibição de mensagens de erro
def test_campos_incompletos(mock_showerror, mock_conectar, setup_tela):
    mock_conn = mock_conectar.return_value
    mock_cursor = mock_conn.cursor.return_value

    tela = setup_tela

    tela.nome_loja.insert(0,"")
    tela.cnpj_loja.insert(0,"") 
    tela.uf_loja.insert(0,"") 
    tela.tipo_loja.insert(0,"") 
    
    tela.cadastrar_loja()

    mock_showerror.assert_called_with("Erro", "Todos os campos devem ser preenchidos.")
    mock_conn.cursor.assert_not_called()


@patch('principal.telas.tela_cadastro_loja.conectar_banco')
@patch('principal.telas.tela_cadastro_loja.messagebox.showerror')
def test_cnpj_existente(mock_showerror, mock_conectar, setup_tela):
    # Configura o mock para o banco de dados
    mock_conn = mock_conectar.return_value
    mock_cursor = mock_conn.cursor.return_value
    
    # Configura o mock de fetchone para retornar um valor simulado
    mock_cursor.fetchone.return_value = (0,)  # Simula que o CNPJ já existe no banco de dados

    # Simula que a contagem de lojas com o CNPJ fornecido é maior que 0

    # Configura os campos da tela
    tela = setup_tela
    tela.nome_loja.insert(0, "Loja fo teste")
    tela.cnpj_loja.insert(0, "111111111")  # CNPJ que já existe
    tela.uf_loja.insert(0, "SC")
    tela.tipo_loja.insert(0, "Geral")

    # Chama o método de cadastro
    tela.cadastrar_loja()

    # Verifica se a função de exibição de erro foi chamada corretamente
    mock_showerror.assert_called_with("Erro", "Já existe uma loja com esse CNPJ.")
    mock_conn.cursor.assert_not_called()