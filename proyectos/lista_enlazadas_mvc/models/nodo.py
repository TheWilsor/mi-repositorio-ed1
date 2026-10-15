"""Módulo que define la estructura del Nodo para la Lista Enlazada."""


class Nodo:
    """Clase que representa un nodo individual en la lista enlazada."""

    def __init__(self, descripcion: str, estado: str = "pendiente"):
        """Inicializa un nuevo nodo con su descripción, estado y puntero al siguiente."""
        self.descripcion = descripcion
        self.estado = estado
        self.siguiente = None

    def __str__(self) -> str:
        """Devuelve una representación en texto del nodo."""
        return f"[{self.estado.upper()}] {self.descripcion}"