"""Detección de beats y construcción de chart rítmico enlazado."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, Optional, Protocol

from models.game_engine import NoteEvent, Song
from models.structures import DoublyLinkedList


class BeatAnalysis:
    """Resultado compacto del análisis temporal de un archivo musical."""

    def __init__(
        self,
        bpm: float,
        beat_times: Iterable[float],
        duration_seconds: float = 0.0,
    ) -> None:
        if bpm <= 0:
            raise ValueError("El tempo debe ser mayor que cero.")
        self.bpm: float = float(bpm)
        self.duration_seconds: float = float(duration_seconds)
        self.beat_times: DoublyLinkedList[float] = DoublyLinkedList()
        previous_time = -1.0
        for beat_time in beat_times:
            normalized_time = float(beat_time)
            if normalized_time < previous_time:
                raise ValueError("Los beats deben estar ordenados por tiempo.")
            if normalized_time >= 0:
                self.beat_times.append(normalized_time)
                previous_time = normalized_time

    def iter_beats(self) -> Iterator[float]:
        """Recorre beats sin convertir la estructura a una lista nativa."""
        return iter(self.beat_times)

    def __len__(self) -> int:
        return len(self.beat_times)


class BeatDetector(Protocol):
    """Interfaz intercambiable para analizadores reales y pruebas."""

    def analyze(self, audio_path: Path) -> BeatAnalysis:
        """Devuelve BPM, instantes de beat y duración del audio."""
        ...


class RhythmPreparer(Protocol):
    """Interfaz del servicio que prepara el chart de una canción."""

    def prepare_song(self, song: Song) -> float:
        """Analiza el audio, carga el chart y devuelve el BPM detectado."""
        ...

class HardstyleOnsetDetector:
    """Detector optimizado para separar percusión (claps/kicks) y drops en Hardstyle."""

    def __init__(self, sample_rate: int = 22050) -> None:
        self.sample_rate: int = sample_rate

    def analyze(self, audio_path: Path) -> BeatAnalysis:
        if not audio_path.is_file():
            raise FileNotFoundError(f"No se encontró la pista: {audio_path}")

        import librosa
        samples, sample_rate = librosa.load(str(audio_path), sr=self.sample_rate, mono=True)
        
        # 1. Obtener el BPM general de la pista
        tempo, _ = librosa.beat.beat_track(y=samples, sr=sample_rate)
        bpm = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)
        if bpm <= 0:
            bpm = 150.0  # El hardstyle suele ser rápido

        # 2. SEPARACIÓN ARMÓNICO-PERCUSIVA (Magia negra para la electrónica)
        # Esto aísla los claps y la batería de la voz y los pads melódicos.
        _, y_percussive = librosa.effects.hpss(samples)

        # 3. Detectar onsets exclusivamente sobre la pista percusiva limpia
        # Usamos un delta más estricto para capturar la velocidad de los claps consecutivos
        onset_frames = librosa.onset.onset_detect(
            y=y_percussive, 
            sr=sample_rate, 
            backtrack=True,
            delta=0.05,  
            wait=3       # Permite capturar ráfagas rápidas de notas típicas del hardstyle
        )
        onset_times = librosa.frames_to_time(onset_frames, sr=sample_rate)
        
        duration = float(librosa.get_duration(y=samples, sr=sample_rate))
        
        return BeatAnalysis(
            bpm,
            (float(t) for t in onset_times),
            duration,
        )



class RhythmEngine:
    """Convierte beats detectados en notas sincronizadas con el audio."""

    LANES: tuple[str, ...] = ("A", "S", "D", "F")
    DEFAULT_BPM: float = 120.0

    def __init__(
        self,
        beat_detector: Optional[BeatDetector] = None,
        count_in_seconds: float = 2.0,
    ) -> None:
        if count_in_seconds < 0:
            raise ValueError("La cuenta inicial no puede ser negativa.")
        self.beat_detector: BeatDetector = (
            beat_detector or HardstyleOnsetDetector()
        )
        self.count_in_seconds: float = count_in_seconds

    def prepare_song(self, song: Song) -> float:
        """Analiza y carga el chart en la pista enlazada de la canción."""
        if song.audio_path is None:
            raise ValueError("La canción no tiene una ruta de audio asociada.")

        analysis = self.beat_detector.analyze(song.audio_path)
        notes = self._notes_from_beats(analysis.iter_beats())
        song.set_rhythm_chart(notes, analysis.bpm)

        if song.notes.is_empty() and analysis.duration_seconds > 0:
            fallback_notes = self._fallback_chart(
                analysis.duration_seconds,
                analysis.bpm,
            )
            song.set_rhythm_chart(fallback_notes, analysis.bpm)
        if song.notes.is_empty():
            raise ValueError("No se detectaron beats para la pista.")
        return analysis.bpm

    def _notes_from_beats(
        self,
        beat_times: Iterable[float],
    ) -> Iterator[NoteEvent]:
        """Genera charts estilo Expert con streams escalonados y acordes dinámicos."""
        times = list(beat_times)
        if not times:
            return

        lane_index = 0
        for i, t in enumerate(times):
            if t < self.count_in_seconds:
                continue

            # Calcular el delta temporal con la nota anterior para medir velocidad
            delta = t - times[i - 1] if i > 0 else 1.0

            # 1. Patrón de Stream Rápido (Notas muy juntas)
            if delta < 0.22:
                lane_index = (lane_index + 1) % len(self.LANES)
                yield NoteEvent(self.LANES[lane_index], t)
                
                # Ocasionalmente, si el delta es ultra corto, añadimos un acorde secundario
                if delta < 0.12 and i % 3 == 0:
                    secondary_lane = (lane_index + 2) % len(self.LANES)
                    yield NoteEvent(self.LANES[secondary_lane], t, duration=0.0)
            
            # 2. Patrón de Notas Sostenidas para sonidos largos o melodías de sintetizador
            elif delta > 0.8:
                # Nota larga (Hold) con duración proporcional al espacio libre
                duration = min(1.5, delta * 0.5)
                lane_index = (i * 7) % len(self.LANES) # Distribución pseudoaleatoria armónica
                yield NoteEvent(self.LANES[lane_index], t, duration=duration)
            
            # 3. Ritmo Normal / Estándar
            else:
                lane_index = (lane_index + 2) % len(self.LANES)
                yield NoteEvent(self.LANES[lane_index], t)

    def _fallback_chart(
        self,
        duration_seconds: float,
        bpm: float,
    ) -> Iterator[NoteEvent]:
        """Genera pulsos regulares si el detector no devuelve beats."""
        interval = 60.0 / bpm if bpm > 0 else 60.0 / self.DEFAULT_BPM
        event_time = self.count_in_seconds
        lane_index = 0
        while event_time < duration_seconds:
            lane = self.LANES[lane_index % len(self.LANES)]
            yield NoteEvent(lane, event_time)
            lane_index += 1
            event_time += interval
