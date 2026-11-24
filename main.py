# imports
import copy
import random

# constants
TAMANHO_TABULEIRO = 3
MARKERS = {'X': 1, 'O': -1, ' ': 0}
ALFABETO = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z'
)

## TAD posicao (1,5 valores)

# construtor:
def cria_posicao(c, l):
    """
    Cria uma posicao, com coluna e linha
    """
    # se posicao nao e valida, mostra um erro
    if not eh_posicao_valida(c, l): raise ValueError('cria_posicao: argumentos invalidos')    
    return (c, l)

def cria_posicao_aleatoria():
    """
    Cria uma posicao aleatoria
    """
    c = random.choice(ALFABETO[0:TAMANHO_TABULEIRO])
    l = str(random.randint(1, TAMANHO_TABULEIRO))
    return cria_posicao(c, l)

def cria_copia_posicao(posicao):
    """
    Retorna uma copia da posicao
    """
    if not eh_posicao(posicao): raise ValueError('cria_copia_posicao: argumento invalido')
    return tuple(posicao)

# seletores:
def obter_pos_c(posicao):
    """
    Retorna a coluna da posicao
    """
    if not eh_posicao(posicao): raise ValueError('obter_pos_c: argumento invalido')
    return posicao[0]

def obter_pos_l(posicao):
    """
    Retorna a linha da posicao
    """
    if not eh_posicao(posicao): raise ValueError('obter_pos_l: argumento invalido')
    return posicao[1]

# reconhecedor:
def eh_posicao(arg):
    """
    Retorna True se arg for uma posicao e False caso contrario
    """
    return isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], str) and arg[1].isdigit()

def eh_posicao_valida(c, l):
    """
    Retorna se a posicao e valida ou nao
    """       
    # condicoes de posicao
    c_eh_valida = (isinstance(c, str) and c in ALFABETO[0:TAMANHO_TABULEIRO])    
    l_eh_valida = (isinstance(l, str) and l.isdigit() and int(l) >= 1 and int(l) <= TAMANHO_TABULEIRO)
    return c_eh_valida and l_eh_valida

# teste:
def posicoes_iguais(p1, p2):
    """
    Retorna True se a p1 e p2 sao iguais e False caso contrario
    """
    if not eh_posicao(p1) or not eh_posicao(p2): 
        raise ValueError('posicoes_iguais: argumentos invalidos')
    c1 = obter_pos_c(p1)
    l1 = obter_pos_l(p1)
    
    c2 = obter_pos_c(p2)
    l2 = obter_pos_l(p2)    
    return c1 == c2 and l1 == l2

# transformador:
def posicao_para_str(posicao):
    """
    Retorna a posicao em uma string
    """
    if not eh_posicao(posicao): raise ValueError('posicao_para_str: argumento invalido')
    c = obter_pos_c(posicao)
    l = obter_pos_l(posicao)    
    return f'{c}{l}'

def str_para_posicao(string):
    """
    Converte uma string como 'a1' numa posicao ('a', '1')
    Retorna None se o movimento for invalido
    """
    quantidade_digitos = 1 + len(str(TAMANHO_TABULEIRO))
    if not isinstance(string, str) or len(string) != quantidade_digitos:
        raise ValueError('str_para_posicao: argumento invalido')

    c = string[0]
    l = string[1]
    return cria_posicao(c, l)

def str_para_movimento(string):
    """
    Retorna um movimento como 'c2a1' num tuplo de duas posicoes
    Retorna None se o movimento for invalido
    """
    
    # quantidade de digitos para cada posicao
    quantidade_digitos = 1 + len(str(TAMANHO_TABULEIRO))

    # movimento tem sempre duas posicoes
    tamanho_necessario = 2 * quantidade_digitos
    if not isinstance(string, str) or len(string) != tamanho_necessario:
        raise ValueError('str_para_movimento: argumento invalido')

    # separar origem e destino
    origem_str  = string[0 : quantidade_digitos]
    destino_str = string[quantidade_digitos : tamanho_necessario]

    # converter as strings em posicoes
    origem = str_para_posicao(origem_str)
    destino = str_para_posicao(destino_str)
    return (origem, destino)

