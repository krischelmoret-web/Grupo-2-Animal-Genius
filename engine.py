import pygame
from album import AlbumCartas
from constants import const
from visual import RenderizadorJuego


class MotorJuego:

    def __init__(self):
        self._pantalla = pygame.display.set_mode(
            (const.ANCHO_PANTALLA, const.ALTO_PANTALLA)
        )
        pygame.display.set_caption(const.TITULO_JUEGO)

        self._reloj = pygame.time.Clock()
        self._ejecutando = True

        self._visual = RenderizadorJuego()
        self._album = AlbumCartas()

        self._estado = "MENU_PRINCIPAL"
        self._zona_seleccionada = None
        self._modo_juego = None  

        self._indice_actual = 0
        self._puntuacion = 0
        self._aciertos = 0  
        self._fallos = 0    
        self._mensaje_retroalimentacion = ""
        self._tiempo_mensaje = 0.0

        self._revelando_carta = False
        self._tiempo_revelacion = 0.0

        self._duracion_rasca = 4.0          
        self._tiempo_restante_rasca = 4.0   
        self._tiempo_agotado_rasca = False  
        self._esta_rascando = False         

        self._musica_activa = True
        self._efectos_activos = True
        
        try:
            self._sonido_clic = pygame.mixer.Sound(str(const.SOUNDS_DIR / "click.oga"))
            self._sonido_clic.set_volume(1.0)
        except Exception:
            self._sonido_clic = None

        try:
            self._sonido_correcto = pygame.mixer.Sound(str(const.SOUNDS_DIR / "correcto.oga"))
            self._sonido_correcto.set_volume(1.0)
        except Exception:
            self._sonido_correcto = None

        try:
            self._sonido_incorrecto = pygame.mixer.Sound(str(const.SOUNDS_DIR / "incorrecto.oga"))
            self._sonido_incorrecto.set_volume(1.0)
        except Exception:
            self._sonido_incorrecto = None

        self._reproducir_musica_menu()

    def _reproducir_musica_menu(self) -> None:
        try:
            ruta_menu = const.SOUNDS_DIR / "menu.oga"
            pygame.mixer.music.load(str(ruta_menu))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Aviso: No se pudo cargar la música del menú: {e}")

    def _reproducir_musica_bioma(self, zona: str) -> None:
           try:
               ruta_bioma = const.SOUNDS_DIR / f"{zona}.oga"
               pygame.mixer.music.load(str(ruta_bioma))
               pygame.mixer.music.set_volume(0.4)
               pygame.mixer.music.play(-1)  
           except Exception as e:
               print(f"Aviso: No se pudo cargar la música de la zona '{zona}': {e}")

    def _reproducir_clic(self) -> None:
        if self._efectos_activos and self._sonido_clic:
            self._sonido_clic.play()

    def _alternar_musica(self) -> None:
        self._musica_activa = not self._musica_activa
        if self._musica_activa:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def _alternar_efectos(self) -> None:
        self._efectos_activos = not self._efectos_activos

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

            elif evento.type == pygame.MOUSEMOTION:
                if self._estado == "JUGANDO" and self._modo_juego == "rasca":
                    if not self._revelando_carta and not self._tiempo_agotado_rasca and self._esta_rascando:
                        self._visual.procesar_rasca_mouse(evento.pos)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self._estado == "MENU_PRINCIPAL":
                    if self._visual.obtener_clic_boton_musica(evento.pos):
                        self._reproducir_clic()
                        self._alternar_musica()
                    elif self._visual.obtener_clic_boton_efectos(evento.pos):
                        self._reproducir_clic()
                        self._alternar_efectos()
                    elif self._visual.obtener_clic_menu_principal(evento.pos):
                        self._reproducir_clic()
                        self._estado = "SELECCION_ZONA"

                elif self._estado == "SELECCION_ZONA":
                    if self._visual.obtener_clic_boton_volver(evento.pos):
                        self._reproducir_clic()
                        self._estado = "MENU_PRINCIPAL"
                        self._reproducir_musica_menu()
                        if not self._musica_activa:
                            pygame.mixer.music.pause()
                    else:
                        zona = self._visual.obtener_clic_zona(evento.pos)
                        if zona:
                            self._reproducir_clic()
                            self._zona_seleccionada = zona
                            self._album.filtrar_por_zona(zona)
                            self._estado = "SELECCION_MODO"
                            self._reproducir_musica_bioma(zona)
                            if not self._musica_activa:
                                pygame.mixer.music.pause()

                elif self._estado == "SELECCION_MODO":
                    if self._visual.obtener_clic_boton_volver(evento.pos):
                        self._reproducir_clic()
                        self._estado = "SELECCION_ZONA"
                        self._reproducir_musica_menu()
                        if not self._musica_activa:
                            pygame.mixer.music.pause()
                    else:
                        modo = self._visual.obtener_clic_menu_modos(evento.pos)
                        if modo:
                            self._reproducir_clic()
                            self._modo_juego = modo  
                            self._estado = "JUGANDO"
                            self._indice_actual = 0
                            self._puntuacion = 0
                            self._aciertos = 0  
                            self._fallos = 0    
                            self._mensaje_retroalimentacion = ""
                            
                            if self._modo_juego == "rasca":
                                self._tiempo_restante_rasca = self._duracion_rasca
                                self._tiempo_agotado_rasca = False
                                self._esta_rascando = False
                            elif self._modo_juego == "preguntas":
                                self._album.filtrar_preguntas_sino(self._zona_seleccionada)

                elif self._estado == "JUGANDO":
                    if self._modo_juego == "rasca":
                        if not self._revelando_carta and not self._tiempo_agotado_rasca:
                            self._esta_rascando = True
                            self._visual.procesar_rasca_mouse(evento.pos)
                        
                        self._evaluar_clic(evento.pos)

                    elif self._modo_juego == "preguntas":
                        self._evaluar_clic_preguntas(evento.pos)
                    else:
                        self._evaluar_clic(evento.pos)

                elif self._estado == "RESULTADOS":
                    if self._visual.obtener_clic_resultados(evento.pos):
                        self._reproducir_clic()
                        self._estado = "MENU_PRINCIPAL"
                        self._reproducir_musica_menu()

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self._estado == "JUGANDO" and self._modo_juego == "rasca":
                    self._esta_rascando = False

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
                self._aciertos += 1
                self._revelando_carta = True
                self._tiempo_revelacion = 2.0
                self._mensaje_retroalimentacion = "¡Muy bien! ¡Correcto!"
                if self._efectos_activos and self._sonido_correcto:
                    self._sonido_correcto.play()
            else:
                self._fallos += 1
                self._revelando_carta = True
                self._tiempo_revelacion = 2.0
                self._mensaje_retroalimentacion = (
                    f"Era: {carta_actual.respuesta_correcta}"
                )
                if self._efectos_activos and self._sonido_incorrecto:
                    self._sonido_incorrecto.play()

    def _evaluar_clic_preguntas(self, pos_mouse: tuple[int, int]) -> None:
        if self._revelando_carta:
            return

        respuesta_usuario = self._visual.obtener_clic_sino(pos_mouse)
        if respuesta_usuario is not None:
            pregunta_actual = self._album.obtener_pregunta_sino(self._indice_actual)

            if pregunta_actual:
                es_correcto = (respuesta_usuario == pregunta_actual.es_verdadero)

                if es_correcto:
                    self._puntuacion += 10
                    self._aciertos += 1
                    self._mensaje_retroalimentacion = "¡Correcto!"
                    if self._efectos_activos and self._sonido_correcto:
                        self._sonido_correcto.play()
                else:
                    self._fallos += 1
                    self._mensaje_retroalimentacion = "¡Incorrecto!"
                    if self._efectos_activos and self._sonido_incorrecto:
                        self._sonido_incorrecto.play()

                self._revelando_carta = True
                self._tiempo_revelacion = 2.0

    def _actualizar(self, dt: float) -> None:
        if self._estado == "JUGANDO" and self._modo_juego == "rasca" and not self._revelando_carta:
            if not self._tiempo_agotado_rasca:
                self._tiempo_restante_rasca -= dt
                if self._tiempo_restante_rasca <= 0:
                    self._tiempo_restante_rasca = 0.0
                    self._tiempo_agotado_rasca = True
                    self._esta_rascando = False

        if self._revelando_carta:
            self._tiempo_revelacion -= dt
            if self._tiempo_revelacion <= 0:
                self._revelando_carta = False
                self._avanzar_siguiente_carta()

    def _avanzar_siguiente_carta(self) -> None:
        self._indice_actual += 1
        self._mensaje_retroalimentacion = ""
        self._visual._ultima_carta_procesada = None

        if self._modo_juego == "rasca":
            self._tiempo_restante_rasca = self._duracion_rasca
            self._tiempo_agotado_rasca = False
            self._esta_rascando = False

        if self._modo_juego == "preguntas":
            limite = len(self._album._preguntas_sino_filtradas)
        else:
            limite = self._album.total_cartas()

        if self._indice_actual >= limite:
            self._estado = "RESULTADOS"

    def _dibujar(self) -> None:
        self._pantalla.fill(const.COLOR_FONDO)

        if self._estado == "MENU_PRINCIPAL":
            self._visual.dibujar_menu_principal(self._pantalla)
            self._visual.dibujar_boton_musica(self._pantalla, self._musica_activa)
            self._visual.dibujar_boton_efectos(self._pantalla, self._efectos_activos)
        elif self._estado == "SELECCION_ZONA":
            self._visual.dibujar_menu_zonas(self._pantalla)
        elif self._estado == "SELECCION_MODO":
            self._visual.dibujar_menu_modos(self._pantalla)
        elif self._estado == "JUGANDO":
            if self._modo_juego == "preguntas":
                pregunta_actual = self._album.obtener_pregunta_sino(self._indice_actual)
                self._visual.dibujar_ronda_sino(
                    self._pantalla,
                    pregunta_actual,
                    puntuacion=self._puntuacion,
                    mensaje=self._mensaje_retroalimentacion
                )
            else:
                carta_actual = self._album.obtener_carta(self._indice_actual)
                self._visual.dibujar_interfaz(
                    self._pantalla,
                    carta_actual,
                    self._puntuacion,
                    self._mensaje_retroalimentacion,
                    modo=self._modo_juego, 
                    tiempo_restante=self._tiempo_restante_rasca,
                    tiempo_agotado=self._tiempo_agotado_rasca
                )
        elif self._estado == "RESULTADOS":
            if self._modo_juego == "preguntas":
                total_preguntas = len(self._album._preguntas_sino_filtradas)
            else:
                total_preguntas = self._album.total_cartas()
            
            total_posible = total_preguntas * 10
            self._visual.dibujar_pantalla_resultados(
                self._pantalla,
                puntuacion_final=self._puntuacion,
                total_posible=total_posible,
                aciertos=self._aciertos,
                fallos=self._fallos
            )
