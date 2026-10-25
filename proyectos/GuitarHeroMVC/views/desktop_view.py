"""Vista arcade Flet con pista animada de cuatro carriles a la derecha y controles a la izquierda."""

from __future__ import annotations

from typing import Any, Callable, Iterable, Optional

import flet as ft

from models.game_engine import NoteEvent, Song
from models.structures import DoublyLinkedList


class DesktopView:
    """Dibuja carriles y notas sin alojar reglas del juego."""

    LANES: tuple[str, ...] = ("A", "S", "D", "F")
    LANE_COLORS: tuple[str, ...] = (
        "#22C55E",
        "#EF4444",
        "#EAB308",
        "#3B82F6",
    )
    BOARD_WIDTH: int = 600
    BOARD_HEIGHT: int = 500
    HIT_LINE_Y: int = 420
    LANE_WIDTH: int = 150
    NOTE_SIZE: int = 32
    APPROACH_SECONDS: float = 3.0

    def __init__(
        self,
        on_start: Callable[[Any], None],
        on_add_player: Callable[[Any], None],
        on_remove_player: Callable[[Any], None],
        on_lane_press: Callable[[str], None],
        on_song_change: Callable[[str], None],
        on_refresh_library: Callable[[Any], None],
        on_export_library: Callable[[Any], None],
        on_volume_change: Callable[[float], None],
    ) -> None:
        self._on_lane_press: Callable[[str], None] = on_lane_press
        self._on_song_change: Callable[[str], None] = on_song_change
        self._on_volume_change: Callable[[float], None] = on_volume_change
        self._on_refresh_library: Callable[[Any], None] = on_refresh_library
        self._on_export_library: Callable[[Any], None] = on_export_library
        
        self.title_label: ft.Text = ft.Text(
            value="No song playing",
            size=22,
            weight=ft.FontWeight.BOLD,
            color="#F4F4F5",
        )
        self.note_label: ft.Text = ft.Text(
            value="Current Note: --",
            size=18,
            color="#A5B4FC",
        )
        self.player_label: ft.Text = ft.Text(
            value="Sin jugador",
            color="#D4D4D8",
        )
        self.score_label: ft.Text = ft.Text(
            value="Puntaje: 0 | Racha: 0 | Multiplicador: x1",
            size=15,
            weight=ft.FontWeight.BOLD,
            color="#34D399",
        )
        self.status_label: ft.Text = ft.Text(value="", color="#A1A1AA")
        
        self.start_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Start Game",
            on_click=on_start,
        )
        self.add_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Add Player",
            on_click=on_add_player,
        )
        self.remove_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Remove Player",
            on_click=on_remove_player,
        )
        self.song_dropdown: ft.Dropdown = ft.Dropdown(
            label="Elige una canción",
            width=360,
            options=[],
            on_change=self._song_changed,
        )
        self.refresh_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Actualizar música",
            on_click=self._on_refresh_library,
        )
        self.export_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Exportar catálogo",
            on_click=self._on_export_library,
        )
        self.volume_label: ft.Text = ft.Text("70%")
        self.volume_slider: ft.Slider = ft.Slider(
            min=0.0,
            max=1.0,
            divisions=20,
            value=0.7,
            width=220,
            on_change=self._volume_changed,
        )
        self.lane_buttons: tuple[ft.Container, ...] = tuple(
            self._create_lane_button(lane, index)
            for index, lane in enumerate(self.LANES)
        )
        self._static_controls: list[ft.Control] = (
            self._create_static_controls()
        )
        self.board_stack: ft.Stack = ft.Stack(
            controls=self._static_controls,
            width=self.BOARD_WIDTH,
            height=self.BOARD_HEIGHT,
        )
        self.start_button_row: ft.Row = ft.Row(
            controls=[self.start_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.player_buttons_row: ft.Row = ft.Row(
            controls=[self.add_button, self.remove_button],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
        )
        self._rendered_song: Optional[Song] = None
        self._rendered_chart: Optional[DoublyLinkedList[NoteEvent]] = None
        self._rendered_note_count: int = 0
        self._note_markers: list[tuple[NoteEvent, ft.Container]] = []

        # Panel izquierdo: Controles, selectores, puntaje y ajustes
        left_panel = ft.Column(
            controls=[
                ft.Text("GUITAR HERO MVC", size=14, weight=ft.FontWeight.BOLD, color="#A78BFA"),
                self.song_dropdown,
                ft.Row(
                    controls=[
                        self.refresh_button,
                        self.export_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                ),
                self.start_button_row,
                ft.Divider(color="#3F3F46", height=20),
                self.title_label,
                self.note_label,
                self.player_label,
                self.score_label,
                ft.Divider(color="#3F3F46", height=20),
                ft.Row(
                    controls=[
                        ft.Text("Volumen"),
                        self.volume_slider,
                        self.volume_label,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.player_buttons_row,
                self.status_label,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            alignment=ft.MainAxisAlignment.CENTER,
            width=400,
        )

        # Contenedor principal: Izquierda (Controles) | Derecha (Pista de notas amplia)
        self.root: ft.Container = ft.Container(
            content=ft.Row(
                controls=[
                    left_panel,
                    ft.VerticalDivider(color="#3F3F46", width=20),
                    self.board_stack,  # Pista de notas grande a la derecha
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=24,
            border_radius=16,
            bgcolor="#18181B",
            width=1080,  # Ancho total de la ventana adaptado a dos columnas
        )

    def _create_static_controls(self) -> list[ft.Control]:
        """Crea fondos y zonas de impacto para los cuatro carriles."""
        controls: list[ft.Control] = []
        for index, lane in enumerate(self.LANES):
            left = index * self.LANE_WIDTH
            controls.append(
                ft.Container(
                    left=left + 2,
                    top=0,
                    width=self.LANE_WIDTH - 4,
                    height=self.BOARD_HEIGHT,
                    bgcolor="#202027" if index % 2 == 0 else "#19191F",
                    border_radius=8,
                )
            )
            controls.append(
                ft.Container(
                    left=left,
                    top=0,
                    width=1,
                    height=self.BOARD_HEIGHT,
                    bgcolor="#3F3F46",
                )
            )
            controls.append(self.lane_buttons[index])

        controls.append(
            ft.Container(
                left=0,
                top=self.HIT_LINE_Y,
                width=self.BOARD_WIDTH,
                height=3,
                bgcolor="#E4E4E7",
            )
        )
        return controls

    def _create_lane_button(self, lane: str, index: int) -> ft.Container:
        """Crea el objetivo táctil/visual asociado a una tecla de carril."""
        left = index * self.LANE_WIDTH + (self.LANE_WIDTH - 82) / 2
        return ft.Container(
            content=ft.Text(
                lane,
                size=18,
                weight=ft.FontWeight.BOLD,
                color="#111827",
            ),
            left=left,
            top=self.HIT_LINE_Y + 18,
            width=82,
            height=42,
            alignment=ft.alignment.center,
            bgcolor=self.LANE_COLORS[index],
            border_radius=12,
            on_click=lambda event, selected_lane=lane: self._on_lane_press(
                selected_lane
            ),
        )

    def set_song_options(
        self,
        options: Iterable[tuple[str, str]],
        selected_key: Optional[str],
    ) -> None:
        """Actualiza el selector de pistas con opciones de la biblioteca."""
        controls: list[Any] = []
        for key, label in options:
            controls.append(ft.dropdown.Option(key=key, text=label))
        self.song_dropdown.options = controls
        self.song_dropdown.value = selected_key

    def set_volume(self, volume: float) -> None:
        """Refleja en el slider el nivel real del reproductor."""
        normalized_volume = min(1.0, max(0.0, float(volume)))
        self.volume_slider.value = normalized_volume
        self.volume_label.value = f"{round(normalized_volume * 100)}%"

    def set_preparing(self, preparing: bool) -> None:
        """Indica visualmente cuando se calcula el chart rítmico."""
        self.start_button.disabled = preparing
        self.start_button.text = (
            "Analizando BPM..." if preparing else "Start Game"
        )

    def _song_changed(self, event: Any) -> None:
        """Entrega al controlador la ruta elegida en el desplegable."""
        selected_path = event.control.value
        if selected_path:
            self._on_song_change(str(selected_path))

    def _volume_changed(self, event: Any) -> None:
        """Envía los cambios del control de volumen al controlador MVC."""
        value = event.control.value
        if value is not None:
            self._on_volume_change(float(value))

    def build(self) -> ft.Container:
        """Devuelve el panel arcade raíz para la página Flet."""
        return self.root

    def render(
        self,
        title: str,
        note: str,
        player: str,
        score: str,
        message: str,
        song: Optional[Song],
        playback_time: float,
    ) -> None:
        """Refresca el marcador y las posiciones de la pista visual."""
        self.title_label.value = title
        self.note_label.value = note
        self.player_label.value = f"Jugador actual: {player}"
        self.score_label.value = score
        self.status_label.value = message
        self._set_song(song)
        self.update_note_positions(playback_time)

    def _set_song(self, song: Optional[Song]) -> None:
        """Asocia controles de nota a los eventos enlazados de la canción."""
        chart = song.notes if song is not None else None
        note_count = len(chart) if chart is not None else 0
        if (
            song is self._rendered_song
            and chart is self._rendered_chart
            and note_count == self._rendered_note_count
        ):
            return

        self._rendered_song = song
        self._rendered_chart = chart
        self._rendered_note_count = note_count
        self._note_markers = []
        controls = list(self._static_controls)
        if song is not None:
            for event in song.iter_notes():
                lane_index = self.LANES.index(event.lane)
                left = lane_index * self.LANE_WIDTH + (
                    self.LANE_WIDTH - self.NOTE_SIZE
                ) / 2
                marker = ft.Container(
                    content=ft.Text(
                        event.lane,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="#111827",
                    ),
                    left=left,
                    top=-self.NOTE_SIZE,
                    width=self.NOTE_SIZE,
                    height=self.NOTE_SIZE,
                    alignment=ft.alignment.center,
                    bgcolor=self.LANE_COLORS[lane_index],
                    border_radius=self.NOTE_SIZE / 2,
                    visible=False,
                )
                controls.append(marker)
                self._note_markers.append((event, marker))
        self.board_stack.controls = controls

    def update_note_positions(self, playback_time: float) -> None:
        """Anima los nodos con el reloj de audio hacia la línea de impacto de forma precisa."""
        pixels_per_second = self.HIT_LINE_Y / self.APPROACH_SECONDS

        for event, marker in self._note_markers:
            time_to_hit = event.time_seconds - playback_time
            top = self.HIT_LINE_Y - (time_to_hit * pixels_per_second)
            
            marker.top = top
            marker.visible = (
                not event.was_hit
                and not event.was_missed
                and -self.NOTE_SIZE <= top <= self.BOARD_HEIGHT + self.NOTE_SIZE
            )
        
        if self.board_stack.page is not None:
            self.board_stack.update()