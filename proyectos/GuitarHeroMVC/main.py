"""Punto de entrada para la aplicación de escritorio Guitar Hero MVC."""

import flet as ft

from controllers.app_controller import AppController


def main(page: ft.Page) -> None:
    """Configura la ventana y monta la vista principal de Flet."""
    page.title = "Guitar Hero MVC"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 1100
    page.window_height = 620
    app_controller = AppController(page)
    page.on_keyboard_event = app_controller.on_keyboard_event
    page.on_disconnect = app_controller.stop
    page.add(app_controller.build())
    page.update()
    


if __name__ == "__main__":
    ft.app(target=main)
