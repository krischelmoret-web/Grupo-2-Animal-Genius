import pygame
from constants import const
from gestor_recursos import GestorRecursos
from ui_components import (
    crear_etiqueta_glossy,
    crear_boton_glossy,
    dibujar_indicadores_progreso, 
    aplicar_marco_capsula,
)


class RenderizadorJuego:

    def __init__(self):
        self.recursos = GestorRecursos()
        self.fuente_texto = self.recursos.fuente_texto
        self.fuente_titulo = self.recursos.fuente_titulo

        self._inicializar_rectangulos()

        self._inicializar_botones_estaticos()
        self._inicializar_badges_biomas()

        self._opciones_actuales = ["", "", "", ""]
        self._surfaces_opciones_actuales = []
        self._ultima_carta_procesada = None
        self._imagen_actual_escalada = None
        self._bloques_rasca = []

    def _inicializar_rectangulos(self) -> None:
        self.rect_btn_jugar = pygame.Rect(const.ANCHO_PANTALLA // 2 - 150, 400, 300, 70)
        self.rect_btn_musica = pygame.Rect(const.ANCHO_PANTALLA // 2 - 150, 490, 300, 50)

        centro_x, centro_y = const.ANCHO_PANTALLA // 2, const.ALTO_PANTALLA // 2 + 20
        radio_orbita_x, radio_orbita_y = 340, 140
        radio_circulo = 95

        self.zonas_circulos = {
            "pradera": {"centro": (centro_x - radio_orbita_x, centro_y - radio_orbita_y), "radio": radio_circulo},
            "bosque":  {"centro": (centro_x - radio_orbita_x, centro_y + radio_orbita_y), "radio": radio_circulo},
            "artico":  {"centro": (centro_x + radio_orbita_x, centro_y - radio_orbita_y), "radio": radio_circulo},
            "oceano":  {"centro": (centro_x + radio_orbita_x, centro_y + radio_orbita_y), "radio": radio_circulo},
            "selva":   {"centro": (centro_x, centro_y), "radio": radio_circulo},
        }

        self.rects_modos = {
            "normal": pygame.Rect(const.ANCHO_PANTALLA // 2 - 175, 250, 350, 60),
            "preguntas": pygame.Rect(const.ANCHO_PANTALLA // 2 - 175, 330, 350, 60),
            "rasca": pygame.Rect(const.ANCHO_PANTALLA // 2 - 175, 410, 350, 60),
        }

        ancho_b, alto_b, espacio_x = 350, 50, 20
        inicio_x = (const.ANCHO_PANTALLA - ((ancho_b * 2) + espacio_x)) // 2
        y_arriba, y_abajo = 470, 535

        self.rects_opciones = [
            pygame.Rect(inicio_x, y_arriba, ancho_b, alto_b),
            pygame.Rect(inicio_x + ancho_b + espacio_x, y_arriba, ancho_b, alto_b),
            pygame.Rect(inicio_x, y_abajo, ancho_b, alto_b),
            pygame.Rect(inicio_x + ancho_b + espacio_x, y_abajo, ancho_b, alto_b),
        ]

        self.rect_btn_si = pygame.Rect(const.ANCHO_PANTALLA // 2 - 220, 480, 180, 70)
        self.rect_btn_no = pygame.Rect(const.ANCHO_PANTALLA // 2 + 40, 480, 180, 70)
        self.rect_btn_reiniciar = pygame.Rect(const.ANCHO_PANTALLA // 2 - 160, 480, 320, 60)

    def _inicializar_botones_estaticos(self) -> None:
        self.surf_btn_jugar = crear_boton_glossy(
            "JUGAR", self.fuente_titulo, 300, 70, (110, 220, 90), (35, 130, 45)
        )
        self.surf_btn_musica_on = crear_boton_glossy(
            "Música: Activada", self.fuente_texto, 300, 50, (110, 220, 90), (35, 130, 45)
        )
        self.surf_btn_musica_off = crear_boton_glossy(
            "Música: Silenciada", self.fuente_texto, 300, 50, (190, 190, 190), (100, 100, 100)
        )
        self.surfs_btn_modos = {
            "normal": crear_boton_glossy("Modo Normal (Clásico)", self.fuente_texto, 350, 60, (85, 165, 255), (20, 65, 175)),
            "preguntas": crear_boton_glossy("Modo Preguntas (Sí / No)", self.fuente_texto, 350, 60, (85, 165, 255), (20, 65, 175)),
            "rasca": crear_boton_glossy("Modo Rasca y Gana", self.fuente_texto, 350, 60, (85, 165, 255), (20, 65, 175)),
        }
        self.surf_btn_si = crear_boton_glossy("SÍ", self.fuente_titulo, 180, 70, (110, 220, 90), (35, 130, 45))
        self.surf_btn_no = crear_boton_glossy("NO", self.fuente_titulo, 180, 70, (240, 65, 65), (150, 20, 20))
        self.surf_btn_reiniciar = crear_boton_glossy("Volver al Menú", self.fuente_texto, 320, 60, (85, 165, 255), (20, 65, 175))

    def _inicializar_badges_biomas(self) -> None:
        nombres_amigables = {
            "artico": "Ártico", "oceano": "Océano", "pradera": "Pradera",
            "selva": "Selva", "bosque": "Bosque"
        }
        self.badges_zonas = {}
        for zona, nombre in nombres_amigables.items():
            colores = const.COLORES_BIOMAS.get(zona, {"arriba": (180, 180, 180), "abajo": (80, 80, 80)})
            self.badges_zonas[zona] = crear_etiqueta_glossy(
                nombre, self.fuente_texto, colores["arriba"], colores["abajo"]
            )

    def dibujar_menu_principal(self, pantalla) -> None:
        titulo = self.fuente_titulo.render("Juego Educativo: Identifica el Animal", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(titulo, titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 250)))
        pantalla.blit(self.surf_btn_jugar, self.rect_btn_jugar)

    def obtener_clic_menu_principal(self, pos_mouse: tuple[int, int]) -> bool:
        return self.rect_btn_jugar.collidepoint(pos_mouse)

    def dibujar_boton_musica(self, pantalla, musica_activa: bool) -> None:
        btn = self.surf_btn_musica_on if musica_activa else self.surf_btn_musica_off
        pantalla.blit(btn, self.rect_btn_musica)

    def obtener_clic_boton_musica(self, pos: tuple[int, int]) -> bool:
        return self.rect_btn_musica.collidepoint(pos)

    def dibujar_menu_zonas(self, pantalla) -> None:
        fondo = self.recursos.fondos.get("menu")
        pantalla.blit(fondo, (0, 0)) if fondo else pantalla.fill((230, 240, 250))

        titulo = self.fuente_titulo.render("Elige un lugar para explorar", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(titulo, titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 70)))

        for zona, datos in self.zonas_circulos.items():
            cx, cy = datos["centro"]
            r = datos["radio"]

            surf_circulo = self.recursos.circulos_biomas.get(zona)
            if surf_circulo:
                pantalla.blit(surf_circulo, (cx - r, cy - r))
            else:
                pygame.draw.circle(pantalla, (220, 220, 220), (cx, cy), r)

            pygame.draw.circle(pantalla, (76, 175, 80), (cx, cy), r, width=5)

            badge = self.badges_zonas[zona]
            pantalla.blit(badge, badge.get_rect(center=(cx, cy + r - 10)))

    def obtener_clic_zona(self, pos_mouse: tuple[int, int]) -> str | None:
        x_mouse, y_mouse = pos_mouse
        for zona, datos in self.zonas_circulos.items():
            cx, cy = datos["centro"]
            if (x_mouse - cx) ** 2 + (y_mouse - cy) ** 2 <= datos["radio"] ** 2:
                return zona
        return None

    def dibujar_menu_modos(self, pantalla) -> None:
        fondo = self.recursos.fondos.get("modos")
        pantalla.blit(fondo, (0, 0)) if fondo else pantalla.fill((230, 240, 250))

        titulo = self.fuente_titulo.render("Selecciona un Modo de Juego", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(titulo, titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 120)))

        for modo, rect in self.rects_modos.items():
            pantalla.blit(self.surfs_btn_modos[modo], rect)

    def obtener_clic_menu_modos(self, pos_mouse: tuple[int, int]) -> str | None:
        for modo, rect in self.rects_modos.items():
            if rect.collidepoint(pos_mouse):
                return modo
        return None

    def _inicializar_grilla_rasca(self) -> None:
        self._bloques_rasca = []
        ancho_img, alto_img = 440, 310
        x_inicio = (const.ANCHO_PANTALLA // 2) - (ancho_img // 2)
        y_inicio = 225 - (alto_img // 2)
        tamanio = 12

        for x in range(x_inicio, x_inicio + ancho_img, tamanio):
            for y in range(y_inicio, y_inicio + alto_img, tamanio):
                self._bloques_rasca.append(pygame.Rect(x, y, tamanio, tamanio))

    def procesar_rasca_mouse(self, pos_mouse: tuple[int, int]) -> None:
        self._bloques_rasca = [
            b for b in self._bloques_rasca if not (
                b.collidepoint(pos_mouse) or 
                (abs(b.centerx - pos_mouse[0]) < 20 and abs(b.centery - pos_mouse[1]) < 20)
            )
        ]

    def dibujar_interfaz(
       self, pantalla, carta_actual, puntuacion: int, mensaje: str, 
       revelada: bool = False, modo: str = "normal", 
       tiempo_restante: float = 0.0, tiempo_agotado: bool = False
    ) -> None:
        fondo = self.recursos.fondos.get("juego")
        pantalla.blit(fondo, (0, 0)) if fondo else pantalla.fill((240, 240, 240))

        if carta_actual:
            # Se compara por el string 'nombre_imagen' para evitar fallos de objeto
            if self._ultima_carta_procesada != carta_actual.nombre_imagen or (modo == "rasca" and not self._bloques_rasca):
                self._opciones_actuales = carta_actual.obtener_opciones_mezcladas()
                self._ultima_carta_procesada = carta_actual.nombre_imagen

                self._surfaces_opciones_actuales = [
                    crear_boton_glossy(
                        op, self.fuente_texto, rect.width, rect.height,
                        color_arriba=(255, 170, 60), color_abajo=(190, 85, 10)
                    ) for op, rect in zip(self._opciones_actuales, self.rects_opciones)
                ]

                if modo == "rasca":
                    self._inicializar_grilla_rasca()

                self._imagen_actual_escalada = self.recursos.cargar_imagen_animal(
                    carta_actual.nombre_imagen, ancho=440, alto=310
                )

        pos_x = (pantalla.get_width() // 2) - 220
        pos_y = 225 - 155

        # Renderizar la imagen con marco cápsula
        if self._imagen_actual_escalada:
            if modo == "rasca":
                pantalla.blit(self._imagen_actual_escalada, (pos_x, pos_y))
            else:
                img_con_marco = aplicar_marco_capsula(
                    self._imagen_actual_escalada, 
                    radio_borde=30, 
                    grosor_borde=5
                )
                pantalla.blit(img_con_marco, (pos_x, pos_y))
        else:
            pygame.draw.rect(pantalla, (220, 220, 220), (pos_x, pos_y, 440, 310), border_radius=30)

        # Renderizado del modo rasca
        if modo == "rasca":      
            for bloque in self._bloques_rasca:
                pygame.draw.rect(pantalla, (150, 150, 150), bloque)
                pygame.draw.rect(pantalla, (100, 100, 100), bloque, width=1)
            pygame.draw.rect(pantalla, (76, 175, 80), (pos_x, pos_y, 440, 310), width=4, border_radius=8)

        # Renderizar los botones de opciones
        for i, rect in enumerate(self.rects_opciones):
            if i < len(self._surfaces_opciones_actuales):
                pantalla.blit(self._surfaces_opciones_actuales[i], rect)

        txt_puntos = self.fuente_titulo.render(f"Puntuación: {puntuacion}", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(txt_puntos, (50, 30))

        if modo == "rasca":
            texto_tiempo = f"Tiempo: {int(tiempo_restante)}s" if not tiempo_agotado else "¡Tiempo agotado!"
            color_tiempo = (211, 47, 47) if tiempo_agotado else const.COLOR_TEXTO_DARK
            txt_tiempo = self.fuente_texto.render(texto_tiempo, True, color_tiempo)
            pantalla.blit(txt_tiempo, txt_tiempo.get_rect(center=(const.ANCHO_PANTALLA // 2, 40)))

        if mensaje:
            txt_msg = self.fuente_titulo.render(mensaje, True, (46, 125, 50))
            pantalla.blit(txt_msg, txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 445)))

    def obtener_opcion_clic(self, pos_mouse: tuple[int, int]) -> str | None:
        for i, rect in enumerate(self.rects_opciones):
            if rect.collidepoint(pos_mouse):
                return self._opciones_actuales[i]
        return None

    def dibujar_ronda_sino(self, pantalla, pregunta_actual, puntuacion: int, mensaje: str) -> None:
        fondo = self.recursos.fondos.get("juego")
        pantalla.blit(fondo, (0, 0)) if fondo else pantalla.fill((240, 240, 240))

        titulo = self.fuente_titulo.render("Ronda Rápida: ¿Sí o No?", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(titulo, titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 100)))

        if pregunta_actual:
            txt_preg = self.fuente_titulo.render(pregunta_actual.enunciado, True, (30, 30, 30))
            pantalla.blit(txt_preg, txt_preg.get_rect(center=(const.ANCHO_PANTALLA // 2, 280)))

        pantalla.blit(self.surf_btn_si, self.rect_btn_si)
        pantalla.blit(self.surf_btn_no, self.rect_btn_no)

        txt_puntos = self.fuente_titulo.render(f"Puntuación: {puntuacion}", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(txt_puntos, (const.ANCHO_PANTALLA - 280, 40))

        if mensaje:
            txt_msg = self.fuente_titulo.render(mensaje, True, (46, 125, 50))
            pantalla.blit(txt_msg, txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 630)))

    def obtener_clic_sino(self, pos_mouse: tuple[int, int]) -> bool | None:
        if self.rect_btn_si.collidepoint(pos_mouse):
            return True
        if self.rect_btn_no.collidepoint(pos_mouse):
            return False
        return None

    def dibujar_pantalla_resultados(
        self, pantalla, puntuacion_final: int, total_posible: int, aciertos: int, fallos: int
    ) -> None:
        titulo = self.fuente_titulo.render("¡Juego Terminado!", True, const.COLOR_TEXTO_DARK)
        pantalla.blit(titulo, titulo.get_rect(center=(const.ANCHO_PANTALLA // 2, 140)))

        txt_score = self.fuente_texto.render(f"Puntuación Final: {puntuacion_final} / {total_posible}", True, (40, 50, 120))
        pantalla.blit(txt_score, txt_score.get_rect(center=(const.ANCHO_PANTALLA // 2, 210)))

        txt_aciertos = self.fuente_texto.render(f"Aciertos: {aciertos}", True, (76, 175, 80))
        pantalla.blit(txt_aciertos, txt_aciertos.get_rect(center=(const.ANCHO_PANTALLA // 2, 270)))

        txt_fallos = self.fuente_texto.render(f"Fallos: {fallos}", True, (244, 67, 54))
        pantalla.blit(txt_fallos, txt_fallos.get_rect(center=(const.ANCHO_PANTALLA // 2, 320)))

        mensaje, color_msg = (
            ("¡Qué pedazo de cerebro! Me dejas impresionado.", (46, 125, 50))
            if aciertos >= fallos else
            ("¡No te desanimes! Sigue practicando para mejorar la próxima.", (211, 47, 47))
        )
        txt_msg = self.fuente_texto.render(mensaje, True, color_msg)
        pantalla.blit(txt_msg, txt_msg.get_rect(center=(const.ANCHO_PANTALLA // 2, 390)))

        pantalla.blit(self.surf_btn_reiniciar, self.rect_btn_reiniciar)

    def obtener_clic_resultados(self, pos_mouse: tuple[int, int]) -> bool:
        return self.rect_btn_reiniciar.collidepoint(pos_mouse)

    def dibujar_indicadores_progreso(
        self, pantalla, total_preguntas: int, resultados: list[str]
    ) -> None:
        dibujar_indicadores_progreso(
            pantalla, const.ANCHO_PANTALLA // 2, 440, total_preguntas, resultados
        )
