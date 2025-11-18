import pytest
from unittest.mock import MagicMock, patch
from truco.truco import Truco

@pytest.fixture
def setup_dados():
    cbr_mock = MagicMock()
    jogador1_mock = MagicMock()
    jogador1_mock.pontos = 0
    jogador2_mock = MagicMock()
    jogador2_mock.pontos = 0
    
    jogador2_mock.avaliar_truco.return_value = 1
    
    return cbr_mock, jogador1_mock, jogador2_mock

def test_truco_inicializacao():
    truco = Truco()
    
    assert truco.estado_atual == "" 
    assert truco.retornar_valor_aposta() == 1
    assert truco.jogador_bloqueado == 0

def test_fluxo_pedir_truco(setup_dados):
    cbr, j1, j2 = setup_dados
    truco = Truco()
    
    truco.pedir_truco(cbr, 1, j1, j2)
    
    assert truco.estado_atual == "truco"
    assert truco.jogador_bloqueado == 1 

def test_fluxo_pedir_retruco(setup_dados):
    cbr, j1, j2 = setup_dados
    truco = Truco()
    
    truco.estado_atual = "truco"

    with patch('builtins.input', return_value='1'):
        truco.pedir_retruco(cbr, 2, j1, j2)
    
    assert truco.estado_atual == "retruco"
    assert truco.retornar_valor_aposta() == 3

def test_fluxo_pedir_vale_quatro(setup_dados):
    cbr, j1, j2 = setup_dados
    truco = Truco()
    
    truco.estado_atual = "retruco"
    truco.valor_aposta = 3
    
    truco.pedir_vale_quatro(cbr, 1, j1, j2)
    
    assert truco.retornar_valor_aposta() == 4

def test_truco_recusado(setup_dados):
    cbr, j1, j2 = setup_dados
    truco = Truco()
    
    j2.avaliar_truco.return_value = 0
    
    aceitou = truco.pedir_truco(cbr, 1, j1, j2)
    
    assert aceitou is False
    assert j1.pontos == 1

def test_resetar():
    truco = Truco()
    
    truco.valor_aposta = 4
    truco.estado_atual = "retruco"
    truco.jogador_bloqueado = 1
    
    truco.resetar()
    
    assert truco.retornar_valor_aposta() == 1
    assert truco.estado_atual == ""
    assert truco.jogador_bloqueado == 0