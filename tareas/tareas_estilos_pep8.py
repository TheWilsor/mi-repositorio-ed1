"""
Modulo para la practica de Estandares de Programacion (PEP 8).
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Libros:
    """
    Representa la estructura de un libro dentro de un catalogo
    """

    def __init__(self, titulo: str, autor: str, isbn: str):
        """
        Constructor de la clase Libros.

        Args:
            titulo (str): Titulo del libro
            autor (str): Nombre del autor del libro
            isbn (str): Codigo identificador unico del libro
        """
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn

    def obtener_titulo(self) -> str:
        """Obtiene el titulo del libro"""
        return self._titulo

    def obtener_isbn(self) -> str:
        """Obtiene el codigo ISBN del libro"""
        return self._isbn

    def establecer_titulo(self, nuevo_titulo: str) -> None:
        """Asigna un nuevo titulo al libro"""
        self._titulo = nuevo_titulo

    def mostrar_informacion(self) -> str:
        """Devuelve la informacion formateada del libro"""
        return f"Libro: '{self._titulo}', Autor: {self._autor}, ISBN: {self._isbn}"


class Catalogo:
    """
    Gestor de coleccion de libros representado como un catalogo
    """

    def __init__(self) -> None:
        """Inicializa una coleccion vacia dentro del catalogo"""
        self._lista_libros: list[Libros] = []

    def agregar_libro(self, libro: Libros) -> None:
        """Adiciona un nuevo libro al catalogo"""
        self._lista_libros.append(libro)
        print(f"-> Libro '{libro.obtener_titulo()}' agregado al catalogo con exito")

    def listar_libros(self) -> None:
        """Muestra en consola la lista con todos los libros registrados"""
        if not self._lista_libros:
            print("El catalogo esta vacio")
            return

        print("\nLista de libros en el catalogo disponibles:")
        for idx, libro in enumerate(self._lista_libros, start=1):
            print(f"{idx}. {libro.mostrar_informacion()}")


if __name__ == "__main__":
    # 1. Instancia del catalogo
    mi_catalogo = Catalogo()

    # 2. Creacion de instancias de Libros
    libro1 = Libros("Estructura de Datos I en Python", "Ing. Peinado", "000-001")
    libro2 = Libros("Como Dejar de ser Pelau", "Pinocho", "000-002")
    libro3 = Libros("Solo un Punto Ing", "No quiero otro Rojo", "000-003")
    libro4 = Libros("El Principito", "Antoine de Saint-Exupery", "000-004")

    # 3. Agregar los libros al catalogo
    print("--- Agregando Libros ---")
    mi_catalogo.agregar_libro(libro1)
    mi_catalogo.agregar_libro(libro2)
    mi_catalogo.agregar_libro(libro3)
    mi_catalogo.agregar_libro(libro4)

    # 4. Mostrar lista disponible
    mi_catalogo.listar_libros()