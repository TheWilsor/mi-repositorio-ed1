"""
Modulo interactivo para la Unidad 1 con interfaz de consola.

Asignatura: INF220 - Estructura de Datos 1 (UAGRM)
Docente: Ing. Juan Carlos Peinado
"""


class ElementoTDA:
    """Representa la entidad de datos basica (TDA) con atributos encapsulados."""

    def __init__(self, identificador: int, valor: str) -> None:
        """
        Inicializa un nuevo elemento TDA.

        Args:
            identificador (int): Clave unica del elemento.
            valor (str): Contenido o descripcion del elemento.
        """
        self._identificador: int = identificador
        self._valor: str = valor

    def obtener_identificador(self) -> int:
        """
        Devuelve el identificador unico del elemento.

        Returns:
            int: El ID del elemento.
        """
        return self._identificador

    def obtener_valor(self) -> str:
        """
        Devuelve el valor o contenido almacenado.

        Returns:
            str: El valor del elemento.
        """
        return self._valor

    def mostrar_informacion(self) -> str:
        """
        Devuelve la representacion en texto del objeto.

        Returns:
            str: Cadena formateada con la informacion del elemento.
        """
        return f"ID: {self._identificador} | Valor: '{self._valor}'"


class EstructuraDatosUnidad1:
    """
    Estructura de datos estatica basada en arreglos de tamano delimitado.

    Permite evidenciar errores de comportamiento (Overflow/Underflow).
    """

    def __init__(self, capacidad: int) -> None:
        """
        Inicializa la estructura estatica con una capacidad fija.

        Args:
            capacidad (int): Tamano maximo de almacenamiento.
        """
        self._capacidad: int = capacidad
        self._elementos: list[ElementoTDA | None] = [None] * capacidad
        self._tamano_actual: int = 0

    def insertar(self, elemento: ElementoTDA) -> bool:
        """
        Inserta un objeto TDA al final de la estructura estatica.

        Args:
            elemento (ElementoTDA): Objeto TDA a insertar.

        Returns:
            bool: True si la insercion fue exitosa, False en caso contrario.
        """
        if self._tamano_actual >= self._capacidad:
            print(
                "\n[ERROR DE COMPORTAMIENTO]: Overflow (Desbordamiento)."
                f" Capacidad max ({self._capacidad}) alcanzada."
            )
            return False

        self._elementos[self._tamano_actual] = elemento
        self._tamano_actual += 1
        id_elem = elemento.obtener_identificador()
        print(f"\n[EXITO]: Elemento con ID {id_elem} insertado.")
        return True

    def eliminar_ultimo(self) -> ElementoTDA | None:
        """
        Remueve el ultimo elemento ingresado en la estructura.

        Returns:
            ElementoTDA | None: El elemento eliminado o None si esta vacia.
        """
        if self._tamano_actual == 0:
            print("\n[ERROR DE COMPORTAMIENTO]: Underflow (Estructura vacia).")
            return None

        self._tamano_actual -= 1
        elemento_eliminado = self._elementos[self._tamano_actual]
        self._elementos[self._tamano_actual] = None

        if elemento_eliminado is not None:
            id_elem = elemento_eliminado.obtener_identificador()
            print(f"\n[EXITO]: Elemento con ID {id_elem} eliminado.")

        return elemento_eliminado

    def modificar_igualitario(
        self, indice: int, nuevo_elemento: ElementoTDA
    ) -> bool:
        """
        Reemplaza el objeto en un indice especifico (Cambio igualitario).

        Args:
            indice (int): Posicion a modificar.
            nuevo_elemento (ElementoTDA): Nuevo objeto TDA a colocar.

        Returns:
            bool: True si la modificacion fue exitosa, False en caso contrario.
        """
        if 0 <= indice < self._tamano_actual:
            self._elementos[indice] = nuevo_elemento
            print(
                f"\n[EXITO]: Cambio igualitario aplicado en el indice {indice}."
            )
            return True

        limite_superior = self._tamano_actual - 1
        print(
            f"\n[ERROR]: Indice {indice} fuera de rango ocupado "
            f"(0 a {limite_superior})."
        )
        return False

    def buscar_por_id(self, identificador: int) -> ElementoTDA | None:
        """
        Realiza una busqueda secuencial por clave unica.

        Args:
            identificador (int): Clave ID a buscar.

        Returns:
            ElementoTDA | None: Objeto si fue encontrado, None si no.
        """
        for i in range(self._tamano_actual):
            elem = self._elementos[i]
            if elem is not None and elem.obtener_identificador() == identificador:
                return elem
        return None

    def listar_elementos(self) -> None:
        """Muestra el estado actual del contenido almacenado en memoria."""
        print("\n" + "=" * 45)
        print(f" ESTADO DE LA MEMORIA ({self._tamano_actual}/{self._capacidad})")
        print("=" * 45)

        if self._tamano_actual == 0:
            print(" La estructura se encuentra vacia.")
        else:
            for idx in range(self._tamano_actual):
                elem = self._elementos[idx]
                if elem is not None:
                    print(f" Posicion [{idx}]: {elem.mostrar_informacion()}")
        print("=" * 45)


