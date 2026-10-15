"""Módulo que representa un Nodo Ticket en el TDA Lista Enlazada."""

from datetime import datetime


class NodoTicket:
    """Nodo individual para la lista enlazada de atención bancaria."""

    def __init__(self, numero: str, area: str):
        """Inicializa los datos del ticket bancario.
        
        Estados posibles: 'En Espera', 'En Atención', 'Finalizado'
        """
        self.numero = numero          # Ej: "AC-001", "CA-002", "PL-003"
        self.area = area              # Ej: "Atención al Cliente", "Cajas", "Plataforma"
        self.estado = "En Espera"     # Estado inicial al registrarse
        self.ventanilla = "-"         # Se asigna cuando entra 'En Atención'
        self.hora_emision = datetime.now().strftime("%H:%M:%S")
        self.siguiente = None         # Puntero al próximo nodo en la lista

    def __str__(self) -> str:
        return f"[{self.numero}] {self.area} | Estado: {self.estado}"