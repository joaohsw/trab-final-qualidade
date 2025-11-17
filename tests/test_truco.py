import pytest
from truco.truco import Truco


def test_truco_inicializacao():
    """
    Testa o estado inicial da classe Truco.
    """
    truco = Truco()
    
    assert truco.get_estado() == 'NAO_CANTADO'
    assert truco.get_pontos() == 1
    assert truco.get_quem_cantou_por_ultimo() is None


def test_fluxo_truco_aceito():
    """
    Testa o fluxo: Jogador 1 canta TRUCO, Jogador 2 ACEITA.
    """
    truco = Truco()
    jogador_1_id = 1
    jogador_2_id = 2
    
    truco.cantar('TRUCO', jogador_1_id)
    
    assert truco.get_estado() == 'TRUCO'
    assert truco.get_pontos() == 2
    assert truco.get_quem_cantou_por_ultimo() == jogador_1_id
    
    truco.cantar('ACEITO', jogador_2_id)
    
    assert truco.get_estado() == 'TRUCO'
    assert truco.get_pontos() == 2 
    assert truco.get_quem_cantou_por_ultimo() == jogador_1_id

def test_fluxo_retruco_aceito():
    """
    Testa o fluxo: TRUCO -> RETRUCO -> ACEITO.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    truco.cantar('TRUCO', j1)
    truco.cantar('RETRUCO', j2)
    
    assert truco.get_estado() == 'RETRUCO'
    assert truco.get_pontos() == 3
    assert truco.get_quem_cantou_por_ultimo() == j2
    
    truco.cantar('ACEITO', j1)
    
    assert truco.get_estado() == 'RETRUCO'
    assert truco.get_pontos() == 3 
    assert truco.get_quem_cantou_por_ultimo() == j2

def test_fluxo_vale4_aceito():
    """
    Testa o fluxo completo: TRUCO -> RETRUCO -> VALE4 -> ACEITO.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    truco.cantar('TRUCO', j1)
    truco.cantar('RETRUCO', j2)
    truco.cantar('VALE4', j1)
    
    assert truco.get_estado() == 'VALE4'
    assert truco.get_pontos() == 4
    assert truco.get_quem_cantou_por_ultimo() == j1
    
    truco.cantar('ACEITO', j2)
    
    assert truco.get_estado() == 'VALE4'
    assert truco.get_pontos() == 4 
    assert truco.get_quem_cantou_por_ultimo() == j1


def test_fluxo_truco_nao_aceito():
    """
    Testa o fluxo: Jogador 1 canta TRUCO, Jogador 2 NÃO ACEITA.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    truco.cantar('TRUCO', j1)
    truco.cantar('NAO ACEITO', j2)
    
    assert truco.get_estado() == 'NAO_ACEITO'
    assert truco.get_pontos() == 1 
    assert truco.get_quem_cantou_por_ultimo() == j1

def test_fluxo_retruco_nao_aceito():
    """
    Testa o fluxo: TRUCO -> RETRUCO, Jogador 1 NÃO ACEITA.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    truco.cantar('TRUCO', j1)
    truco.cantar('RETRUCO', j2)
    truco.cantar('NAO ACEITO', j1)
    
    assert truco.get_estado() == 'NAO_ACEITO'
    assert truco.get_pontos() == 2
    assert truco.get_quem_cantou_por_ultimo() == j2

def test_fluxo_vale4_nao_aceito():
    """
    Testa o fluxo: TRUCO -> RETRUCO -> VALE4, Jogador 2 NÃO ACEITA.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    truco.cantar('TRUCO', j1)
    truco.cantar('RETRUCO', j2)
    truco.cantar('VALE4', j1)
    truco.cantar('NAO ACEITO', j2)
    
    assert truco.get_estado() == 'NAO_ACEITO'
    assert truco.get_pontos() == 3
    assert truco.get_quem_cantou_por_ultimo() == j1


def test_reset_truco():
    """
    Testa o método 'reset_truco' após uma aposta.
    """
    truco = Truco()
    j1 = 1
    
    truco.cantar('TRUCO', j1)
    
    truco.reset_truco()
    
    assert truco.get_estado() == 'NAO_CANTADO'
    assert truco.get_pontos() == 1
    assert truco.get_quem_cantou_por_ultimo() is None