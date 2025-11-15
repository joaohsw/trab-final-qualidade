# Arquivo: test_carta.py
#
# Este arquivo contém os testes de unidade para a classe Carta.
# O objetivo é garantir que cada objeto 'Carta' seja criado corretamente
# e que seus métodos (valor_truco, valor_envido) retornem os valores
# esperados de acordo com as regras do jogo.
#
# Para rodar este teste, use o comando: pytest

import pytest
from truco.carta import Carta  # Importa a classe Carta do seu projeto

# --- Testes de Criação e Representação ---

def test_criacao_carta():
    """
    Testa a criação (construtor __init__) de uma carta.
    Verifica se os atributos 'valor' e 'naipe' são definidos corretamente.
    """
    # Cria uma carta específica (ex: 1 de Ouros)
    carta = Carta(1, 'Ouros')
    
    # Verifica se o valor e o naipe foram armazenados corretamente
    assert carta.valor == 1
    assert carta.naipe == 'Ouros'

def test_representacao_str_carta():
    """
    Testa a representação em string da carta (método __str__).
    Isso é útil para logs e debug, garantindo que "12 de Espadas"
    seja impresso corretamente.
    """
    carta = Carta(12, 'Espadas')
    
    # Verifica se a saída do __str__ é a esperada
    assert str(carta) == '12 de Espadas'
    
    carta_dois = Carta(7, 'Copas')
    assert str(carta_dois) == '7 de Copas'

# --- Testes de Lógica de Jogo (Envido) ---

def test_valor_envido_cartas_numericas():
    """
    Testa o cálculo do 'valor_envido' para cartas que não são figuras.
    O valor do envido deve ser o próprio valor da carta.
    """
    carta_1 = Carta(1, 'Paus')
    carta_5 = Carta(5, 'Ouros')
    carta_7 = Carta(7, 'Espadas')
    
    assert carta_1.valor_envido() == 1
    assert carta_5.valor_envido() == 5
    assert carta_7.valor_envido() == 7

def test_valor_envido_figuras():
    """
    Testa o cálculo do 'valor_envido' para as figuras (10, 11 e 12).
    Pelas regras do truco, o valor do envido para figuras é sempre 0.
    """
    carta_10 = Carta(10, 'Copas')
    carta_11 = Carta(11, 'Paus')
    carta_12 = Carta(12, 'Espadas')
    
    assert carta_10.valor_envido() == 0
    assert carta_11.valor_envido() == 0
    assert carta_12.valor_envido() == 0

# --- Testes de Lógica de Jogo (Valor do Truco) ---

def test_valor_truco_manilhas_principais():
    """
    Testa o 'valor_truco' (força) das cartas mais fortes do jogo (manilhas).
    1 de Espadas (Espadão) -> 14
    1 de Paus (Bastão) -> 13
    """
    # O "Ás de Espadas" (Espadão) é a carta mais forte
    as_espadas = Carta(1, 'Espadas')
    assert as_espadas.valor_truco() == 14
    
    # O "Ás de Paus" (Bastão) é a segunda carta mais forte
    as_paus = Carta(1, 'Paus')
    assert as_paus.valor_truco() == 13

def test_valor_truco_manilhas_secundarias():
    """
    Testa o 'valor_truco' (força) das manilhas secundárias.
    7 de Espadas -> 12
    7 de Ouros -> 11
    """
    sete_espadas = Carta(7, 'Espadas')
    assert sete_espadas.valor_truco() == 12
    
    sete_ouros = Carta(7, 'Ouros')
    assert sete_ouros.valor_truco() == 11

def test_valor_truco_cartas_comuns():
    """
    Testa o 'valor_truco' (força) das cartas comuns (3, 2, 1s restantes).
    Todos os 3s -> 10
    Todos os 2s -> 9
    1 de Ouros e 1 de Copas -> 8
    """
    # Testando os 3s
    assert Carta(3, 'Ouros').valor_truco() == 10
    assert Carta(3, 'Copas').valor_truco() == 10
    assert Carta(3, 'Espadas').valor_truco() == 10
    assert Carta(3, 'Paus').valor_truco() == 10
    
    # Testando os 2s
    assert Carta(2, 'Ouros').valor_truco() == 9
    assert Carta(2, 'Copas').valor_truco() == 9
    assert Carta(2, 'Espadas').valor_truco() == 9
    assert Carta(2, 'Paus').valor_truco() == 9

    # Testando os 1s restantes (Ás de Ouros e Copas)
    assert Carta(1, 'Ouros').valor_truco() == 8
    assert Carta(1, 'Copas').valor_truco() == 8

def test_valor_truco_figuras_e_cartas_baixas():
    """
    Testa o 'valor_truco' (força) das figuras e das cartas mais fracas.
    Reis (12) -> 7
    Cavalos (11) -> 6
    Valetes (10) -> 5
    7 de Paus e 7 de Copas -> 4
    6s -> 3
    5s -> 2
    4s -> 1
    """
    # Figuras
    assert Carta(12, 'Ouros').valor_truco() == 7  # Reis
    assert Carta(11, 'Espadas').valor_truco() == 6 # Cavalos
    assert Carta(10, 'Paus').valor_truco() == 5    # Valetes
    
    # Cartas baixas
    assert Carta(7, 'Paus').valor_truco() == 4    # 7s restantes
    assert Carta(7, 'Copas').valor_truco() == 4
    assert Carta(6, 'Ouros').valor_truco() == 3    # 6s
    assert Carta(5, 'Copas').valor_truco() == 2    # 5s
    assert Carta(4, 'Espadas').valor_truco() == 1   # 4s (mais fracas)