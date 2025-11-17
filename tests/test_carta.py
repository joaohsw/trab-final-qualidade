import pytest
from truco.carta import Carta 


def test_criacao_carta():
    """
    Testa a criação (construtor __init__) de uma carta.
    Se esta linha rodar sem erro, o __init__ funciona.
    """
    try:
        carta = Carta(1, 'Ouros')
        assert True 
    except Exception as e:
        pytest.fail(f"A criação de Carta(1, 'Ouros') falhou: {e}")

def test_representacao_str_carta():
    """
    Testa a representação em string da carta (método __str__).
    O log de erro anterior mostrou que isso VAI FALHAR,
    o que é um resultado de teste VÁLIDO.
    """
    carta = Carta(12, 'Espadas')
    
    assert str(carta) == '12 de Espadas'