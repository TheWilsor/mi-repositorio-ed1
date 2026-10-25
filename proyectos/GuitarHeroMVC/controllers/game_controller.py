"""Controlador para el ciclo arcade, el audio y la evaluación de impactos."""

from __future__ import annotations

from pathlib import Path
from threading import RLock
from typing import Iterable, Optional

from controllers.audio_controller import AudioController, AudioPlayer
from models.game_engine import GameEngine, NoteEvent, Player, Song


class GameController:
    """Sincroniza eventos enlazados con el reloj de pygame y la puntuación."""

    def __init__(
        self,
        audio_player: Optional[AudioPlayer] = None,
        hit_window_seconds: float = 0.22,
    ) -> None:
        if hit_window_seconds <= 0:
            raise ValueError("La ventana de acierto debe ser positiva.")
        self.engine: GameEngine = GameEngine()
        self.audio_player: AudioPlayer = audio_player or AudioController()
        self.current_player: Optional[Player] = None
        self.running: bool = False
        self.audio_started: bool = False
        self.playback_time: float = 0.0
        self.duration_seconds: float = 0.0
        self.hit_window_seconds: float = hit_window_seconds
        self._next_player_number: int = 1
        self._lock: RLock = RLock()

    def add_player(self, name: Optional[str] = None) -> Player:
        """Registra y selecciona un jugador, generando nombre si hace falta."""
        with self._lock:
            if name is None:
                while True:
                    candidate = f"Player {self._next_player_number}"
                    self._next_player_number += 1
                    if self.engine.get_player(candidate) is None:
                        name = candidate
                        break

            player = self.engine.add_player(Player(name))
            if self.current_player is None:
                self.current_player = player
            return player

    def remove_player(self, player_name: str) -> bool:
        """Elimina un jugador y reasigna el activo de forma segura."""
        with self._lock:
            player = self.engine.get_player(player_name)
            if player is None:
                return False

            was_current = player is self.current_player
            removed = self.engine.remove_player(player_name)
            if removed and was_current:
                self.current_player = self.engine.first_player()
            return removed

    def add_song_to_queue(
        self,
        title: str,
        artist: str,
        notes: Iterable[NoteEvent],
        audio_path: Optional[Path | str] = None,
    ) -> Song:
        """Encola una canción con pista cronometrada en nodos enlazados."""
        song = Song(title, artist, notes, audio_path)
        self.enqueue_song(song)
        return song

    def enqueue_song(self, song: Song) -> None:
        """Encola una canción ya construida sin copiar su pista de nodos."""
        with self._lock:
            self.engine.add_song_to_queue(song)

    def start_game_loop(self) -> str:
        """Inicia la canción y reproduce el MP3 de forma asíncrona."""
        with self._lock:
            if self.current_player is None:
                self.running = False
                return "Agrega un jugador antes de iniciar."
            if self.running and self.engine.current_song is not None:
                song = self.engine.current_song
                return f"Reproduciendo: {song.title} - {song.artist}"

            song = self.engine.start_next_song()
            if song is None:
                self.running = False
                return "No hay canciones en la cola."

            song.reset()
            self.playback_time = 0.0
            self.duration_seconds = self.audio_player.get_duration_seconds(
                song.audio_path
            )
            self.audio_started = self.audio_player.play(song.audio_path)
            self.running = not song.is_complete()
            return f"Reproduciendo: {song.title} - {song.artist}"

    def update_playback(self) -> float:
        """Actualiza el puntero con avance fluido y tolerancia para ráfagas rápidas."""
        with self._lock:
            if not self.running:
                return self.playback_time

            # 1. Obtener la posición real del audio
            elapsed = self.audio_player.get_position_seconds()
            
            # 2. Avance híbrido: Si el audio se congela o da saltos, el reloj del juego 
            # avanza suavemente con el delta del loop de 60 FPS (aprox 0.016s) para evitar baches.
            if elapsed > 0 and elapsed >= self.playback_time:
                self.playback_time = elapsed
            else:
                self.playback_time += 1.0 / 60.0

            song = self.engine.current_song
            player = self.current_player
            
            if song is not None:
                event = song.current_note
                while (
                    event is not None
                    and self.playback_time
                    > event.time_seconds + self.hit_window_seconds
                ):
                    event.was_missed = True
                    if player is not None:
                        player.register_miss()
                    song.advance_note()
                    event = song.current_note

            if (
                self.duration_seconds > 0
                and self.playback_time >= self.duration_seconds
            ):
                self.running = False
                self.audio_player.stop()
                
            return self.playback_time

    def press_lane(self, lane: str) -> bool:
        """Evalúa el carril y su cercanía temporal a la zona de impacto."""
        normalized_lane = lane.strip().upper()
        if normalized_lane not in NoteEvent.VALID_LANES:
            return False

        with self._lock:
            self.update_playback()
            song = self.engine.current_song
            player = self.current_player
            if not self.running or song is None or player is None:
                return False

            event = song.current_note
            if event is None:
                return False
            distance = abs(self.playback_time - event.time_seconds)
            if distance > self.hit_window_seconds:
                return False
            if normalized_lane != event.lane:
                player.register_miss()
                return False

            event.was_hit = True
            player.register_hit()
            song.advance_note()
            return True

    def process_note(self, note: str) -> bool:
        """Alias de compatibilidad para el evento de tecla de un carril."""
        return self.press_lane(note)

    def process_key_press(self, lane_index: int) -> bool:
        """Traduce índices 0-3 a las teclas A-S-D-F."""
        if lane_index < 0 or lane_index > 3:
            return False
        return self.press_lane(NoteEvent.VALID_LANES[lane_index])

    def get_score_summary(self) -> str:
        """Devuelve puntaje, racha y multiplicador del jugador activo."""
        with self._lock:
            player = self.current_player
            if player is None:
                return "Puntaje: 0 | Racha: 0 | Multiplicador: x1"
            return (
                f"Puntaje: {player.score} | Racha: {player.streak} | "
                f"Multiplicador: x{player.multiplier}"
            )

    def stop(self) -> None:
        """Detiene el audio y el ciclo de juego actual."""
        with self._lock:
            self.running = False
            self.audio_player.stop()

    @property
    def current_note(self) -> Optional[NoteEvent]:
        """Devuelve el próximo evento de la canción activa."""
        song = self.engine.current_song
        return song.current_note if song is not None else None

    @property
    def has_playable_song(self) -> bool:
        """Indica si hay una canción activa o pendiente de reproducción."""
        return self.running or not self.engine.queue.is_empty()