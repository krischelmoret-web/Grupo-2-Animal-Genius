import random
from cartas import Carta, PreguntaSiNo

class AlbumCartas:

    def __init__(self):
        # Lista con todas las cartas y 4 opciones de respuesta por tarjeta
        self._cartas_totales = [
            #artico
            Carta(
                nombre_imagen="oso_polar.png",
                respuesta_correcta="Oso polar",
                opciones_falsas=["Foca", "Pingüino", "Ballena"],
                zona="artico",
            ),
            #oceano
            Carta(
                nombre_imagen="delfin.png",
                respuesta_correcta="Delfín",
                opciones_falsas=["Tiburón", "Ballena", "Pulpo"],
                zona="oceano",
            ),
            #pradera
            Carta(
                nombre_imagen="leon.png",
                respuesta_correcta="León",
                opciones_falsas=["Cebra", "Jirafa", "Elefante"],
                zona="pradera",
            ),
            #selva
            Carta(
                nombre_imagen="mono.png",
                respuesta_correcta="Mono",
                opciones_falsas=["Tigre", "Loro", "Serpiente"],
                zona="selva",
            ),
            #bosque
            Carta(
                nombre_imagen="oso_pardo.png",
                respuesta_correcta="Oso pardo",
                opciones_falsas=["Zorro", "Ciervo", "Búho"],
                zona="bosque",
            ),
        ]

        self._preguntas_sino_totales = [
            PreguntaSiNo(
                enunciado="¿El oso polar vive en el Ártico?",
                es_verdadero=True,
                zona="artico",
            ),
            PreguntaSiNo(
                enunciado="¿El delfín es un mamífero marino?",
                es_verdadero=True,
                zona="oceano",
            ),
            PreguntaSiNo(
                enunciado="¿El león habita en la pradera?",
                es_verdadero=True,
                zona="pradera",
            ),
            PreguntaSiNo(
                enunciado="¿El mono vive comúnmente en la selva?",
                es_verdadero=True,
                zona="selva",
            ),
            PreguntaSiNo(
                enunciado="¿El oso pardo suele habitar en zonas de bosque?",
                es_verdadero=True,
                zona="bosque",
            ),
        ]

        # Lista que se usará en la partida actual según la zona elegida
        self._cartas_filtradas = []
        self._preguntas_sino_filtradas = []


    def filtrar_por_zona(self, zona: str) -> None:
        self._cartas_filtradas = [
            carta for carta in self._cartas_totales if carta.zona == zona
        ]
        random.shuffle(self._cartas_filtradas)

    def filtrar_preguntas_sino(self, zona: str) -> None:
        self._preguntas_sino_filtradas = [
            p for p in self._preguntas_sino_totales if p.zona == zona
        ]
        random.shuffle(self._preguntas_sino_filtradas)

    def obtener_pregunta_sino(self, indice: int) -> PreguntaSiNo | None:
        if 0 <= indice < len(self._preguntas_sino_filtradas):
            return self._preguntas_sino_filtradas[indice]
        return None

    def obtener_carta(self, indice: int) -> Carta | None:
        if 0 <= indice < len(self._cartas_filtradas):
            return self._cartas_filtradas[indice]
        return None

    def total_cartas(self) -> int:
        return len(self._cartas_filtradas)

