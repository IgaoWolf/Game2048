# 2048 Game

Uma implementação em Python do clássico jogo 2048, com gráficos e sons personalizados.

## Índice

- [Introdução](#introdução)
- [Recursos](#recursos)
- [Instalação](#instalação)
  - [Clonar o Repositório](#clonar-o-repositório)
  - [Instalar Dependências](#instalar-dependências)
- [Como Jogar](#como-jogar)
  - [Controles](#controles)
  - [Objetivo do Jogo](#objetivo-do-jogo)
- [Regras do Jogo](#regras-do-jogo)
- [Créditos](#créditos)

## Introdução

Este é um jogo 2048 desenvolvido em Python, utilizando a biblioteca Pygame. O jogo apresenta gráficos personalizados e efeitos sonoros para melhorar a experiência do jogador.

## Instalação

### Clonar o Repositório

Para começar, clone o repositório do GitHub:

```bash
git clone https://github.com/IgaoWolf/Game2048.git
```

### Instalar Dependências

O jogo requer o **Python 3** e a biblioteca **Pygame**. Siga as etapas abaixo para instalar as dependências:

1. **Python 3**:

   - Verifique se o Python 3 está instalado executando `python3 --version` em seu terminal.
   - Caso não esteja instalado, faça o download em [python.org](https://www.python.org/downloads/) e siga as instruções de instalação para o seu sistema operacional.

2. **Pygame**:

   - Instale o Pygame usando o `pip`:

     ```bash
     pip install pygame
     ```

   - Ou, se estiver usando o `pip3`:

     ```bash
     pip3 install pygame
     ```

## Como Jogar

### Executar o Jogo

1. **Navegue até o diretório do jogo**:

   ```bash
   cd Game2048
   ```

2. **Inicie o jogo**:

   ```bash
   python 2048.py
   ```

   - Ou, se estiver usando `python3`:

     ```bash
     python3 2048.py
     ```

### Controles

- **Setas do Teclado**:

  - **↑** : Move as peças para cima.
  - **↓** : Move as peças para baixo.
  - **←** : Move as peças para a esquerda.
  - **→** : Move as peças para a direita.

- **Teclas Especiais**:

  - **M** : Retorna ao menu principal (após perder ou vencer).
  - **ESC** : Sai do jogo.

### Objetivo do Jogo

- **Alcance a peça de valor 2048** para vencer o jogo.

## Regras do Jogo

- **Mesclagem de Peças**: Quando duas peças com o mesmo número se tocam, elas se mesclam em uma só com o valor somado.
- **Adição de Novas Peças**: A cada movimento, uma nova peça de valor 2 ou 4 aparece em uma posição aleatória vazia.
- **Movimentos Válidos**: As peças se movem na direção escolhida até encontrarem outra peça ou a borda do tabuleiro.
- **Condições de Vitória**: O jogo é vencido quando o jogador atinge uma peça com o valor 2048.
- **Condições de Derrota**: O jogo termina quando não há mais movimentos possíveis (sem espaços vazios e sem peças adjacentes iguais).

## Créditos

- **Desenvolvedor**: [IgaoWolf](https://github.com/IgaoWolf)
- **Imagens e Sons**: Recursos personalizados localizados nas pastas `images` e `sounds`.

---

Aproveite o jogo e boa sorte em alcançar a peça 2048!