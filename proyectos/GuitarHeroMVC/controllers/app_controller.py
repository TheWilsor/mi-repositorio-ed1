import flet as ft
from views.desktop_view import DesktopView
from models.game_engine import Game, Song, Player
from models.structures import DoublyLinkedList, Queue

class AppController(ft.UserControl):
    """
    Clase que controla la lógica de la aplicación, conectando la vista con el modelo de datos del juego.
    """

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.desktop_view = DesktopView()

    def build(self):
        """
        Método que construye la interfaz gráfica de usuario.
        Returns:
            ft.UserControl: La interfaz gráfica de usuario.
        """
        return self.desktop_view

    def on_start_button_click(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se hace clic en el botón "Start Game".
        """
        self.game.add_song_to_queue(Song("Song Title", "Artist", ["A", "B", "C", "D"]))
        self.desktop_view.current_song = self.game.queue.peek()
        self.desktop_view.update_labels()

    def on_add_button_click(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se hace clic en el botón "Add Player".
        """
        player_name = "Player " + str(len(self.game.players) + 1)
        self.game.add_player(Player(player_name))
        self.desktop_view.update_labels()

    def on_remove_button_click(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se hace clic en el botón "Remove Player".
        """
        if self.game.players:
            player_name = next(iter(self.game.players.keys()))
            self.game.remove_player(player_name)
            self.desktop_view.update_labels()

    def on_note_submit(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se envía el texto en el campo de entrada de notas.
        Args:
            e (ft.control_event.Event): El evento de envío del texto.
        """
        note = e.control.value
        self.game.process_note(next(iter(self.game.players.keys())), note)
        self.desktop_view.update_labels()

    def update_labels(self):
        """
        Método que actualiza las etiquetas de la interfaz gráfica con los datos actuales.
        """
        if self.game.current_song:
            self.desktop_view.current_song = self.game.current_song
            self.desktop_view.current_note = self.game.current_song.get_current_note()
        else:
            self.desktop_view.current_song = None
            self.desktop_view.current_note = None

        if self.desktop_view.current_song and self.desktop_view.current_note:
            self.desktop_view.title_label.value = f"{self.desktop_view.current_song.title} - {self.desktop_view.current_song.artist}"
            self.desktop_view.note_label.value = f"Current Note: {self.desktop_view.current_note}"
            self.desktop_view.score_label.value = f"Score: {self.game.get_player_score(next(iter(self.game.players.keys())))}"
        else:
            self.desktop_view.title_label.value = "No song playing"
            self.desktop_view.note_label.value = "Waiting for song"
            self.desktop_view.score_label.value = "Score: 0"

        self.desktop_view.update()