# funcao de alto nivel:
def obter_posicoes_adjacentes(posicao):
    """
    Retorna um tuplo com as posicoes adjacentes, inclui diagonais apenas 
    se a posicao estiver no meio ou nos cantos.
    """
    if not eh_posicao(posicao):
        raise ValueError('obter_posicoes_adjacentes: argumento invalido')

    c = obter_pos_c(posicao)
    l = obter_pos_l(posicao)
    c_idx = ALFABETO.index(c)
    l_idx = int(l) - 1

    adjacentes = []

    # flags de localizacao
    no_topo = l_idx == 0
    no_fundo = l_idx == TAMANHO_TABULEIRO - 1
    na_esquerda = c_idx == 0
    na_direita = c_idx == TAMANHO_TABULEIRO - 1

    eh_canto = (no_topo or no_fundo) and (na_esquerda or na_direita)
    eh_meio = not (no_topo or no_fundo or na_esquerda or na_direita)
    incluir_diagonais = eh_canto or eh_meio
    
    # cima-esquerda
    if incluir_diagonais:
        if l_idx - 1 >= 0 and c_idx - 1 >= 0:
            adjacentes.append(cria_posicao(ALFABETO[c_idx - 1], str(l_idx)))

    # cima
    if l_idx - 1 >= 0:
        adjacentes.append(cria_posicao(c, str(l_idx)))
                
    # cima-direita
    if incluir_diagonais:
        if l_idx - 1 >= 0 and c_idx + 1 < TAMANHO_TABULEIRO:
            adjacentes.append(cria_posicao(ALFABETO[c_idx + 1], str(l_idx)))

    # esquerda
    if c_idx - 1 >= 0:
        adjacentes.append(cria_posicao(ALFABETO[c_idx - 1], str(l_idx + 1)))
        
    # direita
    if c_idx + 1 < TAMANHO_TABULEIRO:
        adjacentes.append(cria_posicao(ALFABETO[c_idx + 1], str(l_idx + 1)))
            
    # baixo-esquerda
    if incluir_diagonais:
        if l_idx + 1 < TAMANHO_TABULEIRO and c_idx - 1 >= 0:
            adjacentes.append(cria_posicao(ALFABETO[c_idx - 1], str(l_idx + 2)))
    
    # baixo
    if l_idx + 1 < TAMANHO_TABULEIRO:
        adjacentes.append(cria_posicao(c, str(l_idx + 2)))    
    
    # baixo-direita
    if incluir_diagonais:
        if l_idx + 1 < TAMANHO_TABULEIRO and c_idx + 1 < TAMANHO_TABULEIRO:
            adjacentes.append(cria_posicao(ALFABETO[c_idx + 1], str(l_idx + 2)))    
    return tuple(adjacentes)

## TAD peca (1,5 valores)

# construtor
def cria_peca(marker):
    """
    Cria uma peca, com o marker
    """
    if not isinstance(marker, str) or marker not in MARKERS:
        raise ValueError('cria_peca: argumento invalido')    
    return tuple(marker)

def cria_copia_peca(peca):
    """
    Cria uma copia da peca
    """
    if not eh_peca(peca): raise ValueError('cria_copia_peca: argumento invalido')
    return tuple(peca)

# seletores
def obter_peca_marker(peca):
    """
    Retorna o marker da peca
    """
    if not eh_peca(peca): raise ValueError('obter_peca_marker: argumento invalido')
    return peca[0]    

# reconhecedor
def eh_peca(arg):
    """
    Retorna True se arg for uma peca e False caso contrario
    """
    return isinstance(arg, tuple) and len(arg) == 1 and isinstance(arg[0], str) and arg[0] in MARKERS

# teste
def pecas_iguais(p1, p2):
    """
    Retorna True se a p1 e p2 sao iguais e False caso contrario
    """
    if not eh_peca(p1) or not eh_peca(p2): raise ValueError('pecas_iguais: argumentos invalidos')
    return obter_peca_marker(p1) == obter_peca_marker(p2)

# transformador
def peca_para_str(peca):
    """
    Retorna a peca em uma string
    """
    if not eh_peca(peca): raise ValueError('peca_para_str: argumento invalido')
    return f'[{obter_peca_marker(peca)}]'

