import random
from dataclasses import dataclass
from elemento import Elemento  


@dataclass
class Carta(Elemento):

    nombre_imagen: str
    respuesta_correcta: str
    opciones_falsas: list[str]  # 3 opciones falsas
    zona: str  # Define el bioma ("artico", "oceano", "praderas", etc.)

    def cargar_recursos(self) -> None:
        pass

    def renderizar(self) -> None:  
        pass

    def obtener_opciones_mezcladas(self) -> list[str]:
        todas = self.opciones_falsas + [self.respuesta_correcta]
        random.shuffle(todas)
        return todas

@dataclass
class PreguntaSiNo:
    enunciado: str
    es_verdadero: bool  
    zona: str  



