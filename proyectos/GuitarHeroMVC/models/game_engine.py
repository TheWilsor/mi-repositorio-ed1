"""Modelo del juego: canciones, jugadores, pistas y cola de reproducción."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, Optional

from models.structures import DoublyLinkedList, Node, Queue


class NoteEvent:
    """Evento de carril y tiempo de impacto desde el inicio del audio."""

    VALID_LANES: tuple[str, ...] = ("A", "S", "D", "F")

    def __init__(self, lane: str, time_seconds: float, duration: float = 0.0) -> None:
        normalized_lane = lane.strip().upper()
        if normalized_lane not in self.VALID_LANES:
            raise ValueError("El carril debe ser A, S, D o F.")
        if time_seconds < 0:
            raise ValueError("El instante de la nota no puede ser negativo.")

        self.lane: str = normalized_lane
        self.time_seconds: float = float(time_seconds)
        self.duration: float = float(duration)
        self.was_hit: bool = False
        self.was_missed: bool = False


class Song:
    """Canción con metadatos y eventos en una lista doble enlazada."""

    def __init__(
        self,
        title: str,
        artist: str,
        notes: Iterable[NoteEvent],
        audio_path: Optional[Path | str] = None,
        bpm: Optional[float] = None,
    ) -> None:
        self.title: str = title.strip()
        self.artist: str = artist.strip()
        self.audio_path: Optional[Path] = (
            Path(audio_path) if audio_path is not None else None
        )
        self.bpm: Optional[float] = bpm
        self.notes: DoublyLinkedList[NoteEvent] = DoublyLinkedList()
        previous_time = -1.0
        for note in notes:
            if note.time_seconds < previous_time:
                raise ValueError("Las notas deben estar ordenadas por tiempo.")
            self.notes.append(note)
            previous_time = note.time_seconds
        self.current_note_node: Optional[Node[NoteEvent]] = self.notes.head

    def set_rhythm_chart(
        self,
        notes: Iterable[NoteEvent],
        bpm: float,
    ) -> None:
        """Reemplaza el chart usando nodos y valida el orden temporal."""
        if bpm <= 0:
            raise ValueError("El BPM debe ser mayor que cero.")

        chart: DoublyLinkedList[NoteEvent] = DoublyLinkedList()
        previous_time = -1.0
        for note in notes:
            if note.time_seconds < previous_time:
                raise ValueError("Las notas deben estar ordenadas por tiempo.")
            chart.append(note)
            previous_time = note.time_seconds

        self.notes = chart
        self.current_note_node = chart.head
        self.bpm = float(bpm)

    @property
    def current_note(self) -> Optional[NoteEvent]:
        """Devuelve el siguiente evento pendiente de acertar o fallar."""
        if self.current_note_node is None:
            return None
        return self.current_note_node.data

    def get_current_event(self) -> Optional[NoteEvent]:
        """Devuelve el evento apuntado por la pista doblemente enlazada."""
        return self.current_note

    def get_current_note(self) -> Optional[str]:
        """Devuelve el carril actual o None cuando la pista terminó."""
        event = self.current_note
        return event.lane if event is not None else None

    def iter_notes(self) -> Iterator[NoteEvent]:
        """Recorre eventos sin copiar la pista a un contenedor nativo."""
        return iter(self.notes)

    def advance_note(self) -> None:
        """Avanza el puntero actual al siguiente nodo de la pista."""
        if self.current_note_node is not None:
            self.current_note_node = self.current_note_node.next

    def reset(self) -> None:
        """Reinicia el puntero de lectura y los estados de cada evento."""
        for note in self.notes:
            note.was_hit = False
            note.was_missed = False
        self.current_note_node = self.notes.head

    def is_complete(self) -> bool:
        """Indica si ya se consumieron todas las notas."""
        return self.current_note_node is None


class Player:
    """Estado y puntuación acumulada de un jugador."""

    def __init__(self, name: str) -> None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("El nombre del jugador no puede estar vacío.")
        self.name: str = cleaned_name
        self.score: int = 0
        self.streak: int = 0
        self.multiplier: int = 1

    def register_hit(self) -> int:
        """Actualiza racha y multiplicador, y devuelve los puntos obtenidos."""
        self.streak += 1
        self.multiplier = min(4, 1 + self.streak // 10)
        points = 100 * self.multiplier
        self.score += points
        return points

    def register_miss(self) -> None:
        """Reinicia racha y multiplicador sin alterar la puntuación."""
        self.streak = 0
        self.multiplier = 1

    def update_score(self, points: int) -> None:
        """Añade puntos explícitos al marcador del jugador."""
        self.score += points


class GameEngine:
    """Coordina la cola de canciones y el registro enlazado de jugadores."""

    def __init__(self) -> None:
        self.songs: DoublyLinkedList[Song] = DoublyLinkedList()
        self.queue: Queue[Song] = Queue()
        self.current_song: Optional[Song] = None
        self.players: DoublyLinkedList[Player] = DoublyLinkedList()

    def add_song(self, song: Song) -> None:
        """Añade una canción al catálogo enlazado."""
        self.songs.append(song)

    def add_song_to_queue(self, song: Song) -> None:
        """Encola una canción para reproducirla en orden FIFO."""
        if not self.songs.search(song):
            self.songs.append(song)
        self.queue.enqueue(song)

    def remove_song_from_queue(self, song: Song) -> bool:
        """Retira la primera coincidencia de la cola de reproducción."""
        return self.queue.delete(song)

    def start_next_song(self) -> Optional[Song]:
        """Inicia la siguiente canción disponible y reinicia su puntero."""
        if (
            self.current_song is not None
            and not self.current_song.is_complete()
        ):
            return self.current_song

        self.current_song = self.queue.dequeue()
        if self.current_song is not None:
            self.current_song.reset()
        return self.current_song

    def end_song(self) -> None:
        """Finaliza y libera la canción activa."""
        self.current_song = None

    def add_player(self, player: Player) -> Player:
        """Registra un jugador, rechazando nombres duplicados."""
        if self.get_player(player.name) is not None:
            raise ValueError(f"Ya existe un jugador llamado {player.name}.")
        self.players.append(player)
        return player

    def get_player(self, player_name: str) -> Optional[Player]:
        """Busca un jugador por nombre recorriendo los nodos enlazados."""
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def first_player(self) -> Optional[Player]:
        """Devuelve el primer jugador registrado, si existe."""
        if self.players.head is None:
            return None
        return self.players.head.data

    def remove_player(self, player_name: str) -> bool:
        """Elimina al jugador indicado y devuelve si se encontró."""
        player = self.get_player(player_name)
        if player is None:
            return False
        return self.players.remove(player)

    def get_song_title(self) -> str:
        """Devuelve el título activo o una etiqueta de espera."""
        if self.current_song is None:
            return "No song playing"
        return self.current_song.title

    def get_player_score(self, player_name: str) -> int:
        """Consulta el marcador; nombres inexistentes producen cero."""
        player = self.get_player(player_name)
        if player is None:
            return 0
        return player.score

    def process_note(self, player_name: str, note: str) -> bool:
        """Procesa una nota para compatibilidad con clientes del modelo."""
        player = self.get_player(player_name)
        if player is None or self.current_song is None:
            return False

        expected_note = self.current_song.get_current_note()
        if expected_note is None or note.strip().upper() != expected_note:
            player.register_miss()
            return False

        player.register_hit()
        self.current_song.advance_note()
        return True

    @property
    def player_count(self) -> int:
        return len(self.players)


# Alias de compatibilidad con versiones anteriores del modelo.
Game = GameEngine
