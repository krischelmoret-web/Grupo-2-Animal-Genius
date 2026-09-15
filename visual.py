import math
import pygame
from constants import const


class RenderizadorJuego:

    def __init__(self):

        ruta_fuente = const.FONTS_DIR / "OpenSans.ttf"
        self.fuente_texto = pygame.font.Font(str(ruta_fuente), 24)
        self.fuente_titulo = pygame.font.Font(str(ruta_fuente), 32)

        # Menú Principal
        self.rect_btn_jugar = pygame.Rect(
            const.ANCHO_PANTALLA // 2 - 150, 400, 300, 70
        )

        #Menú de Zonas
        centro_x, centro_y = const.ANCHO_PANTALLA // 2, const.ALTO_PANTALLA // 2 + 20
        radio_orbita = 220
        radio_circulo_imagen = 75

        angulos_zonas = {
            "pradera": math.radians(210),
            "bosque": math.radians(150),
            "selva": math.radians(85),
            "oceano": math.radians(20),
            "artico": math.radians(330),
        }

        self.zonas_circulos = {}
        for zona, angulo in angulos_zonas.items():
            x = int(centro_x + radio_orbita * math.cos(angulo))
            y = int(centro_y + radio_orbita * math.sin(angulo))
            self.zonas_circulos[zona] = {
                "centro": (x, y),
                "radio": radio_circulo_imagen,
            }

        # Menú de modos
        self.rects_modos = {
            "normal": pygame.Rect(const.ANCHO_PANTALLA // 2 - 175, 250, 350, 60),
            "preguntas": pygame.Rect(const.ANCHO_PANTALLA // 2 - 175, 330, 350, 60),
            "rasca": pygame.Rect(const.ANCHO_PANTALLA // 2 - 175, 410, 350, 60),
        }

        self._bloques_rasca = []

        ancho_b, alto_b = 350, 50
        espacio_x = 20  
        ancho_total_fila = (ancho_b * 2) + espacio_x
        inicio_x = (const.ANCHO_PANTALLA - ancho_total_fila) // 2

        x_izq = inicio_x
        x_der = inicio_x + ancho_b + espacio_x        
        y_arriba, y_abajo = 470, 535
        self.rects_opciones = [
            pygame.Rect(x_izq, y_arriba, ancho_b, alto_b),
            pygame.Rect(x_der, y_arriba, ancho_b, alto_b),
            pygame.Rect(x_izq, y_abajo, ancho_b, alto_b),
            pygame.Rect(x_der, y_abajo, ancho_b, alto_b),
        ]
        self._opciones_actuales = ["", "", "", ""]
        self._ultima_carta_procesada = None  

        # Ronda Sí / No 
        self.rect_btn_si = pygame.Rect(
            const.ANCHO_PANTALLA // 2 - 220, 480, 180, 70
        )
        self.rect_btn_no = pygame.Rect(
            const.ANCHO_PANTALLA // 2 + 40, 480, 180, 70
        )

    #PANTALLA 1: MENÚ PRINCIPAL

    def dibujar_menu_principal(self, pantalla) -> None:
        titulo = self.fuente_titulo.render(
            "Juego Educativo: Identifica el Animal", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 250))
        pantalla.blit(titulo, t_rect)

        pygame.draw.rect(
            pantalla, const.COLOR_BOTON, self.rect_btn_jugar, border_radius=15
        )
        txt_jugar = self.fuente_texto.render("JUGAR", True, const.COLOR_TEXTO)
        j_rect = txt_jugar.get_rect(center=self.rect_btn_jugar.center)
        pantalla.blit(txt_jugar, j_rect)

    def obtener_clic_menu_principal(self, pos_mouse: tuple[int, int]) -> bool:
        return self.rect_btn_jugar.collidepoint(pos_mouse)

    #PANTALLA 2: MENÚ DE ZONAS 

    def dibujar_menu_zonas(self, pantalla) -> None:
        titulo = self.fuente_titulo.render(
            "Selecciona una Zona", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 70))
        pantalla.blit(titulo, t_rect)

        centro_x, centro_y = (
            const.ANCHO_PANTALLA // 2,
            const.ALTO_PANTALLA // 2 + 20,
        )
        pygame.draw.circle(pantalla, (255, 255, 255), (centro_x, centro_y), 90)
        pygame.draw.circle(
            pantalla, (40, 150, 220), (centro_x, centro_y), 90, width=6
        )

        nombres_amigables = {
            "artico": "Ártico",
            "oceano": "Océano",
            "pradera": "Pradera",
            "selva": "Selva",
            "bosque": "Bosque",
        }

        imagenes_zonas = {
            "artico": "artico.jpg",
            "oceano": "oceano.jpg",
            "pradera": "pradera.jpg",
            "selva": "selva.jpg",
            "bosque": "bosque.jpg",
        }

        for zona, datos in self.zonas_circulos.items():
            cx, cy = datos["centro"]
            r = datos["radio"]

            try:
                nombre_archivo = imagenes_zonas.get(zona, "")
                ruta_img = const.IMAGES_DIR / nombre_archivo
                imagen = pygame.image.load(str(ruta_img)).convert()
                diametro = r * 2
                imagen = pygame.transform.scale(
                    imagen, (diametro, diametro)
                )

                mascara = pygame.Surface(
                    (diametro, diametro), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    mascara, (255, 255, 255, 255), (r, r), r
                )
                imagen.blit(
                    mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN
                )
                pantalla.blit(imagen, (cx - r, cy - r))
            except Exception:
                pygame.draw.circle(pantalla, (255, 255, 255), (cx, cy), r)

            pygame.draw.circle(
                pantalla, (76, 175, 80), (cx, cy), r, width=5
            )

            txt = self.fuente_texto.render(
                nombres_amigables[zona], True, (255, 255, 255)
            )
            rect_txt = txt.get_rect(center=(cx, cy + r - 10))
            rect_fondo_txt = rect_txt.inflate(28, 12)
            pygame.draw.rect(
                pantalla, (40, 50, 120), rect_fondo_txt, border_radius=12
            )
            pygame.draw.rect(
                pantalla,
                (255, 255, 255),
                rect_fondo_txt,
                width=2,
                border_radius=12,
            )
            pantalla.blit(txt, rect_txt)

    def obtener_clic_zona(self, pos_mouse: tuple[int, int]) -> str | None:
        x_mouse, y_mouse = pos_mouse
        for zona, datos in self.zonas_circulos.items():
            cx, cy = datos["centro"]
            radio = datos["radio"]
            if (x_mouse - cx) ** 2 + (y_mouse - cy) ** 2 <= radio**2:
                return zona
        return None

    # PANTALLA 3: MENÚ DE MODOS DE JUEGO 

    def dibujar_menu_modos(self, pantalla) -> None:
        titulo = self.fuente_titulo.render(
            "Selecciona un Modo de Juego", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 120))
        pantalla.blit(titulo, t_rect)

        nombres_modos = {
            "normal": "Modo Normal (Clásico)",
            "preguntas": "Modo Preguntas (Sí / No)",
            "rasca": "Modo Rasca y Gana",
        }

        for modo, rect in self.rects_modos.items():
            pygame.draw.rect(pantalla, const.COLOR_BOTON, rect, border_radius=12)
            pygame.draw.rect(pantalla, (40, 150, 220), rect, width=2, border_radius=12)
            
            txt_modo = self.fuente_texto.render(nombres_modos[modo], True, const.COLOR_TEXTO)
            m_rect = txt_modo.get_rect(center=rect.center)
            pantalla.blit(txt_modo, m_rect)

    def obtener_clic_menu_modos(self, pos_mouse: tuple[int, int]) -> str | None:
        for modo, rect in self.rects_modos.items():
            if rect.collidepoint(pos_mouse):
                return modo
        return None


    def _inicializar_grilla_rasca(self) -> None:
       self._bloques_rasca = []
       ancho_img = 440
       alto_img = 310
       centro_img_x = const.ANCHO_PANTALLA // 2
       centro_img_y = 225
        
       x_inicio = centro_img_x - (ancho_img // 2)
       y_inicio = centro_img_y - (alto_img // 2)
       tamanio_bloque = 12
        
       for x in range(x_inicio, x_inicio + ancho_img, tamanio_bloque):
            for y in range(y_inicio, y_inicio + alto_img, tamanio_bloque):
                self._bloques_rasca.append(
                    pygame.Rect(x, y, tamanio_bloque, tamanio_bloque)
                )

    def procesar_rasca_mouse(self, pos_mouse: tuple[int, int]) -> None:
        self._bloques_rasca = [
            b for b in self._bloques_rasca if not (b.collidepoint(pos_mouse) or 
            (abs(b.centerx - pos_mouse[0]) < 20 and abs(b.centery - pos_mouse[1]) < 20))
        ]

    # PANTALLA 4: JUEGO 

    def dibujar_interfaz(
        self, pantalla, carta_actual, puntuacion: int, mensaje: str, revelada: bool = False, modo: str = "normal"
    ) -> None:
        if carta_actual:
            if carta_actual != self._ultima_carta_procesada or (modo == "rasca" and not self._bloques_rasca):
                self._opciones_actuales = carta_actual.obtener_opciones_mezcladas()
                self._ultima_carta_procesada = carta_actual
                if modo == "rasca":
                    self._inicializar_grilla_rasca()

            ruta_img = const.IMAGES_DIR / carta_actual.nombre_imagen
            ancho_real = pantalla.get_width()
            centro_img_x = ancho_real // 2            
            centro_img_y = 225

            ancho_img = 440
            alto_img = 310

            try:
                imagen = pygame.image.load(str(ruta_img)).convert()
                
                imagen = pygame.image.load(str(ruta_img)).convert()
                imagen_escalada = pygame.transform.scale(imagen, (ancho_img, alto_img))
                
                pos_x = centro_img_x - (ancho_img // 2)
                pos_y = centro_img_y - (alto_img // 2)
                        
                pantalla.blit(imagen_escalada, (pos_x, pos_y))                        


                if modo == "rasca":      
                    for bloque in self._bloques_rasca:
                            pygame.draw.rect(pantalla, (150, 150, 150), bloque)
                            pygame.draw.rect(pantalla, (100, 100, 100), bloque, width=1)
            except Exception as e:
                print(f"Error cargando imagen: {e}")
                rect_error = pygame.Rect(0, 0, ancho_img, alto_img)
                rect_error.center = (centro_img_x, centro_img_y)
                pygame.draw.rect(pantalla, (220, 220, 220), rect_error)

            if modo != "rasca":
                rect_marco = pygame.Rect(0, 0, ancho_img, alto_img)
                rect_marco.center = (centro_img_x, centro_img_y)
                pygame.draw.rect(
                    pantalla,
                    (76, 175, 80),
                    rect_marco,
                    width=4,
                    border_radius=8,
                )

        for i, rect in enumerate(self.rects_opciones):
            pygame.draw.rect(
                pantalla, const.COLOR_BOTON, rect, border_radius=12
            )
            texto_opcion = self._opciones_actuales[i] if i < len(self._opciones_actuales) else ""
            txt_surf = self.fuente_texto.render(
                texto_opcion, True, const.COLOR_TEXTO
            )
            txt_rect = txt_surf.get_rect(center=rect.center)
            pantalla.blit(txt_surf, txt_rect)

        # Puntuación
        txt_puntos = self.fuente_titulo.render(
            f"Puntuación: {puntuacion}", True, const.COLOR_TEXTO_DARK
        )
        pantalla.blit(txt_puntos, (50, 30))

        # Mensajes de acierto / error
        if mensaje:
            txt_msg = self.fuente_titulo.render(mensaje, True, (46, 125, 50))
            msg_rect = txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 445))
            pantalla.blit(txt_msg, msg_rect)

    def obtener_opcion_clic(self, pos_mouse: tuple[int, int]) -> str | None:
        for i, rect in enumerate(self.rects_opciones):
            if rect.collidepoint(pos_mouse):
                return self._opciones_actuales[i]
        return None

    #PANTALLA 5: RONDA SÍ / NO 

    def dibujar_ronda_sino(
        self,
        pantalla,
        pregunta_actual,
        puntuacion: int,
        mensaje: str,
    ) -> None:
        titulo_ronda = self.fuente_titulo.render(
            "Ronda Rápida: ¿Sí o No?", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo_ronda.get_rect(center=(const.ANCHO_PANTALLA // 2, 100))
        pantalla.blit(titulo_ronda, t_rect)

        if pregunta_actual:
            txt_preg = self.fuente_titulo.render(
                pregunta_actual.enunciado, True, (30, 30, 30)
            )
            p_rect = txt_preg.get_rect(center=(const.ANCHO_PANTALLA // 2, 280))
            pantalla.blit(txt_preg, p_rect)

        pygame.draw.rect(
            pantalla, (76, 175, 80), self.rect_btn_si, border_radius=15
        )
        txt_si = self.fuente_titulo.render("SÍ", True, (255, 255, 255))
        si_rect = txt_si.get_rect(center=self.rect_btn_si.center)
        pantalla.blit(txt_si, si_rect)

        pygame.draw.rect(
            pantalla, (244, 67, 54), self.rect_btn_no, border_radius=15
        )
        txt_no = self.fuente_titulo.render("NO", True, (255, 255, 255))
        no_rect = txt_no.get_rect(center=self.rect_btn_no.center)
        pantalla.blit(txt_no, no_rect)

        txt_puntos = self.fuente_titulo.render(
            f"Puntuación: {puntuacion}", True, const.COLOR_TEXTO_DARK
        )
        pantalla.blit(txt_puntos, (const.ANCHO_PANTALLA - 280, 40))

        if mensaje:
            txt_msg = self.fuente_titulo.render(mensaje, True, (46, 125, 50))
            msg_rect = txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 630))
            pantalla.blit(txt_msg, msg_rect)

    def obtener_clic_sino(self, pos_mouse: tuple[int, int]) -> bool | None:
        if self.rect_btn_si.collidepoint(pos_mouse):
            return True
        if self.rect_btn_no.collidepoint(pos_mouse):
            return False
        return None


    def dibujar_indicadores_progreso(
        self, pantalla, total_preguntas: int, resultados: list[str]
    ) -> None:
        radio = 10
        espacio = 30
        ancho_total = (total_preguntas * espacio) - (espacio - (radio * 2))
        inicio_x = (const.ANCHO_PANTALLA - ancho_total) // 2
        y = 440

        for i in range(total_preguntas):
            x = inicio_x + (i * espacio)
            estado = resultados[i] if i < len(resultados) else "pendiente"

            if estado == "acierto":
                color_relleno = (76, 175, 80)
                color_borde = (56, 142, 60)
            elif estado == "fallo":
                color_relleno = (244, 67, 54)
                color_borde = (198, 40, 40)
            else:
                color_relleno = (255, 255, 255)
                color_borde = (76, 175, 80)

            pygame.draw.circle(pantalla, color_relleno, (x, y), radio)
            pygame.draw.circle(pantalla, color_borde, (x, y), radio, width=2)
