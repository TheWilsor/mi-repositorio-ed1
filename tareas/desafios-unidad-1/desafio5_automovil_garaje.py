"""
Modulo para el Desafio 5: Coleccion de Objetos Automovil en Garaje.
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Automovil:
    """Representa un auto con placa y modelo."""

    def __init__(self, placa: str, modelo: str):
        self.placa = placa
        self.modelo = modelo


class Garaje:
    """Almacena una coleccion de autos distintos."""

    def __init__(self) -> None:
        self._autos: list[Automovil] = []

    def agregar_auto(self, auto: Automovil) -> None:
        """Agrega una instancia al garaje."""
        self._autos.append(auto)

    def mostrar_garaje(self) -> None:
        """Muestra todos los autos almacenados."""
        for idx, auto in enumerate(self._autos, start=1):
            print(f"Auto {idx}: Placa={auto.placa}, Modelo={auto.modelo}")


if __name__ == "__main__":
    print("--- DESAFIO 5: AUTOMOVIL Y GARAJE ---")
    garaje = Garaje()

    # SOLUCION: Instanciar cada auto individualmente
    auto1 = Automovil("123-ABC", "Toyota")
    auto2 = Automovil("456-DEF", "Nissan")

    garaje.agregar_auto(auto1)
    garaje.agregar_auto(auto2)

    garaje.mostrar_garaje()