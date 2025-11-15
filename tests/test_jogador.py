# Arquivo: test_jogador.py
#
# Este arquivo contém os testes de unidade para a classe Jogador.
# O objetivo é garantir que um jogador possa ser criado, receber cartas,
# jogar cartas, e que seus métodos de cálculo de pontos (envido/flor)
# e de "cantar" (ações) estejam funcionando como esperado.
#
# Para rodar este teste, use o comando: pytest

import pytest
from truco.jogador import Jogador
from truco.carta import Carta
# Importamos as funções de envido e flor para verificar
# se o jogador as chama corretamente.
from truco import envido
from truco import flor

# --- Testes de Inicialização e Estado ---

def test_jogador_criacao():
    """
    Testa a criação (construtor __init__) de um jogador.
    Verifica se os atributos (ID, nome, eh_bot) são definidos corretamente.
    """
    jogador = Jogador(1, "João", eh_bot=False)
    
    assert jogador.id == 1
    assert jogador.nome == "João"
    assert jogador.eh_bot is False
    assert jogador.cartas_mao == []  # Deve começar com a mão vazia

def test_jogador_bot_criacao():
    """
    Testa a criação de um jogador que é um Bot.
    """
    bot = Jogador(2, "Bot_CPU", eh_bot=True)
    
    assert bot.id == 2
    assert bot.nome == "Bot_CPU"
    assert bot.eh_bot is True

def test_receber_cartas():
    """
    Testa o método 'receber_cartas'.
    Verifica se a mão do jogador é preenchida corretamente.
    """
    jogador = Jogador(1, "João")
    cartas = [
        Carta(1, 'Espadas'),
        Carta(7, 'Ouros'),
        Carta(3, 'Copas')
    ]
    
    jogador.receber_cartas(cartas)
    
    # Verifica se o jogador tem 3 cartas
    assert len(jogador.cartas_mao) == 3
    # Verifica se as cartas são as mesmas que foram passadas
    assert jogador.cartas_mao[0] == cartas[0]
    assert jogador.cartas_mao[1] == cartas[1]

def test_limpar_mao():
    """
    Testa o método 'limpar_mao'.
    Verifica se a mão do jogador fica vazia após a chamada.
    """
    jogador = Jogador(1, "João")
    cartas = [Carta(1, 'Espadas'), Carta(7, 'Ouros')]
    jogador.receber_cartas(cartas)
    
    assert len(jogador.cartas_mao) == 2  # Mão não está vazia
    
    jogador.limpar_mao()
    
    assert len(jogador.cartas_mao) == 0  # Mão deve estar vazia

# --- Testes de Ações (Jogar Carta) ---

def test_jogar_carta_por_indice():
    """
    Testa o método 'jogar_carta' usando um índice (ex: 0, 1, 2).
    Verifica se a carta correta é retornada e removida da mão.
    """
    jogador = Jogador(1, "João")
    carta1 = Carta(1, 'Espadas')
    carta2 = Carta(7, 'Ouros')
    jogador.receber_cartas([carta1, carta2]) # Mão: [As Espadas, 7 Ouros]
    
    # Jogador decide jogar a carta no índice 1 (7 Ouros)
    carta_jogada = jogador.jogar_carta(1)
    
    # Verifica se a carta jogada foi a 7 de Ouros
    assert carta_jogada.valor == 7
    assert carta_jogada.naipe == 'Ouros'
    
    # Verifica se a mão do jogador agora só tem 1 carta
    assert len(jogador.cartas_mao) == 1
    # Verifica se a carta restante é o As de Espadas
    assert jogador.cartas_mao[0].valor == 1
    assert jogador.cartas_mao[0].naipe == 'Espadas'

