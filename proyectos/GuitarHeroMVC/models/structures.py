"""Estructuras de datos enlazadas implementadas sin contenedores nativos."""

from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """Nodo con dato y referencias explícitas al siguiente y anterior."""

    def __init__(
        self,
        data: T,
        next: Optional[Node[T]] = None,
        prev: Optional[Node[T]] = None,
    ) -> None:
        self.data: T = data
        self.next: Optional[Node[T]] = next
        self.prev: Optional[Node[T]] = prev


class DoublyLinkedList(Generic[T]):
    """Lista doblemente enlazada con inserción y extracción eficiente."""

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.size: int = 0

    def is_empty(self) -> bool:
        """Indica si la estructura no contiene nodos."""
        return self.head is None

    def append(self, data: T) -> None:
        """Agrega un dato al final en tiempo O(1)."""
        new_node = Node(data, prev=self.tail)
        if self.tail is None:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def prepend(self, data: T) -> None:
        """Agrega un dato al inicio en tiempo O(1)."""
        new_node = Node(data, next=self.head)
        if self.head is None:
            self.tail = new_node
        else:
            self.head.prev = new_node
        self.head = new_node
        self.size += 1

    def pop_front(self) -> Optional[T]:
        """Retira y devuelve el primer dato, o None si está vacía."""
        if self.head is None:
            return None

        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        node.next = None
        node.prev = None
        self.size -= 1
        return node.data

    def remove(self, data: T) -> bool:
        """Elimina la primera coincidencia y comunica si la encontró."""
        current = self.head
        while current is not None:
            if current.data == data:
                if current.prev is None:
                    self.head = current.next
                else:
                    current.prev.next = current.next

                if current.next is None:
                    self.tail = current.prev
                else:
                    current.next.prev = current.prev

                current.next = None
                current.prev = None
                self.size -= 1
                return True
            current = current.next
        return False

    def delete(self, data: T) -> bool:
        """Alias compatible para eliminar la primera coincidencia."""
        return self.remove(data)

    def search(self, data: T) -> bool:
        """Busca un dato recorriendo los nodos enlazados."""
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def get_size(self) -> int:
        """Devuelve el número de nodos almacenados."""
        return self.size

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[T]:
        current = self.head
        while current is not None:
            yield current.data
            current = current.next


class Queue(Generic[T]):
    """Cola FIFO respaldada exclusivamente por una lista enlazada manual."""

    def __init__(self) -> None:
        self.items: DoublyLinkedList[T] = DoublyLinkedList()

    def is_empty(self) -> bool:
        return self.items.is_empty()

    def enqueue(self, item: T) -> None:
        """Inserta un elemento al final de la cola en tiempo O(1)."""
        self.items.append(item)

    def dequeue(self) -> Optional[T]:
        """Retira el elemento más antiguo en tiempo O(1)."""
        return self.items.pop_front()

    def peek(self) -> Optional[T]:
        """Consulta el primer elemento sin retirarlo."""
        if self.items.head is None:
            return None
        return self.items.head.data

    def delete(self, item: T) -> bool:
        """Elimina la primera coincidencia de la cola."""
        return self.items.remove(item)

    def size(self) -> int:
        return self.items.get_size()
