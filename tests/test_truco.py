# Arquivo: test_truco.py
#
# Este arquivo contém os testes de unidade para a classe Truco.
# Esta classe funciona como uma "máquina de estados" para controlar
# o nível da aposta (Truco, Retruco, Vale4) e quantos pontos
# ela vale se for aceita ou recusada.
#
# Para rodar este teste, use o comando: pytest

import pytest
from truco.truco import Truco

# --- Testes de Inicialização ---

def test_truco_inicializacao():
    """
    Testa o estado inicial da classe Truco.
    O nível da aposta deve começar em 1 (mão simples) e
    o estado deve ser 'NAO_CANTADO'.
    """
    truco = Truco()
    
    assert truco.get_estado() == 'NAO_CANTADO'
    assert truco.get_pontos() == 1  # Mão simples vale 1 ponto
    assert truco.get_quem_cantou_por_ultimo() is None

# --- Testes de Fluxo de Apostas (Aceitando) ---

def test_fluxo_truco_aceito():
    """
    Testa o fluxo: Jogador 1 canta TRUCO, Jogador 2 ACEITA.
    """
    truco = Truco()
    jogador_1_id = 1
    jogador_2_id = 2
    
    # Jogador 1 canta TRUCO
    truco.cantar('TRUCO', jogador_1_id)
    
    assert truco.get_estado() == 'TRUCO'
    assert truco.get_pontos() == 2  # Se aceito, vale 2
    assert truco.get_quem_cantou_por_ultimo() == jogador_1_id
    
    # Jogador 2 ACEITA
    truco.cantar('ACEITO', jogador_2_id)
    
    # O estado permanece TRUCO, mas agora está "travado"
    assert truco.get_estado() == 'TRUCO'
    assert truco.get_pontos() == 2 # Pontos finais são 2
    # Quem cantou por último não muda ao aceitar
    assert truco.get_quem_cantou_por_ultimo() == jogador_1_id

def test_fluxo_retruco_aceito():
    """
    Testa o fluxo: TRUCO -> ACEITO -> RETRUCO -> ACEITO.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    # J1 canta TRUCO
    truco.cantar('TRUCO', j1)
    # J2 canta RETRUCO (implica que aceitou o truco)
    truco.cantar('RETRUCO', j2)
    
    assert truco.get_estado() == 'RETRUCO'
    assert truco.get_pontos() == 3  # Se aceito, vale 3
    assert truco.get_quem_cantou_por_ultimo() == j2
    
    # J1 ACEITA o RETRUCO
    truco.cantar('ACEITO', j1)
    
    assert truco.get_estado() == 'RETRUCO'
    assert truco.get_pontos() == 3 # Pontos finais são 3
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
    # J1 canta VALE4
    truco.cantar('VALE4', j1)
    
    assert truco.get_estado() == 'VALE4'
    assert truco.get_pontos() == 4  # Se aceito, vale 4
    assert truco.get_quem_cantou_por_ultimo() == j1
    
    # J2 ACEITA o VALE4
    truco.cantar('ACEITO', j2)
    
    assert truco.get_estado() == 'VALE4'
    assert truco.get_pontos() == 4 # Pontos finais são 4
    assert truco.get_quem_cantou_por_ultimo() == j1

# --- Testes de Recusa (Não Aceitar) ---

def test_fluxo_truco_nao_aceito():
    """
    Testa o fluxo: Jogador 1 canta TRUCO, Jogador 2 NÃO ACEITA.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    # J1 canta TRUCO
    truco.cantar('TRUCO', j1)
    
    # J2 NÃO ACEITA
    truco.cantar('NAO ACEITO', j2)
    
    # O estado muda para 'NAO_ACEITO'
    assert truco.get_estado() == 'NAO_ACEITO'
    # Os pontos devem ser o valor ANTERIOR (mão simples)
    assert truco.get_pontos() == 1 
    # Quem cantou por último (J1) ganha os pontos
    assert truco.get_quem_cantou_por_ultimo() == j1

def test_fluxo_retruco_nao_aceito():
    """
    Testa o fluxo: TRUCO -> RETRUCO, Jogador 1 NÃO ACEITA.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    truco.cantar('TRUCO', j1)
    # J2 canta RETRUCO
    truco.cantar('RETRUCO', j2)
    
    # J1 NÃO ACEITA o RETRUCO
    truco.cantar('NAO ACEITO', j1)
    
    assert truco.get_estado() == 'NAO_ACEITO'
    # Os pontos devem ser o valor do TRUCO (2 pontos)
    assert truco.get_pontos() == 2
    # Quem cantou por último (J2) ganha os pontos
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
    
    # J2 NÃO ACEITA o VALE4
    truco.cantar('NAO ACEITO', j2)
    
    assert truco.get_estado() == 'NAO_ACEITO'
    # Os pontos devem ser o valor do RETRUCO (3 pontos)
    assert truco.get_pontos() == 3
    # Quem cantou por último (J1) ganha os pontos
    assert truco.get_quem_cantou_por_ultimo() == j1

# --- Testes de Reset ---

def test_reset_truco():
    """
    Testa o método 'reset_truco' após uma aposta.
    """
    truco = Truco()
    j1 = 1
    j2 = 2
    
    # Simula um VALE4 aceito
    truco.cantar('TRUCO', j1)
    truco.cantar('RETRUCO', j2)
    truco.cantar('VALE4', j1)
    truco.cantar('ACEITO', j2)
    
    assert truco.get_estado() == 'VALE4'
    assert truco.get_pontos() == 4
    
    # Reseta para a próxima mão
    truco.reset_truco()
    
    # Deve voltar ao estado inicial
    assert truco.get_estado() == 'NAO_CANTADO'
    assert truco.get_pontos() == 1
    assert truco.get_quem_cantou_por_ultimo() is None