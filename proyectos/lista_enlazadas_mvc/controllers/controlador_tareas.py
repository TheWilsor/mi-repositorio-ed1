"""Módulo del Controlador que conecta la UI con la lógica de negocio y maneja excepciones."""

from models.lista_enlazada import ListaEnlazada


class ControladorTareas:
    """Controlador MVC para gestionar las operaciones sobre las tareas."""

    def __init__(self):
        """Inicializa la lista enlazada como modelo de datos."""
        self.modelo = ListaEnlazada()

    def agregar_tarea(self, descripcion: str, posicion: str) -> str:
        """Valida y añade una tarea al inicio o al final según la opción."""
        descripcion = descripcion.strip()
        if not descripcion:
            raise ValueError("La descripción de la tarea no puede estar vacía.")

        if posicion == "inicio":
            self.modelo.agregar_al_principio(descripcion)
        else:
            self.modelo.agregar_al_final(descripcion)

        return f"Tarea '{descripcion}' agregada con éxito."

    def completar_tarea(self, descripcion: str) -> str:
        """Marca una tarea seleccionada como completada."""
        if not descripcion:
            raise ValueError("Debes seleccionar una tarea de la lista.")

        texto_limpio = self._extraer_texto(descripcion)

        if self.modelo.marcar_como_completada(texto_limpio):
            return f"Tarea '{texto_limpio}' marcada como completada."
        raise KeyError("La tarea no se encontró en la lista.")

    def eliminar_tarea(self, descripcion: str) -> str:
        """Elimina la tarea seleccionada de la lista."""
        if not descripcion:
            raise ValueError("Debes seleccionar una tarea para eliminar.")

        texto_limpio = self._extraer_texto(descripcion)

        if self.modelo.eliminar_tarea(texto_limpio):
            return f"Tarea '{texto_limpio}' eliminada."
        raise KeyError("La tarea no pudo ser encontrada.")

    def obtener_lista_tareas(self) -> list:
        """Obtiene las tareas actuales para actualizar la Vista."""
        return self.modelo.obtener_todas()

    @staticmethod
    def _extraer_texto(cadena: str) -> str:
        """Limpia el prefijo de estado '[PENDIENTE]' o '[COMPLETADA]'."""
        if "]" in cadena:
            return cadena.split("]", 1)[1].strip()
        return cadena.strip()