"""Adaptador de audio pygame para reproducción MP3 y reloj de pista."""

from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any, Optional, Protocol


class AudioPlayer(Protocol):
    """Contrato mínimo que usa el controlador del juego."""

    def play(self, audio_path: Optional[Path]) -> bool:
        """Inicia la pista y devuelve si el audio real comenzó."""
        ...

    def get_position_seconds(self) -> float:
        """Devuelve el tiempo actual de reproducción en segundos."""
        ...

    def get_duration_seconds(self, audio_path: Optional[Path]) -> float:
        """Devuelve la duración de la pista en segundos."""
        ...

    def set_volume(self, volume: float) -> float:
        """Ajusta el volumen de salida entre silencio y nivel máximo."""
        ...

    def stop(self) -> None:
        """Detiene la pista activa."""
        ...


class AudioController:
    """Reproduce MP3 con pygame.mixer y usa reloj monotónico como respaldo."""

    FALLBACK_DURATION_SECONDS: float = 120.0

    def __init__(self) -> None:
        self._pygame: Any = None
        self._using_mixer: bool = False
        self._started_at: float = monotonic()
        self._track_duration: float = self.FALLBACK_DURATION_SECONDS
        self._volume: float = 0.7
        self.last_error: Optional[str] = None

        try:
            import pygame

            self._pygame = pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception as error:
            self.last_error = f"No se pudo inicializar pygame.mixer: {error}"
            self._pygame = None

    @property
    def is_available(self) -> bool:
        """Indica si pygame.mixer quedó inicializado correctamente."""
        return self._pygame is not None

    def get_duration_seconds(self, audio_path: Optional[Path]) -> float:
        """Lee la duración del MP3 o usa un valor de respaldo."""
        if audio_path is None or self._pygame is None:
            return self.FALLBACK_DURATION_SECONDS

        try:
            sound = self._pygame.mixer.Sound(str(audio_path))
            self._track_duration = float(sound.get_length())
            del sound
            return self._track_duration
        except Exception as error:
            self.last_error = f"No se pudo leer la duración del audio: {error}"
            return self.FALLBACK_DURATION_SECONDS

    def play(self, audio_path: Optional[Path]) -> bool:
        """Carga y reproduce el archivo sin bloquear la interfaz gráfica."""
        self._started_at = monotonic()
        self._using_mixer = False
        if audio_path is None or not audio_path.is_file():
            self.last_error = "No se encontró el archivo de audio."
            return False
        if self._pygame is None:
            return False

        try:
            self._pygame.mixer.music.load(str(audio_path))
            self._pygame.mixer.music.set_volume(self._volume)
            self._pygame.mixer.music.play()
            self._using_mixer = True
            self.last_error = None
            return True
        except Exception as error:
            self.last_error = f"No se pudo reproducir el MP3: {error}"
            return False

    def get_position_seconds(self) -> float:
        """Lee la posición del mezclador o el reloj monotónico de respaldo."""
        if self._using_mixer and self._pygame is not None:
            position_ms = self._pygame.mixer.music.get_pos()
            if position_ms >= 0:
                return position_ms / 1000.0
            if not self._pygame.mixer.music.get_busy():
                return self._track_duration

        elapsed = monotonic() - self._started_at
        return min(elapsed, self._track_duration)

    def set_volume(self, volume: float) -> float:
        """Ajusta el mezclador al rango válido de pygame, de 0.0 a 1.0."""
        self._volume = min(1.0, max(0.0, float(volume)))
        if self._pygame is not None and self._pygame.mixer.get_init():
            self._pygame.mixer.music.set_volume(self._volume)
        return self._volume

    def stop(self) -> None:
        """Detiene la reproducción actual si pygame está disponible."""
        if self._using_mixer and self._pygame is not None:
            try:
                self._pygame.mixer.music.stop()
            except Exception as error:
                self.last_error = f"No se pudo detener el audio: {error}"
        self._using_mixer = False
