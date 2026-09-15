"""Punto de entrada principal para ejecutar la aplicación de Listas Enlazadas."""

from controllers.controlador_tareas import ControladorTareas
from views.vista_tareas import VistaTareas


def main():
    controlador = ControladorTareas()
    app = VistaTareas(controlador)
    app.mainloop()


if __name__ == "__main__":
    main()