def _obtener_capacidad_inicial() -> int:
    """
    Solicita al usuario la capacidad del buffer con control de excepciones.

    Returns:
        int: Capacidad validada para la estructura.
    """
    try:
        capacidad = int(
            input("Ingrese la capacidad maxima del buffer en memoria: ")
        )
        if capacidad <= 0:
            print("Capacidad invalida. Se asignara 3 por defecto.")
            return 3
        return capacidad
    except ValueError:
        print("Entrada invalida. Se asignara capacidad 3 por defecto.")
        return 3


def ejecutar_menu_consola() -> None:
    """Gestiona el bucle interactivo de opciones en la consola de comandos."""
    capacidad = _obtener_capacidad_inicial()
    estructura = EstructuraDatosUnidad1(capacidad=capacidad)

    while True:
        print("\n--- MENU INTERACTIVO - INF220 UNIDAD 1 ---")
        print("1. Insertar elemento (Probar Overflow)")
        print("2. Eliminar ultimo elemento (Probar Underflow)")
        print("3. Modificacion igualitaria por indice")
        print("4. Buscar elemento por ID")
        print("5. Mostrar estado de la memoria")
        print("6. Salir")

        opcion = input("Seleccione una opcion (1-6): ").strip()

        if opcion == "1":
            try:
                id_elem = int(input("Ingrese el ID (entero): "))
                valor_elem = input("Ingrese la descripcion/valor: ")
                nuevo_tda = ElementoTDA(id_elem, valor_elem)
                estructura.insertar(nuevo_tda)
            except ValueError:
                print("[ERROR]: El ID debe ser un numero entero.")

        elif opcion == "2":
            estructura.eliminar_ultimo()

        elif opcion == "3":
            try:
                idx = int(input("Ingrese el indice a modificar: "))
                id_elem = int(input("Ingrese el nuevo ID (entero): "))
                valor_elem = input("Ingrese el nuevo valor: ")
                nuevo_tda = ElementoTDA(id_elem, valor_elem)
                estructura.modificar_igualitario(idx, nuevo_tda)
            except ValueError:
                print("[ERROR]: Entrada numerica invalida.")

        elif opcion == "4":
            try:
                id_elem = int(input("Ingrese el ID a buscar: "))
                resultado = estructura.buscar_por_id(id_elem)
                if resultado:
                    info = resultado.mostrar_informacion()
                    print(f"\n[ENCONTRADO]: {info}")
                else:
                    print(
                        f"\n[NO ENCONTRADO]: No existe elemento "
                        f"con ID {id_elem}."
                    )
            except ValueError:
                print("[ERROR]: El ID debe ser un numero entero.")

        elif opcion == "5":
            estructura.listar_elementos()

        elif opcion == "6":
            print("\nSaliendo del programa interactivo.")
            break

        else:
            print("\n[OPCION INVALIDA]: Elija un numero entre 1 y 6.")


if __name__ == "__main__":
    ejecutar_menu_consola()