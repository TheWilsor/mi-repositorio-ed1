"""Pruebas del analizador rítmico, catálogo y control de volumen."""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Optional

from controllers.app_controller import AppController
from models.game_engine import Song
from models.music_library import MusicLibrary
from models.rhythm_engine import BeatAnalysis, RhythmEngine


class FakeBeatDetector:
    """Entrega una cuadrícula temporal fija para probar el motor rítmico."""

    def analyze(self, audio_path: Path) -> BeatAnalysis:
        del audio_path
        return BeatAnalysis(120.0, (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5))


class FakeAudioPlayer:
    """Reproductor mínimo que registra el volumen aplicado por la vista."""

    def __init__(self) -> None:
        self.volume: float = 0.7

    def play(self, audio_path: Optional[Path]) -> bool:
        del audio_path
        return True

    def get_position_seconds(self) -> float:
        return 0.0

    def get_duration_seconds(self, audio_path: Optional[Path]) -> float:
        del audio_path
        return 10.0

    def set_volume(self, volume: float) -> float:
        self.volume = volume
        return volume

    def stop(self) -> None:
        return None


class RhythmEngineTests(unittest.TestCase):
    """Comprueba que los eventos queden sobre la cuadrícula de beats."""

    def test_chart_uses_detected_beats_after_count_in(self) -> None:
        song = Song("Prueba", "Artista", (), Path("track.mp3"))
        rhythm_engine = RhythmEngine(
            beat_detector=FakeBeatDetector(),
            count_in_seconds=2.0,
        )

        bpm = rhythm_engine.prepare_song(song)

        chart = tuple(
            (event.lane, event.time_seconds)
            for event in song.iter_notes()
        )
        self.assertEqual(bpm, 120.0)
        self.assertEqual(
            chart,
            (("A", 2.0), ("S", 2.5), ("D", 3.0), ("F", 3.5)),
        )

    def test_music_library_exports_metadata_and_rhythm_chart(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            music_folder = Path(temp_dir) / "songs"
            music_folder.mkdir()
            track_path = music_folder / "Solo - Banda.mp3"
            track_path.write_bytes(b"placeholder")
            library = MusicLibrary(music_folder)
            library.refresh()
            song = library.first_song()
            self.assertIsNotNone(song)
            RhythmEngine(
                beat_detector=FakeBeatDetector(),
                count_in_seconds=2.0,
            ).prepare_song(song)

            export_path = library.export_json(
                Path(temp_dir) / "exports" / "music_catalog.json"
            )
            exported = json.loads(export_path.read_text(encoding="utf-8"))

            self.assertEqual(exported["songs"][0]["title"], "Solo")
            self.assertEqual(exported["songs"][0]["artist"], "Banda")
            self.assertEqual(exported["songs"][0]["bpm"], 120.0)
            self.assertEqual(len(exported["songs"][0]["chart"]), 4)


class VolumeControlTests(unittest.TestCase):
    """Comprueba que el slider ajuste y limite el volumen del reproductor."""

    def test_volume_callback_clamps_and_updates_audio_and_view(self) -> None:
        audio = FakeAudioPlayer()
        app = AppController(audio_player=audio, hit_sound=lambda: None)

        app.on_volume_change(1.5)

        self.assertEqual(audio.volume, 1.0)
        self.assertEqual(app.desktop_view.volume_slider.value, 1.0)
        self.assertEqual(app.desktop_view.volume_label.value, "100%")


if __name__ == "__main__":
    unittest.main()
