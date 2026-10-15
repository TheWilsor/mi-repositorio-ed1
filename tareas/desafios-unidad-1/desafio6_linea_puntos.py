"""
Modulo para el Desafio 6: Composicion de Linea con Puntos Inmutables
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Punto:
    """Coordenada en espacio 2D."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Linea:
    """Define un segmento mediante dos puntos independientes """

    def __init__(self, inicio: Punto, fin: Punto):
        # Clonacion para proteger el estado interno de la linea
        self._inicio = Punto(inicio.x, inicio.y)
        self._fin = Punto(fin.x, fin.y)

    def mostrar_segmento(self) -> None:
        """Imprime los extremos de la linea """
        print(
            f"Linea de ({self._inicio.x}, {self._inicio.y}) "
            f"a ({self._fin.x}, {self._fin.y})"
        )


if __name__ == "__main__":
    print("--- DESAFIO 6: LINEA Y PUNTOS ---")
    p1 = Punto(1, 1)
    p2 = Punto(5, 5)

    linea = Linea(p1, p2)

    # Intento de alteracion externa
    p1.x = 10
    p2.y = 10

    print("Estado del segmento (debe mantenerse inalterado):")
    linea.mostrar_segmento()