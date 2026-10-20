# models/track_list.py - GuitarHeroMVC
from __future__ import annotations
from typing import Any, Optional, Generator
from models.song_node import NoteNode

class DoublyLinkedList:
    """Estructura de datos manual TDA Doblemente Enlazada (O(1) en inserción al final)."""
    def __init__(self) -> None:
        self.head: Optional[NoteNode] = None
        self.tail: Optional[NoteNode] = None
        self._size: int = 0

    def append(self, data: Any) -> None:
        """Inserta un nuevo nodo al final de la lista."""
        new_node = NoteNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            if self.tail:
                self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def add_song(self, song: Any) -> None:
        self.append(song)

    def remove(self, data: Any) -> bool:
        """Elimina la primera ocurrencia del elemento indicado."""
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def traverse(self) -> Generator[Any, None, None]:
        """Generador para recorrer los elementos de inicio a fin."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return self._size