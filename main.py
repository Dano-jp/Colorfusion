import pygame
import os
import sys
from pathlib import Path
from enfocate import GameBase, GameMetadata
from colorfusion import ColorFusion

class MainMenu(GameBase):
    def __init__(self):
        metadata = GameMetadata(
            title="Menu Color Fusion",
            description="Menú principal con assets",
            authors=["TuNombre"],
            group_number=7
        )
        super().__init__(metadata)

        pygame.font.init()
        self.estado = "menu"
        self.opcion = 0
        self.juego = None
        self.tecla_bloqueada = False
        
        # --- RUTA DINÁMICA ---
        self.base_path = Path(__file__).parent.resolve()
        self.ruta_recursos = self.base_path / "fuente"
        
        # 1. CARGAR IMAGEN
        self.imagen_fondo_raw = None
        self.fondo_escalado = None
        ruta_foto = self.ruta_recursos / "fondo2.jpeg"
        
        if ruta_foto.exists():
            try:
                self.imagen_fondo_raw = pygame.image.load(str(ruta_foto))
            except Exception as e:
                print(f"❌ Error al cargar imagen: {e}")

        # 2. CARGAR FUENTE
        ruta_fuente_archivo = self.ruta_recursos / "Fuente.otf"
        if ruta_fuente_archivo.exists():
            self.font_titulo = pygame.font.Font(str(ruta_fuente_archivo), 110)
            self.font_botones = pygame.font.Font(str(ruta_fuente_archivo), 75)
        else:
            self.font_titulo = pygame.font.SysFont("Arial", 110, bold=True)
            self.font_botones = pygame.font.SysFont("Arial", 75, bold=True)

    def on_start(self):
        ancho, alto = self.surface.get_size()
        if self.imagen_fondo_raw:
            try:
                self.fondo_escalado = pygame.transform.scale(
                    self.imagen_fondo_raw.convert(), (ancho, alto)
                )
            except Exception as e:
                print(f"❌ Error en on_start: {e}")

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.estado == "menu":
            if not self.tecla_bloqueada:
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.opcion = 1
                    self.tecla_bloqueada = True
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.opcion = 0
                    self.tecla_bloqueada = True
                elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                    if self.opcion == 0:
                        self.juego = ColorFusion()
                        self.juego._surface = self.surface 
                        self.juego.on_start()
                        self.estado = "juego"
                    else:
                        pygame.quit()
                        sys.exit()
            
            if not any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_RETURN]]):
                self.tecla_bloqueada = False

        elif self.estado == "juego" and self.juego:
            if keys[pygame.K_ESCAPE]:
                self.estado = "menu"
                self.juego = None
            else:
                self.juego.update(dt)

    def draw(self):
        ancho, alto = self.surface.get_size()

        if self.fondo_escalado:
            self.surface.blit(self.fondo_escalado, (0, 0))
        else:
            self.surface.fill((28, 28, 56)) 

        if self.estado == "menu":
            # --- COLORES ---
            ROJO_PASTEL = (255, 120, 120)
            DORADO = (255, 215, 0)
            BLANCO = (255, 255, 255)

            # 2. Dibujar Título con BORDE BLANCO
            texto_str = "COLORFUSION"
            rect_titulo = self.font_titulo.render(texto_str, True, ROJO_PASTEL).get_rect(center=(ancho // 2, 180))
            
            # --- EFECTO DE BORDE (Dibujar en blanco desplazado) ---
            grosor = 3
            for dx in range(-grosor, grosor + 1):
                for dy in range(-grosor, grosor + 1):
                    if dx != 0 or dy != 0:
                        temp_borde = self.font_titulo.render(texto_str, True, BLANCO)
                        self.surface.blit(temp_borde, (rect_titulo.x + dx, rect_titulo.y + dy))

            # Dibujar el texto principal encima
            txt_titulo = self.font_titulo.render(texto_str, True, ROJO_PASTEL)
            self.surface.blit(txt_titulo, rect_titulo)

            # 3. Dibujar Botones
            botones = ["JUGAR", "SALIR"]
            posiciones_y = [380, 520]

            for i, texto in enumerate(botones):
                color_texto = DORADO if self.opcion == i else BLANCO
                txt_render = self.font_botones.render(texto, True, color_texto)
                rect_btn = txt_render.get_rect(center=(ancho // 2, posiciones_y[i]))
                
                if self.opcion == i:
                    borde_rect = rect_btn.inflate(60, 30) 
                    pygame.draw.rect(self.surface, DORADO, borde_rect, 5, 15)

                self.surface.blit(txt_render, rect_btn)

        elif self.estado == "juego" and self.juego:
            self.juego.draw()

if __name__ == "__main__":
    MainMenu().run_preview()