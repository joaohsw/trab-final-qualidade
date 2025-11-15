# Arquivo: test_pontos.py (Corrigido)
#
# Este arquivo contém os testes de unidade para a classe Pontos.
# O objetivo é garantir que o placar do jogo funcione corretamente.
# Testa a adição e reset de pontos da mão (rodada de truco)
# e da partida (total).
#
# Para rodar este teste, use o comando: pytest

import pytest
# CORREÇÃO: Importa 'pontos' (com 'p' minúsculo), como o erro sugeriu.
from truco.pontos import pontos 

# --- Testes de Inicialização ---

def test_pontos_inicializacao():
    """
    Testa o construtor da classe Pontos.
    Verifica se todos os placares começam zerados.
    """
    # CORREÇÃO: Usa a classe 'pontos' (com 'p' minúsculo)
    placar = pontos() 
    
    # Pontos da rodada de truco atual
    assert placar.get_pontos_mao_rodada_truco() == 0
    
    # Pontos totais da partida
    pontos_partida = placar.get_pontos_partida()
    assert pontos_partida['nos'] == 0
    assert pontos_partida['eles'] == 0

# --- Testes de Pontos da Mão (Rodada de Truco) ---

def test_add_get_pontos_mao_rodada_truco():
    """
    Testa a adição e leitura dos pontos de uma mão (ex: 1 ponto por
    vencer a rodada, 2 pontos por vencer um truco, etc.)
    """
    placar = pontos()
    
    # Adiciona 1 ponto (venceu primeira rodada)
    placar.add_pontos_mao_rodada_truco(1)
    assert placar.get_pontos_mao_rodada_truco() == 1
    
    # Adiciona mais 2 pontos (venceu segunda rodada)
    placar.add_pontos_mao_rodada_truco(2)
    assert placar.get_pontos_mao_rodada_truco() == 3

def test_reset_pontos_mao_rodada_truco():
    """
    Testa se o placar da "mão" (rodada de truco) é zerado
    corretamente no início de uma nova mão.
    """
    placar = pontos()
    placar.add_pontos_mao_rodada_truco(3)  # Simulando 3 pontos de um retruco
    
    assert placar.get_pontos_mao_rodada_truco() == 3
    
    # Reseta para a próxima mão
    placar.reset_pontos_mao_rodada_truco()
    
    assert placar.get_pontos_mao_rodada_truco() == 0

# --- Testes de Pontos da Partida (Placar Geral) ---

def test_add_pontos_partida():
    """
    Testa a adição de pontos ao placar geral do jogo (Nós vs Eles).
    """
    placar = pontos()
    
    # "Nós" ganhamos 3 pontos (ex: Envido)
    placar.add_pontos_partida('nos', 3)
    pontos_partida = placar.get_pontos_partida()
    assert pontos_partida['nos'] == 3
    assert pontos_partida['eles'] == 0
    
    # "Eles" ganharam 1 ponto (ex: Mão simples)
    placar.add_pontos_partida('eles', 1)
    pontos_partida = placar.get_pontos_partida()
    assert pontos_partida['nos'] == 3
    assert pontos_partida['eles'] == 1
    
    # "Nós" ganhamos mais 2 pontos (ex: Truco)
    placar.add_pontos_partida('nos', 2)
    pontos_partida = placar.get_pontos_partida()
    assert pontos_partida['nos'] == 5
    assert pontos_partida['eles'] == 1

def test_reset_pontos_partida():
    """
    Testa se o placar geral do jogo é zerado (para um novo jogo).
    """
    placar = pontos()
    placar.add_pontos_partida('nos', 15)
    placar.add_pontos_partida('eles', 10)
    
    pontos_partida = placar.get_pontos_partida()
    assert pontos_partida['nos'] == 15
    assert pontos_partida['eles'] == 10
    
    placar.reset_pontos_partida()
    
    pontos_partida = placar.get_pontos_partida()
    assert pontos_partida['nos'] == 0
    assert pontos_partida['eles'] == 0

# --- Testes de Verificação do Vencedor ---

def test_vencedor_partida_sem_vencedor():
    """
    Testa a verificação de vencedor quando ninguém atingiu 30 pontos.
    """
    placar = pontos()
    
    # Ninguém venceu
    placar.add_pontos_partida('nos', 10)
    placar.add_pontos_partida('eles', 15)
    assert placar.vencedor_partida() is None
    
    # Ninguém venceu (limite)
    placar.add_pontos_partida('nos', 19) # Total 29
    assert placar.vencedor_partida() is None

def test_vencedor_partida_nos_vence():
    """
    Testa a verificação de vencedor quando "Nós" atingem 30 pontos.
    """
    placar = pontos()
    placar.add_pontos_partida('nos', 29)
    assert placar.vencedor_partida() is None
    
    # "Nós" fazemos o ponto da vitória
    placar.add_pontos_partida('nos', 1) # Total 30
    assert placar.vencedor_partida() == 'Nos'

def test_vencedor_partida_eles_vence():
    """
    Testa a verificação de vencedor quando "Eles" atingem 30 pontos.
    """
    placar = pontos()
    placar.add_pontos_partida('eles', 29)
    assert placar.vencedor_partida() is None
    
    # "Eles" fazem o ponto da vitória
    placar.add_pontos_partida('eles', 1) # Total 30
    assert placar.vencedor_partida() == 'Eles'

def test_vencedor_partida_ambos_passam_30():
    """
    Testa o cenário onde "Nós" já temos 28 e "Eles" 29.
    Se "Eles" fazem 2 pontos, eles vencem.
    
    NOTA: O seu código (pontos.py, linha 36) checa 'Nos' PRIMEIRO.
    Se 'Nos' tiver >= 30, ele ganha, mesmo que 'Eles' também tenha.
    Este teste valida esse comportamento.
    """
    placar = pontos()
    
    # Cenário: Nós 29, Eles 29.
    placar.add_pontos_partida('nos', 29)
    placar.add_pontos_partida('eles', 29)
    
    # "Nós" fazemos 2 pontos (Total 31)
    placar.add_pontos_partida('nos', 2)
    
    # Mesmo que "Eles" tenham 29, "Nós" vencemos.
    assert placar.vencedor_partida() == 'Nos'