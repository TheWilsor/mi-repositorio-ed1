import flet as ft
from models.game_engine import Game, Song, Player
from models.structures import DoublyLinkedList, Queue

class DesktopView(ft.UserControl):
    """
    Clase que representa la interfaz gráfica de usuario (GUI) utilizando Flet.
    """

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.current_song = None
        self.current_note = None
        self.current_player = None

        self.title_label = ft.Text(value="", style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.note_label = ft.Text(value="", style=ft.TextThemeStyle.BODY_MEDIUM)
        self.score_label = ft.Text(value="", style=ft.TextThemeStyle.BODY_MEDIUM)

        self.note_input = ft.TextField(hint_text="Enter note", on_submit=self.on_note_submit)
        self.start_button = ft.ElevatedButton(text="Start Game", on_click=self.on_start_button_click)
        self.add_button = ft.ElevatedButton(text="Add Player", on_click=self.on_add_button_click)
        self.remove_button = ft.ElevatedButton(text="Remove Player", on_click=self.on_remove_button_click)

    def build(self):
        """
        Método que construye la interfaz gráfica de usuario.
        Returns:
            ft.Column: Una columna que contiene todos los componentes de la interfaz.
        """
        return ft.Column(
            [
                ft.Row([self.title_label, self.score_label]),
                ft.Row([self.note_label]),
                ft.Row([self.note_input]),
                ft.Row([self.start_button, self.add_button, self.remove_button]),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def on_start_button_click(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se hace clic en el botón "Start Game".
        """
        self.game.add_song_to_queue(Song("Song Title", "Artist", ["A", "B", "C", "D"]))
        self.current_song = self.game.queue.peek()
        self.update_labels()

    def on_add_button_click(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se hace clic en el botón "Add Player".
        """
        player_name = "Player " + str(len(self.game.players) + 1)
        self.game.add_player(Player(player_name))
        self.update_labels()

    def on_remove_button_click(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se hace clic en el botón "Remove Player".
        """
        if self.game.players:
            player_name = next(iter(self.game.players.keys()))
            self.game.remove_player(player_name)
            self.update_labels()

    def on_note_submit(self, e: ft.control_event.Event):
        """
        Método que se ejecuta cuando se envía el texto en el campo de entrada de notas.
        Args:
            e (ft.control_event.Event): El evento de envío del texto.
        """
        note = e.control.value
        self.game.process_note(self.current_player.name, note)
        self.update_labels()

    def update_labels(self):
        """
        Método que actualiza los etiquetas de la interfaz gráfica con los datos actuales.
        """
        if self.game.current_song:
            self.current_song = self.game.current_song
            self.current_note = self.current_song.get_current_note()
        else:
            self.current_song = None
            self.current_note = None

        if self.current_song and self.current_note:
            self.title_label.value = f"{self.current_song.title} - {self.current_song.artist}"
            self.note_label.value = f"Current Note: {self.current_note}"
            self.score_label.value = f"Score: {self.game.get_player_score(self.current_player.name)}"
        else:
            self.title_label.value = "No song playing"
            self.note_label.value = "Waiting for song"
            self.score_label.value = "Score: 0"

        self.update()
