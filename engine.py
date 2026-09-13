import pygame
from album import AlbumCartas
from constants import const
from visual import RenderizadorJuego


class MotorJuego:

    def __init__(self):
        # Configuración de pantalla y rendimiento
        self._pantalla = pygame.display.set_mode(
            (const.ANCHO_PANTALLA, const.ALTO_PANTALLA)
        )
        pygame.display.set_caption(const.TITULO_JUEGO)

        self._reloj = pygame.time.Clock()
        self._ejecutando = True

        self._visual = RenderizadorJuego()
        self._album = AlbumCartas()

        # Control de Estados
        self._estado = "MENU_PRINCIPAL"
        self._zona_seleccionada = None

        # Variables de juego
        self._indice_actual = 0
        self._puntuacion = 0
        self._mensaje_retroalimentacion = ""
        self._tiempo_mensaje = 0.0

        self._revelando_carta = False
        self._tiempo_revelacion = 0.0

    def ejecutar(self) -> None:
        while self._ejecutando:
            dt = self._reloj.tick(const.FPS) / 1000.0

            self._procesar_eventos()
            self._actualizar(dt)
            self._dibujar()

            pygame.display.flip()

    def _procesar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Menú Principal
                if self._estado == "MENU_PRINCIPAL":
                    if self._visual.obtener_clic_menu_principal(evento.pos):
                        self._estado = "SELECCION_ZONA"

                # Eleccion de zona/bioma
                elif self._estado == "SELECCION_ZONA":
                    zona = self._visual.obtener_clic_zona(evento.pos)
                    if zona:
                        self._zona_seleccionada = zona
                        self._album.filtrar_por_zona(zona)
                        self._estado = "JUGANDO"
                        self._indice_actual = 0

                # Partida
                elif self._estado == "JUGANDO":
                    self._evaluar_clic(evento.pos)

    def _evaluar_clic(self, pos_mouse: tuple[int, int]) -> None:
        if self._revelando_carta:
            return

        opcion_seleccionada = self._visual.obtener_opcion_clic(pos_mouse)

        if opcion_seleccionada:
            carta_actual = self._album.obtener_carta(self._indice_actual)

            if (
                carta_actual
                and opcion_seleccionada == carta_actual.respuesta_correcta
            ):
                self._puntuacion += 10
                self._revelando_carta = True   
                self._tiempo_revelacion = 4.0  
                self._mensaje_retroalimentacion = "¡Muy bien! ¡Correcto!"
            else:
                self._revelando_carta = True   
                self._tiempo_revelacion = 2.0  
                self._mensaje_retroalimentacion = (
                    f"Era: {carta_actual.respuesta_correcta}"
                )


    def _actualizar(self, dt: float) -> None:
        if self._revelando_carta:
            self._tiempo_revelacion -= dt
            if self._tiempo_revelacion <= 0:
                self._revelando_carta = False
                self._avanzar_siguiente_carta()

    def _avanzar_siguiente_carta(self) -> None:
            self._indice_actual += 1
            self._mensaje_retroalimentacion = ""
            self._visual._ultima_carta_procesada = None 
    
            if self._indice_actual >= self._album.total_cartas():
                self._indice_actual = 0

    def _dibujar(self) -> None:
        self._pantalla.fill(const.COLOR_FONDO)

        if self._estado == "MENU_PRINCIPAL":
            self._visual.dibujar_menu_principal(self._pantalla)
        elif self._estado == "SELECCION_ZONA":
            self._visual.dibujar_menu_zonas(self._pantalla)
        elif self._estado == "JUGANDO":
            carta_actual = self._album.obtener_carta(self._indice_actual)
            self._visual.dibujar_interfaz(
                self._pantalla,
                carta_actual,
                self._puntuacion,
                self._mensaje_retroalimentacion,
                revelada=self._revelando_carta,
            )                self._ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._evaluar_clic(evento.pos)

    def _evaluar_clic(self, pos_mouse: tuple[int, int]) -> None:
        opcion_seleccionada = self._visual.obtener_opcion_clic(pos_mouse)

        if opcion_seleccionada:
            carta_actual = self._album.obtener_carta(self._indice_actual)

            if carta_actual and opcion_seleccionada == carta_actual.respuesta_correcta:
                self._puntuacion += 10
                self._mensaje_retroalimentacion = obtener_mensaje_aliento()
            else:
                self._mensaje_retroalimentacion = "Inténtalo de nuevo"

            self._tiempo_mensaje = 2.0
            self._avanzar_siguiente_carta()

    def _avanzar_siguiente_carta(self) -> None:
        self._indice_actual += 1
        if self._indice_actual >= self._album.total_cartas():
            self._indice_actual = 0

    def _actualizar(self, dt: float) -> None:
        if self._tiempo_mensaje > 0:
            self._tiempo_mensaje -= dt
            if self._tiempo_mensaje <= 0:
                self._mensaje_retroalimentacion = ""  
                self._tiempo_mensaje = 0.0

    def _dibujar(self) -> None:
        self._pantalla.fill(const.COLOR_FONDO)
        carta_actual = self._album.obtener_carta(self._indice_actual)

        self._visual.dibujar_interfaz(
            self._pantalla,
            carta_actual,
            self._puntuacion,
            self._mensaje_retroalimentacion,
        )


