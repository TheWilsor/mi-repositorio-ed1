"""
Modulo para el Desafio 4: Encapsulamiento de Circunferencia y Punto
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Punto:
    """Representa una coordenada cartesiana X, Y."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Circunferencia:
    """Representa una figura geometrica con centro independiente"""

    def __init__(self, centro: Punto, radio: float):
        # SOLUCION: Crear una nueva instancia para aislar la referencia
        self.centro = Punto(centro.x, centro.y)
        self.radio = radio

    def mostrar_centro(self) -> None:
        """Muestra las coordenadas del centro"""
        print(f"Centro: ({self.centro.x}, {self.centro.y}), Radio: {self.radio}")


if __name__ == "__main__":
    print("--- DESAFIO 4: CIRCUNFERENCIA Y PUNTO ---")
    punto_origen = Punto(1, 2)
    circulo = Circunferencia(punto_origen, radio=5)

    # Modificacion externa del punto original
    punto_origen.x = 10
    punto_origen.y = 20

    print("Estado del circulo (no debe cambiar):")
    circulo.mostrar_centro()