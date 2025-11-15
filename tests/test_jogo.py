# Arquivo: test_jogo.py
#
# Este arquivo contém os testes de INTEGRAÇÃO para a classe Jogo.
# O objetivo é garantir que o fluxo principal do jogo (nova mão,
# novas rodadas, jogar cartas, apostas e pontuação) funcione
# de ponta a ponta.
#
# Para testar a classe 'Jogo', que depende da 'Interface',
# usamos um 'Mock'. Um Mock é um objeto simulado que finge
# ser a Interface, permitindo-nos controlar o que o "usuário" faz.
#
# Para rodar, você precisa do 'pytest-mock': pip install pytest-mock
# Comando: pytest

import pytest
from unittest.mock import MagicMock  # A biblioteca para criar Mocks
from truco.jogo import Jogo
from truco.jogador import Jogador
from truco.carta import Carta

# --- Fixture de Configuração ---
# Uma 'fixture' é uma função que o Pytest roda ANTES de cada teste
# que a solicita. Ela é usada para configurar um estado limpo
# para cada teste, garantindo que um teste não interfira no outro.

@pytest.fixture
def jogo_com_mock(mocker):
    """
    Esta fixture cria uma instância limpa do 'Jogo' para cada teste.
    Ela também cria uma 'Interface' falsa (Mock) e a injeta no Jogo.
    
    'mocker' é uma fixture especial da biblioteca pytest-mock.
    """
    
    # 1. Cria a Interface Falsa
    # MagicMock() é um objeto que aceita qualquer chamada de método
    # sem dar erro e registra que foi chamado.
    mock_interface = MagicMock()
    
    # 2. Cria o Jogo
    # Passamos a interface falsa para o construtor do Jogo.
    jogo = Jogo(mock_interface)
    
    # 3. Substitui (Mocks) funções internas que dependem de aleatoriedade
    # Para que nossos testes sejam previsíveis, não podemos depender
    # do 'random' do baralho. Vamos "trapacear" e dizer quais
    # cartas cada jogador vai receber.
    
    # Mapeia as mãos que queremos
    mao_jogador_0 = [Carta(1, 'Espadas'), Carta(7, 'Espadas'), Carta(3, 'Copas')] # Mão forte
    mao_jogador_1 = [Carta(2, 'Paus'), Carta(4, 'Ouros'), Carta(5, 'Copas')]     # Mão fraca
    mao_jogador_2 = [Carta(1, 'Paus'), Carta(7, 'Ouros'), Carta(6, 'Copas')]     # Mão forte (parceiro)
    mao_jogador_3 = [Carta(10, 'Espadas'), Carta(11, 'Ouros'), Carta(12, 'Copas')] # Mão fraca (parceiro)
    
    # Simula a função 'retirar_carta' do baralho para retornar essas cartas
    # na ordem correta de distribuição (0, 1, 2, 3, 0, 1, 2, 3, ...)
    mock_baralho = jogo.baralho
    mocker.patch.object(mock_baralho, 'retirar_carta', side_effect=[
        # Rodada 1 de distribuição
        mao_jogador_0[0], mao_jogador_1[0], mao_jogador_2[0], mao_jogador_3[0],
        # Rodada 2 de distribuição
        mao_jogador_0[1], mao_jogador_1[1], mao_jogador_2[1], mao_jogador_3[1],
        # Rodada 3 de distribuição
        mao_jogador_0[2], mao_jogador_1[2], mao_jogador_2[2], mao_jogador_3[2],
    ])
    
    # Garante que o baralho será "embaralhado" (embora não afete o mock)
    mocker.patch.object(mock_baralho, 'embaralhar')
    
    # Retorna o jogo e o mock para serem usados no teste
    yield jogo, mock_interface

# --- Testes de Fluxo de Jogo ---

