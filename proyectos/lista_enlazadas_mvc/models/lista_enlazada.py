"""Módulo del TDA Lista Enlazada para la gestión de tareas."""

from models.nodo import Nodo


class ListaEnlazada:
    """TDA Lista Enlazada Simple para manejar la colección de tareas."""

    def __init__(self):
        """Inicializa una lista enlazada vacía."""
        self.cabeza = None

    def agregar_al_principio(self, descripcion: str) -> None:
        """Añade una nueva tarea al inicio de la lista (Complejidad: O(1))."""
        nuevo_nodo = Nodo(descripcion)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    def agregar_al_final(self, descripcion: str) -> None:
        """Añade una nueva tarea al final de la lista (Complejidad: O(n))."""
        nuevo_nodo = Nodo(descripcion)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo_nodo

    def marcar_como_completada(self, descripcion: str) -> bool:
        """Busca una tarea por su descripción y cambia su estado a 'completada'."""
        actual = self.cabeza
        while actual:
            if actual.descripcion == descripcion:
                actual.estado = "completada"
                return True
            actual = actual.siguiente
        return False

    def eliminar_tarea(self, descripcion: str) -> bool:
        """Busca una tarea por su descripción y la remueve de la lista (Complejidad: O(n))."""
        actual = self.cabeza
        anterior = None

        while actual:
            if actual.descripcion == descripcion:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def obtener_todas(self) -> list:
        """Recorre la lista enlazada y retorna una lista con las representaciones en texto."""
        tareas = []
        actual = self.cabeza
        while actual:
            tareas.append(str(actual))
            actual = actual.siguiente
        return tareas