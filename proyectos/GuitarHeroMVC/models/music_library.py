"""Catálogo de música respaldado por estructuras enlazadas manuales."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Optional, TextIO

from models.game_engine import Song
from models.structures import DoublyLinkedList


class MusicLibrary:
    """Descubre pistas locales y exporta sus metadatos y charts rítmicos."""

    AUDIO_EXTENSIONS: tuple[str, ...] = (".mp3", ".wav", ".ogg", ".flac")

    def __init__(self, music_folder: Path) -> None:
        self.music_folder: Path = Path(music_folder)
        self.songs: DoublyLinkedList[Song] = DoublyLinkedList()

    def refresh(self) -> int:
        """Actualiza el catálogo con pistas de la carpeta songs."""
        self.music_folder.mkdir(parents=True, exist_ok=True)
        previous_songs = self.songs
        refreshed_songs: DoublyLinkedList[Song] = DoublyLinkedList()

        for audio_path in self.music_folder.rglob("*"):
            if not audio_path.is_file():
                continue
            if audio_path.suffix.lower() not in self.AUDIO_EXTENSIONS:
                continue

            song = self._find_in(previous_songs, audio_path)
            if song is None:
                title, artist = self._metadata_from_path(audio_path)
                song = Song(title, artist, (), audio_path)
            refreshed_songs.append(song)

        self.songs = refreshed_songs
        return len(self.songs)

    def _metadata_from_path(self, audio_path: Path) -> tuple[str, str]:
        """Lee título/artista del nombre cuando no hay etiquetas ID3."""
        stem = audio_path.stem
        if "nickpanek" in stem.lower():
            return "Classic Rock Solo", "Nick Panek"
        if " - " in stem:
            title, artist = stem.split(" - ", 1)
            return title.strip(), artist.strip()
        title = stem.replace("_", " ").replace("-", " ").strip().title()
        return title, "Artista desconocido"

    def _find_in(
        self,
        songs: DoublyLinkedList[Song],
        audio_path: Path,
    ) -> Optional[Song]:
        """Busca una pista anterior para conservar su chart entre recargas."""
        target_path = audio_path.resolve()
        for song in songs:
            if song.audio_path is not None:
                if song.audio_path.resolve() == target_path:
                    return song
        return None

    def iter_songs(self) -> Iterator[Song]:
        """Recorre la biblioteca en orden de descubrimiento."""
        return iter(self.songs)

    def first_song(self) -> Optional[Song]:
        """Devuelve la primera pista disponible, si existe."""
        if self.songs.head is None:
            return None
        return self.songs.head.data

    def find_by_path(self, audio_path: str | Path) -> Optional[Song]:
        """Busca una pista por ruta sin usar diccionarios de almacenamiento."""
        return self._find_in(self.songs, Path(audio_path))

    def export_json(self, export_path: Optional[Path] = None) -> Path:
        """Exporta catálogo y chart completo como JSON en streaming."""
        destination = export_path or self.music_folder / "rhythm_catalog.json"
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        with destination.open("w", encoding="utf-8") as output_file:
            output_file.write('{"songs":[')
            first_song = True
            for song in self.songs:
                if not first_song:
                    output_file.write(",")
                first_song = False
                self._write_song(output_file, song)
            output_file.write("]}")
        return destination

    def _write_song(self, output_file: TextIO, song: Song) -> None:
        """Escribe una canción y sus beats sin materializar otra lista."""
        output_file.write("{\"title\":")
        json.dump(song.title, output_file, ensure_ascii=False)
        output_file.write(",\"artist\":")
        json.dump(song.artist, output_file, ensure_ascii=False)
        output_file.write(",\"audio_path\":")
        json.dump(
            song.audio_path.as_posix() if song.audio_path is not None else "",
            output_file,
            ensure_ascii=False,
        )
        output_file.write(',"bpm":')
        json.dump(song.bpm, output_file)
        output_file.write(',"chart":[')

        first_note = True
        for note in song.iter_notes():
            if not first_note:
                output_file.write(",")
            first_note = False
            json.dump(
                {"lane": note.lane, "time_seconds": note.time_seconds},
                output_file,
                ensure_ascii=False,
            )
        output_file.write("]}")

    @property
    def song_count(self) -> int:
        return len(self.songs)
