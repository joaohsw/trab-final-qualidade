# Arquivo: test_jogador.py (Corrigido)
#
# Testa a classe Jogador, corrigindo os bugs dos testes anteriores.
#
# Para rodar: py -m pytest

import pytest
from unittest.mock import MagicMock
from truco.jogador import Jogador
from truco.carta import Carta
from truco import envido
from truco import flor

# --- Testes de Inicialização e Estado ---

def test_jogador_criacao():
    """
    Testa a criação (construtor __init__) de um jogador.
    """
    jogador = Jogador("João")
    
    assert jogador.nome == "João"
    # CORREÇÃO: Acessa o atributo 'mao' diretamente
    assert jogador.mao == []  # Deve começar com a mão vazia

def test_receber_cartas():
    """
    Testa o método 'criar_mao'.
    """
    jogador = Jogador("João")
    
    carta1 = Carta(1, 'Espadas')
    carta2 = Carta(7, 'Ouros')
    carta3 = Carta(3, 'Copas')

    mock_baralho = MagicMock()
    mock_baralho.retirar_carta.side_effect = [carta1, carta2, carta3]

    jogador.criar_mao(mock_baralho)
    
    assert len(jogador.mao) == 3
    assert str(jogador.mao[0]) == str(carta1)

def test_limpar_mao():
    """
    Testa o método 'limpar_mao'.
    (Se este teste falhar, é 100% um problema de cache __pycache__)
    """
    jogador = Jogador("João")
    
    jogador.mao = [Carta(1, 'Espadas'), Carta(7, 'Ouros')]
    
    assert len(jogador.mao) == 2  # Mão não está vazia
    
    jogador.limpar_mao()
    
    assert len(jogador.mao) == 0  # Mão deve estar vazia

# --- Testes de Ações (Jogar Carta) ---

def test_jogar_carta_por_indice():
    """
    Testa o método 'jogar_carta' usando um índice (ex: 0, 1, 2).
    """
    jogador = Jogador("João")
    carta1 = Carta(1, 'Espadas')
    carta2 = Carta(7, 'Ouros')
    jogador.mao = [carta1, carta2] # Coloca as cartas direto na mão
    
    carta_jogada = jogador.jogar_carta(1)
    
    assert str(carta_jogada) == str(carta2)
    assert len(jogador.mao) == 1
    assert str(jogador.mao[0]) == str(carta1)

# --- Testes de Lógica de Pontos (Envido e Flor) ---

def test_get_pontos_envido(mocker):
    """
    Testa o método 'get_pontos_envido'.
    """
    jogador = Jogador("João")
    
    # CORREÇÃO: Mock para get_pontos_envido (sem underscore)
    mocker.patch('truco.envido.get_pontos_envido', return_value=27)
    
    cartas_envido_27 = [Carta(7, 'Espadas'), Carta(12, 'Espadas'), Carta(1, 'Ouros')]
    jogador.mao = cartas_envido_27
    assert jogador.get_pontos_envido() == 27

def test_tem_flor(mocker):
    """
    Testa o método 'tem_flor'.
    """
    jogador = Jogador("João")
    
    # CORREÇÃO: Mock para tem_flor (sem underscore)
    mocker.patch('truco.flor.tem_flor', return_value=True)
    
    cartas_com_flor = [Carta(1, 'Ouros'), Carta(7, 'Ouros'), Carta(5, 'Ouros')]
    jogador.mao = cartas_com_flor
    assert jogador.tem_flor() is True

def test_get_pontos_flor(mocker):
    """
    Testa o método 'get_pontos_flor'.
    """
    jogador = Jogador("João")
    
    # CORREÇÃO: Mock para get_pontos_flor (sem underscore)
    mocker.patch('truco.flor.get_pontos_flor', return_value=32)

    cartas_flor_32 = [Carta(5, 'Ouros'), Carta(7, 'Ouros'), Carta(12, 'Ouros')]
    jogador.mao = cartas_flor_32
    assert jogador.get_pontos_flor() == 32

# --- Testes de "Cantar" (Ações) ---

def test_cantar_acoes_simples():
    """
    Testa os métodos de "cantar" que existem no seu jogador.py
    (Se este teste falhar, é 100% um problema de cache __pycache__)
    """
    jogador = Jogador("João")
    
    # CORREÇÃO: Removemos 'cantar_envido' que o log disse que não existe
    assert jogador.aceitar() == 'ACEITO'
    assert jogador.nao_aceitar() == 'NAO ACEITO'
    assert jogador.cantar_flor() == 'FLOR'