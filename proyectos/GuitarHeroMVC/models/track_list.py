# Módulo models/track_list.py - GuitarHeroMVC
# Generado por ABISMO V15 Omni-Orchestrator bajo PEP 8 y Tipado Estático
from typing import Optional, Any

class Node:
    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None
