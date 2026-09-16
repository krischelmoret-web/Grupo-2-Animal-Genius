import math
import pygame
from constants import const

COLORES_BIOMAS = {
    "pradera": {"arriba": (255, 160, 50), "abajo": (180, 80, 15)},
    "bosque":  {"arriba": (240, 65, 65),  "abajo": (150, 20, 20)},
    "selva":   {"arriba": (110, 220, 90), "abajo": (35, 130, 45)},
    "artico":  {"arriba": (185, 125, 245),"abajo": (105, 45, 165)},
    "oceano":  {"arriba": (85, 165, 255), "abajo": (20, 65, 175)},
}


def crear_etiqueta_glossy(texto: str, fuente: pygame.font.Font, color_arriba: tuple, color_abajo: tuple) -> pygame.Surface:
    """Genera una placa estilo cápsula/píldora con degradado vertical, brillo glossy y contorno blanco."""
    txt_surf = fuente.render(texto, True, (255, 255, 255))
    tw, th = txt_surf.get_size()

    pad_x, pad_y = 22, 8
    w = tw + pad_x * 2
    h = th + pad_y * 2

    badge = pygame.Surface((w, h), pygame.SRCALPHA)

    grad_1x2 = pygame.Surface((1, 2), pygame.SRCALPHA)
    grad_1x2.set_at((0, 0), (*color_arriba, 255))
    grad_1x2.set_at((0, 1), (*color_abajo, 255))
    grad_surf = pygame.transform.smoothscale(grad_1x2, (w, h))

    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=h // 2)

    grad_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    badge.blit(grad_surf, (0, 0))

    brillo = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(brillo, (255, 255, 255, 110), (4, 2, w - 8, h // 2))
    brillo.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    badge.blit(brillo, (0, 0))

    pygame.draw.rect(badge, (255, 255, 255), (0, 0, w, h), width=4, border_radius=h // 2)

    sombra = fuente.render(texto, True, (0, 0, 0, 120))
    badge.blit(sombra, (pad_x + 1, pad_y + 2))
    badge.blit(txt_surf, (pad_x, pad_y))

    return badge


def crear_boton_glossy(
    texto: str, 
    fuente: pygame.font.Font, 
    ancho: int, 
    alto: int, 
    color_arriba: tuple = (100, 200, 255), 
    color_abajo: tuple = (30, 100, 200)
) -> pygame.Surface:
    """Genera un botón con forma de píldora, degradado lineal, efecto bisel y texto."""
    btn = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    grad_1x2 = pygame.Surface((1, 2), pygame.SRCALPHA)
    grad_1x2.set_at((0, 0), (*color_arriba, 255))
    grad_1x2.set_at((0, 1), (*color_abajo, 255))
    grad_surf = pygame.transform.smoothscale(grad_1x2, (ancho, alto))

    mask = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, ancho, alto), border_radius=alto // 2)

    grad_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    btn.blit(grad_surf, (0, 0))

    brillo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.ellipse(brillo, (255, 255, 255, 100), (6, 2, ancho - 12, alto // 2))
    brillo.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    btn.blit(brillo, (0, 0))

    pygame.draw.rect(btn, (255, 255, 255), (0, 0, ancho, alto), width=3, border_radius=alto // 2)

    txt_surf = fuente.render(texto, True, (255, 255, 255))
    sombra = fuente.render(texto, True, (0, 0, 0, 120))
    t_rect = txt_surf.get_rect(center=(ancho // 2, alto // 2))

    btn.blit(sombra, (t_rect.x + 1, t_rect.y + 2))
    btn.blit(txt_surf, t_rect)

    return btn


class RenderizadorJuego:

    def __init__(self):
        ruta_fuente = const.FONTS_DIR / "comic.ttf"
        self.fuente_texto = pygame.font.Font(str(ruta_fuente), 24)
        self.fuente_titulo = pygame.font.Font(str(ruta_fuente), 32)

        # 1. Definición de Rectángulos
        self.rect_btn_jugar = pygame.Rect(const.ANCHO_PANTALLA // 2 - 150, 400, 300, 70)
        self.rect_btn_musica = pygame.Rect(const.ANCHO_PANTALLA // 2 - 150, 490, 300, 50)

        centro_x, centro_y = const.ANCHO_PANTALLA // 2, const.ALTO_PANTALLA // 2 + 20
        radio_orbita_x = 340  
        radio_orbita_y = 140  
        radio_circulo_imagen = 95
        
        self.zonas_circulos = {
            "pradera": {"centro": (centro_x - radio_orbita_x, centro_y - radio_orbita_y), "radio": radio_circulo_imagen},
            "bosque":  {"centro": (centro_x - radio_orbita_x, centro_y + radio_orbita_y), "radio": radio_circulo_imagen},
            "artico":  {"centro": (centro_x + radio_orbita_x, centro_y - radio_orbita_y), "radio": radio_circulo_imagen},
            "oceano":  {"centro": (centro_x + radio_orbita_x, centro_y + radio_orbita_y), "radio": radio_circulo_imagen},
            "selva":   {"centro": (centro_x, centro_y), "radio": radio_circulo_imagen},            
        }

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

        self.rect_btn_si = pygame.Rect(const.ANCHO_PANTALLA // 2 - 220, 480, 180, 70)
        self.rect_btn_no = pygame.Rect(const.ANCHO_PANTALLA // 2 + 40, 480, 180, 70)
        self.rect_btn_reiniciar = pygame.Rect(const.ANCHO_PANTALLA // 2 - 160, 480, 320, 60)

        # 2. Carga de Fondos
        try:
            img_menu = pygame.image.load(str(const.IMAGES_DIR / "fondo_menu.jpg")).convert()
            self.fondo_menu = pygame.transform.scale(img_menu, (const.ANCHO_PANTALLA, const.ALTO_PANTALLA))

            img_modos = pygame.image.load(str(const.IMAGES_DIR / "fondo_modos.jpg")).convert()
            self.fondo_modos = pygame.transform.scale(img_modos, (const.ANCHO_PANTALLA, const.ALTO_PANTALLA))

            img_juego = pygame.image.load(str(const.IMAGES_DIR / "fondo_juego.jpg")).convert()
            self.fondo_juego = pygame.transform.scale(img_juego, (const.ANCHO_PANTALLA, const.ALTO_PANTALLA))
        except Exception as e:
            print(f"Error al cargar fondos, se usará color sólido de respaldo: {e}")
            self.fondo_menu = self.fondo_modos = self.fondo_juego = None

        # 3. PRE-RENDERIZADO Y CACHÉ DE BOTONES ESTÁTICOS
        self.surf_btn_jugar = crear_boton_glossy(
            "JUGAR", self.fuente_titulo, 
            self.rect_btn_jugar.width, self.rect_btn_jugar.height,
            color_arriba=(110, 220, 90), color_abajo=(35, 130, 45)
        )

        self.surf_btn_musica_on = crear_boton_glossy(
            "Música: Activada", self.fuente_texto,
            self.rect_btn_musica.width, self.rect_btn_musica.height,
            color_arriba=(110, 220, 90), color_abajo=(35, 130, 45)
        )

        self.surf_btn_musica_off = crear_boton_glossy(
            "Música: Silenciada", self.fuente_texto,
            self.rect_btn_musica.width, self.rect_btn_musica.height,
            color_arriba=(190, 190, 190), color_abajo=(100, 100, 100)
        )

        nombres_modos = {
            "normal": "Modo Normal (Clásico)",
            "preguntas": "Modo Preguntas (Sí / No)",
            "rasca": "Modo Rasca y Gana",
        }
        self.surfs_btn_modos = {
            modo: crear_boton_glossy(
                texto, self.fuente_texto,
                self.rects_modos[modo].width, self.rects_modos[modo].height,
                color_arriba=(85, 165, 255), color_abajo=(20, 65, 175)
            ) for modo, texto in nombres_modos.items()
        }

        self.surf_btn_si = crear_boton_glossy(
            "SÍ", self.fuente_titulo,
            self.rect_btn_si.width, self.rect_btn_si.height,
            color_arriba=(110, 220, 90), color_abajo=(35, 130, 45)
        )

        self.surf_btn_no = crear_boton_glossy(
            "NO", self.fuente_titulo,
            self.rect_btn_no.width, self.rect_btn_no.height,
            color_arriba=(240, 65, 65), color_abajo=(150, 20, 20)
        )

        self.surf_btn_reiniciar = crear_boton_glossy(
            "Volver al Menú", self.fuente_texto,
            self.rect_btn_reiniciar.width, self.rect_btn_reiniciar.height,
            color_arriba=(85, 165, 255), color_abajo=(20, 65, 175)
        )

        # 4. PRE-CORTAR Y PRE-RENDERIZAR ZONAS/BIOMAS Y ETIQUETAS
        nombres_amigables = {
            "artico": "Ártico", "oceano": "Océano", "pradera": "Pradera",
            "selva": "Selva", "bosque": "Bosque"
        }
        nombres_archivos = {
            "pradera": "pradera.jpg", "bosque": "bosque.jpg", "selva": "selva.jpg",
            "artico": "artico.jpg", "oceano": "oceano.jpg"
        }

        self.surfaces_circulos_zonas = {}
        self.badges_zonas = {}

        for zona, archivo in nombres_archivos.items():
            r = self.zonas_circulos[zona]["radio"]
            diametro = r * 2
            ruta = const.IMAGES_DIR / archivo

            # Recorte circular
            try:
                img_base = pygame.image.load(str(ruta)).convert()
                img_escalada = pygame.transform.smoothscale(img_base, (diametro, diametro)).convert_alpha()
                
                superficie_final = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
                mascara = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
                pygame.draw.circle(mascara, (255, 255, 255, 255), (r, r), r)

                superficie_final.blit(img_escalada, (0, 0))
                superficie_final.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                self.surfaces_circulos_zonas[zona] = superficie_final
            except Exception as e:
                print(f"Error procesando imagen circular para {zona}: {e}")
                self.surfaces_circulos_zonas[zona] = None

            # Etiqueta Glossy
            colores = COLORES_BIOMAS.get(zona, {"arriba": (180, 180, 180), "abajo": (80, 80, 80)})
            self.badges_zonas[zona] = crear_etiqueta_glossy(
                nombres_amigables.get(zona, zona),
                self.fuente_texto,
                colores["arriba"],
                colores["abajo"]
            )

        # 5. Variables de Caché Dinámico
        self._opciones_actuales = ["", "", "", ""]
        self._surfaces_opciones_actuales = []
        self._ultima_carta_procesada = None
        self._imagen_actual_escalada = None

    def dibujar_menu_principal(self, pantalla) -> None:
        titulo = self.fuente_titulo.render(
            "Juego Educativo: Identifica el Animal", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 250))
        pantalla.blit(titulo, t_rect)
        pantalla.blit(self.surf_btn_jugar, self.rect_btn_jugar)

    def obtener_clic_menu_principal(self, pos_mouse: tuple[int, int]) -> bool:
        return self.rect_btn_jugar.collidepoint(pos_mouse)

    def obtener_clic_boton_musica(self, pos: tuple[int, int]) -> bool:
        return self.rect_btn_musica.collidepoint(pos)

    def dibujar_boton_musica(self, pantalla, musica_activa: bool) -> None:
        btn = self.surf_btn_musica_on if musica_activa else self.surf_btn_musica_off
        pantalla.blit(btn, self.rect_btn_musica)

    def dibujar_menu_zonas(self, pantalla) -> None:
        if self.fondo_menu:
            pantalla.blit(self.fondo_menu, (0, 0))
        else:
            pantalla.fill((230, 240, 250))

        titulo = self.fuente_titulo.render(
            "Elige un lugar para explorar", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 70))
        pantalla.blit(titulo, t_rect)

        for zona, datos in self.zonas_circulos.items():
            cx, cy = datos["centro"]
            r = datos["radio"]

            surf_circulo = self.surfaces_circulos_zonas.get(zona)
            if surf_circulo:
                pantalla.blit(surf_circulo, (cx - r, cy - r))
            else:
                pygame.draw.circle(pantalla, (220, 220, 220), (cx, cy), r)

            pygame.draw.circle(pantalla, (76, 175, 80), (cx, cy), r, width=5)

            badge = self.badges_zonas[zona]
            rect_badge = badge.get_rect(center=(cx, cy + r - 10))
            pantalla.blit(badge, rect_badge)

    def obtener_clic_zona(self, pos_mouse: tuple[int, int]) -> str | None:
        x_mouse, y_mouse = pos_mouse
        for zona, datos in self.zonas_circulos.items():
            cx, cy = datos["centro"]
            radio = datos["radio"]
            if (x_mouse - cx) ** 2 + (y_mouse - cy) ** 2 <= radio**2:
                return zona
        return None

    def dibujar_menu_modos(self, pantalla) -> None:
        if self.fondo_modos:
            pantalla.blit(self.fondo_modos, (0, 0))
        else:
            pantalla.fill((230, 240, 250))

        titulo = self.fuente_titulo.render(
            "Selecciona un Modo de Juego", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 120))
        pantalla.blit(titulo, t_rect)

        for modo, rect in self.rects_modos.items():
            pantalla.blit(self.surfs_btn_modos[modo], rect)

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

    def dibujar_interfaz(
       self, pantalla, carta_actual, puntuacion: int, mensaje: str, 
       revelada: bool = False, modo: str = "normal", 
       tiempo_restante: float = 0.0, tiempo_agotado: bool = False
    ) -> None:
        if self.fondo_juego:
            pantalla.blit(self.fondo_juego, (0, 0))
        else:
            pantalla.fill((240, 240, 240))

        if carta_actual:
            # SÓLO recalcular opciones e imagen si la carta cambió o si se reinició el modo rasca
            if carta_actual != self._ultima_carta_procesada or (modo == "rasca" and not self._bloques_rasca):
                self._opciones_actuales = carta_actual.obtener_opciones_mezcladas()
                self._ultima_carta_procesada = carta_actual

                # Regenerar botones glossy para las nuevas opciones en caché
                self._surfaces_opciones_actuales = [
                    crear_boton_glossy(
                        op, self.fuente_texto,
                        rect.width, rect.height,
                        color_arriba=(255, 170, 60), color_abajo=(190, 85, 10)
                    ) for op, rect in zip(self._opciones_actuales, self.rects_opciones)
                ]

                if modo == "rasca":
                    self._inicializar_grilla_rasca()

                # Cargar y escalar la imagen una sola vez en memoria
                ruta_img = const.IMAGES_DIR / carta_actual.nombre_imagen
                try:
                    img_cruda = pygame.image.load(str(ruta_img)).convert()
                    self._imagen_actual_escalada = pygame.transform.scale(img_cruda, (440, 310))
                except Exception as e:
                    print(f"Error cargando imagen: {e}")
                    self._imagen_actual_escalada = None

            # Renderizado de la imagen en caché
            centro_img_x = pantalla.get_width() // 2            
            centro_img_y = 225
            pos_x = centro_img_x - 220
            pos_y = centro_img_y - 155

            if self._imagen_actual_escalada:
                pantalla.blit(self._imagen_actual_escalada, (pos_x, pos_y))
            else:
                pygame.draw.rect(pantalla, (220, 220, 220), (pos_x, pos_y, 440, 310))

            if modo == "rasca":       
                for bloque in self._bloques_rasca:
                    pygame.draw.rect(pantalla, (150, 150, 150), bloque)
                    pygame.draw.rect(pantalla, (100, 100, 100), bloque, width=1)
            else:
                rect_marco = pygame.Rect(pos_x, pos_y, 440, 310)
                pygame.draw.rect(pantalla, (76, 175, 80), rect_marco, width=4, border_radius=8)

        # Dibujar los botones de opciones (usando la superficie en caché)
        for i, rect in enumerate(self.rects_opciones):
            if i < len(self._surfaces_opciones_actuales):
                pantalla.blit(self._surfaces_opciones_actuales[i], rect)

        txt_puntos = self.fuente_titulo.render(
            f"Puntuación: {puntuacion}", True, const.COLOR_TEXTO_DARK
        )
        pantalla.blit(txt_puntos, (50, 30))

        if modo == "rasca":
            texto_tiempo = f"Tiempo: {int(tiempo_restante)}s" if not tiempo_agotado else "¡Tiempo agotado!"
            color_tiempo = (211, 47, 47) if tiempo_agotado else const.COLOR_TEXTO_DARK
            txt_tiempo = self.fuente_texto.render(texto_tiempo, True, color_tiempo)
            tiempo_rect = txt_tiempo.get_rect(center=(const.ANCHO_PANTALLA // 2, 40))
            pantalla.blit(txt_tiempo, tiempo_rect)

        if mensaje:
            txt_msg = self.fuente_titulo.render(mensaje, True, (46, 125, 50))
            msg_rect = txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 445))
            pantalla.blit(txt_msg, msg_rect)

    def obtener_opcion_clic(self, pos_mouse: tuple[int, int]) -> str | None:
        for i, rect in enumerate(self.rects_opciones):
            if rect.collidepoint(pos_mouse):
                return self._opciones_actuales[i]
        return None

    def dibujar_ronda_sino(
        self, pantalla, pregunta_actual, puntuacion: int, mensaje: str
    ) -> None:
        if self.fondo_juego:
            pantalla.blit(self.fondo_juego, (0, 0))
        else:
            pantalla.fill((240, 240, 240))

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

        pantalla.blit(self.surf_btn_si, self.rect_btn_si)
        pantalla.blit(self.surf_btn_no, self.rect_btn_no)

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

    def dibujar_pantalla_resultados(
        self, pantalla, puntuacion_final: int, total_posible: int, aciertos: int, fallos: int
    ) -> None:
        titulo = self.fuente_titulo.render(
            "¡Juego Terminado!", True, const.COLOR_TEXTO_DARK
        )
        t_rect = titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 140))
        pantalla.blit(titulo, t_rect)

        texto_puntos = f"Puntuación Final: {puntuacion_final} / {total_posible}"
        txt_score = self.fuente_texto.render(texto_puntos, True, (40, 50, 120))
        s_rect = txt_score.get_rect(center=(const.ANCHO_PANTALLA // 2, 210))
        pantalla.blit(txt_score, s_rect)

        txt_aciertos = self.fuente_texto.render(f"Aciertos: {aciertos}", True, (76, 175, 80))
        a_rect = txt_aciertos.get_rect(center=(const.ANCHO_PANTALLA // 2, 270))
        pantalla.blit(txt_aciertos, a_rect)

        txt_fallos = self.fuente_texto.render(f"Fallos: {fallos}", True, (244, 67, 54))
        f_rect = txt_fallos.get_rect(center=(const.ANCHO_PANTALLA // 2, 320))
        pantalla.blit(txt_fallos, f_rect)

        if aciertos >= fallos:
            mensaje = "¡Qué pedazo de cerebro! Me dejas impresionado."
            color_msg = (46, 125, 50)  
        else:
            mensaje = "¡No te desanimes! Sigue practicando para mejorar la próxima."
            color_msg = (211, 47, 47)  

        txt_msg = self.fuente_texto.render(mensaje, True, color_msg)
        m_rect = txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 390))
        pantalla.blit(txt_msg, m_rect)

        pantalla.blit(self.surf_btn_reiniciar, self.rect_btn_reiniciar)

    def obtener_clic_resultados(self, pos_mouse: tuple[int, int]) -> bool:
        return self.rect_btn_reiniciar.collidepoint(pos_mouse)

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
