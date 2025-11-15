# Arquivo: test_envido.py (Corrigido)
#
# Este arquivo contém os testes de unidade para a lógica de 'Envido'.
# O objetivo é garantir que a função 'get_pontos_envido' calcule
# corretamente os pontos da mão do jogador.
#
# Para rodar este teste, use o comando: pytest

import pytest
from truco.carta import Carta
# CORREÇÃO: Importa a função com underscore: _get_pontos_envido
from truco.envido import _get_pontos_envido 

# --- Cenário 1: Nenhuma carta do mesmo naipe ---

def test_envido_sem_naipes_iguais():
    """
    Testa o cálculo do envido quando todas as cartas são de naipes diferentes.
    O resultado deve ser o valor da carta mais alta (figuras valem 0).
    """
    # Mão: 7 Ouros, 5 Paus, 1 Copas. Maior valor = 7
    mao = [Carta(7, 'Ouros'), Carta(5, 'Paus'), Carta(1, 'Copas')]
    # CORREÇÃO: Chama a função _get_pontos_envido
    assert _get_pontos_envido(mao) == 7
    
    # Mão: 12 Ouros (0), 11 Paus (0), 10 Copas (0). Maior valor = 0
    mao_figuras = [Carta(12, 'Ouros'), Carta(11, 'Paus'), Carta(10, 'Copas')]
    assert _get_pontos_envido(mao_figuras) == 0
    
    # Mão: 12 Ouros (0), 6 Paus (6), 2 Copas (2). Maior valor = 6
    mao_mista = [Carta(12, 'Ouros'), Carta(6, 'Paus'), Carta(2, 'Copas')]
    assert _get_pontos_envido(mao_mista) == 6

# --- Cenário 2: Duas cartas do mesmo naipe ---

def test_envido_duas_cartas_mesmo_naipe_simples():
    """
    Testa o cálculo com duas cartas do mesmo naipe (não figuras).
    Resultado = ValorA + ValorB + 20.
    """
    # Mão: 7 Ouros, 5 Ouros, 1 Copas.
    # Cálculo: 7 + 5 + 20 = 32
    mao = [Carta(7, 'Ouros'), Carta(5, 'Ouros'), Carta(1, 'Copas')]
    assert _get_pontos_envido(mao) == 32

def test_envido_duas_cartas_mesmo_naipe_com_figura():
    """
    Testa o cálculo com duas cartas do mesmo naipe, sendo uma figura.
    Resultado = ValorA (0) + ValorB + 20.
    """
    # Mão: 12 Ouros (Valor 0), 6 Ouros, 1 Copas.
    # Cálculo: 0 + 6 + 20 = 26
    mao = [Carta(12, 'Ouros'), Carta(6, 'Ouros'), Carta(1, 'Copas')]
    assert _get_pontos_envido(mao) == 26
    
def test_envido_duas_cartas_mesmo_naipe_duas_figuras():
    """
    Testa o cálculo com duas cartas do mesmo naipe, sendo ambas figuras.
    Resultado = ValorA (0) + ValorB (0) + 20.
    """
    # Mão: 10 Paus (Valor 0), 11 Paus (Valor 0), 7 Espadas.
    # Cálculo: 0 + 0 + 20 = 20
    mao = [Carta(10, 'Paus'), Carta(11, 'Paus'), Carta(7, 'Espadas')]
    assert _get_pontos_envido(mao) == 20

# --- Cenário 3: Três cartas do mesmo naipe (Flor) ---

def test_envido_tres_cartas_mesmo_naipe_simples():
    """
    Testa o cálculo com três cartas do mesmo naipe (não figuras).
    A regra manda descartar a menor e somar as duas maiores + 20.
    """
    # Mão: 7 Ouros, 5 Ouros, 3 Ouros.
    # Descarta o 3. Cálculo: 7 + 5 + 20 = 32
    mao = [Carta(7, 'Ouros'), Carta(5, 'Ouros'), Carta(3, 'Ouros')]
    assert _get_pontos_envido(mao) == 32

def test_envido_tres_cartas_mesmo_naipe_com_figura():
    """
    Testa o cálculo com três cartas do mesmo naipe, sendo uma figura.
    A figura (valor 0) será a menor e será descartada.
    """
    # Mão: 7 Ouros, 5 Ouros, 12 Ouros (Valor 0).
    # Descarta o 12 (valor 0). Cálculo: 7 + 5 + 20 = 32
    mao = [Carta(7, 'Ouros'), Carta(5, 'Ouros'), Carta(12, 'Ouros')]
    assert _get_pontos_envido(mao) == 32

def test_envido_tres_cartas_mesmo_naipe_duas_figuras():
    """
    Testa o cálculo com três cartas, sendo duas figuras.
    Uma figura (valor 0) será descartada.
    """
    # Mão: 7 Ouros, 10 Ouros (Valor 0), 12 Ouros (Valor 0).
    # Descarta o 10 (valor 0). Cálculo: 7 + 0 + 20 = 27
    mao = [Carta(7, 'Ouros'), Carta(10, 'Ouros'), Carta(12, 'Ouros')]
    assert _get_pontos_envido(mao) == 27
    
def test_envido_tres_cartas_mesmo_naipe_tres_figuras():
    """
    Testa o cálculo com três cartas, sendo todas figuras.
    O resultado deve ser 20 (0 + 0 + 20).
    """
    # Mão: 10 Ouros (0), 11 Ouros (0), 12 Ouros (0).
    # Descarta o 10 (valor 0). Cálculo: 0 + 0 + 20 = 20
    mao = [Carta(10, 'Ouros'), Carta(11, 'Ouros'), Carta(12, 'Ouros')]
    assert _get_pontos_envido(mao) == 20