from typing import Optional, Generic, TypeVar, Any, Callable

# Definición del tipo de dato genérico T
T = TypeVar('T')

class Node(Generic[T]):
    """
    Clase que representa un nodo en una lista enlazada.
    Cada nodo tiene un dato, un puntero al siguiente nodo y un puntero al nodo anterior.
    """

    def __init__(self, data: T, next_node: Optional['Node'] = None, prev_node: Optional['Node'] = None):
        self.data = data
        self.next = next_node
        self.prev = prev_node

class DoublyLinkedList(Generic[T]):
    """
    Clase que representa una lista enlazada doblemente enlazada.
    Permite la inserción y eliminación de nodos en O(1) en extremos y recorrido bidireccional.
    """

    def __init__(self):
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.size: int = 0

    def is_empty(self) -> bool:
        """
        Método que verifica si la lista enlazada está vacía.
        Returns:
            bool: True si la lista está vacía, False en caso contrario.
        """
        return self.head is None

    def append(self, data: T) -> None:
        """
        Método que agrega un nuevo nodo al final de la lista enlazada.
        Args:
            data (T): El dato que se desea agregar al nodo.
        """
        new_node = Node(data, prev=self.tail)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def prepend(self, data: T) -> None:
        """
        Método que agrega un nuevo nodo al principio de la lista enlazada.
        Args:
            data (T): El dato que se desea agregar al nodo.
        """
        new_node = Node(data, next=self.head)
        if self.is_empty():
            self.tail = new_node
        else:
            self.head.prev = new_node
        self.head = new_node
        self.size += 1

    def delete(self, data: T) -> None:
        """
        Método que elimina el primer nodo que contenga el dato especificado.
        Args:
            data (T): El dato que se desea eliminar.
        """
        current = self.head
        while current is not None:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.size -= 1
                return
            current = current.next

    def search(self, data: T) -> bool:
        """
        Método que verifica si un dato está presente en la lista enlazada.
        Args:
            data (T): El dato que se desea buscar.
        Returns:
            bool: True si el dato está presente, False en caso contrario.
        """
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def get_size(self) -> int:
        """
        Método que devuelve el tamaño de la lista enlazada.
        Returns:
            int: El número de nodos en la lista.
        """
        return self.size

class Queue(Generic[T]):
    """
    Clase que representa una cola basada en una lista enlazada doblemente enlazada.
    Permite la inserción y eliminación de elementos en O(1) estricto en FIFO.
    """

    def __init__(self):
        self.items: DoublyLinkedList[T] = DoublyLinkedList()

    def is_empty(self) -> bool:
        """
        Método que verifica si la cola está vacía.
        Returns:
            bool: True si la cola está vacía, False en caso contrario.
        """
        return self.items.is_empty()

    def enqueue(self, item: T) -> None:
        """
        Método que agrega un nuevo elemento al final de la cola.
        Args:
            item (T): El elemento que se desea agregar.
        """
        self.items.append(item)

    def dequeue(self) -> Optional[T]:
        """
        Método que elimina y devuelve el primer elemento de la cola.
        Returns:
            Optional[T]: El primer elemento de la cola, None si la cola está vacía.
        """
        if self.is_empty():
            return None
        item = self.items.head.data
        self.items.delete(item)
        return item

    def peek(self) -> Optional[T]:
        """
        Método que devuelve el primer elemento de la cola sin eliminarlo.
        Returns:
            Optional[T]: El primer elemento de la cola, None si la cola está vacía.
        """
        if self.is_empty():
            return None
        return self.items.head.data

    def size(self) -> int:
        """
        Método que devuelve el tamaño de la cola.
        Returns:
            int: El número de elementos en la cola.
        """
        return self.items.get_size()
