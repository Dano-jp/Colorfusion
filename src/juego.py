import pygame
import random
from enfocate import GameBase, GameMetadata
from .menu import Menu

class Juego:
    def __init__(self, surface):
        self.surface = surface

        # Paleta de colores pasteles amigables
        self.COLORES = {
            0: (55, 55, 60),
            2: (255, 173, 173), 4: (255, 214, 165), 8: (253, 255, 182),
            16: (202, 255, 191), 32: (155, 251, 192), 64: (160, 196, 255),
            128: (189, 178, 255), 256: (255, 198, 255), 512: (255, 255, 252),
            1024: (152, 245, 255), 2048: (255, 222, 173)
        }

        # Fuentes
        self.font = pygame.font.SysFont("Arial", 55, True)
        self.font_guia = pygame.font.SysFont("Arial", 18, True)
        self.font_ayuda = pygame.font.SysFont("Arial", 28, True)
        self.font_motivacion = pygame.font.SysFont("Arial", 35, True)
        self.font_pequena = pygame.font.SysFont("Arial", 20, True)

        self.frases_motivadoras = [
            "¡Vuelve a intentarlo, lo harás genial!",
            "¡Casi lo logras! ¡Una vez más!",
            "¡Tu esfuerzo es increíble, sigue así!",
            "¡Cada partida te hace más fuerte!",
            "¡No te rindas, eres un campeón!"
        ]
        
        self.modo = "color" 
        self.frase_actual = ""
        self.mostrando_ayuda = True 
        self.game_over = False
        self.tecla = True

        self.reset_game()

    def reset_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.game_over = False
        self.mostrando_ayuda = True 
        self.frase_actual = ""
        self.generate()
        self.generate()

    def generate(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = random.choice([2, 4])
    
    def check_game_over(self):
        if any(0 in row for row in self.board): return False
        for i in range(4):
            for j in range(4):
                val = self.board[i][j]
                if (i < 3 and val == self.board[i+1][j]) or (j < 3 and val == self.board[i][j+1]):
                    return False
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]: 
            self.mostrando_ayuda = True 
            return "menu"

        if self.mostrando_ayuda:
            if keys[pygame.K_1]: 
                self.modo = "color"
                self.mostrando_ayuda = False
            elif keys[pygame.K_2]:
                self.modo = "numeros"
                self.mostrando_ayuda = False
            return

        if self.game_over:
            if keys[pygame.K_r]: self.reset_game()
            return

        if self.tecla:
            moved = False
            if keys[pygame.K_LEFT]:    moved = self.move_general("LEFT")
            elif keys[pygame.K_RIGHT]: moved = self.move_general("RIGHT")
            elif keys[pygame.K_UP]:    moved = self.move_general("UP")
            elif keys[pygame.K_DOWN]:  moved = self.move_general("DOWN")
            
            if moved:
                self.generate()
                if self.check_game_over():
                    self.game_over = True
                    self.frase_actual = random.choice(self.frases_motivadoras)
                self.tecla = False 
        
        if not any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]]):
            self.tecla = True

    def draw(self):
        self.surface.fill((43, 43, 45))
        self.draw_board()
        self.draw_guide()
        
        # Texto de ayuda permanente para volver
        txt_esc = self.font_pequena.render("Presiona [ ESC ] para volver al menu", True, (150, 150, 150))
        self.surface.blit(txt_esc, (20, 20))
        
        if self.mostrando_ayuda: 
            self.draw_help_modo()
        elif self.game_over: 
            self.draw_game_over()

    def draw_board(self):
        size, gap = 110, 10
        offsetx, offsety = 400, 100
        pygame.draw.rect(self.surface, (30, 30, 35), (offsetx-10, offsety-10, 490, 490), border_radius=15)
        
        for i in range(4):
            for j in range(4):
                val = self.board[i][j]
                rect = pygame.Rect(offsetx + j*(size+gap), offsety + i*(size+gap), size, size)
                color_bloque = self.COLORES.get(val, (200, 200, 200))
                pygame.draw.rect(self.surface, color_bloque, rect, border_radius=8)
                
                if val != 0:
                    color_texto = color_bloque if self.modo == "color" else (60, 60, 60)
                    text = self.font.render(str(val), True, color_texto)
                    self.surface.blit(text, text.get_rect(center=rect.center))

    def draw_guide(self):
        self._render_column_guide([2, 4, 8, 16, 32], 50, 80)
        self._render_column_guide([64, 128, 256, 512, 1024], 950, 80)

    def _render_column_guide(self, valores, x, y_start):
        for i, v in enumerate(valores):
            y = y_start + i * 95
            c1 = self.COLORES[v]
            c_res = self.COLORES.get(v*2, (255,255,255))
            pygame.draw.rect(self.surface, c1, (x, y, 30, 30), border_radius=5)
            pygame.draw.rect(self.surface, c1, (x + 35, y, 30, 30), border_radius=5)
            pygame.draw.rect(self.surface, (100, 100, 100), (x + 72, y + 13, 10, 4))
            pygame.draw.rect(self.surface, c_res, (x + 90, y, 30, 30), border_radius=5)
            
            msg = "Une combinaciones" if self.modo == "color" else f"{v}+{v}={v*2}"
            txt = self.font_guia.render(msg, True, (180, 180, 180))
            self.surface.blit(txt, (x, y + 35))

    def draw_help_modo(self):
        w, h = self.surface.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 245)) 
        self.surface.blit(overlay, (0, 0))
        
        lineas = [
            ("¿COMO QUIERES JUGAR HOY?", (255, 214, 165)),
            ("", (0,0,0)),
            ("Presiona [ 1 ] : Solo por Colores", (255, 255, 255)),
            ("Presiona [ 2 ] : Colores y Numeros", (255, 255, 255)),
            ("", (0,0,0)),
            ("Usa las flechas para moverte", (155, 251, 192)),
            ("Presiona [ ESC ] para volver al menu", (255, 173, 173))
        ]
        for i, (texto, color) in enumerate(lineas):
            txt_surf = self.font_ayuda.render(texto, True, color)
            self.surface.blit(txt_surf, (w//2 - txt_surf.get_width()//2, 180 + i * 60))

    def draw_game_over(self):
        w, h = self.surface.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 225)) 
        self.surface.blit(overlay, (0, 0))
        
        txt_frase = self.font_motivacion.render(self.frase_actual, True, (155, 251, 192))
        self.surface.blit(txt_frase, (w//2 - txt_frase.get_width()//2, h//2 - 40))
        
        txt_r = self.font_ayuda.render("Presiona [ R ] para volver a intentar", True, (255, 255, 252))
        self.surface.blit(txt_r, (w//2 - txt_r.get_width()//2, h//2 + 60))

    def compress(self, line):
        new_line = [x for x in line if x != 0]
        return new_line + [0] * (4 - len(new_line))

    def merge(self, line):
        for i in range(3):
            if line[i] == line[i+1] and line[i] != 0:
                line[i] *= 2
                line[i+1] = 0
        return line

    def move_general(self, direction):
        moved = False
        for i in range(4):
            if direction in ["LEFT", "RIGHT"]: original_line = self.board[i][:]
            else: original_line = [self.board[j][i] for j in range(4)]
            temp_line = original_line[::-1] if direction in ["RIGHT", "DOWN"] else original_line[:]
            temp_line = self.compress(temp_line)
            temp_line = self.merge(temp_line)
            temp_line = self.compress(temp_line)
            final_line = temp_line[::-1] if direction in ["RIGHT", "DOWN"] else temp_line[:]
            if final_line != original_line:
                moved = True
                if direction in ["LEFT", "RIGHT"]: self.board[i] = final_line
                else:
                    for j in range(4): self.board[j][i] = final_line[j]
        return moved

class MiJuego(GameBase):
    def __init__(self):
        meta = GameMetadata(
            title="Color Fusion",
            description="Juego 2048 con colores pastel",
            authors=["Luis Lameda", "Genesis Bentancout", "Antonella Fermin", "Alexandra Cedeño"],
            group_number=8
        )
        super().__init__(meta)
        self.estado = "menu"

    def on_start(self):
        self.menu = Menu(self.surface)
        self.juego = Juego(self.surface)

    def update(self, dt):
        if self.estado == "menu":
            resultado = self.menu.update()
            if resultado == "jugar":
                self.juego.reset_game()
                self.estado = "juego"
            elif resultado == "salir":
                self.exit_game()
        elif self.estado == "juego":
            resultado = self.juego.update()
            if resultado == "menu":
                self.estado = "menu"

    def draw(self):
        if self.estado == "menu":
            self.menu.draw()
        else:
            self.juego.draw()