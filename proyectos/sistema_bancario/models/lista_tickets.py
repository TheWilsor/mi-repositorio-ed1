"""TDA Lista Enlazada adaptado para la gestión de colas de tickets bancarios."""

from models.nodo_ticket import NodoTicket


class ListaTickets:
    """Lista enlazada simple para administrar los nodos de tickets por punteros."""

    def __init__(self):
        """Inicializa la lista vacía con punteros de cabeza y correlativos."""
        self.cabeza = None
        self.correlativo_area = {
            "Atención al Cliente": 1,
            "Cajas": 1,
            "Plataforma": 1
        }

    def generar_ticket(self, area: str) -> NodoTicket:
        """Crea un nuevo ticket y lo enlaza al final de la lista enlazada (Inserción O(n))."""
        prefijo = {
            "Atención al Cliente": "AC",
            "Cajas": "CA",
            "Plataforma": "PL"
        }.get(area, "TK")

        numero_fmt = f"{prefijo}-{self.correlativo_area[area]:03d}"
        self.correlativo_area[area] += 1

        nuevo_nodo = NodoTicket(numero_fmt, area)

        # Inserción por punteros: Caso 1 (Lista vacía)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return nuevo_nodo

        # Inserción por punteros: Caso 2 (Recorrer hasta el puntero libre)
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo_nodo
        return nuevo_nodo

    def llamar_siguiente_ticket(self, ventanilla: str) -> NodoTicket:
        """Avanza al primer ticket 'En Espera', lo pone 'En Atención' y finaliza el anterior."""
        actual = self.cabeza
        
        # Finalizar ticket anterior en atención
        while actual is not None:
            if actual.estado == "En Atención":
                actual.estado = "Finalizado"
            actual = actual.siguiente

        # Buscar el siguiente en lista con estado 'En Espera'
        actual = self.cabeza
        while actual is not None:
            if actual.estado == "En Espera":
                actual.estado = "En Atención"
                actual.ventanilla = ventanilla
                return actual
            actual = actual.siguiente

        return None

    def obtener_clasificados(self) -> dict:
        """Recorre la lista enlazada por punteros y clasifica los tickets para las pantallas."""
        en_espera = []
        finalizados = []
        en_atencion = None

        actual = self.cabeza
        while actual is not None:
            if actual.estado == "En Espera":
                en_espera.append(f"{actual.numero} ({actual.area})")
            elif actual.estado == "En Atención":
                en_atencion = f"{actual.numero} -> {actual.ventanilla}"
            elif actual.estado == "Finalizado":
                finalizados.append(f"{actual.numero} ({actual.area}) - {actual.ventanilla}")
            actual = actual.siguiente

        return {
            "en_espera": en_espera,
            "en_atencion": en_atencion or "Esperando llamado...",
            "finalizados": finalizados[::-1]
        }