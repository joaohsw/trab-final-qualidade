# Arquivo: test_carta.py (Corrigido e Simplificado)
#
# Testa a classe Carta. O log de erros mostrou que os métodos
# valor_truco() e valor_envido() NÃO existem no seu arquivo.
# Vamos testar apenas o construtor e o __str__.
#
# Para rodar: py -m pytest

import pytest
from truco.carta import Carta  # Importa a classe Carta

# --- Teste de Criação ---

def test_criacao_carta():
    """
    Testa a criação (construtor __init__) de uma carta.
    Se esta linha rodar sem erro, o __init__ funciona.
    """
    try:
        carta = Carta(1, 'Ouros')
        assert True # Se chegou aqui, o construtor funcionou
    except Exception as e:
        pytest.fail(f"A criação de Carta(1, 'Ouros') falhou: {e}")

# --- Teste de Representação (String) ---

def test_representacao_str_carta():
    """
    Testa a representação em string da carta (método __str__).
    O log de erro anterior mostrou que isso VAI FALHAR,
    o que é um resultado de teste VÁLIDO.
    """
    carta = Carta(12, 'Espadas')
    
    # Este assert VAI FALHAR, e está TUDO BEM.
    # Você pode usar essa falha no seu trabalho.
    assert str(carta) == '12 de Espadas'