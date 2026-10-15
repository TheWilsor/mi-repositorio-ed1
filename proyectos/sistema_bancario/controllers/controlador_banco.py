"""Controlador MVC que coordina los tickets y el llamado por voz (TTS)."""

import threading
import pyttsx3
from models.lista_tickets import ListaTickets


class ControladorBanco:
    """Gestiona las operaciones del banco y los anuncios por altavoz."""

    def __init__(self):
        """Inicializa la lista enlazada de tickets."""
        self.modelo = ListaTickets()

    def solicitar_ticket(self, area: str) -> str:
        """Solicita la creación de un nuevo nodo ticket en el TDA."""
        ticket = self.modelo.generar_ticket(area)
        return ticket.numero

    def llamar_siguiente(self, ventanilla: str) -> str:
        """Atiende al siguiente ticket de la lista y emite la voz por altavoz."""
        ticket = self.modelo.llamar_siguiente_ticket(ventanilla)
        if ticket:
            # Texto formateado para una pronunciación completa, fluida y clara
            # Ejemplo: "Ticket A C 0 0 1, favor pasar a Ventanilla 1"
            numero_deletreado = " ".join(ticket.numero)  # Separa letras y números para que los lea uno a uno
            mensaje_voz = f"Ticket {numero_deletreado}, favor pasar a {ventanilla}."
            
            # Ejecutar anuncio de voz en un hilo secundario para no congelar la GUI
            threading.Thread(target=self._anunciar_por_voz, args=(mensaje_voz,), daemon=True).start()
            return f"Atendiendo a {ticket.numero}"
        return "No hay tickets en espera."

    def obtener_estado_pantallas(self) -> dict:
        """Retorna las listas de tickets formateadas para la vista."""
        return self.modelo.obtener_clasificados()

    @staticmethod
    def _anunciar_por_voz(texto: str):
        """Inicializa el motor nativo de voz de Windows y reproduce el mensaje."""
        try:
            engine = pyttsx3.init()
            
            # Configurar velocidad y volumen
            engine.setProperty('rate', 110)   # Velocidad ligeramente más pausada y clara
            engine.setProperty('volume', 1.0) # Volumen máximo
            
            # (Opcional) Seleccionar voz en español si está disponible en Windows
            voices = engine.getProperty('voices')
            for voice in voices:
                if "spanish" in voice.name.lower() or "es" in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.say(texto)
            engine.runAndWait()
        except Exception as e:
            print(f"Error al reproducir audio: {e}")