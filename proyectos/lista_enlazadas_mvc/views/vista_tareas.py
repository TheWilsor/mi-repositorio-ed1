"""Módulo de la Vista utilizando Tkinter para la interfaz de usuario."""

import tkinter as tk
from tkinter import messagebox


class VistaTareas(tk.Tk):
    """Clase principal de la UI construida con Tkinter."""

    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Gestor de Tareas - Lista Enlazada (MVC)")
        self.geometry("480x450")
        self.resizable(False, False)

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Entrada de Texto
        lbl_instruccion = tk.Label(self, text="Descripción de la Tarea:")
        lbl_instruccion.pack(pady=(10, 2))

        self.entry_tarea = tk.Entry(self, width=45)
        self.entry_tarea.pack(pady=5)

        # Botones de Agregar
        frame_agregar = tk.Frame(self)
        frame_agregar.pack(pady=5)

        btn_agregar_final = tk.Button(
            frame_agregar,
            text="Agregar al Final",
            command=lambda: self._ejecutar_agregar("final")
        )
        btn_agregar_final.pack(side=tk.LEFT, padx=5)

        btn_agregar_inicio = tk.Button(
            frame_agregar,
            text="Agregar al Inicio",
            command=lambda: self._ejecutar_agregar("inicio")
        )
        btn_agregar_inicio.pack(side=tk.LEFT, padx=5)

        # Lista de Tareas (Listbox + Scrollbar)
        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=10)

        self.listbox = tk.Listbox(frame_lista, width=50, height=12)
        scrollbar = tk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones de Acciones (Completar / Eliminar)
        frame_acciones = tk.Frame(self)
        frame_acciones.pack(pady=5)

        btn_completar = tk.Button(
            frame_acciones, text="Marcar Completada", command=self._ejecutar_completar
        )
        btn_completar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(
            frame_acciones, text="Eliminar Tarea", command=self._ejecutar_eliminar
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

    def _ejecutar_agregar(self, posicion: str):
        texto = self.entry_tarea.get()
        try:
            self.controlador.agregar_tarea(texto, posicion)
            self.entry_tarea.delete(0, tk.END)
            self._actualizar_vista()
        except ValueError as e:
            messagebox.showwarning("Atención", str(e))

    def _ejecutar_completar(self):
        try:
            seleccion = self._obtener_seleccion()
            self.controlador.completar_tarea(seleccion)
            self._actualizar_vista()
        except (ValueError, KeyError) as e:
            messagebox.showwarning("Atención", str(e))

    def _ejecutar_eliminar(self):
        try:
            seleccion = self._obtener_seleccion()
            self.controlador.eliminar_tarea(seleccion)
            self._actualizar_vista()
        except (ValueError, KeyError) as e:
            messagebox.showwarning("Atención", str(e))

    def _obtener_seleccion(self) -> str:
        indices = self.listbox.curselection()
        if not indices:
            return ""
        return self.listbox.get(indices[0])

    def _actualizar_vista(self):
        self.listbox.delete(0, tk.END)
        tareas = self.controlador.obtener_lista_tareas()
        for tarea in tareas:
            self.listbox.insert(tk.END, tarea)