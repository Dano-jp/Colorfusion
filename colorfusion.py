import pygame 
import sys
import random

# --- CONFIGURACIÓN DE PANTALLA ---
Width = 1280
Height = 720
board_size = 600  
cell_size = board_size // 4
offset_x = (Width - board_size) // 2
offset_y = (Height - board_size) // 2

# Colores
fondo_pantalla = (45, 45, 48)  
COLORES = {
    0: (55, 55, 60), 2: (255, 173, 173), 4: (255, 214, 165),
    8: (253, 255, 182), 16: (202, 255, 191), 32: (155, 246, 255),
    64: (160, 196, 255), 128: (189, 178, 255), 256: (255, 198, 255),
    512: (216, 226, 233), 1024: (178, 235, 242), 2048: (255, 229, 180),
}

# --- FRASES MOTIVADORAS ---
FRASES = [
    "¡No te rindas! Cada error es una lección.",
    "El éxito es la suma de pequeños esfuerzos.",
    "¡Casi lo logras! Inténtalo una vez más.",
    "Tu único rival es tu puntuación anterior.",
    "¡Ánimo! La persistencia vence al tablero.",
    "No es un fracaso, es un entrenamiento.",
    "¡Tú puedes! Mañana serás mejor que hoy.",
    "El camino al Colorfusion está lleno de intentos.",
    "¡Respira profundo y vuelve a empezar!",
    "La magia ocurre cuando no te detienes."
]

pygame.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("ColorFusion - Edición Motivadora")
clock = pygame.time.Clock()

board = [[0]*4 for _ in range(4)]
game_over = False
gamer_won = False
frase_actual = "" # Variable para guardar la frase del momento

# --- LÓGICA DEL JUEGO ---
def generate_new_number():
    empty = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        board[i][j] = random.choice([2, 4])

def compress(nums):
    new_nums = [num for num in nums if num != 0]
    nums[:] = new_nums + [0] * (4 - len(new_nums))

def merge(nums):
    global gamer_won
    for i in range(3):
        if nums[i] == nums[i+1] and nums[i] != 0:
            nums[i] *= 2
            nums[i+1] = 0
            if nums[i] == 2048: gamer_won = True

def move_left():
    moved = False
    for i in range(4):
        original = board[i][:]
        compress(board[i]); merge(board[i]); compress(board[i])
        if original != board[i]: moved = True
    return moved

def move_right():
    moved = False
    for i in range(4):
        original = board[i][:]
        row = board[i][::-1]
        compress(row); merge(row); compress(row)
        board[i] = row[::-1]
        if original != board[i]: moved = True
    return moved

def move_up():
    moved = False
    for j in range(4):
        col = [board[i][j] for i in range(4)]
        original = col[:]
        compress(col); merge(col); compress(col)
        for i in range(4): board[i][j] = col[i]
        if original != [board[i][j] for i in range(4)]: moved = True
    return moved

def move_down():
    moved = False
    for j in range(4):
        col = [board[i][j] for i in range(4)][::-1]
        original = col[::-1]
        compress(col); merge(col); compress(col)
        col = col[::-1]
        for i in range(4): board[i][j] = col[i]
        if original != [board[i][j] for i in range(4)]: moved = True
    return moved

def check_game_over():
    if any(0 in row for row in board): return False
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] or board[j][i] == board[j+1][i]: return False
    return True

def reset_game():
    global board, game_over, gamer_won
    board = [[0]*4 for _ in range(4)]
    game_over = False; gamer_won = False
    generate_new_number(); generate_new_number()

# --- FUNCIONES DE DIBUJO ---

def draw_color_guide():
    fuente_guia = pygame.font.SysFont("Verdana", 14, bold=True)
    evolucion = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    mitad = len(evolucion) // 2
    izq = evolucion[:mitad]
    der = evolucion[mitad:]
    
    def dibujar_seccion(x_start, lista):
        for i, val in enumerate(lista):
            y_pos = 110 + (i * 95)
            proximo = val * 2
            c1, c_res = COLORES.get(val), COLORES.get(proximo)
            pygame.draw.rect(screen, c1, (x_start, y_pos, 30, 30), border_radius=5)
            pygame.draw.rect(screen, c1, (x_start + 40, y_pos, 30, 30), border_radius=5)
            pygame.draw.rect(screen, (150, 150, 150), (x_start + 78, y_pos + 12, 12, 4))
            pygame.draw.rect(screen, c_res, (x_start + 100, y_pos, 30, 30), border_radius=5)
            txt = fuente_guia.render(f"{val}+{val}={proximo}", True, (220, 220, 220))
            screen.blit(txt, (x_start, y_pos + 35))

    dibujar_seccion(40, izq)
    dibujar_seccion(Width - 175, der)

def draw_screen():
    screen.fill(fondo_pantalla)
    draw_color_guide()
    fuente = pygame.font.SysFont("Verdana", 60, bold=True)
    
    pygame.draw.rect(screen, (35, 35, 38), (offset_x-10, offset_y-10, board_size+20, board_size+20), border_radius=20)

    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color_f = COLORES.get(value, COLORES[0])
            rect = pygame.Rect(offset_x + j * cell_size + 8, offset_y + i * cell_size + 8, cell_size - 16, cell_size - 16)
            pygame.draw.rect(screen, color_f, rect, border_radius=15)
            if value != 0:
                color_t = (max(0, color_f[0]-50), max(0, color_f[1]-50), max(0, color_f[2]-50))
                text_surf = fuente.render(str(value), True, color_t)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

    if gamer_won or game_over:
        overlay = pygame.Surface((Width, Height))
        color_overlay = (255, 229, 180) if gamer_won else (40, 40, 45)
        overlay.fill(color_overlay)
        overlay.set_alpha(210)
        screen.blit(overlay, (0, 0))
        
        msg = "¡Fusión Lograda!" if gamer_won else "Game Over"
        msg_font = pygame.font.SysFont("Verdana", 60, bold=True)
        txt = msg_font.render(msg, True, (200, 50, 50) if game_over else (100, 200, 100))
        screen.blit(txt, (Width//2 - txt.get_width()//2, Height//2 - 80))
        
        # --- DIBUJAR FRASE MOTIVADORA ---
        if game_over:
            fuente_frase = pygame.font.SysFont("Verdana", 30, italic=True)
            txt_frase = fuente_frase.render(frase_actual, True, (255, 255, 255))
            screen.blit(txt_frase, (Width//2 - txt_frase.get_width()//2, Height//2))

        sub_txt = pygame.font.SysFont("Verdana", 25).render("Presiona R para reiniciar", True, (150, 150, 150))
        screen.blit(sub_txt, (Width//2 - sub_txt.get_width()//2, Height//2 + 80))

# --- BUCLE PRINCIPAL ---
reset_game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if (game_over or gamer_won) and event.key == pygame.K_r:
                reset_game()
            elif not game_over and not gamer_won:
                moved = False
                if event.key == pygame.K_LEFT: moved = move_left()
                elif event.key == pygame.K_RIGHT: moved = move_right()
                elif event.key == pygame.K_UP: moved = move_up()
                elif event.key == pygame.K_DOWN: moved = move_down()
                
                if moved:
                    generate_new_number()
                    if check_game_over(): 
                        game_over = True
                        frase_actual = random.choice(FRASES) # Elige frase al perder

    draw_screen()
    pygame.display.flip()
    clock.tick(60)r


            