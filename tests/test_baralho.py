import pytest
import copy 
from truco.baralho import Baralho
from truco.carta import Carta

def test_baralho_criacao_padrao_truco():
    baralho = Baralho()
    assert len(baralho.cartas) == 40
    for carta in baralho.cartas:
        assert carta.retornar_numero() != 8
        assert carta.retornar_numero() != 9

def test_baralho_retirar_carta():
    baralho = Baralho()
    tamanho_inicial = len(baralho.cartas)
    carta_topo_esperada = baralho.cartas[-1] 
    carta_retirada = baralho.retirar_carta()
    assert carta_retirada == carta_topo_esperada
    assert len(baralho.cartas) == tamanho_inicial - 1

def test_baralho_retirar_todas_as_cartas_gera_erro():
    baralho = Baralho()
    for _ in range(40):
        baralho.retirar_carta()
    assert len(baralho.cartas) == 0
    with pytest.raises(IndexError):
        baralho.retirar_carta() 

def test_baralho_embaralhar():
    baralho = Baralho()
    baralho_original_ordenado = [str(c) for c in baralho.cartas]
    baralho.embaralhar()
    baralho_apos_embaralhar = [str(c) for c in baralho.cartas]
    assert baralho_original_ordenado != baralho_apos_embaralhar