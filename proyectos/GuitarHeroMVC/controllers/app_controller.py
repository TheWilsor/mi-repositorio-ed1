"""Controlador de aplicación para biblioteca, beats y vista Flet."""

from __future__ import annotations

from pathlib import Path
from threading import Event, RLock, Thread, current_thread
from typing import Any, Callable, Iterator, Optional

import flet as ft

from controllers.audio_controller import AudioController, AudioPlayer
from controllers.game_controller import GameController
from models.game_engine import NoteEvent, Song
from models.music_library import MusicLibrary
from models.rhythm_engine import RhythmEngine, RhythmPreparer
from views.desktop_view import DesktopView


class AppController:
    """Coordina selección musical, motor rítmico, audio y eventos Flet."""

    MUSIC_FOLDER: Path = Path(__file__).resolve().parents[1] / "songs"
    HIT_TONE_HZ: int = 880
    HIT_TONE_MS: int = 60
    DEFAULT_VOLUME: float = 0.7

    def __init__(
        self,
        page: Optional[ft.Page] = None,
        audio_player: Optional[AudioPlayer] = None,
        hit_sound: Optional[Callable[[], None]] = None,
        rhythm_engine: Optional[RhythmPreparer] = None,
        music_library: Optional[MusicLibrary] = None,
    ) -> None:
        self.page: Optional[ft.Page] = page
        self.audio_player: AudioPlayer = audio_player or AudioController()
        self._hit_sound: Callable[[], None] = hit_sound or self._beep_on_hit
        self.game: GameController = GameController(
            audio_player=self.audio_player
        )
        self.rhythm_engine: RhythmPreparer = rhythm_engine or RhythmEngine()
        self.music_library: MusicLibrary = (
            music_library or MusicLibrary(self.MUSIC_FOLDER)
        )
        self.music_library.refresh()
        self.selected_song: Optional[Song] = self.music_library.first_song()
        self._stop_event: Event = Event()
        self._loop_thread: Optional[Thread] = None
        self._view_lock: RLock = RLock()
        self._preparation_lock: RLock = RLock()
        self._preparing_song: bool = False
        self.desktop_view: DesktopView = DesktopView(
            on_start=self.on_start_button_click,
            on_add_player=self.on_add_button_click,
            on_remove_player=self.on_remove_button_click,
            on_lane_press=self.on_lane_press,
            on_song_change=self.on_song_selected,
            on_refresh_library=self.on_refresh_library,
            on_export_library=self.on_export_library,
            on_volume_change=self.on_volume_change,
        )
        self.desktop_view.set_song_options(
            self._song_options(),
            self._selected_song_key(),
        )
        self.audio_player.set_volume(self.DEFAULT_VOLUME)
        self.desktop_view.set_volume(self.DEFAULT_VOLUME)
        self.update_labels(
            "Agrega música en songs/ o selecciona una pista.",
            update_page=False,
        )

    def _song_options(self) -> Iterator[tuple[str, str]]:
        """Adapta el TDA de canciones a las opciones visuales del selector."""
        for song in self.music_library.iter_songs():
            if song.audio_path is not None:
                yield (
                    str(song.audio_path.resolve()),
                    f"{song.title}\n{song.artist}",
                )

    def _selected_song_key(self) -> Optional[str]:
        """Devuelve la clave de selector asociada a la canción elegida."""
        if self.selected_song is None or self.selected_song.audio_path is None:
            return None
        return str(self.selected_song.audio_path.resolve())

    def build(self) -> ft.Container:
        """Devuelve el control raíz que Flet agrega a la página."""
        return self.desktop_view.build()

    def on_song_selected(self, audio_path: str) -> None:
        """Selecciona una pista del catálogo para reproducir o analizar."""
        if self.game.running:
            self.desktop_view.set_song_options(
                self._song_options(),
                self._selected_song_key(),
            )
            self.update_labels("Espera a que termine la pista actual.")
            return

        song = self.music_library.find_by_path(audio_path)
        if song is None:
            self.update_labels("No encontré esa canción en songs/.")
            return
        self.selected_song = song
        self.update_labels(f"Seleccionada: {song.title}\n{song.artist}")

    def on_refresh_library(self, event: Any = None) -> None:
        """Busca archivos de audio nuevos en la carpeta songs/."""
        del event
        selected_key = self._selected_song_key()
        count = self.music_library.refresh()
        self.selected_song = (
            self.music_library.find_by_path(selected_key)
            if selected_key is not None
            else None
        )
        if self.selected_song is None:
            self.selected_song = self.music_library.first_song()
        self.desktop_view.set_song_options(
            self._song_options(),
            self._selected_song_key(),
        )
        self.update_labels(f"Biblioteca actualizada: {count} pistas.")

    def on_export_library(self, event: Any = None) -> None:
        """Exporta biblioteca y charts BPM a songs/rhythm_catalog.json."""
        del event
        export_path = self.music_library.export_json()
        self.update_labels(f"Catálogo exportado: {export_path.name}")

    def on_volume_change(self, volume: float) -> None:
        """Aplica y muestra el volumen normalizado de pygame.mixer."""
        normalized_volume = min(1.0, max(0.0, float(volume)))
        self.audio_player.set_volume(normalized_volume)
        self.desktop_view.set_volume(normalized_volume)
        if hasattr(self, "page") and self.page is not None:
            self.page.update()

    def on_start_button_click(self, event: Any = None) -> None:
        """Analiza los beats si hace falta y reproduce la canción elegida."""
        del event
        if self.game.current_player is None:
            self.game.add_player()
        if self.selected_song is None:
            self.update_labels("Agrega un MP3 a songs/ y actualiza.")
            return
        if self.game.running:
            self.update_labels("La pista ya está en reproducción.")
            return

        song = self.selected_song
        if song.notes.is_empty():
            with self._preparation_lock:
                if self._preparing_song:
                    return
                self._preparing_song = True
            self.desktop_view.set_preparing(True)
            self.update_labels(f"Analizando ritmo: {song.title}...")
            if self.page is None:
                self._prepare_and_start(song)
            else:
                self.page.run_thread(self._prepare_and_start, song)
            return

        self._queue_and_start(song)

    def _prepare_and_start(self, song: Song) -> None:
        """Detecta beats fuera del hilo gráfico y comienza la pista."""
        try:
            bpm = self.rhythm_engine.prepare_song(song)
            self._queue_and_start(song, f"Ritmo detectado: {bpm:.1f} BPM")
        except Exception as error:
            self.update_labels(f"No pude analizar el ritmo: {error}")
        finally:
            with self._preparation_lock:
                self._preparing_song = False
            self.desktop_view.set_preparing(False)
            self.update_labels(self.desktop_view.status_label.value)

    def _queue_and_start(self, song: Song, message: str = "") -> None:
        """Conecta el chart listo con la cola FIFO y reproduce el audio."""
        if not self.game.has_playable_song:
            self.game.enqueue_song(song)
        status = self.game.start_game_loop()
        if song.bpm is not None:
            status = f"{status} | {song.bpm:.1f} BPM"
        if not self.game.audio_started:
            audio_error = getattr(self.audio_player, "last_error", None)
            status = f"{status} | Audio: {audio_error or 'no disponible'}"
        if message:
            status = f"{message} | {status}"
        self.update_labels(status)
        if self.game.running:
            self._start_update_loop()

    def on_add_button_click(self, event: Any = None) -> None:
        """Agrega y selecciona un jugador."""
        del event
        player = self.game.add_player()
        self.update_labels(f"Jugador agregado: {player.name}.")

    def on_remove_button_click(self, event: Any = None) -> None:
        """Elimina el jugador activo sin dejar referencias inválidas."""
        del event
        player = self.game.current_player
        if player is None:
            message = "No hay jugadores para eliminar."
        else:
            self.game.remove_player(player.name)
            message = "Jugador eliminado."
        self.update_labels(message)

    def on_keyboard_event(self, event: Any) -> None:
        """Captura teclas personalizadas y las mapea a los carriles del juego."""
        if getattr(event, "repeat", False):
            return
        key = str(getattr(event, "key", "")).strip().upper()
        
        # Limpieza para que Flet reconozca bien algunas teclas especiales o letras
        if key.startswith("KEY"):
            key = key.replace("KEY", "")

        #  DICCIONARIO DE MAPEO DE CONTROLES
        # Aquí puedes cambiar la letra de la IZQUIERDA por la tecla que prefieras en tu teclado físico,
        # manteniéndolo vinculado al carril correspondiente de la DERECHA ("A", "S", "D", "F").
        key_mapping = {
            "A": "A",  # Carril 1 (Izquierda)
            "D": "S",  # Carril 2
            "J": "D",  # Carril 3
            "L": "F",  # Carril 4 (Derecha)
            
        }

        if key in key_mapping:
            lane = key_mapping[key]
            self.on_lane_press(lane)

    def _play_hit_effect(self) -> None:
        """Emite el beep en segundo plano para no bloquear el game loop."""
        if self.page is not None:
            self.page.run_thread(self._hit_sound)
        else:
            self._hit_sound()

    def _beep_on_hit(self) -> None:
        """Reproduce un tono breve de acierto con winsound en Windows."""
        try:
            import winsound

            winsound.Beep(self.HIT_TONE_HZ, self.HIT_TONE_MS)
        except Exception:
            return

    def on_lane_press(self, lane: str) -> None:
        """Envía la pulsación al juego y refresca el marcador."""
        accepted = self.game.press_lane(lane)
        if accepted:
            self._play_hit_effect()
            message = "¡Nota acertada!"
        elif self.game.current_note is None:
            message = "No hay una nota pendiente en la pista."
        elif not self.game.running:
            message = "Inicia una canción antes de tocar."
        else:
            message = "Carril incorrecto o fuera de la zona de impacto."
        self.update_labels(message)

    def update_labels(
        self,
        message: str = "",
        update_page: bool = True,
    ) -> None:
        """Sincroniza título, beat actual, racha y posiciones de la vista."""
        with self._view_lock:
            active_song = self.game.engine.current_song
            song = (
                active_song
                if self.game.running and active_song is not None
                else self.selected_song
            )
            player = self.game.current_player
            event = song.current_note if song is not None else None
            if song is None:
                title = "No hay canciones disponibles"
                note_text = "Current Note: --"
            elif song.notes.is_empty():
                title = f"{song.title}\n{song.artist}"
                if self._preparing_song:
                    note_text = "Analizando BPM..."
                else:
                    note_text = "Pulsa Start Game para analizar el ritmo."
            else:
                title = f"{song.title}\n{song.artist}"
                note_lane = event.lane if event is not None else "Fin de pista"
                note_text = f"Current Note: {note_lane}"
                if song.bpm is not None:
                    note_text = f"{note_text} | {song.bpm:.1f} BPM"

            player_name = player.name if player is not None else "Sin jugador"
            self.desktop_view.render(
                title=title,
                note=note_text,
                player=player_name,
                score=self.game.get_score_summary(),
                message=message,
                song=song,
                playback_time=self.game.playback_time,
            )
            page = self.page

        if update_page and page is not None:
            page.update()

    def _start_update_loop(self) -> None:
        """Inicia un único hilo de actualización de la pista visual."""
        if self.page is None:
            return
        if self._loop_thread is not None and self._loop_thread.is_alive():
            return
        self._stop_event.clear()
        self._loop_thread = Thread(
            target=self._run_update_loop,
            name="guitar-hero-game-loop",
            daemon=True,
        )
        self._loop_thread.start()

    def _run_update_loop(self) -> None:
        """Mueve la pista y evalúa notas a fluidos 60 fotogramas por segundo."""
        try:
            # 🚀 OPTIMIZADO A 60 FPS (1.0 / 60.0) en lugar de 30 FPS para eliminar tirones
            while not self._stop_event.wait(1.0 / 60.0):
                self.game.update_playback()
                if not self.game.running:
                    self.update_labels("Canción terminada.")
                    break
                self.update_labels(self.desktop_view.status_label.value)
        finally:
            self._loop_thread = None

    def stop(self, event: Any = None) -> None:
        """Detiene el hilo y el audio al cerrar la ventana."""
        del event
        self._stop_event.set()
        self.game.stop()
        thread = self._loop_thread
        if thread is not None and thread is not current_thread():
            thread.join(timeout=1.0)