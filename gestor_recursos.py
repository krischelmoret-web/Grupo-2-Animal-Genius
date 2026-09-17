import pygame
from constants import const


class GestorRecursos:

    def __init__(self):
        # 1. Carga de Fuentes
        ruta_fuente = const.FONTS_DIR / "comic.ttf"
        self.fuente_texto = pygame.font.Font(str(ruta_fuente), 24)
        self.fuente_titulo = pygame.font.Font(str(ruta_fuente), 32)

        # 2. Carga y Escalado de Fondos
        self.fondos = self._cargar_fondos()

        # 3. Carga y Recorte Circular de Biomas
        self.circulos_biomas = self._cargar_circulos_biomas(radio=95)

    def _cargar_fondos(self) -> dict[str, pygame.Surface | None]:
        archivos = {
            "menu_principal": "fondo_menu_principal.jpg",
            "menu": "fondo_menu.jpg",
            "modos": "fondo_modos.jpg",
            "juego": "fondo_juego.jpg",
        }
        fondos = {}

        for clave, archivo in archivos.items():
            ruta = const.BACKGROUNDS_DIR / archivo
            try:
                img = pygame.image.load(str(ruta)).convert()
                fondos[clave] = pygame.transform.scale(
                    img, (const.ANCHO_PANTALLA, const.ALTO_PANTALLA)
                )
            except Exception as e:
                print(f"Error cargando fondo '{archivo}': {e}")
                fondos[clave] = None

        return fondos

    def _cargar_circulos_biomas(self, radio: int) -> dict[str, pygame.Surface | None]:
        archivos_biomas = {
            "pradera": "pradera.jpg",
            "bosque": "bosque.jpg",
            "selva": "selva.jpg",
            "artico": "artico.jpg",
            "oceano": "oceano.jpg",
        }
        diametro = radio * 2
        surfaces = {}

        for bioma, archivo in archivos_biomas.items():
            ruta = const.BACKGROUNDS_DIR / archivo
            try:
                img_base = pygame.image.load(str(ruta)).convert()
                img_escalada = pygame.transform.smoothscale(
                    img_base, (diametro, diametro)
                ).convert_alpha()

                # Aplicar máscara circular con canal Alpha
                superficie_final = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
                mascara = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
                pygame.draw.circle(mascara, (255, 255, 255, 255), (radio, radio), radio)

                superficie_final.blit(img_escalada, (0, 0))
                superficie_final.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                surfaces[bioma] = superficie_final
            except Exception as e:
                print(f"Error procesando imagen de bioma '{bioma}': {e}")
                surfaces[bioma] = None

        return surfaces

    def cargar_imagen_animal(
        self, nombre_archivo: str, ancho: int = 440, alto: int = 310
    ) -> pygame.Surface | None:
        ruta = const.IMAGES_DIR / nombre_archivo
        try:
            img = pygame.image.load(str(ruta)).convert()
            return pygame.transform.scale(img, (ancho, alto))
        except Exception as e:
            print(f"Error cargando imagen del animal '{nombre_archivo}': {e}")
            return None

    def cargar_logo(self, ancho: int = 400, alto: int = 200) -> pygame.Surface | None:
        ruta = const.BACKGROUNDS_DIR / "logo.png" # Nombre de tu archivo de logo
        try:
            img = pygame.image.load(str(ruta)).convert_alpha()
            return pygame.transform.smoothscale(img, (ancho, alto))
        except Exception as e:
            print(f"Error cargando el logo: {e}")
            return None