def test_nova_mao_distribui_cartas(jogo_com_mock):
    """
    Testa se o método 'nova_mao' distribui 3 cartas para cada jogador
    usando as cartas que definimos na fixture.
    """
    jogo, mock_interface = jogo_com_mock
    
    # Inicia a nova mão
    jogo.nova_mao()
    
    # Verifica se os jogadores receberam as cartas esperadas
    # Jogador 0 (Humano)
    assert len(jogo.jogadores[0].cartas_mao) == 3
    assert str(jogo.jogadores[0].cartas_mao[0]) == '1 de Espadas'
    assert str(jogo.jogadores[0].cartas_mao[1]) == '7 de Espadas'
    assert str(jogo.jogadores[0].cartas_mao[2]) == '3 de Copas'

    # Jogador 1 (Bot)
    assert len(jogo.jogadores[1].cartas_mao) == 3
    assert str(jogo.jogadores[1].cartas_mao[0]) == '2 de Paus'
    
    # Jogador 2 (Parceiro Humano)
    assert len(jogo.jogadores[2].cartas_mao) == 3
    assert str(jogo.jogadores[2].cartas_mao[0]) == '1 de Paus'

    # Jogador 3 (Parceiro Bot)
    assert len(jogo.jogadores[3].cartas_mao) == 3
    assert str(jogo.jogadores[3].cartas_mao[0]) == '10 de Espadas'
    
    # Verifica se a interface foi chamada para mostrar as mãos
    mock_interface.mostrar_maos.assert_called()
    # Verifica se o primeiro jogador é o 0
    assert jogo.jogador_atual == 0

def test_define_vencedor_rodada_nos_vencemos(jogo_com_mock):
    """
    Testa a lógica de 'define_vencedor_rodada'
    Cenário: Nós (J0) jogamos a carta mais forte.
    """
    jogo, mock_interface = jogo_com_mock
    jogo.nova_mao() # Define o J0 como "mão"

    # Simula as cartas jogadas na rodada
    jogo.cartas_jogadas_rodada = [
        (0, Carta(1, 'Espadas')), # J0 (Nós) - Mais forte (14)
        (1, Carta(1, 'Paus')),    # J1 (Eles) - (13)
        (2, Carta(7, 'Ouros')),   # J2 (Nós) - (11)
        (3, Carta(2, 'Copas'))    # J3 (Eles) - (9)
    ]
    
    # Define o primeiro jogador da rodada como 0
    jogo.primeiro_jogador_rodada = 0
    
    jogo.define_vencedor_rodada()
    
    # 'rodada_atual' deve ser 1 (próxima rodada)
    assert jogo.rodada_atual == 1
    # 'rodadas_ganhas' deve marcar vitória para 'nos'
    assert jogo.rodadas_ganhas['nos'] == 1
    assert jogo.rodadas_ganhas['eles'] == 0
    # O vencedor da rodada (J0) deve ser o primeiro a jogar na próxima
    assert jogo.primeiro_jogador_rodada == 0

def test_define_vencedor_rodada_empate(jogo_com_mock):
    """
    Testa a lógica de 'define_vencedor_rodada'
    Cenário: Empate (parda) na primeira rodada.
    """
    jogo, mock_interface = jogo_com_mock
    jogo.nova_mao() # Define o J0 como "mão"

    # Simula as cartas jogadas
    jogo.cartas_jogadas_rodada = [
        (0, Carta(1, 'Ouros')),   # J0 (Nós) - Valor 8
        (1, Carta(1, 'Copas')),   # J1 (Eles) - Valor 8 (Empate mais alto)
        (2, Carta(4, 'Paus')),    # J2 (Nós) - Valor 1
        (3, Carta(2, 'Copas'))    # J3 (Eles) - Valor 9 (Ops, J3 vence J1, mas J0/J2 vs J1/J3)
    ]
    
    # Cenário de empate mais realista:
    # J0 (Nós) joga 7 de Ouros (11)
    # J1 (Eles) joga 7 de Ouros (11) -> IMPOSSÍVEL no truco
    
    # Cenário de empate realista:
    # Maior carta 'Nós' (J0) é 3 de Copas (Valor 10)
    # Maior carta 'Eles' (J1) é 3 de Paus (Valor 10)
    jogo.cartas_jogadas_rodada = [
        (0, Carta(3, 'Copas')),   # J0 (Nós) - Valor 10
        (1, Carta(3, 'Paus')),    # J1 (Eles) - Valor 10
        (2, Carta(4, 'Paus')),    # J2 (Nós) - Valor 1
        (3, Carta(5, 'Copas'))    # J3 (Eles) - Valor 2
    ]
    
    jogo.primeiro_jogador_rodada = 0
    jogo.define_vencedor_rodada()
    
    # 'rodada_atual' deve ser 1 (próxima rodada)
    assert jogo.rodada_atual == 1
    # 'rodadas_ganhas' deve marcar empate
    assert jogo.rodadas_ganhas['nos'] == 1
    assert jogo.rodadas_ganhas['eles'] == 1
    # Quem joga é o "mão" original
    assert jogo.primeiro_jogador_rodada == 0 

