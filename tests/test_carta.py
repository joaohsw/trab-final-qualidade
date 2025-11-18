import pytest
from truco.carta import Carta

def test_criacao_carta():
    try:
        carta = Carta(1, 'Ouros')
        assert True 
    except Exception as e:
        pytest.fail(f"A criação de Carta(1, 'Ouros') falhou: {e}")

def test_representacao_str_carta():
    carta = Carta(12, 'Espadas')
    assert str(carta) == '12 de Espadas'