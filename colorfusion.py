import pygame
import random
from enfocate import GameBase, GameMetadata

class ColorFusion(GameBase):
    def __init__(self):
        metadata = GameMetadata(
            title="Color Fusion",
            description="2048 con guía de colores lateral",
            authors=["Luis Lameda", "Genesis Bentancout", "Antonella Fermin", "Alexandra Cedeño"],
            group_number=8
        )
        super().__init__(metadata)

        # Colores Pastel
        self.COLORES = {
            0: (55, 55, 60), 2: (255, 173, 173), 4: (255, 214, 165),
            8: (253, 255, 182), 16: (202, 255, 191), 32: (155, 251, 192),
            64: (160, 196, 255), 128: (189, 178, 255), 256: (255, 198, 255),
            512: (255, 255, 252), 1024: (152, 245, 255), 2048: (255, 222, 173)
        }

        self.board = [[0]*4 for _ in range(4)]
        self.game_over = False
        self.tecla_liberada = True 
        self.mostrando_ayuda = True 

    def on_start(self):
        pygame.font.init()
        # Usamos una fuente un poco más gruesa para que el color se note mejor
        self.font = pygame.font.SysFont("Arial", 55, bold=True)
        self.font_guia = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_ayuda = pygame.font.SysFont("Arial", 24, bold=True)
        self.reset_game()

    def reset_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.generate_new_number()
        self.generate_new_number()

    def generate_new_number(self):
        empty = [(i,j) for i in range(4) for j in range(4) if self.board[i][j]==0]
        if empty:
            i,j = random.choice(empty)
            self.board[i][j] = random.choice([2,4])

    def compress(self, row):
        new = [i for i in row if i != 0]
        return new + [0]*(4-len(new))

    def merge(self, row):
        for i in range(3):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                row[i+1] = 0
        return row

    def move(self, direction):
        moved = False
        for i in range(4):
            if direction in ['LEFT', 'RIGHT']:
                row = self.board[i][:]
                if direction == 'RIGHT': row = row[::-1]
                row = self.compress(row)
                row = self.merge(row)
                row = self.compress(row)
                if direction == 'RIGHT': row = row[::-1]
                if row != self.board[i]:
                    self.board[i] = row
                    moved = True
            else:
                col = [self.board[k][i] for k in range(4)]
                if direction == 'DOWN': col = col[::-1]
                col = self.compress(col)
                col = self.merge(col)
                col = self.compress(col)
                if direction == 'DOWN': col = col[::-1]
                for k in range(4):
                    if self.board[k][i] != col[k]:
                        self.board[k][i] = col[k]
                        moved = True
        return moved

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        if self.mostrando_ayuda:
            if keys[pygame.K_SPACE]:
                self.mostrando_ayuda = False
            return 

        if self.tecla_liberada:
            moved = False
            if keys[pygame.K_LEFT]: moved = self.move('LEFT')
            elif keys[pygame.K_RIGHT]: moved = self.move('RIGHT')
            elif keys[pygame.K_UP]: moved = self.move('UP')
            elif keys[pygame.K_DOWN]: moved = self.move('DOWN')
            
            if moved:
                self.generate_new_number()
                self.tecla_liberada = False
        
        if not any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]]):
            self.tecla_liberada = True

    def dibujar_columna_guia(self, x_base, valores):
        tam_mini = 35
        y_inicial = 80
        for idx, val in enumerate(valores):
            y_pos = y_inicial + (idx * 100)
            txt = self.font_guia.render(f"{val}+{val}={val*2}", True, (200, 200, 200))
            self.surface.blit(txt, (x_base, y_pos - 20))
            pygame.draw.rect(self.surface, self.COLORES[val], (x_base, y_pos, tam_mini, tam_mini), border_radius=5)
            pygame.draw.rect(self.surface, self.COLORES[val], (x_base + 45, y_pos, tam_mini, tam_mini), border_radius=5)
            pygame.draw.rect(self.surface, (100, 100, 100), (x_base + 85, y_pos + 15, 10, 3))
            res_val = val * 2
            pygame.draw.rect(self.surface, self.COLORES.get(res_val, (255,255,255)), (x_base + 105, y_pos, tam_mini, tam_mini), border_radius=5)

    def draw(self):
        self.surface.fill((43, 43, 45))
        ancho, alto = self.surface.get_size()
        
        self.dibujar_columna_guia(50, [2, 4, 8, 16, 32])
        self.dibujar_columna_guia(ancho - 180, [64, 128, 256, 512, 1024])

        cell_size = 120
        gap = 10
        board_size = (cell_size * 4) + (gap * 5)
        offset_x, offset_y = (ancho - board_size) // 2, (alto - board_size) // 2

        pygame.draw.rect(self.surface, (34, 34, 34), (offset_x, offset_y, board_size, board_size), border_radius=15)

        for i in range(4):
            for j in range(4):
                val = self.board[i][j]
                color_fondo = self.COLORES.get(val, (60,60,65))
                rect = pygame.Rect(offset_x + gap + (j*(cell_size+gap)), offset_y + gap + (i*(cell_size+gap)), cell_size, cell_size)
                
                pygame.draw.rect(self.surface, color_fondo, rect, border_radius=8)
                
                if val != 0:
                    # CALCULAMOS UN COLOR BASADO EN EL FONDO (Más oscuro para contraste)
                    # Tomamos los valores R, G, B del bloque y los reducimos un 40%
                    txt_color = (
                        max(0, int(color_fondo[0] * 0.6)),
                        max(0, int(color_fondo[1] * 0.6)),
                        max(0, int(color_fondo[2] * 0.6))
                    )
                    
                    text = self.font.render(str(val), True, txt_color)
                    self.surface.blit(text, text.get_rect(center=rect.center))

        if self.mostrando_ayuda:
            overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.surface.blit(overlay, (0,0))

            cuadro_ayuda = pygame.Rect(0, 0, 500, 350)
            cuadro_ayuda.center = (ancho // 2, alto // 2)
            pygame.draw.rect(self.surface, (50, 50, 70), cuadro_ayuda, border_radius=20)
            pygame.draw.rect(self.surface, (255, 255, 255), cuadro_ayuda, 3, border_radius=20)

            tit = self.font_ayuda.render("¿CÓMO JUGAR?", True, (255, 255, 255))
            self.surface.blit(tit, tit.get_rect(center=(ancho//2, cuadro_ayuda.top + 50)))

            teclas_txt = [
                "Usa las FLECHAS del teclado",
                "para mover los bloques.",
                "¡Une colores iguales para ganar!"
            ]
            for i, linea in enumerate(teclas_txt):
                l_render = self.font_ayuda.render(linea, True, (200, 200, 200))
                self.surface.blit(l_render, l_render.get_rect(center=(ancho//2, cuadro_ayuda.top + 120 + (i*35))))

            cierre = self.font_ayuda.render("Presiona ESPACIO para comenzar", True, (255, 215, 0))
            self.surface.blit(cierre, cierre.get_rect(center=(ancho//2, cuadro_ayuda.bottom - 50)))