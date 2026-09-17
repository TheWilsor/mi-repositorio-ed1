"""Módulo del TDA Lista Enlazada Simple con inserción secuencial y desvinculación por punteros."""

from models.nodo import Nodo


class ListaEnlazada:
    """TDA Lista Enlazada para gestionar la colección de tareas mediante punteros."""

    def __init__(self):
        """Inicializa una lista enlazada vacía sin nodos."""
        self.cabeza = None

    def agregar_tarea(self, descripcion: str) -> None:
        """Busca el primer lugar vacío y enlaza el nuevo nodo al final de la secuencia."""
        nuevo_nodo = Nodo(descripcion)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo_nodo

    def eliminar_tarea(self, descripcion: str) -> bool:
        """Desvincula un nodo de la lista reconectando el nodo anterior con el siguiente."""
        actual = self.cabeza
        anterior = None

        while actual is not None:
            if actual.descripcion == descripcion:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                actual.siguiente = None
                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def marcar_como_completada(self, descripcion: str) -> bool:
        """Recorre los punteros para encontrar la tarea y actualizar su estado."""
        actual = self.cabeza
        while actual is not None:
            if actual.descripcion == descripcion:
                actual.estado = "completada"
                return True
            actual = actual.siguiente
        return False

    def obtener_todas(self) -> list:
        """Recorre la cadena de punteros y retorna tuplas con (descripción, estado)."""
        tareas = []
        actual = self.cabeza
        while actual is not None:
            tareas.append((actual.descripcion, actual.estado))
            actual = actual.siguiente
        return tareas