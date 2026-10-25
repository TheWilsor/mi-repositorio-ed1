"""Pruebas RED-GREEN para controles arcade A-S-D-F y efecto de impacto."""

import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from controllers.app_controller import AppController
from controllers.game_controller import GameController
from models.game_engine import NoteEvent, Song


class FakeAudioPlayer:
    """Reloj de pista controlado para las pruebas de teclas."""

    def __init__(self) -> None:
        self.position: float = 0.0
        self.duration: float = 8.0
        self.volume: float = 0.7

    def play(self, audio_path: Optional[Path]) -> bool:
        del audio_path
        self.position = 0.0
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
        return None


class FakeRhythmEngine:
    """Crea un chart pequeño para pruebas del controlador de vista."""

    def prepare_song(self, song: Song) -> float:
        song.set_rhythm_chart(
            (NoteEvent("A", 2.0), NoteEvent("S", 2.6)),
            100.0,
        )
        return 100.0


class ArcadeControlTests(unittest.TestCase):
    """Valida carriles, mapeo de teclas y sonido solo en aciertos."""

    def test_note_events_accept_only_asdf_lanes(self) -> None:
        for lane in ("A", "S", "D", "F"):
            self.assertEqual(NoteEvent(lane, 0.0).lane, lane)

        with self.assertRaises(ValueError):
            NoteEvent("B", 0.0)

    def test_second_keyboard_lane_maps_to_s(self) -> None:
        audio = FakeAudioPlayer()
        controller = GameController(audio_player=audio)
        controller.add_player("Arcade")
        controller.add_song_to_queue(
            "Teclas",
            "Banda",
            (NoteEvent("S", 1.0),),
        )
        controller.start_game_loop()
        audio.position = 1.0

        self.assertTrue(controller.process_key_press(1))
        self.assertEqual(controller.current_player.score, 100)

    def test_hit_effect_runs_for_hits_but_not_wrong_lanes(self) -> None:
        audio = FakeAudioPlayer()
        effects: list[str] = []
        app = AppController(
            audio_player=audio,
            hit_sound=lambda: effects.append("hit"),
            rhythm_engine=FakeRhythmEngine(),
        )
        labels = tuple(
            button.content.value
            for button in app.desktop_view.lane_buttons
        )
        self.assertEqual(labels, ("A", "S", "D", "F"))

        app.on_add_button_click()
        app.on_start_button_click()
        audio.position = 2.0
        app.on_keyboard_event(SimpleNamespace(key="A"))
        self.assertEqual(effects, ["hit"])

        audio.position = 2.6
        app.on_keyboard_event(SimpleNamespace(key="A"))
        self.assertEqual(effects, ["hit"])


if __name__ == "__main__":
    unittest.main()
