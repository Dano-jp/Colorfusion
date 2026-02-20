import pygame
import os
import sys
from enfocate import GameBase, GameMetadata
from colorfusion import ColorFusion

class MainMenu(GameBase):
    def __init__(self):
        metadata = GameMetadata(
            title="Color Fusion",
            description="Menu Principal Centrado con Fondo",
            authors=["TuNombre"],
            group_number=7
        )
        super().__init__(metadata)
        self.estado = "menu"
        self.opcion = 0
        self.juego = None
        self.tecla_presionada = False

        pygame.font.init()
        
        # --- CARGA DE RECURSOS ---
        ruta_fondo = os.path.join("fuente", "fondo2.jpeg")
        try:
            self.imagen_fondo = pygame.image.load(ruta_fondo)
        except:
            self.imagen_fondo = None

        ruta_fuente = os.path.join("fuente", "Fuente.otf")
        try:
            self.fuente_titulo = pygame.font.Font(ruta_fuente, 110) # Título un poco más grande
        except:
            self.fuente_titulo = pygame.font.SysFont("Arial", 110, bold=True)
        
        self.fuente_btn = pygame.font.SysFont("Arial", 50, bold=True)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if self.estado == "menu":
            if not self.tecla_presionada:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.opcion = 0
                    self.tecla_presionada = True
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.opcion = 1
                    self.tecla_presionada = True
                elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                    if self.opcion == 0:
                        self.juego = ColorFusion()
                        self.estado = "juego"
                    else:
                        pygame.quit()
                        sys.exit()
            
            if not any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_RETURN]]):
                self.tecla_presionada = False

        elif self.estado == "juego" and self.juego:
            if keys[pygame.K_ESCAPE]:
                self.estado = "menu"
                self.juego = None
            else:
                self.juego.update(dt)

    def draw(self):
        screen = pygame.display.get_surface()
        if not screen: return
        
        ancho, alto = screen.get_size()

        if self.estado == "juego" and self.juego:
            self.juego.draw(screen)
        else:
            # --- DIBUJAR FONDO ---
            if self.imagen_fondo:
                fondo_escalado = pygame.transform.scale(self.imagen_fondo, (ancho, alto))
                screen.blit(fondo_escalado, (0, 0))
            else:
                screen.fill((43, 48, 58))

            # --- DIBUJAR TÍTULO (ARRIBA) ---
            tit_surf = self.fuente_titulo.render("COLOR FUSION", True, (158, 210, 232))
            tit_rect = tit_surf.get_rect(center=(ancho // 2, alto * 0.25)) # Posicionado al 25% de la altura
            # Sombra del título
            screen.blit(self.fuente_titulo.render("COLOR FUSION", True, (20, 20, 20)), (tit_rect.x + 4, tit_rect.y + 4))
            screen.blit(tit_surf, tit_rect)

            # --- DIBUJAR BOTONES (EN EL MEDIO) ---
            ancho_btn = 420
            alto_btn = 100
            espaciado = 130
            
            # Calculamos la posición inicial para que el grupo de botones esté centrado verticalmente
            # alto // 2 es el centro, restamos la mitad del bloque total de botones
            y_inicial = (alto // 2) - 50 

            for i, texto in enumerate(["JUGAR", "SALIR"]):
                # Rectángulo centrado horizontalmente
                rect = pygame.Rect(0, 0, ancho_btn, alto_btn)
                rect.center = (ancho // 2, y_inicial + (i * espaciado))
                
                col_btn = (245, 245, 225) if self.opcion == i else (40, 50, 65)
                col_txt = (40, 40, 40) if self.opcion == i else (245, 245, 225)
                
                # Dibujamos el botón con borde resaltado
                pygame.draw.rect(screen, col_btn, rect, border_radius=35)
                pygame.draw.rect(screen, (158, 210, 232), rect, width=4, border_radius=35)
                
                txt_surf = self.fuente_btn.render(texto, True, col_txt)
                screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

if __name__ == "__main__":
    MainMenu().run_preview()