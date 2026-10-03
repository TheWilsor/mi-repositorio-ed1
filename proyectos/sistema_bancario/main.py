"""Punto de entrada principal para el Sistema de Tickets Bancarios BNB."""

from controllers.controlador_banco import ControladorBanco
from views.vista_banco import VistaBanco


def main():
    """Inicializa el controlador y lanza la interfaz gráfica del banco."""
    controlador = ControladorBanco()
    app = VistaBanco(controlador)
    app.mainloop()


if __name__ == "__main__":
    main()