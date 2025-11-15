# Arquivo: test_baralho.py
#
# Este arquivo contém os testes de unidade para a classe Baralho.
# O objetivo é garantir que o baralho seja inicializado corretamente,
# que as funções de embaralhar, retirar carta e reiniciar funcionem
# como o esperado.
#
# Para rodar este teste, use o comando: pytest

import pytest
import copy  # Usado para fazer cópias do estado do baralho
from truco.baralho import Baralho
from truco.carta import Carta

# --- Testes de Inicialização ---

def test_baralho_criacao_padrao_truco():
    """
    Testa a criação padrão do baralho para Truco.
    O baralho deve conter 40 cartas (excluindo os 8s e 9s).
    """
    baralho = Baralho()
    
    # Verifica se o número de cartas é 40
    assert len(baralho.cartas) == 40
    
    # Verifica se não há 8s ou 9s no baralho
    for carta in baralho.cartas:
        assert carta.valor != 8
        assert carta.valor != 9

def test_baralho_criacao_completo():
    """
    Testa a criação de um baralho completo (não-truco), se o construtor permitir.
    No seu código, `Baralho(truco=False)` cria um baralho de 48 cartas.
    """
    baralho_completo = Baralho(truco=False)
    
    # Verifica se o número de cartas é 48 (12 valores * 4 naipes)
    assert len(baralho_completo.cartas) == 48
    
    # Verifica se os 8s e 9s ESTÃO presentes
    tem_8 = any(c.valor == 8 for c in baralho_completo.cartas)
    tem_9 = any(c.valor == 9 for c in baralho_completo.cartas)
    assert tem_8
    assert tem_9

# --- Testes de Funcionalidade ---

def test_baralho_retirar_carta():
    """
    Testa o método 'retirar_carta'.
    Verifica se a carta é removida do topo e se o tamanho do baralho diminui.
    """
    baralho = Baralho()
    tamanho_inicial = len(baralho.cartas) # Deve ser 40
    
    # Pega a carta que está no topo (a última da lista)
    carta_topo_esperada = baralho.cartas[-1] 
    
    # Retira a carta
    carta_retirada = baralho.retirar_carta()
    
    # Verifica se a carta retirada é a esperada
    assert carta_retirada == carta_topo_esperada
    
    # Verifica se o tamanho do baralho diminuiu em 1
    assert len(baralho.cartas) == tamanho_inicial - 1

def test_baralho_retirar_todas_as_cartas():
    """
    Testa o comportamento de 'retirar_carta' quando o baralho está vazio.
    O método deve retornar 'None' (conforme implementado em baralho.py).
    """
    baralho = Baralho()
    
    # Retira todas as 40 cartas
    for _ in range(40):
        baralho.retirar_carta()
        
    # Verifica se o baralho está vazio
    assert len(baralho.cartas) == 0
    
    # Tenta retirar mais uma carta
    carta_extra = baralho.retirar_carta()
    
    # Verifica se o retorno é None, indicando que não há mais cartas
    assert carta_extra is None

def test_baralho_embaralhar():
    """
    Testa o método 'embaralhar'.
    Este teste verifica duas coisas:
    1. A ordem das cartas mudou.
    2. O baralho AINDA contém as mesmas 40 cartas, apenas em posições diferentes.
    """
    baralho = Baralho()
    
    # Cria uma cópia profunda do baralho original (antes de embaralhar)
    # Usamos str(c) para facilitar a comparação
    baralho_original_ordenado = [str(c) for c in baralho.cartas]
    
    # Embaralha o baralho
    baralho.embaralhar()
    
    # Pega a lista de cartas após embaralhar
    baralho_apos_embaralhar = [str(c) for c in baralho.cartas]
    
    # 1. Testa se a ordem mudou.
    #    (Existe uma chance matemática mínima de embaralhar para a mesma ordem,
    #    mas para um baralho de 40 cartas, é astronomicamente improvável)
    assert baralho_original_ordenado != baralho_apos_embaralhar
    
    # 2. Testa se as cartas são as mesmas (conjunto de cartas).
    #    Comparamos os conjuntos (sets) para ignorar a ordem.
    assert set(baralho_original_ordenado) == set(baralho_apos_embaralhar)
    
    # 3. Testa se o número de cartas permanece 40.
    assert len(baralho.cartas) == 40

def test_baralho_reiniciar():
    """
    Testa o método 'reiniciar'.
    Verifica se o baralho retorna ao seu estado original de 40 cartas
    após cartas terem sido retiradas e embaralhadas.
    """
    baralho = Baralho()
    
    # Guarda o estado original (como lista de strings)
    cartas_originais = [str(c) for c in baralho.cartas]
    
    # Modifica o baralho: retira 5 cartas
    for _ in range(5):
        baralho.retirar_carta()
        
    assert len(baralho.cartas) == 35
    
    # Embaralha o baralho incompleto (não deve fazer diferença após reiniciar)
    baralho.embaralhar()
    
    # Reinicia o baralho
    baralho.reiniciar()
    
    # Verifica se o baralho voltou a ter 40 cartas
    assert len(baralho.cartas) == 40
    
    # Pega o estado após reiniciar
    cartas_reiniciadas = [str(c) for c in baralho.cartas]
    
    # Verifica se o estado reiniciado é IDÊNTICO ao estado original
    # (mesmas cartas, na mesma ordem inicial)
    assert cartas_reiniciadas == cartas_originais