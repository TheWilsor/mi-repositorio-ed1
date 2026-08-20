"""
Modulo para la practica de Estandares de Programacion (PEP 8).
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Libros:
    """
    Representa la estructura de un libro dentro de un catalogo.
    """

    def __init__(self, titulo: str, autor: str, isbn: str):
        """
        Constructor de la clase Libros.

        Args:
            titulo (str): Titulo del libro.
            autor (str): Nombre del autor del libro.
            isbn (str): Codigo identificador unico del libro.
        """
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn

    def obtener_titulo(self) -> str:
        """Obtiene el titulo del libro."""
        return self._titulo

    def obtener_isbn(self) -> str:
        """Obtiene el codigo ISBN del libro."""
        return self._isbn

    def establecer_titulo(self, nuevo_titulo: str) -> None:
        """Asigna un nuevo titulo al libro."""
        self._titulo = nuevo_titulo

    def mostrar_informacion(self) -> str:
        """Devuelve la informacion formateada del libro."""
        return f"Libro: '{self._titulo}', Autor: {self._autor}, ISBN: {self._isbn}"


class Catalogo:
    """
    Gestor de coleccion de libros representado como un catalogo.
    """

    def __init__(self) -> None:
        """Inicializa una coleccion vacia dentro del catalogo."""
        self._lista_libros: list[Libros] = []

    def agregar_libro(self, libro: Libros) -> None:
        """Adiciona un nuevo libro al catalogo si el ISBN no existe."""
        if self.buscar_por_isbn(libro.obtener_isbn()) is not None:
            print(f"-> Error: El libro con ISBN '{libro.obtener_isbn()}' ya existe.")
            return

        self._lista_libros.append(libro)
        print(f"-> Libro '{libro.obtener_titulo()}' agregado al catalogo con exito.")

    def buscar_por_isbn(self, isbn: str) -> Libros | None:
        """
        Busca un libro en el catalogo mediante su ISBN.

        Args:
            isbn (str): Identificador del libro a buscar.

        Returns:
            Libros | None: Objeto Libros si lo encuentra, o None si no existe.
        """
        for libro in self._lista_libros:
            if libro.obtener_isbn() == isbn:
                return libro
        return None

    def eliminar_libro(self, isbn: str) -> bool:
        """
        Elimina un libro del catalogo buscando su ISBN.

        Args:
            isbn (str): Identificador del libro a eliminar.

        Returns:
            bool: True si lo elimino correctamente, False si no lo encontro.
        """
        libro_encontrado = self.buscar_por_isbn(isbn)
        if libro_encontrado:
            self._lista_libros.remove(libro_encontrado)
            print(f"-> Libro '{libro_encontrado.obtener_titulo()}' eliminado con exito.")
            return True

        print(f"-> No se pudo eliminar: El ISBN '{isbn}' no existe en el catalogo.")
        return False

    def listar_libros(self) -> None:
        """Muestra en consola la lista con todos los libros registrados."""
        if not self._lista_libros:
            print("El catalogo esta vacio.")
            return

        print("\nLista de libros en el catalogo disponibles:")
        for idx, libro in enumerate(self._lista_libros, start=1):
            print(f"{idx}. {libro.mostrar_informacion()}")


def ejecucion_demostracion_directa():
    """Demostracion automatica de la primera parte del ejercicio."""
    mi_catalogo = Catalogo()

    libro1 = Libros("Estructura de Datos I en Python", "Ing. Peinado", "000-001")
    libro2 = Libros("Como Dejar de ser Pelau", "Pinocho", "000-002")
    libro3 = Libros("Solo un Punto Ing", "No quiero otro Rojo", "000-003")
    libro4 = Libros("El Principito", "Antoine de Saint-Exupery", "000-004")

    print("--- Agregando Libros (Carga Inicial) ---")
    mi_catalogo.agregar_libro(libro1)
    mi_catalogo.agregar_libro(libro2)
    mi_catalogo.agregar_libro(libro3)
    mi_catalogo.agregar_libro(libro4)

    mi_catalogo.listar_libros()

# "No toma encuenta los Datos de Ejecucion Directa"^^^^^ X
def ejecucion_menu_interactivo():
    """Demostracion interactiva mediante menu en consola."""
    mi_catalogo = Catalogo()

    # Carga inicial opcional de prueba puede agregarlos o eliminar
    mi_catalogo.agregar_libro(
        Libros("Estructura de Datos I en Python", "Ing. Peinado", "000-001")
    )
    mi_catalogo.agregar_libro(
        Libros("El Principito", "Antoine de Saint-Exupery", "000-004")
    )
    # Aqui solo se mostraran lo que se agreguen en la carga inicial^^^^^^
    while True:
        print("\n==============================")
        print("  GESTION DE CATALOGO DE LIBROS")
        print("==============================")
        print("1. Agregar libro manualmente")
        print("2. Buscar libro por ISBN")
        print("3. Eliminar libro por ISBN")
        print("4. Listar todos los libros")
        print("5. Salir")

        opcion = input("Seleccione una opcion (1-5): ").strip()
        
        if opcion == "1":
            # Agregado del nuevo libro
            print("\n--- AGREGAR LIBRO ---")
            titulo = input("Ingrese el titulo del libro: ").strip()
            autor = input("Ingrese el autor del libro: ").strip()
            isbn = input("Ingrese el codigo ISBN: ").strip()

            if titulo and autor and isbn:
                nuevo_libro = Libros(titulo, autor, isbn)
                mi_catalogo.agregar_libro(nuevo_libro)
            else:
                print("-> Error: Todos los campos son obligatorios.")
            # Si no cumple con el llenado correcto lo descarta
        elif opcion == "2":
            # Buscador del catalogo por medio del ISBN
            print("\n--- BUSCAR LIBRO ---")
            isbn = input("Ingrese el ISBN a buscar: ").strip()
            resultado = mi_catalogo.buscar_por_isbn(isbn)

            if resultado:
                print(f"-> Libro encontrado: {resultado.mostrar_informacion()}")
            else:
                print(f"-> No se encontro ningun libro con el ISBN '{isbn}'.")

        elif opcion == "3":
            # Elimina el libro por medio del ISBN
            print("\n--- ELIMINAR LIBRO ---")
            isbn = input("Ingrese el ISBN a eliminar: ").strip()
            mi_catalogo.eliminar_libro(isbn)

        elif opcion == "4":
            # Muestra el listado de libros
            mi_catalogo.listar_libros()
            # Solo los que se agregaron en la ejucion o agregados en la carga inicial
        elif opcion == "5":
            # Cierra el programa
            print("Saliendo del programa...")
            break

        else:
            print("-> Opcion no valida. Intente de nuevo.")

        # Primera vercion estatica su Estructura en Pep8
if __name__ == "__main__":
    # 1. Ejecutamos la demostracion estatica inicial
    ejecucion_demostracion_directa()

    # 2. Ejecutamos el menu interactivo adicional funcional
    ejecucion_menu_interactivo()