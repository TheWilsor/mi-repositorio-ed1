"""
Modulo para el Desafio 2: Correccion del TDA Pila 
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Stack:
    """
    Estructura LIFO (Last In, First Out) corregida 
    """

    def __init__(self) -> None:
        self._items: list = []

    def is_empty(self) -> bool:
        """Verifica correctamente si la pila no tiene elementos """
        return len(self._items) == 0

    def push(self, item: str) -> None:
        """Agrega un elemento a la cima de la pila """
        self._items.append(item)
        print(f"-> Elemento '{item}' apilado.")

    def pop(self) -> str | None:
        """
        Extrae y devuelve el elemento superior validando pila vacia
        """
        if self.is_empty():
            print("-> Error de comportamiento: Pila vacia (Stack Underflow) ")
            return None
        return self._items.pop()


if __name__ == "__main__":
    print("--- DESAFIO 2: CORRECCION DE TDA PILA ---")
    pila = Stack()
    pila.push("Modulo 1")
    pila.push("Modulo 2")
    pila.push("Modulo 3")
    pila.push("Modulo 4")

    # Para que el apilado se muestre
    # Se debe agregar la misma cantidad de modulos

    print(f"Desapilado: {pila.pop()}")
    print(f"Desapilado: {pila.pop()}")
    print(f"Desapilado: {pila.pop()}")
    print(f"Desapilado: {pila.pop()}")
    

    # Validacion de vacio
    pila.pop()