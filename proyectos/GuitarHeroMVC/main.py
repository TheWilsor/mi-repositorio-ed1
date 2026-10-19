import flet as ft
from controllers.app_controller import AppController

def main(page: ft.Page):
    """
    Función principal que inicializa y muestra la interfaz gráfica de usuario.
    Args:
        page (ft.Page): La página principal de Flet.
    """
    page.title = "Guitar Hero MVC"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    app_controller = AppController()
    page.add(app_controller)

    page.update()

ft.app(target=main)
