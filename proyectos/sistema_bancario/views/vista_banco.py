"""Vista gráfica en Tkinter para el Sistema Bancario estilo BNB."""

import tkinter as tk
from tkinter import messagebox, ttk


class VistaBanco(tk.Tk):
    """Interfaz principal dividida en Dispensador, Pantalla Principal TV y Panel de Cajeros."""

    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Sistema de Atención de Tickets - Estilo BNB (TDA Lista Enlazada)")
        self.geometry("950x620")
        self.configure(bg="#1E1E2E")
        self.resizable(False, False)

        self._crear_interfaz()
        self._actualizar_pantallas()

    def _crear_interfaz(self):
        # --- TÍTULO SUPERIOR ---
        lbl_titulo = tk.Label(
            self,
            text="BANCO NACIONAL DE BOLIVIA - MÓDULO DE ATENCIÓN",
            font=("Helvetica", 16, "bold"),
            bg="#2A2A3D",
            fg="#F39C12",
            pady=12
        )
        lbl_titulo.pack(fill=tk.X)

        # Contenedor Principal
        container = tk.Frame(self, bg="#1E1E2E")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- PANEL IZQUIERDO: DISPENSADOR Y PANEL CAJERO ---
        panel_izq = tk.Frame(container, bg="#1E1E2E", width=380)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        # 1. Dispensador de Tickets (Para Clientes)
        box_dispensador = tk.LabelFrame(
            panel_izq, text=" 🎫 Dispensador de Tickets ",
            font=("Helvetica", 11, "bold"), bg="#282A36", fg="#F8F8F2", padx=10, pady=10
        )
        box_dispensador.pack(fill=tk.X, pady=(0, 15))

        lbl_disp_info = tk.Label(
            box_dispensador, text="Seleccione el área para obtener su ticket:",
            bg="#282A36", fg="#BD93F9", font=("Helvetica", 9)
        )
        lbl_disp_info.pack(pady=(0, 10))

        areas = [
            ("Atención al Cliente", "#3498DB"),
            ("Cajas", "#2ECC71"),
            ("Plataforma", "#E67E22")
        ]

        for area_nombre, color in areas:
            btn = tk.Button(
                box_dispensador, text=f"+ {area_nombre}",
                font=("Helvetica", 10, "bold"), bg=color, fg="white",
                activebackground=color, cursor="hand2", relief=tk.FLAT,
                command=lambda a=area_nombre: self._solicitar_ticket(a)
            )
            btn.pack(fill=tk.X, pady=4, ipady=4)

        # 2. Panel del Cajero / Operador
        box_cajero = tk.LabelFrame(
            panel_izq, text=" 🖥️ Módulo Operador / Cajero ",
            font=("Helvetica", 11, "bold"), bg="#282A36", fg="#F8F8F2", padx=10, pady=10
        )
        box_cajero.pack(fill=tk.X)

        lbl_ventanilla = tk.Label(
            box_cajero, text="Número / Nombre de Ventanilla:",
            bg="#282A36", fg="#F8F8F2", font=("Helvetica", 9)
        )
        lbl_ventanilla.pack(anchor=tk.W, pady=(0, 2))

        self.combo_ventanilla = ttk.Combobox(
            box_cajero, values=["Ventanilla 1", "Ventanilla 2", "Ventanilla 3", "Plataforma 1"],
            state="readonly", font=("Helvetica", 10)
        )
        self.combo_ventanilla.current(0)
        self.combo_ventanilla.pack(fill=tk.X, pady=(0, 10))

        btn_llamar = tk.Button(
            box_cajero, text="📢 LLAMAR SIGUIENTE TICKET",
            font=("Helvetica", 11, "bold"), bg="#E74C3C", fg="white",
            cursor="hand2", relief=tk.FLAT,
            command=self._llamar_siguiente
        )
        btn_llamar.pack(fill=tk.X, ipady=8)

        # --- PANEL DERECHO: PANTALLA PRINCIPAL TV ---
        panel_derecho = tk.Frame(container, bg="#282A36", highlightthickness=2, highlightbackground="#F39C12")
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Header Pantalla TV
        lbl_tv_title = tk.Label(
            panel_derecho, text="PANTALLA DE TURNOS",
            font=("Helvetica", 12, "bold"), bg="#191A21", fg="#F39C12", pady=8
        )
        lbl_tv_title.pack(fill=tk.X)

        # Cuadro Gigante del Ticket En Atención
        box_atencion = tk.Frame(panel_derecho, bg="#44475A", padx=10, pady=15)
        box_atencion.pack(fill=tk.X, padx=15, pady=15)

        lbl_atencion_sub = tk.Label(
            box_atencion, text="TURNO ACTUAL EN ATENCIÓN",
            font=("Helvetica", 10, "bold"), bg="#44475A", fg="#50FA7B"
        )
        lbl_atencion_sub.pack()

        self.lbl_ticket_actual = tk.Label(
            box_atencion, text="---",
            font=("Helvetica", 28, "bold"), bg="#44475A", fg="#FF79C6"
        )
        self.lbl_ticket_actual.pack(pady=5)

        # Listas de Próximos y Finalizados
        frame_tablas = tk.Frame(panel_derecho, bg="#282A36")
        frame_tablas.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # En Espera
        box_espera = tk.LabelFrame(
            frame_tablas, text=" Próximos en Espera ",
            font=("Helvetica", 10, "bold"), bg="#282A36", fg="#F8F8F2"
        )
        box_espera.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.lb_espera = tk.Listbox(box_espera, bg="#191A21", fg="#8BE9FD", font=("Consolas", 10), relief=tk.FLAT)
        self.lb_espera.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Historial Finalizados
        box_fin = tk.LabelFrame(
            frame_tablas, text=" Últimos Atendidos ",
            font=("Helvetica", 10, "bold"), bg="#282A36", fg="#F8F8F2"
        )
        box_fin.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.lb_finalizados = tk.Listbox(box_fin, bg="#191A21", fg="#6272A4", font=("Consolas", 10), relief=tk.FLAT)
        self.lb_finalizados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _solicitar_ticket(self, area: str):
        num_ticket = self.controlador.solicitar_ticket(area)
        messagebox.showinfo("Ticket Generado", f"Su ticket es: {num_ticket}\nPor favor tome asiento y espere su llamado.")
        self._actualizar_pantallas()

    def _llamar_siguiente(self):
        ventanilla = self.combo_ventanilla.get()
        res = self.controlador.llamar_siguiente(ventanilla)
        if res == "No hay tickets en espera.":
            messagebox.showwarning("Cola Vacía", "No hay tickets pendientes en la lista enlazada.")
        self._actualizar_pantallas()

    def _actualizar_pantallas(self):
        datos = self.controlador.obtener_estado_pantallas()

        # Actualizar ticket gigante
        self.lbl_ticket_actual.config(text=datos["en_atencion"])

        # Actualizar Próximos en Espera
        self.lb_espera.delete(0, tk.END)
        for t in datos["en_espera"]:
            self.lb_espera.insert(tk.END, f" • {t}")

        # Actualizar Finalizados
        self.lb_finalizados.delete(0, tk.END)
        for f in datos["finalizados"]:
            self.lb_finalizados.insert(tk.END, f" ✓ {f}")



 # --- PIE DE PÁGINA (DERECHOS DE AUTOR) ---
        lbl_credits = tk.Label(
            self,
            text="© 2026 Wilson Leonel Mojica Cuellar — Todos los derechos reservados | Licencia de Funcionamiento v1.0",
            font=("Helvetica", 8),
            bg="#1E1E2E",
            fg="#6272A4"
        )
        lbl_credits.pack(side=tk.BOTTOM, pady=4)           