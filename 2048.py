import pygame
import sys
import random

# Largura e altura da janla
WIDTH = 400          
HEIGHT = 500         
GRID_SIZE = 4        
CELL_SIZE = WIDTH // GRID_SIZE   # Tamanho de cada célula
CELL_PADDING = 5     

# Cores utilizadas no jogo
BACKGROUND_COLOR = (187, 173, 160)       
TEXT_COLOR = (255, 165, 0)               
SCORE_COLOR = (255, 255, 255)            
BUTTON_COLOR = (0, 122, 204)            
BUTTON_HOVER_COLOR = (0, 150, 255)       
BUTTON_TEXT_COLOR = (255, 255, 255)      

# Start pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))    # puxa ali de cima o tamanho da janela
pygame.display.set_caption('2048')                  
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
#fontes dos texto
font = pygame.font.Font(None, 55)       
score_font = pygame.font.Font(None, 35)  
button_font = pygame.font.Font(None, 30) 

# INICIAR MÚSICAS
pygame.mixer.init()

# SONS DA PASTA SOUNDS
menu_sound = pygame.mixer.Sound("sounds/menu_sound.mp3")
game_sound = pygame.mixer.Sound("sounds/game_sound.mp3")
victory_sound = pygame.mixer.Sound("sounds/victory_sound.mp3")
lose_sound = pygame.mixer.Sound("sounds/lose_sound.mp3")
move_sound = pygame.mixer.Sound("sounds/move_sound.mp3")
merge_sound = pygame.mixer.Sound("sounds/merge_sound.mp3")

#Aktura do som
menu_sound.set_volume(0.2)
game_sound.set_volume(0.05)
victory_sound.set_volume(0.4)
lose_sound.set_volume(0.4)
move_sound.set_volume(0.1)
merge_sound.set_volume(0.1)

#Iniciar canais de auido
move_channel = pygame.mixer.Channel(1)
merge_channel = pygame.mixer.Channel(2)

#Imagens para cada numero
tile_images = {
    2: pygame.image.load("images/2.png"),
    4: pygame.image.load("images/4.png"),
    8: pygame.image.load("images/8.png"),
    16: pygame.image.load("images/16.png"),
    32: pygame.image.load("images/32.png"),
    64: pygame.image.load("images/64.png"),
    128: pygame.image.load("images/128.png"),
    256: pygame.image.load("images/256.png"),
    512: pygame.image.load("images/512.png"),
    1024: pygame.image.load("images/1024.png"),
    2048: pygame.image.load("images/2048.png"),
}

win_image = pygame.image.load("images/win.png")
lose_image = pygame.image.load("images/lose.png")

# Monta o tabuleiro do jogo, com os numeros e a pontuação
def draw_grid(board, score):
   
    screen.fill(BACKGROUND_COLOR) 

    # Loop para desenhar as células do tabuleiro
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            value = board[y][x]  
            rect = pygame.Rect(
                x * CELL_SIZE + CELL_PADDING,
                y * CELL_SIZE + CELL_PADDING + 100,  
                CELL_SIZE - 2 * CELL_PADDING,
                CELL_SIZE - 2 * CELL_PADDING
            )
            pygame.draw.rect(screen, BACKGROUND_COLOR, rect) 

            if value != 0:
                # Ajusta e redimensiona a imagem setadas acima
                image = pygame.transform.scale(tile_images[value], (rect.width, rect.height))
                screen.blit(image, rect)

              
                shadow_color = (0, 0, 0)  #cor preta pra realça o laranja
                shadow = font.render(str(value), True, shadow_color)
                shadow_rect = shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2))
                screen.blit(shadow, shadow_rect)

                text = font.render(str(value), True, TEXT_COLOR) #força o texto em cima das imagem, como se fosse 2 = 2,png
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        #demarca as linhas no eixo y na horizontal
        for y in range(GRID_SIZE + 1):
            pygame.draw.line(screen, (187, 173, 160), (0, y * CELL_SIZE + 100), (WIDTH, y * CELL_SIZE + 100))

   #demarca as linhas no eixo x na vertical
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, (187, 173, 160), (x * CELL_SIZE, 100), (x * CELL_SIZE, HEIGHT))

    # Score em cima da tela, com setado na linha 83
    score_text = score_font.render(f"Pontuação: {score}", True, SCORE_COLOR)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_text, score_rect)

    pygame.display.update()  # Atualiza a tela com o eixo x e y

def add_new_tile(board):
    # Lista de posições vazias
    empty_cells = [(y, x) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if board[y][x] == 0]

    if empty_cells:
        y, x = random.choice(empty_cells)  # Acha e escolhe um campo na grid vazio
        board[y][x] = random.choice([2, 4])  

def merge(row, score):
    #Função para juntar valores como por exemplo = 2 * 2 = 4
    new_row = [i for i in row if i != 0] 
    merged = False
    i = 0
    #sempre ele precisará multiplicar valores iguais, entre eles pra incrementar na peça e adicionar 10 pontos por merge

    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2  # Dobra o valor da peça
            #precisa do pop para remover 1 das peças para ser multiplicada na outra
            new_row.pop(i + 1) 
            score += 10  
            merged = True

            # toca o som de merge
            merge_channel.play(merge_sound, maxtime=200)
        i += 1

    # Preenche o resto da linha se não tive vazio com 0
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row, score

def move_left(board, score):
#função pra mover tudo as peça pra esquerda
    moved = False
    for y in range(GRID_SIZE):
        original_row = board[y][:]
        board[y], score = merge(board[y], score) 
        if board[y] != original_row:
            moved = True  
    return moved, score