def str_para_peca(string: str):
    """
    Converte uma string no formato '[X]' de volta para uma peca
    """
    if not isinstance(string, str):
        raise ValueError("str_para_peca: argumento invalido")
    
    # verifica se comeca com '[' e termina com ']'
    if len(string) != 3 or string[0] != '[' or string[2] != ']':
        raise ValueError("str_para_peca: argumento invalido")
    
    # character no meio
    marker = string[1] 
    if not MARKERS[marker]:
        raise ValueError("str_para_peca: argumento invalido")
    
    # converte o marker em peca
    peca = cria_peca(marker)
    if not eh_peca(peca):
        raise ValueError("str_para_peca: peca invalida")
    
    return peca

# funcao de alto nivel:
def peca_para_inteiro(peca):
    """
    Retorna a peca em inteiro
    """
    if not eh_peca(peca): raise ValueError('peca_para_inteiro: argumento invalido')
    return MARKERS[obter_peca_marker(peca)]

## TAD tabuleiro (3 valores)

# construtor
def cria_tabuleiro():
    """ 
    Cria um tabuleiro
    """         
    cols = {}
    for c in range(TAMANHO_TABULEIRO):
        rows = {}
        for l in range(1, TAMANHO_TABULEIRO + 1):
            rows[str(l)] = cria_peca(' ')
        cols[ALFABETO[c]] = rows
    return cols

def cria_copia_tabuleiro(tabuleiro):
    """
    Cria uma copia do tabuleiro
    """
    if not eh_tabuleiro(tabuleiro): raise ValueError('cria_copia_tabuleiro: argumento invalido')
    return copy.deepcopy(tabuleiro)

# seletores
def obter_peca(tabuleiro, posicao):
    """
    Retorna a peca na posicao do tabuleiro
    """
    if not eh_posicao(posicao): raise ValueError('obter_peca: argumento invalido')
    c = obter_pos_c(posicao)
    l = obter_pos_l(posicao)
    return tabuleiro[c][l]

def obter_vetor(tabuleiro, index):
    """
    Retorna todas as pecas da linha ou coluna especificada
    pelo seu argumento
    """
    if not eh_tabuleiro or not isinstance(index, str): raise ValueError('obter_vetor: argumento invalido')
    vetor = []
    if index.isdigit():
        for c in range(TAMANHO_TABULEIRO):
            vetor.append(obter_peca(tabuleiro, cria_posicao(ALFABETO[c], index)))        
    else:
        for l in range(1, TAMANHO_TABULEIRO + 1):
            vetor.append(obter_peca(tabuleiro, cria_posicao(index, str(l))))
    return tuple(vetor)

def obter_vetor_num_pecas(tabuleiro, index, peca):
    """
    Retorna a quantidade da peca na linha ou coluna especificada
    """
    if not eh_tabuleiro or not isinstance(index, str) or not eh_peca(peca): 
        raise ValueError('obter_vetor: argumento invalido')
    
    num = 0
    vetor = obter_vetor(tabuleiro, index)
    for p in vetor:
        if pecas_iguais(peca, p):
            num += 1
    return num

def obter_num_pecas(tabuleiro, peca):
    """
    Retorna a quantidade da peca no tabuleiro
    """
    if not eh_peca(peca): raise ValueError('obter_num_pecas: argumento invalido')
    num = 0
    for l in range(1, TAMANHO_TABULEIRO + 1):
        vetor = obter_vetor(tabuleiro, str(l))
        for p in vetor:
            if pecas_iguais(peca, p):
                num += 1
    return num

# modificadores
def coloca_peca(tabuleiro, peca, posicao):
    """
    Coloca uma peca na posicao do tabuleiro
    """
    if not eh_tabuleiro(tabuleiro) or not eh_peca(peca) or not eh_posicao(posicao): raise ValueError('coloca_peca: argumento invalido')
    tabuleiro[obter_pos_c(posicao)][obter_pos_l(posicao)] = cria_copia_peca(peca)
    return tabuleiro

