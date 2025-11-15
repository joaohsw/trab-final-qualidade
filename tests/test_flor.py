# Arquivo: test_flor.py (Corrigido)
#
# Este arquivo contém os testes de unidade para a lógica de 'Flor'.
# O objetivo é garantir que as funções 'tem_flor' e 'get_pontos_flor'
# funcionem corretamente.
#
# Para rodar este teste, use o comando: pytest

import pytest
from truco.carta import Carta
# CORREÇÃO: Importa as funções com underscore: _tem_flor, _get_pontos_flor
from truco.flor import _tem_flor, _get_pontos_flor

# --- Testes da função 'tem_flor' (Detecção) ---

def test_tem_flor_verdadeiro():
    """
    Testa se a função 'tem_flor' retorna True quando todas as
    três cartas são do mesmo naipe.
    """
    # Mão com flor de Ouros
    mao_flor = [Carta(1, 'Ouros'), Carta(5, 'Ouros'), Carta(12, 'Ouros')]
    # CORREÇÃO: Chama a função _tem_flor
    assert _tem_flor(mao_flor) is True
    
    # Mão com flor de Paus
    mao_flor_paus = [Carta(10, 'Paus'), Carta(11, 'Paus'), Carta(3, 'Paus')]
    assert _tem_flor(mao_flor_paus) is True

def test_tem_flor_falso():
    """
    Testa se a função 'tem_flor' retorna False quando as cartas
    não são todas do mesmo naipe.
    """
    # Mão sem flor (duas cartas iguais)
    mao_sem_flor_1 = [Carta(1, 'Ouros'), Carta(5, 'Ouros'), Carta(12, 'Espadas')]
    assert _tem_flor(mao_sem_flor_1) is False
    
    # Mão sem flor (todas diferentes)
    mao_sem_flor_2 = [Carta(1, 'Ouros'), Carta(5, 'Copas'), Carta(12, 'Espadas')]
    assert _tem_flor(mao_sem_flor_2) is False

# --- Testes da função 'get_pontos_flor' (Cálculo) ---

def test_get_pontos_flor_com_flor():
    """
    Testa o cálculo de pontos quando o jogador TEM flor.
    O cálculo é idêntico ao 'get_pontos_envido' para 3 cartas
    do mesmo naipe (soma as duas maiores + 20).
    """
    # Mão: 7 Ouros, 5 Ouros, 12 Ouros (Valor 0).
    # Descarta o 12 (valor 0). Cálculo: 7 + 5 + 20 = 32
    mao = [Carta(7, 'Ouros'), Carta(5, 'Ouros'), Carta(12, 'Ouros')]
    # CORREÇÃO: Chama a função _get_pontos_flor
    assert _get_pontos_flor(mao) == 32
    
    # Mão: 10 Paus (0), 11 Paus (0), 3 Paus (3).
    # Descarta o 10 (valor 0). Cálculo: 0 + 3 + 20 = 23
    mao_2 = [Carta(10, 'Paus'), Carta(11, 'Paus'), Carta(3, 'Paus')]
    assert _get_pontos_flor(mao_2) == 23

def test_get_pontos_flor_sem_flor():
    """
    Testa o cálculo de pontos quando o jogador NÃO TEM flor.
    Neste caso, a função 'get_pontos_flor' deve se comportar
    exatamente como 'get_pontos_envido', calculando o envido normal.
    """
    # Mão: 7 Ouros, 5 Ouros, 1 Copas. (Sem flor)
    # Cálculo de Envido: 7 + 5 + 20 = 32
    mao_envido = [Carta(7, 'Ouros'), Carta(5, 'Ouros'), Carta(1, 'Copas')]
    assert _get_pontos_flor(mao_envido) == 32
    
    # Mão: 7 Ouros, 5 Paus, 1 Copas. (Sem flor, naipes diferentes)
    # Cálculo de Envido: 7 (carta mais alta)
    mao_envido_alto = [Carta(7, 'Ouros'), Carta(5, 'Paus'), Carta(1, 'Copas')]
    assert _get_pontos_flor(mao_envido_alto) == 7