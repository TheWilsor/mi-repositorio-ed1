"""Lista doblemente enlazada usada para pistas y colecciones ordenadas."""

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from models.structures import DoublyLinkedList as _DoublyLinkedList

T = TypeVar("T")


class DoublyLinkedList(_DoublyLinkedList[T], Generic[T]):
    """Extiende el TDA central con nombres históricos del módulo de pistas."""

    def add_song(self, song: T) -> None:
        """Agrega una canción o dato al final de la lista."""
        self.append(song)

    def traverse(self) -> Iterator[T]:
        """Recorre los datos de principio a fin sin crear una lista nativa."""
        return iter(self)
