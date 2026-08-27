"""
Modulo para el Desafio 3: Enlazado de Nodos en el Heap
Asignatura: Estructura de Datos 1 - UAGRM
"""


class Nodo:
    """Representa un nodo dinamico guardado en el Heap """

    def __init__(self, valor: int):
        self.valor: int = valor
        self.siguiente: "Nodo | None" = None


def demostracion_nodos() -> None:
    """Demuestra el enlazado correcto sin perder la referencia inicial """
    # Creacion del primer nodo (Cabeza)
    cabeza = Nodo(100)

    # ERROR TIPICO: cabeza = Nodo(200) deshace el enlace anterior

    # SOLUCION: Enlazar mediante el puntero 'siguiente'
    segundo_nodo = Nodo(200)
    cabeza.siguiente = segundo_nodo

    # Hacemos la prueba con mas de 2 nodos
    tercer_nodo = Nodo(300)
    cabeza.siguiente = tercer_nodo
    
    cuarto_nodo = Nodo(400)
    cabeza.siguiente = cuarto_nodo
    # Mantiene el recorrido en cadenas de nodos hasta el ultimo de esta forma

    # Recorrido desde el nodo raiz
    actual = cabeza
    idx = 1
    while actual is not None:
        print(f"Nodo {idx} en memoria -> Valor: {actual.valor}")
        actual = actual.siguiente
        idx += 1


if __name__ == "__main__":
    print("--- DESAFIO 3: NODOS Y PUNTEROS EN HEAP ---")
    demostracion_nodos()