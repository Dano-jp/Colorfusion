import pygame
from pathlib import Path

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.opcion = 0
        self.tecla_liberada = True

        # Ajuste de ruta para que encuentre la carpeta 'fuente' en la raíz
        base = Path(__file__).parent.parent
        ruta_fuente = base / "fuente" / "Fuente.otf"
        ruta_fondo = base / "fuente" / "fondo2.jpeg"

        if ruta_fuente.exists():
            self.font_titulo = pygame.font.Font(str(ruta_fuente), 110)
            self.font = pygame.font.Font(str(ruta_fuente), 75)
        else:
            self.font_titulo = pygame.font.SysFont("Arial Black", 110)
            self.font = pygame.font.SysFont("Arial Black", 75)

        self.fondo = None
        if ruta_fondo.exists():
            img = pygame.image.load(str(ruta_fondo))
            self.fondo = pygame.transform.scale(img, surface.get_size())

    def draw_text_with_outline(self, text, font, color, outline_color, center_pos):
        text_surf = font.render(text, True, color)
        outline_surf = font.render(text, True, outline_color)
        rect = text_surf.get_rect(center=center_pos)
        
        grosor = 4
        for dx in range(-grosor, grosor + 1):
            for dy in range(-grosor, grosor + 1):
                if dx != 0 or dy != 0:
                    self.surface.blit(outline_surf, (rect.x + dx, rect.y + dy))
        self.surface.blit(text_surf, rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.tecla_liberada:
            if keys[pygame.K_DOWN]:
                self.opcion = 1
                self.tecla_liberada = False
            elif keys[pygame.K_UP]:
                self.opcion = 0
                self.tecla_liberada = False
            elif keys[pygame.K_RETURN]:
                self.tecla_liberada = False
                if self.opcion == 0: return "jugar"
                else: return "salir"

        if not any(keys):
            self.tecla_liberada = True

    def draw(self):
        if self.fondo:
            self.surface.blit(self.fondo, (0, 0))
        else:
            self.surface.fill((30, 30, 50))

        ancho, alto = self.surface.get_size()
        self.draw_text_with_outline("COLORFUSION", self.font_titulo, (255, 120, 120), (255, 255, 255), (ancho // 2, 180))

        opciones = ["JUGAR", "SALIR"]
        for i, texto in enumerate(opciones):
            pos_y = 400 + i * 140
            if i == self.opcion:
                btn_rect = pygame.Rect(0, 0, 350, 100)
                btn_rect.center = (ancho // 2, pos_y)
                pygame.draw.rect(self.surface, (255, 215, 0), btn_rect, 5, border_radius=15)
                render = self.font.render(texto, True, (255, 215, 0))
                self.surface.blit(render, render.get_rect(center=btn_rect.center))
            else:
                render = self.font.render(texto, True, (255, 255, 255))
                self.surface.blit(render, render.get_rect(center=(ancho // 2, pos_y)))