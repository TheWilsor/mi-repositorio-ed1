"""Pruebas de integración del flujo principal de Guitar Hero MVC."""

import unittest
from pathlib import Path
from typing import Optional

from controllers.game_controller import GameController
from models.game_engine import NoteEvent


class FakeAudioPlayer:
    """Reloj de prueba fijo para las pruebas del controlador."""

    def __init__(self) -> None:
        self.position: float = 0.0

    def play(self, audio_path: Optional[Path]) -> bool:
        del audio_path
        return True

    def get_position_seconds(self) -> float:
        return self.position

    def get_duration_seconds(self, audio_path: Optional[Path]) -> float:
        del audio_path
        return 60.0

    def set_volume(self, volume: float) -> float:
        del volume
        return 0.7

    def stop(self) -> None:
        return None


class GameFlowTests(unittest.TestCase):
    """Comprueba que los controles del juego coordinan modelo y puntuación."""

    def test_player_can_start_song_and_score_matching_notes(self) -> None:
        """Un jugador inicia la cola y suma puntos con notas correctas."""
        controller = GameController(audio_player=FakeAudioPlayer())
        player = controller.add_player("Ada")
        controller.add_song_to_queue(
            "Solo clásico",
            "Nick Panek",
            (
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("A", 0.0),
                NoteEvent("S", 0.0),
            ),
        )

        status = controller.start_game_loop()

        self.assertIn("Solo clásico", status)
        self.assertTrue(controller.running)
        self.assertEqual(controller.current_note.lane, "A")

        for _ in range(10):
            self.assertTrue(controller.process_note("A"))

        self.assertEqual(player.score, 1100)
        self.assertEqual(player.streak, 10)
        self.assertEqual(player.multiplier, 2)
        self.assertEqual(controller.current_note.lane, "S")

    def test_wrong_note_resets_multiplier_and_keeps_target(self) -> None:
        """Una nota errada conserva la nota objetivo y reinicia la racha."""
        controller = GameController(audio_player=FakeAudioPlayer())
        player = controller.add_player("Rocker")
        controller.add_song_to_queue(
            "Prueba",
            "Artista",
            (NoteEvent("A", 0.0), NoteEvent("S", 0.0)),
        )
        controller.start_game_loop()
        controller.press_lane("A")
        player.streak = 10
        player.multiplier = 2

        result = controller.press_lane("D")

        self.assertFalse(result)
        self.assertEqual(controller.current_note.lane, "S")
        self.assertEqual(player.streak, 0)
        self.assertEqual(player.multiplier, 1)


if __name__ == "__main__":
    unittest.main()
