import random
from cartas import Carta, PreguntaSiNo

class AlbumCartas:

    def __init__(self):
        # Lista con todas las cartas y 4 opciones de respuesta por tarjeta
        self._cartas_totales = [
            #artico
            Carta(
                nombre_imagen="frailecillo.png",
                respuesta_correcta="Frailecillo",
                opciones_falsas=["Pato", "Pingüino", "Gaviota"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="osopolar.png",
                respuesta_correcta="Oso Polar",
                opciones_falsas=["Oso Pardo", "Lobo", "Oso Negro"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="zorroartico.png",
                respuesta_correcta="Zorro Ártico",
                opciones_falsas=["Liebre", "Zorro Rojo", "Lobo"],
                zona="artico",
            ),
             Carta(
                nombre_imagen="pinguino.png",
                respuesta_correcta="Pingüino",
                opciones_falsas=["Gaviota", "Pato", "Águila"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="morsa.png",
                respuesta_correcta="Morsa",
                opciones_falsas=["Foca", "Oso Polar", "Ballena"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="orca.png",
                respuesta_correcta="Orca",
                opciones_falsas=["Ballena", "Foca", "Delfín"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="ballena.png",
                respuesta_correcta="Ballena",
                opciones_falsas=["Foca", "Pingüino", "Delfín"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="reno.png",
                respuesta_correcta="Reno",
                opciones_falsas=["Ciervo", "Vaca", "Caballo"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="buho.png",
                respuesta_correcta="Búho",
                opciones_falsas=["Águila", "Loro", "Pingüino"],
                zona="artico",
            ),
            Carta(
                nombre_imagen="foca.png",
                respuesta_correcta="Foca",
                opciones_falsas=["Morsa", "Delfín", "Ballena"],
                zona="artico",
            ),

            #oceano
            Carta(
                nombre_imagen="tiburon.png",
                respuesta_correcta="Tiburón",
                opciones_falsas=["Ballena", "Delfín", "Pez Payaso"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="delfin.png",
                respuesta_correcta="Delfín",
                opciones_falsas=["Tiburón", "Ballena", "Foca"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="estrellademar.png",
                respuesta_correcta="Estrella de Mar",
                opciones_falsas=["Cangrejo", "Pez Payaso", "Tortuga"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="pulpo.png",
                respuesta_correcta="Pulpo",
                opciones_falsas=["Calamar", "Medusa", "Tortuga"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="tortuga.png",
                respuesta_correcta="Tortuga",
                opciones_falsas=["Cangrejo", "Estrella de Mar", "Pez Payaso"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="caballitodemar.png",
                respuesta_correcta="Caballito de Mar",
                opciones_falsas=["Pez Payaso", "Delfín", "Foca"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="pezpayaso.png",
                respuesta_correcta="Pez Payaso",
                opciones_falsas=["Tiburón", "Ballena", "Delfín"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="medusa.png",
                respuesta_correcta="Medusa",
                opciones_falsas=["Pulpo", "Calamar", "Tortuga"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="cangrejo.png",
                respuesta_correcta="Cangrejo",
                opciones_falsas=["Pulpo", "Estrella de Mar", "Medusa"],
                zona="oceano",
            ),
            Carta(
                nombre_imagen="calamar.png",
                respuesta_correcta="Calamar",
                opciones_falsas=["Pulpo", "Medusa", "Cangrejo"],
                zona="oceano",
            ),

            #pradera
            Carta(
                nombre_imagen="leon.png",
                respuesta_correcta="León",
                opciones_falsas=["Tigre", "Leopardo", "Guepardo"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="elefante.png",
                respuesta_correcta="Elefante",
                opciones_falsas=["Jirafa", "Rinoceronte", "Hipopótamo"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="jirafa.png",
                respuesta_correcta="Jirafa",
                opciones_falsas=["Cebra", "Antílope", "Buey"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="cebra.png",
                respuesta_correcta="Cebra",
                opciones_falsas=["Caballo", "Burro", "Okapi"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="hipopotamo.png",
                respuesta_correcta="Hipopótamo",
                opciones_falsas=["Rinoceronte", "Elefante", "Cerdo"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="rinoceronte.png",
                respuesta_correcta="Rinoceronte",
                opciones_falsas=["Hipopótamo", "Elefante", "Cerdo"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="vaca.png",
                respuesta_correcta="Vaca",
                opciones_falsas=["Toro", "Bisonte", "Caballo"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="avestruz.png",
                respuesta_correcta="Avestruz",
                opciones_falsas=["Pavo", "Águila", "Ganso"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="canguro.png",
                respuesta_correcta="Canguro",
                opciones_falsas=["Gorila", "Chimpancé", "Koala"],
                zona="pradera",
            ),
            Carta(
                nombre_imagen="cocodrilo.png",
                respuesta_correcta="Cocodrilo",
                opciones_falsas=["Iguana", "Camaleón", "Serpiente"],
                zona="pradera",
            ),

            #selva
            Carta(
                nombre_imagen="jaguar.png",
                respuesta_correcta="Jaguar",
                opciones_falsas=["Puma", "Leopardo", "Tigre"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="tucan.png",
                respuesta_correcta="Tucán",
                opciones_falsas=["Loro", "Guacamaya", "Águila"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="serpiente.png",
                respuesta_correcta="Serpiente",
                opciones_falsas=["Lagartija", "Iguana", "Rana"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="gorila.png",
                respuesta_correcta="Gorila",
                opciones_falsas=["Chimpancé", "Orangután", "Mono"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="rana.png",
                respuesta_correcta="Rana",
                opciones_falsas=["Camaleón", "Iguana", "Serpiente"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="loro.png",
                respuesta_correcta="Loro",
                opciones_falsas=["Guacamaya", "Tucán", "Búho"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="araña.png",
                respuesta_correcta="Araña",
                opciones_falsas=["Mono", "Mariposa", "Serpiente"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="mono.png",
                respuesta_correcta="Mono",
                opciones_falsas=["Gorila", "Chimpancé", "Lémur"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="koala.png",
                respuesta_correcta="Koala",
                opciones_falsas=["Canguro", "Mono", "Ardilla"],
                zona="selva",
            ),
            Carta(
                nombre_imagen="mariposa.png",
                respuesta_correcta="Mariposa",
                opciones_falsas=["Tigre", "Ardilla", "Tucán"],
                zona="selva",
            ),

            #bosque
            Carta(
                nombre_imagen="osopardo.png",
                respuesta_correcta="Oso Pardo",
                opciones_falsas=["Oso Negro", "Lobo", "Zorro"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="ciervo.png",
                respuesta_correcta="Ciervo",
                opciones_falsas=["Reno", "Vaca", "Caballo"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="lobo.png",
                respuesta_correcta="Lobo",
                opciones_falsas=["Zorro", "Coyote", "Perro"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="urracaazul.png",
                respuesta_correcta="Urraca Azul",
                opciones_falsas=["Águila", "Cuervo", "Paloma"],
                zona="bosque",
            ), 
            Carta(
                nombre_imagen="ardilla.png",
                respuesta_correcta="Ardilla",
                opciones_falsas=["Ratón", "Conejo", "Castor"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="pajarocarpintero.png",
                respuesta_correcta="Pájaro Carpintero",
                opciones_falsas=["Águila", "Loro", "Colibrí"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="osopanda.png",
                respuesta_correcta="Oso Panda",
                opciones_falsas=["Oso Negro", "Mapache", "Zorro"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="puercoespin.png",
                respuesta_correcta="Puercoespín",
                opciones_falsas=["Ratón", "Erizo", "Castor"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="aguila.png",
                respuesta_correcta="Águila",
                opciones_falsas=["Gaviota", "Cuervo", "Búho"],
                zona="bosque",
            ),
            Carta(
                nombre_imagen="zorrillo.png",
                respuesta_correcta="Zorrillo",
                opciones_falsas=["Zorro", "Mapache", "Comadreja"],
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

        # Lista que se usará en la partida según la zona elegida
        self._cartas_filtradas = []
        self._preguntas_sino_filtradas = []


    def filtrar_por_zona(self, zona: str) -> None:
        self._cartas_filtradas = [
            carta for carta in self._cartas_totales if carta.zona == zona
        ]
        random.shuffle(self._cartas_filtradas)
        self._cartas_filtradas = self._cartas_filtradas[:10]

    def filtrar_preguntas_sino(self, zona: str) -> None:
        self._preguntas_sino_filtradas = [
            p for p in self._preguntas_sino_totales if p.zona == zona
        ]
        random.shuffle(self._preguntas_sino_filtradas)
        self._preguntas_sino_filtradas = self._preguntas_sino_filtradas[:10]

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