def move_right(board, score):
#função pra mover tudo as peça pra direita
    moved = False
    for y in range(GRID_SIZE):
        original_row = board[y][:]
        row_reversed, score = merge(board[y][::-1], score)  # Inverte a linha pra mesclar
        board[y] = row_reversed[::-1]  #Volta pra traz na mesclagem 
        if board[y] != original_row:
            moved = True
    return moved, score

def move_up(board, score):
#função pra mover tudo as peça pra cima
    transposed_board = transpose(board)  # Transpõe o tabuleiro para reutilizar a lógica de movimento
    moved, score = move_left(transposed_board, score)

    # Atualiza o tabuleiro original com a transposição 
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            board[y][x] = transposed_board[x][y]
    return moved, score
    # Mesma logica para baixo

def move_down(board, score):
#função pra mover tudo as peça pra baixo
    transposed_board = transpose(board)
    moved, score = move_right(transposed_board, score)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            board[y][x] = transposed_board[x][y]
    return moved, score

def transpose(board):
    return [list(row) for row in zip(*board)]

def is_game_over(board):
# definição pra quando não tiver mais movimento no tabuleiro
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 0:
                return False # quando tiver vazio
            if x < GRID_SIZE - 1 and board[y][x] == board[y][x + 1]:
                return False  # Quando o na vertical, colado tiver iguais é possivel
            if y < GRID_SIZE - 1 and board[y][x] == board[y + 1][x]:
                return False  
    return True  #Quando não tiver mais movimentos

def has_won(board):
# def para vitorio quando alcançar o 2048, ajustado para 64 por testes
    for row in board:
        if 2048 in row:
            return True
    return False

def main_menu():
#Menu do jogo
    menu_sound.play(-1)  #som do menu

    while True:
        screen.fill(BACKGROUND_COLOR) 

        # TITULO
        title_font = pygame.font.Font(None, 70)
        title_text = title_font.render("2048", True, SCORE_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        # ENTER PARA ENTRA
        start_text = score_font.render("Pressione ENTER para jogar", True, SCORE_COLOR)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(start_text, start_rect)

        # ESC PARA SAIR
        exit_text = score_font.render("Pressione ESC para sair", True, SCORE_COLOR)
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(exit_text, exit_rect)

        # ENTRAR BRAZINO
        access_text = score_font.render("Acesse ", True, SCORE_COLOR)
        brazino_text = score_font.render("BRAZINO", True, (0, 0, 255))  
        access_rect = access_text.get_rect()
        brazino_rect = brazino_text.get_rect()

        total_width = access_rect.width + brazino_rect.width
        x_start = (WIDTH - total_width) // 2
        y_position = HEIGHT // 2 + 100  

        # Define as posições dos retângulos de texto
        access_rect.topleft = (x_start, y_position)
        brazino_rect.topleft = (x_start + access_rect.width, y_position)

        # Desenha os textos na tela
        screen.blit(access_text, access_rect)
        screen.blit(brazino_text, brazino_rect)

        pygame.display.update()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_sound.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_sound.stop()
                    game()   #puxa a func de jogo pra iniciar
                if event.key == pygame.K_ESCAPE:
                    menu_sound.stop()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  
                if brazino_rect.collidepoint(mouse_pos):
                    # link do brazino pra acessar puxando no clic
                    webbrowser.open("https://brazino777.com/pt")

def game():

    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)  # primeira peça
    add_new_tile(board)  # segunda peça
    score = 0  
    draw_grid(board, score)  #Grid de jogo inicial

    game_sound.play(-1)  #mantem o audio em loop

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_sound.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    moved, score = move_left(board, score)
                elif event.key == pygame.K_RIGHT:
                    moved, score = move_right(board, score)
                elif event.key == pygame.K_UP:
                    moved, score = move_up(board, score)
                elif event.key == pygame.K_DOWN:
                    moved, score = move_down(board, score)

                if moved:
                    # audio muito curto pra mover, mas caso seja alterado limitar o tempo do som
                    move_channel.play(move_sound, maxtime=200)
                    add_new_tile(board)  # Adiciona peça depois de todo o movimento
                    draw_grid(board, score)  # Atualiza o tabuleiro

                    if has_won(board):
                        # Quando ganhar o game
                        game_sound.stop()
                        victory_sound.play()
                        print("Você venceu!")
                        wait_for_menu(win=True)

                    elif is_game_over(board):
                        # Quando perder o game
                        game_sound.stop()
                        lose_sound.play(-1)  # som de derrota
                        print("Game Over!")
                        wait_for_menu(win=False)  

def wait_for_menu(win):
    #Exibe a tela de vitória ou derrota
    #botão de munu
    button_width = 150
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # ifelse para vitoria ou derrota para as imagens ou sons
    if win:
        end_image = win_image
        sound = victory_sound
    else:
        end_image = lose_image
        sound = lose_sound

    #limita a imagem
    end_image = pygame.transform.scale(end_image, (WIDTH, HEIGHT))

    while True:
        mouse_pos = pygame.mouse.get_pos()  
        mouse_pressed = pygame.mouse.get_pressed()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sound.stop()
                    main_menu()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    sound.stop()
                    main_menu()  

        #puxa a imagem de fim 
        screen.blit(end_image, (0, 0))

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  

        button_text = button_font.render("Menu", True, BUTTON_TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.update()

if __name__ == "__main__":
    main_menu()  