def remove_peca(tabuleiro, posicao):
    """
    Remove uma peca do tabuleiro
    """
    if not eh_tabuleiro(tabuleiro) or not eh_posicao(posicao): raise ValueError('remove_peca: argumento invalido')
    tabuleiro[obter_pos_c(posicao)][obter_pos_l(posicao)] = cria_peca(' ')
    return tabuleiro

def move_peca(tabuleiro, pos_1, pos_2):
    """
    Move a peca da pos_1 para a pos_2, deixando a pos_1 vazia
    """
    if not eh_tabuleiro(tabuleiro) or not eh_posicao(pos_1) or not eh_posicao(pos_2): raise ValueError('move_peca: argumento invalido')
    
    # verificar as adjacentes
    adjacentes = obter_posicoes_adjacentes(pos_1)
    if not pos_2 in adjacentes: raise ValueError('move_peca: movimento invalido')
    
    peca_1 = obter_peca(tabuleiro, pos_1)
    coloca_peca(tabuleiro, peca_1, pos_2)
    coloca_peca(tabuleiro, cria_peca(' '), pos_1)
    return tabuleiro

# reconhecedores
def eh_tabuleiro(arg):
    """
    Retorna True se arg for um tabuleiro e False caso contrario
    """
    # tem de ser dict
    if not isinstance(arg, dict): 
        return False
    
    # numero de colunas
    if len(arg) != TAMANHO_TABULEIRO: 
        return False

    # verificar cada coluna
    for c, l in arg.items():
        # coluna deve ser uma letra valida
        if c not in ALFABETO[0:TAMANHO_TABULEIRO]: 
            return False
        
        # linha deve ser dict
        if not isinstance(l, dict): 
            return False
        
        # numero de linhas
        if len(l) != TAMANHO_TABULEIRO: 
            return False
        
        # verificar cada linha
        for l, peca in l.items():
            # linha deve ser string numerica
            if not isinstance(l, str) or not l.isdigit(): 
                return False

            # linha dentro dos limites
            if int(l) < 1 or int(l) > TAMANHO_TABULEIRO: 
                return False
            
            # peca valida
            if not eh_peca(peca): 
                return False
    return True

def eh_posicao_livre(tabuleiro, posicao):
    """
    Retorna True se a posicao estiver livre, False caso contrario
    """
    peca = obter_peca(tabuleiro, posicao)
    return peca_para_inteiro(peca) == 0

# testes
def tabuleiro_iguais(t1, t2):
    """
    Retorna True se sao tabuleiros iguais, False caso contrario
    """    
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1 == t2

# transformador
def tabuleiro_para_str(tabuleiro):
    """
    Retorna o tabuleiro em uma string
    """
    linhas = {}
    string = ''
    
    # cabecalho de cima
    for c in range(TAMANHO_TABULEIRO):         
        letra = ALFABETO[c]
        if 0 not in linhas: linhas[0] = ''
        espaco = '   ' if c == 0 else '   '
        linhas[0] += espaco + letra
        
    # cabecalho da esquerda e o grid
    for l in range(TAMANHO_TABULEIRO):           
        linha_visual = l * 2 + 1  # linha real ("+1" para nao sobrescrever o cabecalho de cima)
        linha_espaco = linha_visual + 1  # linha de espacamento
        
        # adiciona a linha real
        linha_str = str(l + 1) + ' '
        for c in range(TAMANHO_TABULEIRO):      
            letra_coluna = ALFABETO[c]
            peca = obter_peca(tabuleiro, cria_posicao(letra_coluna, str(l + 1)))
            linha_str += peca_para_str(peca)
            if c < (TAMANHO_TABULEIRO - 1):
                linha_str += '-'
        linhas[linha_visual] = linha_str
        
        # se for 3x3 desenha as diagonais
        if TAMANHO_TABULEIRO == 3 and l < TAMANHO_TABULEIRO - 1:
            espaco = '   | '
            # linha conector com diagonais alternadas
            if l % 2 == 0:
                espaco = '   | \\ | / |'
            else:
                espaco = '   | / | \\ |'
                  
            linhas[linha_espaco] = espaco
        else:
            if l < (TAMANHO_TABULEIRO - 1):
                # adiciona a linha de espacamento                    
                espaco = ''
                for i in range(TAMANHO_TABULEIRO):
                    espaco += '   |'
                    if i < (TAMANHO_TABULEIRO - 1):
                        espaco += ''
                linhas[linha_espaco] = espaco
    
    # converte o dicionario de linhas em string
    for i in range(len(linhas)):
        string += linhas[i] if i == len(linhas) - 1 else linhas[i] + '\n'
    return string

