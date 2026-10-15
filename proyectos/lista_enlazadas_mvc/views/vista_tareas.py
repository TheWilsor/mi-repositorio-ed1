"""Vista de Tkinter organizada en 3 paneles enumerados."""

import tkinter as tk
from tkinter import messagebox


class VistaTareas(tk.Tk):
    """Interfaz gráfica con 3 cuadros delimitados para la gestión visual."""

    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Gestor de Tareas - Lista Enlazada (3 Paneles)")
        self.geometry("820x480")
        self.resizable(False, False)

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Entrada de Texto
        frame_top = tk.Frame(self)
        frame_top.pack(pady=10)

        lbl_instruccion = tk.Label(frame_top, text="Descripción de la Tarea:")
        lbl_instruccion.pack(side=tk.LEFT, padx=5)

        self.entry_tarea = tk.Entry(frame_top, width=40)
        self.entry_tarea.pack(side=tk.LEFT, padx=5)

        btn_agregar = tk.Button(
            frame_top, text="Agregar Tarea", command=self._ejecutar_agregar
        )
        btn_agregar.pack(side=tk.LEFT, padx=5)

        # Contenedor para los 3 cuadros
        frame_listas = tk.Frame(self)
        frame_listas.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Panel 1: Todas las Tareas
        frame_todas = tk.LabelFrame(frame_listas, text="1. Todas las Tareas", padx=5, pady=5)
        frame_todas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.lb_todas = tk.Listbox(frame_todas, width=30, height=14)
        self.lb_todas.pack(fill=tk.BOTH, expand=True)

        # Panel 2: Tareas Pendientes
        frame_pendientes = tk.LabelFrame(frame_listas, text="2. Pendientes", padx=5, pady=5)
        frame_pendientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.lb_pendientes = tk.Listbox(frame_pendientes, width=30, height=14)
        self.lb_pendientes.pack(fill=tk.BOTH, expand=True)

        # Panel 3: Tareas Completadas
        frame_completadas = tk.LabelFrame(frame_listas, text="3. Completadas", padx=5, pady=5)
        frame_completadas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.lb_completadas = tk.Listbox(frame_completadas, width=30, height=14)
        self.lb_completadas.pack(fill=tk.BOTH, expand=True)

        # Botones de Acciones abajo
        frame_acciones = tk.Frame(self)
        frame_acciones.pack(pady=10)

        btn_completar = tk.Button(
            frame_acciones, text="Marcar Completada", command=self._ejecutar_completar
        )
        btn_completar.pack(side=tk.LEFT, padx=10)

        btn_eliminar = tk.Button(
            frame_acciones, text="Eliminar Tarea", command=self._ejecutar_eliminar
        )
        btn_eliminar.pack(side=tk.LEFT, padx=10)

    def _ejecutar_agregar(self):
        texto = self.entry_tarea.get()
        try:
            self.controlador.agregar_tarea(texto)
            self.entry_tarea.delete(0, tk.END)
            self._actualizar_vista()
        except ValueError as e:
            messagebox.showwarning("Atención", str(e))

    def _ejecutar_completar(self):
        try:
            seleccion = self._obtener_seleccion_global()
            self.controlador.completar_tarea(seleccion)
            self._actualizar_vista()
        except (ValueError, KeyError) as e:
            messagebox.showwarning("Atención", str(e))

    def _ejecutar_eliminar(self):
        try:
            seleccion = self._obtener_seleccion_global()
            self.controlador.eliminar_tarea(seleccion)
            self._actualizar_vista()
        except (ValueError, KeyError) as e:
            messagebox.showwarning("Atención", str(e))

    def _obtener_seleccion_global(self) -> str:
        """Busca cuál de las 3 listas tiene un elemento seleccionado."""
        for lb in [self.lb_todas, self.lb_pendientes, self.lb_completadas]:
            indices = lb.curselection()
            if indices:
                return lb.get(indices[0])
        return ""

    def _actualizar_vista(self):
        """Limpia los 3 cuadros y coloca la información numerada actualizada."""
        self.lb_todas.delete(0, tk.END)
        self.lb_pendientes.delete(0, tk.END)
        self.lb_completadas.delete(0, tk.END)

        datos = self.controlador.obtener_listas_clasificadas()

        for t in datos["todas"]:
            self.lb_todas.insert(tk.END, t)

        for p in datos["pendientes"]:
            self.lb_pendientes.insert(tk.END, p)

        for c in datos["completadas"]:
            self.lb_completadas.insert(tk.END, c)