# models/song_node.py
from __future__ import annotations
from typing import Any, Optional

class NoteNode:
    """Nodo individual para la lista doblemente enlazada."""
    def __init__(self, data: Any, next_node: Optional[NoteNode] = None, prev_node: Optional[NoteNode] = None) -> None:
        self.data: Any = data
        self.next: Optional[NoteNode] = next_node
        self.prev: Optional[NoteNode] = prev_node