def tuplo_para_tabuleiro(tuplo):
    """
    Retorna o tabuleiro que e representado pelo tuplo,
    cada um deles contendo n valores inteiros iguais
    a 1, -1 ou 0
    """
    # verifica as colunas
    if not isinstance(tuplo, tuple) or len(tuplo) != TAMANHO_TABULEIRO:
        raise ValueError('tuplo_para_tabuleiro: argumento invalido')
    
    # verificar cada linha
    for linha in tuplo:
        if not isinstance(linha, tuple) or len(linha) != TAMANHO_TABULEIRO:
            raise ValueError('tuplo_para_tabuleiro: argumento invalido')
        
        # verificar cada elemento
        for elem in linha:
            if elem not in MARKERS.values():
                raise ValueError('tuplo_para_tabuleiro: argumento invalido')
    
    # cria um tabuleiro vazio
    tabuleiro = cria_tabuleiro()
    
    # inverso: 1: 'X', -1: 'O', 0: ' '
    inv_markers = {}
    for k, v in MARKERS.items():
        # troca os valores de lugar
        inv_markers[v] = k    
    
    # coloca as pecas no tabuleiro
    for l in range(1, TAMANHO_TABULEIRO + 1):
        for c in range(TAMANHO_TABULEIRO):
            letra_coluna = ALFABETO[c]
            valor = tuplo[l - 1][c]
            peca = cria_peca(inv_markers[valor])
            coloca_peca(tabuleiro, peca, cria_posicao(letra_coluna, str(l)))
    return tabuleiro

# funcoes de alto nivel
def obter_ganhador(tabuleiro):
    """
    Retorna a peca do jogador que tenha as suas 3 pecas 
    em linha na vertical ou na horizontal no tabuleiro
    """
    if not eh_tabuleiro(tabuleiro):
        raise ValueError('obter_ganhador: argumento invalido')
    
    # verifica linhas
    for l in range(1, TAMANHO_TABULEIRO + 1):
        vetor = obter_vetor(tabuleiro, str(l))
        ganhador = vetor[0]
        
        # se a peca for vazia, avancar para a proxima linha
        if peca_para_inteiro(ganhador) == 0: continue
        
        # verificar se as pecas sao todas iguais, se nao, nao ganhou
        ganhou = True
        for peca in vetor:
            if not pecas_iguais(ganhador, peca):
                ganhou = False
                break
        if ganhou:
            return ganhador

    # verifica colunas
    for letra in ALFABETO[0:TAMANHO_TABULEIRO]:
        vetor = obter_vetor(tabuleiro, letra)
        ganhador = vetor[0]
        
        # se a peca for vazia, avancar para a proxima coluna
        if peca_para_inteiro(ganhador) == 0: continue
        
        # verificar se as pecas sao todas iguais, se nao, nao ganhou
        ganhou = True
        for peca in vetor:
            if not pecas_iguais(ganhador, peca):
                ganhou = False
                break
        if ganhou:
            return ganhador

    # se nao houver ganhador retorna peca vazia
    return cria_peca(' ')

def obter_posicoes_livres(tabuleiro):
    """
    Retorna todas as posicoes vazias no tabuleiro
    """
    posicoes = []
    # percorre colunas
    for letra in ALFABETO[0:TAMANHO_TABULEIRO]:
        # percorre linhas
        for num in range(1, TAMANHO_TABULEIRO + 1):
            pos = cria_posicao(letra, str(num))
            # verifica se a posicao esta vazia
            if eh_posicao_livre(tabuleiro, pos):          
                posicoes.append(pos)
    return tuple(posicoes)

