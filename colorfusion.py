import pygame
import random
import os
from enfocate import GameBase, GameMetadata

class ColorFusion(GameBase):
    def __init__(self):
        metadata = GameMetadata(
            title="Color Fusion - Edición Motivadora",
            description="Lógica 2048 con Guía Lateral Ampliada",
            authors=["TuNombre"],
            group_number=7
        )
        super().__init__(metadata)
        
        # --- COLORES EXACTOS DE LA IMAGEN (Pasteles) ---
        self.colores = {
            0: (55, 60, 70),
            2: (255, 173, 173),    # Rosa
            4: (255, 214, 165),    # Naranja
            8: (253, 255, 182),    # Amarillo
            16: (202, 255, 191),   # Verde claro
            32: (155, 251, 192),   # Verde menta
            64: (160, 196, 255),   # Azul
            128: (189, 178, 255),  # Morado
            256: (255, 198, 255),  # Fucsia
            512: (255, 255, 252),  # Blanco
            1024: (152, 245, 255), # Cian
            2048: (255, 222, 173)  # Dorado
        }
        
        pygame.font.init()
        self.font_num = pygame.font.SysFont("Verdana", 40, bold=True)
        self.font_guia_txt = pygame.font.SysFont("Arial", 16, bold=True)
        
        self.tecla_liberada = True
        self.reset_game()

    def reset_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.generate_number()
        self.generate_number()

    def generate_number(self):
        vacias = [(i,j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if vacias:
            i, j = random.choice(vacias)
            self.board[i][j] = random.choice([2, 4])

    def update(self, dt):
        keys = pygame.key.get_pressed()
        # Detectar si alguna tecla de movimiento está siendo presionada
        presionada = keys[pygame.K_UP] or keys[pygame.K_w] or \
                     keys[pygame.K_DOWN] or keys[pygame.K_s] or \
                     keys[pygame.K_LEFT] or keys[pygame.K_a] or \
                     keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if presionada and self.tecla_liberada:
            moved = False
            if keys[pygame.K_UP] or keys[pygame.K_w]:    moved = self.move('U')
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  moved = self.move('D')
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:  moved = self.move('L')
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: moved = self.move('R')
            
            if moved:
                self.generate_number()
            self.tecla_liberada = False # Bloqueo hasta soltar la tecla
            
        if not presionada:
            self.tecla_liberada = True

    def move(self, dir):
        moved = False
        for i in range(4):
            # Extraer fila o columna según dirección
            line = self.board[i][:] if dir in ['L','R'] else [self.board[k][i] for k in range(4)]
            
            # Limpiar ceros y orientar según dirección
            temp = [x for x in (line[::-1] if dir in ['R','D'] else line) if x != 0]
            
            # Fusionar números iguales
            for k in range(len(temp)-1):
                if temp[k] == temp[k+1] and temp[k] != 0:
                    temp[k] *= 2
                    temp[k+1] = 0
            
            # Limpiar ceros post-fusión y rellenar hasta 4
            temp = [x for x in temp if x != 0]
            temp += [0]*(4-len(temp))
            
            # Volver a la orientación original si era necesario
            final = temp[::-1] if dir in ['R','D'] else temp
            
            if final != line:
                moved = True
                if dir in ['L','R']: self.board[i] = final
                else:
                    for k in range(4): self.board[k][i] = final[k]
        return moved

    def dibujar_columna_guia(self, screen, x_base, valores):
        # Configuración de tamaño de la guía (MÁS GRANDE)
        tam_cuadro = 42
        espaciado_y = 95
        
        for idx, val in enumerate(valores):
            y_pos = 70 + (idx * espaciado_y)
            
            # Texto de la operación (ej: 2+2=4)
            txt = self.font_guia_txt.render(f"{val}+{val}={val*2}", True, (200, 200, 200))
            screen.blit(txt, (x_base, y_pos))
            
            # Dibujo de la secuencia: [Cuadro] [Cuadro] - [Resultado]
            y_cuadros = y_pos + 25
            # Bloque 1
            pygame.draw.rect(screen, self.colores[val], (x_base, y_cuadros, tam_cuadro, tam_cuadro-5), border_radius=6)
            # Bloque 2
            pygame.draw.rect(screen, self.colores[val], (x_base + tam_cuadro + 10, y_cuadros, tam_cuadro, tam_cuadro-5), border_radius=6)
            # Guion
            pygame.draw.rect(screen, (120, 120, 120), (x_base + (tam_cuadro*2) + 15, y_cuadros + 18, 12, 4))
            # Bloque Resultado
            res_val = val * 2
            pygame.draw.rect(screen, self.colores.get(res_val, (255,255,255)), (x_base + (tam_cuadro*2) + 35, y_cuadros, tam_cuadro, tam_cuadro-5), border_radius=6)

    def draw(self, screen):
        screen.fill((43, 44, 48)) # Fondo gris oscuro
        sw, sh = screen.get_size()
        
        # --- GUÍAS LATERALES ---
        # Izquierda: 2 al 32
        self.dibujar_columna_guia(screen, 35, [2, 4, 8, 16, 32])
        # Derecha: 64 al 1024
        self.dibujar_columna_guia(screen, sw - 195, [64, 128, 256, 512, 1024])

        # --- TABLERO CENTRADO ---
        tile_size = 105
        gap = 12
        board_size = (tile_size * 4) + (gap * 5)
        bx = (sw - board_size) // 2
        by = (sh - board_size) // 2
        
        # Fondo del tablero
        pygame.draw.rect(screen, (34, 34, 38), (bx, by, board_size, board_size), border_radius=15)
        
        for i in range(4):
            for j in range(4):
                val = self.board[i][j]
                color = self.colores.get(val, (60, 60, 65))
                rx = bx + gap + (j * (tile_size + gap))
                ry = by + gap + (i * (tile_size + gap))
                
                pygame.draw.rect(screen, color, (rx, ry, tile_size, tile_size), border_radius=10)
                
                if val != 0:
                    # Texto del número con color gris oscuro para contraste
                    txt_surf = self.font_num.render(str(val), True, (90, 90, 90))
                    rect = txt_surf.get_rect(center=(rx + tile_size//2, ry + tile_size//2))
                    screen.blit(txt_surf, rect)