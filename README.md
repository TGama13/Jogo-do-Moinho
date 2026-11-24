# Jogo do Moinho

Uma implementação em Python do jogo do moinho (Mill), jogável no terminal. O projeto usa um tabuleiro 3×3 e permite enfrentar o computador em três níveis de dificuldade.

## Sobre o jogo

Cada jogador recebe três peças: um utiliza `X` e o outro utiliza `O`.

A partida é dividida em duas fases:

1. **Colocação:** os jogadores colocam alternadamente as suas peças em posições livres.
2. **Movimento:** depois de colocadas todas as peças, cada jogador pode mover uma peça para uma posição adjacente livre.

Ganha o jogador que consiga colocar as suas três peças numa linha ou coluna do tabuleiro.

## Requisitos

- Python 3
- Nenhuma dependência externa

## Como executar

No diretório do projeto, execute:

```bash
python main.py
```

Por padrão, o ficheiro inicia uma partida com o jogador humano a usar `[X]` e o computador no nível `facil`.

## Como jogar

O tabuleiro usa letras para as colunas (`a`, `b`, `c`) e números para as linhas (`1`, `2`, `3`).

### Colocar uma peça

Durante a fase de colocação, introduza apenas a posição desejada:

```text
b2
```

### Mover uma peça

Depois de todas as peças terem sido colocadas, introduza a origem seguida da posição de destino, sem espaço:

```text
b2b3
```

O destino deve estar adjacente à origem e não pode conter outra peça.

## Dificuldade do computador

O nível está configurado na chamada à função `moinho` em `main.py`:

- `facil`: escolhe o primeiro movimento livre disponível.
- `normal`: utiliza o minimax com profundidade limitada.
- `dificil`: utiliza o minimax com maior profundidade.

Exemplo:

```python
moinho('[X]', 'dificil')
```

Os símbolos disponíveis para o jogador humano são `[X]` e `[O]`.

## Estrutura do projeto

- `main.py`: implementação das estruturas de dados, regras do jogo, inteligência do computador e interface de terminal.
- `README.md`: documentação do projeto.

## Regras implementadas

- Validação de posições e movimentos.
- Colocação de peças em casas vazias.
- Movimento apenas para posições adjacentes.
- Detecção de vitória em linhas e colunas.
- Jogadas automáticas para o computador.
- Níveis fácil, normal e difícil.
- Implementação de minimax para a jogada automática.