def obter_posicoes_jogador(tabuleiro, peca_jogador):
    """
    Retorna todas as posicoes da peca do jogador no tabuleiro
    """
    posicoes = []
    # percorre colunas
    for letra in ALFABETO[0:TAMANHO_TABULEIRO]:
        # percorre linhas
        for num in range(1, TAMANHO_TABULEIRO + 1):
            pos = cria_posicao(letra, str(num))
            peca = obter_peca(tabuleiro, pos)
            # verifica se a peca pertence ao jogador
            if pecas_iguais(peca_jogador, peca):          
                posicoes.append(pos)
    return tuple(posicoes)

# funcoes adicionais
def obter_movimento_manual(tabuleiro, peca):
    """
    Permite ao jogador fazer uma jogada manual pelo terminal
    Na fase de colocacao devolve um tuplo com a posicao escolhida
    Na fase de movimento devolve um tuplo com origem e destino
    """
    if not eh_tabuleiro(tabuleiro) or not eh_peca(peca):
        raise ValueError('obter_movimento_manual: argumento invalido')
    num_pecas = obter_num_pecas(tabuleiro, peca)
    
    # fase de colocacao
    if num_pecas < TAMANHO_TABULEIRO:
        jogada = input("Turno do jogador. Escolha uma posicao: ")
        posicao = str_para_posicao(jogada)
        if posicao is None:
            raise ValueError('obter_movimento_manual: escolha invalida')
        
        # verificar se esta livre
        if not eh_posicao_livre(tabuleiro, posicao):
            raise ValueError('obter_movimento_manual: escolha invalida')
        return (posicao,)
    
    # fase de movimento
    jogada = input("Turno do jogador. Escolha um movimento: ")
    posicoes = str_para_movimento(jogada)
    if posicoes is None or len(posicoes) < 2:
        raise ValueError('obter_movimento_manual: escolha invalida')
    
    # separar as posicoes
    origem, destino = posicoes[0], posicoes[1]
    
    # verificar se a peca na origem pertence ao jogador
    if not pecas_iguais(peca, obter_peca(tabuleiro, origem)):
        raise ValueError('obter_movimento_manual: escolha invalida')
    
    # verificar se a posicao do destino esta livre
    if not eh_posicao_livre(tabuleiro, destino):
        raise ValueError('obter_movimento_manual: escolha invalida')    
    return posicoes

def minimax(tabuleiro, peca, profundidade, seq_movimentos):
    """
    Implementacao do minimax que retorna uma tupla (valor, seq_movimentos), 
    retorna o valor que resulta da avaliacao do tabuleiro 1 para X e -1 para O 
    e 0 para empate e a sequencia de movimentos que levou aquele valor.
    A funcao trata as duas fases do jogo (colocacao e movimento).
    """
    # condicao de paragem: profundidade zero ou ganhador
    if profundidade == 0 or peca_para_inteiro(obter_ganhador(tabuleiro)) != 0:
        return peca_para_inteiro(obter_ganhador(tabuleiro)), seq_movimentos

    melhor_seq = None
    if peca_para_inteiro(peca) == 1:
        melhor_valor = float('-inf')
    else:
        melhor_valor = float('inf')

    num_pecas = obter_num_pecas(tabuleiro, peca)
    if num_pecas < TAMANHO_TABULEIRO:
        # Fase de colocacao: tentar todas posicoes livres
        for pos in obter_posicoes_livres(tabuleiro):
            novo_tab = cria_copia_tabuleiro(tabuleiro)
            coloca_peca(novo_tab, peca, pos)
            novo_resultado = minimax(
                novo_tab,
                cria_peca('O') if peca_para_inteiro(peca) == 1 else cria_peca('X'),
                profundidade - 1,
                seq_movimentos + [(pos,)]
            )
            if peca_para_inteiro(peca) == 1:
                if novo_resultado[0] > melhor_valor or melhor_seq is None:
                    melhor_valor = novo_resultado[0]
                    melhor_seq = novo_resultado[1]
            else:
                if novo_resultado[0] < melhor_valor or melhor_seq is None:
                    melhor_valor = novo_resultado[0]
                    melhor_seq = novo_resultado[1]
    else:
        # Fase de movimento: tentar mover cada peca do jogador para adjacente livre
        for origem in obter_posicoes_jogador(tabuleiro, peca):
            for destino in obter_posicoes_adjacentes(origem):
                if eh_posicao_livre(tabuleiro, destino):
                    novo_tab = cria_copia_tabuleiro(tabuleiro)
                    move_peca(novo_tab, origem, destino)
                    novo_resultado = minimax(
                        novo_tab,
                        cria_peca('O') if peca_para_inteiro(peca) == 1 else cria_peca('X'),
                        profundidade - 1,
                        seq_movimentos + [(origem, destino)]
                    )
                    if peca_para_inteiro(peca) == 1:
                        if novo_resultado[0] > melhor_valor or melhor_seq is None:
                            melhor_valor = novo_resultado[0]
                            melhor_seq = novo_resultado[1]
                    else:
                        if novo_resultado[0] < melhor_valor or melhor_seq is None:
                            melhor_valor = novo_resultado[0]
                            melhor_seq = novo_resultado[1]
    return melhor_valor, (melhor_seq if melhor_seq is not None else seq_movimentos)

