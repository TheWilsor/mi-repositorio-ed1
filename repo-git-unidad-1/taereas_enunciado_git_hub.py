"""
Modulo correspondiente a los ejercicios de la Unidad 1
Asignatura: INF220 - Estructura de Datos 1 (UAGRM)
Docente: Ing. Juan Carlos Peinado
Repositorio: INF220-EstructurasDatos1/unidad1/ejercicios/enunciados.md
"""


class ElementoTDA:
    """
    Representa la entidad de datos basica (TDA) con atributos encapsulados
    """

    def __init__(self, identificador: int, valor: str) -> None:
        """
        Constructor de la clase ElementoTDA

        Args:
            identificador (int): Clave unica del elemento.
            valor (str): Contenido o descripcion del elemento
        """
        self._identificador: int = identificador
        self._valor: str = valor

    def obtener_identificador(self) -> int:
        """Devuelve el identificador unico del elemento"""
        return self._identificador

    def obtener_valor(self) -> str:
        """Devuelve el valor o contenido almacenado"""
        return self._valor

    def establecer_valor(self, nuevo_valor: str) -> None:
        """
        Actualiza el valor del elemento (Cambio simple)

        Args:
            nuevo_valor (str): Nuevo contenido a asignar
        """
        self._valor = nuevo_valor

    def mostrar_informacion(self) -> str:
        """Devuelve la representacion en texto del objeto"""
        return f"ID: {self._identificador} | Valor: '{self._valor}'"


class EstructuraDatosUnidad1:
    """
    Estructura de datos estatica basada en arreglos de tamano delimitado
    Permite evidenciar errores de comportamiento (Overflow/Underflow)
    y la aplicacion de cambios simples e igualitarios
    """

    def __init__(self, capacidad: int) -> None:
        """
        Inicializa el buffer de memoria con capacidad fija

        Args:
            capacidad (int): Tamano maximo de elementos permitidos
        """
        self._capacidad: int = capacidad
        self._elementos: list[ElementoTDA | None] = [None] * capacidad
        self._tamano_actual: int = 0

    def insertar(self, elemento: ElementoTDA) -> bool:
        """
        Inserta un objeto TDA al final de la estructura estatica

        Args:
            elemento (ElementoTDA): Instancia a almacenar

        Returns:
            bool: True si la insercion fue exitosa, False si hubo error
        """
        # Validacion de Error de Comportamiento: Overflow
        if self._tamano_actual >= self._capacidad:
            print(
                f"-> Error de comportamiento (Overflow): "
                f"Se alcanzaron los {self._capacidad} elementos maximos"
            )
            return False

        self._elementos[self._tamano_actual] = elemento
        self._tamano_actual += 1
        print(f"-> Elemento con ID {elemento.obtener_identificador()} insertado")
        return True

    def eliminar_ultimo(self) -> ElementoTDA | None:
        """
        Remueve el ultimo elemento ingresado en la estructura

        Returns:
            ElementoTDA | None: Elemento eliminado o None si esta vacia
        """
        # Validacion de Error de Comportamiento: Underflow
        if self._tamano_actual == 0:
            print("-> Error de comportamiento (Underflow): La estructura esta vacia")
            return None

        self._tamano_actual -= 1
        elemento_eliminado = self._elementos[self._tamano_actual]
        self._elementos[self._tamano_actual] = None
        print(f"-> Elemento con ID {elemento_eliminado.obtener_identificador()} eliminado")
        return elemento_eliminado

    def modificar_igualitario(self, indice: int, nuevo_elemento: ElementoTDA) -> bool:
        """
        Reemplaza el objeto en un indice especifico (Cambio igualitario en memoria)

        Args:
            indice (int): Posicion a modificar dentro del arreglo.
            nuevo_elemento (ElementoTDA): Nuevo objeto que ocupara la celda

        Returns:
            bool: True si la modificacion fue exitosa, False en caso contrario
        """
        if 0 <= indice < self._tamano_actual:
            self._elementos[indice] = nuevo_elemento
            print(f"-> Cambio igualitario aplicado en la posicion {indice}.")
            return True

        print(f"-> Error: El indice {indice} esta fuera del rango ocupado")
        return False

    def buscar_por_id(self, identificador: int) -> ElementoTDA | None:
        """
        Realiza una busqueda secuencial por clave unica

        Args:
            identificador (int): Clave del objeto a buscar

        Returns:
            ElementoTDA | None: Objeto si es localizado, de lo contrario None
        """
        for i in range(self._tamano_actual):
            elem = self._elementos[i]
            if elem is not None and elem.obtener_identificador() == identificador:
                return elem

        print(f"-> Busqueda fallida: No se encontro el ID {identificador}.")
        return None

    def listar_elementos(self) -> None:
        """Muestra el estado actual del contenido almacenado en memoria"""
        if self._tamano_actual == 0:
            print("La estructura se encuentra vacia")
            return

        print("\n--- ESTADO DE LA ESTRUCTURA EN MEMORIA ---")
        for idx in range(self._tamano_actual):
            elem = self._elementos[idx]
            if elem is not None:
                print(f"Posicion [{idx}]: {elem.mostrar_informacion()}")


if __name__ == "__main__":
    print("=== DEMOSTRACION UNIDAD 1: ENUNCIADOS DE ESTRUCTURAS DE DATOS ===")

    # 1. Creacion de la estructura con capacidad delimitada (2 elementos)
    estructura = EstructuraDatosUnidad1(capacidad=2)

    # 2. Inserciones validas
    elem1 = ElementoTDA(101, "Estructura de Datos I")
    elem2 = ElementoTDA(102, "Programacion Orientada a Objetos")
    estructura.insertar(elem1)
    estructura.insertar(elem2)

    # 3. Provocar Error de Comportamiento (Overflow)
    elem3 = ElementoTDA(103, "Base de Datos")
    estructura.insertar(elem3)

    # 4. Listar contenido
    estructura.listar_elementos()

    # 5. Aplicar Cambio Igualitario (Reemplazo en posicion 0)
    elem_nuevo = ElementoTDA(101, "Estructura de Datos I - Python PEP 8")
    estructura.modificar_igualitario(indice=0, nuevo_elemento=elem_nuevo)

    # 6. Eliminar elementos hasta provocar Error de Comportamiento (Underflow)
    print("\n--- PRUEBA DE ELIMINACION Y UNDERFLOW ---")
    estructura.eliminar_ultimo()
    estructura.eliminar_ultimo()
    estructura.eliminar_ultimo()  # Provoca Underflow

    # 7. Listar estado final
    estructura.listar_elementos()