def test_jogar_carta_por_objeto():
    """
    Testa o método 'jogar_carta' passando o objeto Carta.
    (O seu código 'jogador.py' faz 'cartas_mao.pop(carta)', o que 
    implica que 'carta' é um índice. Vamos testar esse comportamento.)
    
    NOTA: A implementação atual em `jogador.py` (linha 22) assume que 
    'carta' é um ÍNDICE (int). Se 'carta' for um objeto Carta, 
    o `pop()` falhará com TypeError.
    
    Este teste valida a funcionalidade como ela está escrita (aceitando índice).
    """
    jogador = Jogador(1, "João")
    carta1 = Carta(1, 'Espadas')
    carta2 = Carta(7, 'Ouros')
    jogador.receber_cartas([carta1, carta2])
    
    # Jogando a carta no índice 0
    carta_jogada = jogador.jogar_carta(0)
    
    assert carta_jogada == carta1
    assert len(jogador.cartas_mao) == 1
    assert jogador.cartas_mao[0] == carta2

# --- Testes de Lógica de Pontos (Envido e Flor) ---

def test_get_pontos_envido():
    """
    Testa o método 'get_pontos_envido'.
    Verifica se ele calcula corretamente os pontos de envido da mão.
    """
    jogador = Jogador(1, "João")
    
    # Mão com envido de 27 (7+0 + 20)
    cartas_envido_27 = [Carta(7, 'Espadas'), Carta(12, 'Espadas'), Carta(1, 'Ouros')]
    jogador.receber_cartas(cartas_envido_27)
    assert jogador.get_pontos_envido() == 27
    
    jogador.limpar_mao()
    
    # Mão com envido de 6 (3+3, naipes diferentes)
    cartas_envido_6 = [Carta(3, 'Paus'), Carta(3, 'Copas'), Carta(1, 'Ouros')]
    jogador.receber_cartas(cartas_envido_6)
    assert jogador.get_pontos_envido() == 6

def test_tem_flor():
    """
    Testa o método 'tem_flor'.
    Verifica se ele identifica corretamente uma mão com flor (3 cartas do mesmo naipe).
    """
    jogador = Jogador(1, "João")

    # Mão COM flor
    cartas_com_flor = [Carta(1, 'Ouros'), Carta(7, 'Ouros'), Carta(5, 'Ouros')]
    jogador.receber_cartas(cartas_com_flor)
    assert jogador.tem_flor() is True
    
    jogador.limpar_mao()
    
    # Mão SEM flor
    cartas_sem_flor = [Carta(1, 'Espadas'), Carta(7, 'Ouros'), Carta(5, 'Ouros')]
    jogador.receber_cartas(cartas_sem_flor)
    assert jogador.tem_flor() is False

def test_get_pontos_flor():
    """
    Testa o método 'get_pontos_flor'.
    Verifica se ele calcula os pontos de flor corretamente.
    """
    jogador = Jogador(1, "João")
    
    # Mão com flor de 32 (5+7+0 + 20)
    cartas_flor_32 = [Carta(5, 'Ouros'), Carta(7, 'Ouros'), Carta(12, 'Ouros')]
    jogador.receber_cartas(cartas_flor_32)
    assert jogador.get_pontos_flor() == 32
    
    jogador.limpar_mao()
    
    # Mão sem flor (deve retornar 0 ou os pontos de envido, dependendo
    # da regra, mas a função 'flor.get_pontos_flor' deve lidar com isso)
    # A 'get_pontos_flor' do jogador chama 'flor.get_pontos_flor',
    # que por sua vez chama 'envido.get_pontos_envido' se não houver flor.
    cartas_sem_flor = [Carta(1, 'Espadas'), Carta(7, 'Ouros'), Carta(5, 'Ouros')]
    jogador.receber_cartas(cartas_sem_flor)
    
    # Deve retornar os pontos de envido (7+5 = 12)
    assert jogador.get_pontos_flor() == 12

# --- Testes de "Cantar" (Ações) ---
# Estes métodos em 'jogador.py' apenas retornam strings.

def test_cantar_acoes_simples():
    """
    Testa os métodos 'cantar_truco', 'cantar_envido', etc.
    Eles devem apenas retornar a string da ação correspondente.
    """
    jogador = Jogador(1, "João")
    
    assert jogador.cantar_truco() == 'TRUCO'
    assert jogador.cantar_envido() == 'ENVIDO'
    assert jogador.cantar_flor() == 'FLOR'
    assert jogador.aceitar() == 'ACEITO'
    assert jogador.nao_aceitar() == 'NAO ACEITO'