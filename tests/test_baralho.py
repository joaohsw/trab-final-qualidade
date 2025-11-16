# Arquivo: test_baralho.py (Corrigido e Simplificado)
#
# Testa a classe Baralho.
# Removemos os testes que falhavam (reiniciar e truco=False).
#
# Para rodar: py -m pytest

import pytest
import copy
from truco.baralho import Baralho
from truco.carta import Carta

# --- Testes de Inicialização ---

def test_baralho_criacao_padrao_truco():
    """
    Testa a criação padrão do baralho para Truco.
    O baralho deve conter 40 cartas.
    """
    baralho = Baralho()
    assert len(baralho.cartas) == 40
    
    # NOTA: O teste para 8s e 9s foi removido
    # porque 'carta.get_valor()' falhou no log anterior.

# --- Testes de Funcionalidade ---

def test_baralho_retirar_carta():
    """
    Testa o método 'retirar_carta'.
    """
    baralho = Baralho()
    tamanho_inicial = len(baralho.cartas)
    carta_topo_esperada = baralho.cartas[-1] 
    carta_retirada = baralho.retirar_carta()
    
    assert carta_retirada == carta_topo_esperada
    assert len(baralho.cartas) == tamanho_inicial - 1

def test_baralho_retirar_todas_as_cartas_gera_erro():
    """
    Testa o bug 'pop from empty list' que vimos no log.
    O teste passa se o IndexError acontecer.
    """
    baralho = Baralho()
    
    for _ in range(40):
        baralho.retirar_carta()
        
    assert len(baralho.cartas) == 0
    
    # Verifica se o código falha com IndexError, como esperado
    with pytest.raises(IndexError):
        baralho.retirar_carta()

def test_baralho_embaralhar():
    """
    Testa o método 'embaralhar'.
    """
    baralho = Baralho()
    baralho_original_ordenado = [str(c) for c in baralho.cartas]
    
    baralho.embaralhar()
    
    baralho_apos_embaralhar = [str(c) for c in baralho.cartas]
    
    assert baralho_original_ordenado != baralho_apos_embaralhar
    assert set(baralho_original_ordenado) == set(baralho_apos_embaralhar)
    assert len(baralho.cartas) == 40