def obter_movimento_auto(tabuleiro, peca, nivel):
    """
    Faz uma movimento automatico, dependendo do nivel
    """
    if not eh_tabuleiro(tabuleiro) or not eh_peca(peca) or not isinstance(nivel, str):
        raise ValueError('obter_movimento_auto: argumento invalido')
    
    # quantidade de pecas do bot
    num_pecas = obter_num_pecas(tabuleiro, peca)
    
    ## fase de colocacao
    if num_pecas < TAMANHO_TABULEIRO:
        # 1. Vitoria: Se o jogador tiver (n - 1) das suas pecas em linha e uma posicao livre, entao
        # deve marcar na posicao livre (ganhando o jogo)
        
        # n - 1 pecas para considerar vitoria
        min_pecas = TAMANHO_TABULEIRO - 1
        peca_vazia = cria_peca(' ')
        jogador_peca = cria_peca('O') if peca_para_inteiro(peca) == 1 else cria_peca('X')
        
        # percorre as colunas
        for c in ALFABETO[:TAMANHO_TABULEIRO]:
            if obter_vetor_num_pecas(tabuleiro, c, peca) == min_pecas:
                vetor = obter_vetor(tabuleiro, c)
                if peca_vazia in vetor:
                    l = vetor.index(peca_vazia) + 1
                    return (cria_posicao(c, str(l)),)
    
        # percorre as linhas
        for l in range(1, TAMANHO_TABULEIRO + 1):
            if obter_vetor_num_pecas(tabuleiro, str(l), peca) == min_pecas:
                vetor = obter_vetor(tabuleiro, str(l))
                if peca_vazia in vetor:
                    c_index = vetor.index(peca_vazia)
                    return (cria_posicao(ALFABETO[c_index], str(l)),)
                
        #Bloqueio
        for i in range(0, TAMANHO_TABULEIRO):
            if obter_vetor_num_pecas(tabuleiro, ALFABETO[i], jogador_peca) == min_pecas:
                vetor = obter_vetor(tabuleiro, ALFABETO[i])
                if peca_vazia in vetor:
                    l = vetor.index(peca_vazia) + 1
                    return (cria_posicao(ALFABETO[i], str(l)),)
            if obter_vetor_num_pecas(tabuleiro, str(i + 1), jogador_peca) == min_pecas:
                vetor = obter_vetor(tabuleiro, str(i + 1))
                if peca_vazia in vetor:
                    l = vetor.index(peca_vazia)
                    return (cria_posicao(ALFABETO[l], str(i + 1)),)
                
        # Centro
        if eh_posicao_livre(tabuleiro, cria_posicao(ALFABETO[TAMANHO_TABULEIRO // 2], str(TAMANHO_TABULEIRO // 2 + 1))):
            return (cria_posicao(ALFABETO[TAMANHO_TABULEIRO // 2], str(TAMANHO_TABULEIRO // 2 + 1)),)
        
        # Cantos vazio
        cantos = [
            cria_posicao(ALFABETO[0], '1'),
            cria_posicao(ALFABETO[0], str(TAMANHO_TABULEIRO)),
            cria_posicao(ALFABETO[TAMANHO_TABULEIRO - 1], '1'),
            cria_posicao(ALFABETO[TAMANHO_TABULEIRO - 1], str(TAMANHO_TABULEIRO))
        ]
        for canto in cantos:
            if eh_posicao_livre(tabuleiro, canto):
                return (canto,)
            
        # Laterais vazios
        laterais = []
        for c in ALFABETO[0:TAMANHO_TABULEIRO]:
            for l in range(1, TAMANHO_TABULEIRO):
                pos = cria_posicao(c, str(l))
                if eh_posicao_livre(tabuleiro, pos):
                    return (pos,)
                
        
    ## fase de movimento
    if nivel == 'facil':
        for l in range(1, TAMANHO_TABULEIRO + 1):
            for c in ALFABETO[0:TAMANHO_TABULEIRO]:
                pos = cria_posicao(c, str(l))
                
                # verificar se e peca do bot
                if obter_peca(tabuleiro, pos) != peca:
                    continue
                
                # obter adjacentes
                adj = obter_posicoes_adjacentes(pos)
                
                # encontrar a primeira livre
                for destino in adj:
                    if eh_posicao_livre(tabuleiro, destino):
                        return (pos, destino)  # movimento encontrado    
    elif nivel == 'normal':
        valor, seq = minimax(tabuleiro, peca, 1, [])
        return seq[0] if seq else ()
    elif nivel == 'dificil':
        valor, seq = minimax(tabuleiro, peca, 5, [])
        return seq[0] if seq else ()
    else:
        raise ValueError('obter_movimento_auto: nivel invalido')
    return ()



def moinho(peca_jogador_humano, dificuldade):
    """
    Comeca o jogo do moinho, retorna o ganhador
    """
    if not isinstance(peca_jogador_humano, str) or not isinstance(dificuldade, str):
        raise ValueError('moinho: argumentos invalidos')
    
    # variaveis do jogo
    jogador = str_para_peca(peca_jogador_humano)
    adversario = cria_peca('O') if peca_para_inteiro(jogador) == 1 else cria_peca('X')
    tabuleiro = cria_tabuleiro()
    turno_do_jogador = True
    
    # funcoes
    def jogada_segura(peca):
        """
        Caso aconteca algum erro, vai avisar e tentar outra vez
        """
        if not eh_peca(peca):
            raise ValueError('jogada_segura: argumento invalido')
        
        while True:
            try:
                if turno_do_jogador:
                    m = obter_movimento_manual(tabuleiro, peca)
                    return m
                else:
                    m = obter_movimento_auto(tabuleiro, adversario, dificuldade)
                    return m               
            except ValueError as e:
                # avisar apenas quando e o jogador
                if turno_do_jogador: print('Erro:', e)
    
    def jogar_movimento(peca, movimento):
        """
        Decide qual o tipo de movimento
        """
        if not eh_peca(peca) or not isinstance(movimento, tuple):
            raise ValueError('jogar_movimento: argumento invalido')
        
        if len(movimento) == 1:
            coloca_peca(tabuleiro, peca, movimento[0])
        elif len(movimento) == 2:
            move_peca(tabuleiro, movimento[0], movimento[1])
        else:
            # isto nunca deve acontecer
            raise ValueError('jogar_movimento: movimento desconhecido')  
    
    # loop do jogo
    print(f'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {dificuldade}.')
    while True:
        print(tabuleiro_para_str(tabuleiro))
        ganhador = obter_ganhador(tabuleiro)
        if peca_para_inteiro(ganhador) != 0:
            return peca_para_str(ganhador)
        
        # decide quem vai jogar
        if turno_do_jogador:
            # repetir a jogada ate ser valida
            while True:
                m = jogada_segura(jogador)
                try:
                    jogar_movimento(jogador, m)
                except ValueError as e:
                    print('Erro:', e)
                    continue
                break
        else:
            print(f'Turno do computador ({dificuldade}):')
            m = jogada_segura(adversario)
            jogar_movimento(adversario, m)           
        # troca de turno
        turno_do_jogador = not turno_do_jogador
        
    # isto nunca deve acontecer
    raise ValueError('moinho: erro critico') 

## testes do código
ganhador = moinho('[X]', 'facil')
print(ganhador)