def test_define_vencedor_mao_nos_vencemos(jogo_com_mock):
    """
    Testa 'define_vencedor_mao' quando 'Nós' ganhamos duas rodadas.
    """
    jogo, mock_interface = jogo_com_mock
    
    # Simula o estado: Jogo vale 1 ponto (NAO_CANTADO)
    # 'Nós' ganhamos 2 rodadas, 'Eles' 0.
    jogo.rodadas_ganhas = {'nos': 2, 'eles': 0}
    jogo.truco.get_pontos = MagicMock(return_value=1)
    
    jogo.define_vencedor_mao(motivo='JOGO_NORMAL')
    
    # Verifica se os pontos foram somados corretamente
    # 'mock_interface.add_pontos_partida' não existe, 
    # o 'jogo.py' chama 'jogo.placar.add_pontos_partida'
    pontos_finais = jogo.placar.get_pontos_partida()
    assert pontos_finais['nos'] == 1
    assert pontos_finais['eles'] == 0
    
    # Verifica se a interface foi atualizada
    mock_interface.atualizar_placar_partida.assert_called_with(0, 1)

def test_define_vencedor_mao_truco_nao_aceito(jogo_com_mock):
    """
    Testa 'define_vencedor_mao' quando o truco não é aceito.
    """
    jogo, mock_interface = jogo_com_mock
    
    # Simula o estado: 'Eles' (J1) cantaram Truco.
    jogo.truco.get_quem_cantou_por_ultimo = MagicMock(return_value=1) # J1 (Eles)
    
    # O valor de um truco não aceito é 1 ponto (o valor anterior)
    jogo.truco.get_pontos = MagicMock(return_value=1) 
    
    jogo.define_vencedor_mao(motivo='TRUCO_NAO_ACEITO')
    
    # 'Eles' (J1) cantaram e 'Nós' (J0) corremos. 'Eles' ganham 1 ponto.
    pontos_finais = jogo.placar.get_pontos_partida()
    assert pontos_finais['nos'] == 0
    assert pontos_finais['eles'] == 1
    
    # Verifica se a interface foi atualizada
    mock_interface.atualizar_placar_partida.assert_called_with(1, 0) # Pontos Eles, Pontos Nós

# --- Testes de 'executa_acao' (O Coração do Jogo) ---

def test_executa_acao_jogar_carta_humano(jogo_com_mock):
    """
    Testa o que acontece quando um jogador humano joga uma carta.
    """
    jogo, mock_interface = jogo_com_mock
    jogo.nova_mao() # Distribui cartas
    
    # Mão do J0: [As Espadas, 7 Espadas, 3 Copas]
    assert jogo.jogador_atual == 0
    assert len(jogo.jogadores[0].cartas_mao) == 3
    
    # Simulamos que o jogador clicou na carta de índice 0 (As Espadas)
    mock_interface.get_carta_selecionada = MagicMock(return_value=0)
    
    # Executa a ação
    jogo.executa_acao('JOGAR_CARTA', 0)
    
    # Verifica se a carta foi jogada
    assert len(jogo.cartas_jogadas_rodada) == 1
    assert str(jogo.cartas_jogadas_rodada[0][1]) == '1 de Espadas'
    
    # Verifica se a carta saiu da mão do jogador
    assert len(jogo.jogadores[0].cartas_mao) == 2
    assert str(jogo.jogadores[0].cartas_mao[0]) == '7 de Espadas' # A mão "andou"
    
    # Verifica se a vez passou para o próximo jogador (J1)
    assert jogo.jogador_atual == 1

