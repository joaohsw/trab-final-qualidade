import pytest
from unittest.mock import MagicMock
from truco.jogador import Jogador
from truco.carta import Carta
from truco import envido
from truco import flor

def test_jogador_criacao():
    jogador = Jogador("João")
    assert jogador.nome == "João"
    assert jogador.mao == []

def test_receber_cartas():
    jogador = Jogador("João")
    carta1 = Carta(1, 'Espadas')
    carta2 = Carta(7, 'Ouros')
    carta3 = Carta(3, 'Copas')
    mock_baralho = MagicMock()
    mock_baralho.retirar_carta.side_effect = [carta1, carta2, carta3]
    jogador.criar_mao(mock_baralho)
    assert len(jogador.mao) == 3
    assert str(jogador.mao[0]) == str(carta1)


def test_jogar_carta_por_indice():
    jogador = Jogador("João")
    carta1 = Carta(1, 'Espadas')
    carta2 = Carta(7, 'Ouros')
    jogador.mao = [carta1, carta2]
    carta_jogada = jogador.jogar_carta(1)
    assert str(carta_jogada) == str(carta2)
    assert len(jogador.mao) == 1
    assert str(jogador.mao[0]) == str(carta1)

def test_jogar_carta():
    jogador = Jogador("João")
    
    c1, c2, c3 = MagicMock(), MagicMock(), MagicMock()
    jogador.mao = [c1, c2, c3]
    
    carta_jogada = jogador.jogar_carta(1)
    
    assert carta_jogada == c2
    assert len(jogador.mao) == 2
    assert jogador.mao == [c1, c3]

def test_checa_flor_verdadeiro():
    jogador = Jogador("João")
    
    c1 = MagicMock()
    c2 = MagicMock()
    c3 = MagicMock()
    
    c1.retornar_naipe.return_value = 'Paus'
    c2.retornar_naipe.return_value = 'Paus'
    c3.retornar_naipe.return_value = 'Paus'
    
    jogador.mao = [c1, c2, c3]
    
    assert jogador.checa_flor() is True

def test_checa_flor_falso():
    jogador = Jogador("João")
    
    c1 = MagicMock()
    c2 = MagicMock()
    c3 = MagicMock()
    
    c1.retornar_naipe.return_value = 'Paus'
    c2.retornar_naipe.return_value = 'Copas' 
    c3.retornar_naipe.return_value = 'Paus'
    
    jogador.mao = [c1, c2, c3]
    
    assert jogador.checa_flor() is False

def test_calcula_envido_logica():

    jogador = Jogador("João")
    
    c1 = MagicMock()
    c2 = MagicMock()
    c3 = MagicMock()
    
    c1.retornar_naipe.return_value = 'Espadas'
    c2.retornar_naipe.return_value = 'Espadas'
    c3.retornar_naipe.return_value = 'Ouros'
    
    c1.retornar_pontos_envido.side_effect = lambda x: 7 if x == c1 else (3 if x == c2 else 0)
    
    jogador.mao = [c1, c2, c3]
    
    resultado = jogador.calcula_envido(jogador.mao)
    
    assert resultado == 30

def test_resetar():
    """Testa se o método resetar zera a mão e as flags."""
    jogador = Jogador("João")
    
    jogador.mao = [1, 2, 3]
    jogador.rodadas = 1
    jogador.flor = True
    jogador.pediu_truco = True
    
    jogador.resetar()
    
    assert jogador.rodadas == 0
    assert jogador.mao == []
    assert jogador.flor is False
    assert jogador.pediu_truco is False