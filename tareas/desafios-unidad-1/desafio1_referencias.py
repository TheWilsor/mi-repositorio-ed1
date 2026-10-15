"""
Modulo para el Desafio 1: Gestion de Memoria y Referencias
Asignatura: Estructura de Datos 1 - UAGRM
"""


def demostracion_referencias() -> None:
    """Demuestra la diferencia entre copiar referencias y copiar datos"""
    # ERROR INICIAL: Ambas variables apuntan a la misma direccion de memoria
    original = [10, 20, 30]
    copia_incorrecta = original
    copia_incorrecta.append(40)

    print(f"Original modificada por error: {original}")

    # SOLUCION: Crear un nuevo objeto independiente en memoria
    original_correcto = [10, 20, 30]
    copia_real = original_correcto.copy()  # O tambien list(original_correcto)
    copia_real.append(40)

    print(f"Original intacta: {original_correcto}")
    print(f"Copia real modificada: {copia_real}")


if __name__ == "__main__":
    print("--- DESAFIO 1: REFERENCIAS Y MEMORIA ---")
    demostracion_referencias()