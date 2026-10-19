from typing import List, Dict, Optional
from models.structures import Queue, DoublyLinkedList

class Song:
    """
    Clase que representa una canción con un título, artista y una lista de notas.
    """

    def __init__(self, title: str, artist: str, notes: List[str]):
        self.title = title
        self.artist = artist
        self.notes = notes
        self.current_note_index: int = 0

    def get_current_note(self) -> str:
        """
        Método que devuelve la nota actual de la canción.
        Returns:
            str: La nota actual de la canción.
        """
        if self.current_note_index < len(self.notes):
            return self.notes[self.current_note_index]
        return None

    def advance_note(self) -> None:
        """
        Método que avanza a la siguiente nota de la canción.
        """
        if self.current_note_index < len(self.notes) - 1:
            self.current_note_index += 1

class Player:
    """
    Clase que representa un jugador con un nombre y una puntuación inicial.
    """

    def __init__(self, name: str):
        self.name = name
        self.score: int = 0

    def update_score(self, points: int) -> None:
        """
        Método que actualiza la puntuación del jugador.
        Args:
            points (int): Puntos a agregar a la puntuación del jugador.
        """
        self.score += points

class Game:
    """
    Clase que representa el juego principal con una lista de canciones, una cola de reproducción,
    una canción actual y un diccionario de jugadores.
    """

    def __init__(self):
        self.songs: DoublyLinkedList[Song] = DoublyLinkedList()
        self.queue: Queue[Song] = Queue()
        self.current_song: Optional[Song] = None
        self.players: Dict[str, Player] = {}

    def add_song(self, song: Song) -> None:
        """
        Método que agrega una canción a la lista de canciones.
        Args:
            song (Song): La canción a agregar.
        """
        self.songs.append(song)

    def add_song_to_queue(self, song: Song) -> None:
        """
        Método que agrega una canción a la cola de reproducción.
        Args:
            song (Song): La canción a agregar.
        """
        self.queue.enqueue(song)

    def remove_song_from_queue(self, song: Song) -> None:
        """
        Método que elimina una canción de la cola de reproducción.
        Args:
            song (Song): La canción a eliminar.
        """
        self.queue.delete(song)

    def start_song(self) -> None:
        """
        Método que inicia la reproducción de la canción en la cola.
        """
        if not self.queue.is_empty():
            self.current_song = self.queue.dequeue()
            self.current_song.current_note_index = 0

    def end_song(self) -> None:
        """
        Método que finaliza la reproducción de la canción.
        """
        if self.current_song:
            self.current_song = None

    def add_player(self, player: Player) -> None:
        """
        Método que agrega un jugador al juego.
        Args:
            player (Player): El jugador a agregar.
        """
        self.players[player.name] = player

    def remove_player(self, player_name: str) -> None:
        """
        Método que elimina un jugador del juego.
        Args:
            player_name (str): El nombre del jugador a eliminar.
        """
        if player_name in self.players:
            del self.players[player_name]

    def get_song_title(self) -> str:
        """
        Método que devuelve el título de la canción actual.
        Returns:
            str: El título de la canción actual.
        """
        if self.current_song:
            return self.current_song.title
        return "No song playing"

    def get_player_score(self, player_name: str) -> int:
        """
        Método que devuelve la puntuación de un jugador.
        Args:
            player_name (str): El nombre del jugador.
        Returns:
            int: La puntuación del jugador.
        """
        if player_name in self.players:
            return self.players[player_name].score
        return 0

    def process_note(self, player_name: str, note: str) -> None:
        """
        Método que procesa una nota ingresada por un jugador y actualiza su puntuación.
        Args:
            player_name (str): El nombre del jugador.
            note (str): La nota ingresada.
        """
        if self.current_song and self.current_song.get_current_note() == note:
            player = self.players.get(player_name)
            if player:
                player.update_score(10)  # Score for correct note
            self.current_song.advance_note()
        else:
            player = self.players.get(player_name)
            if player:
                player.update_score(-5)  # Penalty for incorrect note
