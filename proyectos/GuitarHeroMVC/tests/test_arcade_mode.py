"""Pruebas de sincronización y entrada de teclado del modo arcade."""

import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

from controllers.app_controller import AppController
from controllers.game_controller import GameController
from models.game_engine import NoteEvent, Song


class FakeAudioPlayer:
    """Reloj determinista que implementa el contrato del reproductor."""

    def __init__(self) -> None:
        self.position: float = 0.0
        self.duration: float = 8.0
        self.audio_path: Optional[Path] = None
        self.playing: bool = False
        self.volume: float = 0.7

    def play(self, audio_path: Optional[Path]) -> bool:
        self.audio_path = audio_path
        self.position = 0.0
        self.playing = True
        return True

    def get_position_seconds(self) -> float:
        return self.position

    def get_duration_seconds(self, audio_path: Optional[Path]) -> float:
        del audio_path
        return self.duration

    def set_volume(self, volume: float) -> float:
        self.volume = volume
        return volume

    def stop(self) -> None:
        self.playing = False


class FakeRhythmEngine:
    """Genera dos beats deterministas para probar el flujo de la vista."""

    def prepare_song(self, song: Song) -> float:
        song.set_rhythm_chart(
            (NoteEvent("A", 2.0), NoteEvent("S", 2.6)),
            100.0,
        )
        return 100.0


class ArcadeTimingTests(unittest.TestCase):
    """Comprueba aciertos, fallos y rachas con un reloj de reproducción."""

    def make_controller(self) -> tuple[GameController, FakeAudioPlayer]:
        audio = FakeAudioPlayer()
        controller = GameController(audio_player=audio)
        controller.add_player("Arcade")
        controller.add_song_to_queue(
            "Prueba",
            "Banda",
            (NoteEvent("A", 1.0), NoteEvent("S", 2.0)),
            audio_path=Path("fake-track.mp3"),
        )
        controller.start_game_loop()
        return controller, audio

    def test_hit_in_window_scores_and_advances_pointer(self) -> None:
        controller, audio = self.make_controller()
        audio.position = 0.8

        result = controller.press_lane("A")

        self.assertTrue(result)
        self.assertEqual(controller.current_player.score, 100)
        self.assertEqual(controller.current_note.lane, "S")
        self.assertEqual(audio.audio_path, Path("fake-track.mp3"))

    def test_wrong_lane_keeps_target_and_breaks_streak(self) -> None:
        controller, audio = self.make_controller()
        audio.position = 0.8
        self.assertTrue(controller.press_lane("A"))
        controller.current_player.streak = 5
        controller.current_player.multiplier = 1
        audio.position = 1.8

        result = controller.press_lane("D")

        self.assertFalse(result)
        self.assertEqual(controller.current_note.lane, "S")
        self.assertEqual(controller.current_player.streak, 0)

    def test_expired_note_is_marked_missed_and_pointer_moves(self) -> None:
        controller, audio = self.make_controller()
        audio.position = 1.3

        controller.update_playback()

        self.assertEqual(controller.current_note.lane, "S")
        self.assertEqual(controller.current_player.streak, 0)

    def test_multiplier_caps_at_four(self) -> None:
        audio = FakeAudioPlayer()
        controller = GameController(audio_player=audio)
        controller.add_player("Racha")
        notes = tuple(NoteEvent("A", 0.0) for _ in range(30))
        controller.add_song_to_queue("Racha", "Banda", notes)
        controller.start_game_loop()

        for _ in range(30):
            self.assertTrue(controller.press_lane("A"))

        self.assertEqual(controller.current_player.streak, 30)
        self.assertEqual(controller.current_player.multiplier, 4)
        self.assertEqual(controller.current_player.score, 6300)


class ArcadeViewTests(unittest.TestCase):
    """Verifica la vista real de Flet y su evento global de teclado."""

    def test_keyboard_event_updates_game_without_text_input(self) -> None:
        audio = FakeAudioPlayer()
        app = AppController(
            audio_player=audio,
            hit_sound=lambda: None,
            rhythm_engine=FakeRhythmEngine(),
        )
        self.assertEqual(len(app.desktop_view.lane_buttons), 4)
        self.assertFalse(hasattr(app.desktop_view, "note_input"))

        app.on_add_button_click()
        app.on_start_button_click()
        audio.position = 2.0

        app.on_keyboard_event(SimpleNamespace(key="A"))

        self.assertIn("Puntaje: 100", app.desktop_view.score_label.value)
        self.assertEqual(
            app.desktop_view.note_label.value,
            "Current Note: S | 100.0 BPM",
        )

    def test_start_button_is_prominent_and_adds_first_player(self) -> None:
        audio = FakeAudioPlayer()
        app = AppController(
            audio_player=audio,
            hit_sound=lambda: None,
            rhythm_engine=FakeRhythmEngine(),
        )
        controls = app.desktop_view.root.content.controls

        self.assertLess(
            controls.index(app.desktop_view.start_button_row),
            controls.index(app.desktop_view.board_stack),
        )

        app.on_start_button_click()

        player = app.game.current_player
        assert player is not None
        self.assertEqual(player.name, "Player 1")
        self.assertTrue(app.game.running)

    def test_notes_appear_when_chart_is_added_to_selected_song(self) -> None:
        audio = FakeAudioPlayer()
        app = AppController(
            audio_player=audio,
            hit_sound=lambda: None,
            rhythm_engine=FakeRhythmEngine(),
        )
        self.assertEqual(len(app.desktop_view._note_markers), 0)

        app.on_start_button_click()

        self.assertEqual(len(app.desktop_view._note_markers), 2)
        first_marker = app.desktop_view._note_markers[0][1]
        self.assertTrue(first_marker.visible)
        initial_y = first_marker.top

        audio.position = 1.0
        app.game.update_playback()
        app.update_labels(update_page=False)

        self.assertGreater(first_marker.top, initial_y)


class DeferredPage:
    """Página falsa que deja el trabajo en segundo plano pendiente."""

    def __init__(self) -> None:
        self.pending_call: Optional[tuple[Any, tuple[Any, ...]]] = None
        self.update_count: int = 0

    def run_thread(self, handler: Any, *args: Any) -> None:
        self.pending_call = (handler, args)

    def update(self) -> None:
        self.update_count += 1


class RhythmLoadingViewTests(unittest.TestCase):
    """Comprueba que el análisis asíncrono avise antes de crear el chart."""

    def test_start_shows_loading_state_until_chart_analysis_finishes(self) -> None:
        page = DeferredPage()
        app = AppController(
            page=page,
            audio_player=FakeAudioPlayer(),
            hit_sound=lambda: None,
            rhythm_engine=FakeRhythmEngine(),
        )
        app.on_add_button_click()

        app.on_start_button_click()

        self.assertEqual(app.desktop_view.note_label.value, "Analizando BPM...")
        self.assertTrue(app.desktop_view.start_button.disabled)
        self.assertIsNotNone(page.pending_call)


if __name__ == "__main__":
    unittest.main()
