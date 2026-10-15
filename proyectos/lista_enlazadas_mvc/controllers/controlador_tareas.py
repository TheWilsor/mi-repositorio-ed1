"""Controlador que procesa las peticiones de la Vista y filtra los datos según su estado."""

from models.lista_enlazada import ListaEnlazada


class ControladorTareas:
    """Controlador MVC para gestionar las operaciones del gestor de tareas."""

    def __init__(self):
        """Inicializa el modelo de la lista enlazada."""
        self.modelo = ListaEnlazada()

    def agregar_tarea(self, descripcion: str) -> str:
        """Valida e inserta una nueva tarea de forma secuencial."""
        descripcion = descripcion.strip()
        if not descripcion:
            raise ValueError("La descripción de la tarea no puede estar vacía.")

        self.modelo.agregar_tarea(descripcion)
        return f"Tarea '{descripcion}' agregada correctamente."

    def completar_tarea(self, texto_seleccionado: str) -> str:
        """Marca como completada la tarea seleccionada limpiando la numeración previa."""
        if not texto_seleccionado:
            raise ValueError("Debes seleccionar una tarea de alguna de las listas.")

        descripcion_limpia = self._extraer_descripcion(texto_seleccionado)
        if self.modelo.marcar_como_completada(descripcion_limpia):
            return f"Tarea '{descripcion_limpia}' marcada como completada."
        raise KeyError("La tarea no se encuentra en la lista.")

    def eliminar_tarea(self, texto_seleccionado: str) -> str:
        """Solicita la desvinculación de la tarea seleccionada en el TDA."""
        if not texto_seleccionado:
            raise ValueError("Debes seleccionar una tarea para eliminar.")

        descripcion_limpia = self._extraer_descripcion(texto_seleccionado)
        if self.modelo.eliminar_tarea(descripcion_limpia):
            return f"Tarea '{descripcion_limpia}' eliminada con éxito."
        raise KeyError("La tarea no pudo ser encontrada.")

    def obtener_listas_clasificadas(self) -> dict:
        """Obtiene todas las tareas y las clasifica numeradas para la Vista."""
        todas_raw = self.modelo.obtener_todas()

        todas_numeradas = []
        pendientes_numeradas = []
        completadas_numeradas = []

        idx_todas = 1
        idx_pendientes = 1
        idx_completadas = 1

        for desc, estado in todas_raw:
            # Lista 1: Todas las tareas
            etiqueta_estado = "[✓]" if estado == "completada" else "[ ]"
            todas_numeradas.append(f"{idx_todas}. {etiqueta_estado} {desc}")
            idx_todas += 1

            # Lista 2 y 3: Pendientes y Completadas
            if estado == "pendiente":
                pendientes_numeradas.append(f"{idx_pendientes}. {desc}")
                idx_pendientes += 1
            else:
                completadas_numeradas.append(f"{idx_completadas}. {desc}")
                idx_completadas += 1

        return {
            "todas": todas_numeradas,
            "pendientes": pendientes_numeradas,
            "completadas": completadas_numeradas
        }

    @staticmethod
    def _extraer_descripcion(cadena: str) -> str:
        """Elimina el número de índice y corchetes de la cadena para obtener solo el texto."""
        # Si tiene formato '1. [✓] Tarea' o '1. Tarea'
        if ". " in cadena:
            cadena = cadena.split(". ", 1)[1]
        if cadena.startswith("[✓] "):
            cadena = cadena.replace("[✓] ", "", 1)
        elif cadena.startswith("[ ] "):
            cadena = cadena.replace("[ ] ", "", 1)
        return cadena.strip()