def test_executa_acao_cantar_truco(jogo_com_mock):
    """
    Testa o que acontece quando um jogador humano canta TRUCO.
    """
    jogo, mock_interface = jogo_com_mock
    jogo.nova_mao()
    
    assert jogo.truco.get_estado() == 'NAO_CANTADO'
    assert jogo.jogador_atual == 0 # Vez do J0
    
    # J0 (Humano) canta TRUCO
    jogo.executa_acao('TRUCO', 0)
    
    # Verifica se o estado do truco mudou
    assert jogo.truco.get_estado() == 'TRUCO'
    assert jogo.truco.get_quem_cantou_por_ultimo() == 0
    
    # Verifica se a vez de responder foi para o adversário (J1)
    assert jogo.jogador_atual == 1
    
    # Verifica se a interface foi chamada para mostrar a ação
    mock_interface.mostrar_acao.assert_called_with(0, 'TRUCO')

def test_executa_acao_aceitar_truco(jogo_com_mock):
    """
    Testa o fluxo: J0 canta TRUCO, J1 (Bot) ACEITA.
    """
    jogo, mock_interface = jogo_com_mock
    jogo.nova_mao()
    
    # J0 (Humano) canta TRUCO
    jogo.executa_acao('TRUCO', 0)
    
    assert jogo.jogador_atual == 1 # Vez do J1 (Bot)
    
    # Simulamos que a IA (Bot) decidiu aceitar
    # (No seu código, Jogo chama 'bot.responder_truco()')
    # Vamos simular a resposta do bot diretamente
    mocker.patch.object(jogo.bot, 'responder_truco', return_value='ACEITO')
    
    # O Jogo agora deve processar a vez do Bot (J1)
    # No seu código, 'executa_acao_bot' é chamado
    jogo.executa_acao_bot()
    
    # Verifica se o estado do truco foi para ACEITO
    assert jogo.truco.get_estado() == 'TRUCO'
    assert jogo.truco.get_pontos() == 2 # Pontos em jogo agora são 2
    
    # A vez deve voltar para quem cantou (J0)
    assert jogo.jogador_atual == 0
    # A interface deve mostrar a resposta do bot
    mock_interface.mostrar_acao.assert_called_with(1, 'ACEITO')

def test_executa_acao_nao_aceitar_truco(jogo_com_mock):
    """
    Testa o fluxo: J0 canta TRUCO, J1 (Bot) NÃO ACEITA (Foge).
    """
    jogo, mock_interface = jogo_com_mock
    jogo.nova_mao()
    
    # J0 (Humano) canta TRUCO
    jogo.executa_acao('TRUCO', 0)
    
    assert jogo.jogador_atual == 1 # Vez do J1 (Bot)
    
    # Simulamos que a IA (Bot) decidiu NÃO aceitar
    mocker.patch.object(jogo.bot, 'responder_truco', return_value='NAO ACEITO')
    
    # O Jogo processa a vez do Bot (J1)
    jogo.executa_acao_bot()
    
    # O estado do truco deve ser 'NAO_ACEITO'
    assert jogo.truco.get_estado() == 'NAO_ACEITO'
    
    # Os pontos (1) devem ser somados para quem cantou (J0 - "Nós")
    pontos_finais = jogo.placar.get_pontos_partida()
    assert pontos_finais['nos'] == 1
    assert pontos_finais['eles'] == 0
    
    # A interface deve ter mostrado a fuga
    mock_interface.mostrar_acao.assert_called_with(1, 'NAO ACEITO')
    
    # A interface deve ter sido chamada para iniciar uma nova mão
    mock_interface.iniciar_nova_mao.assert_called()