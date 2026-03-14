import tkinter as tk
from tkinter import ttk, messagebox
from servicios.garaje_servicio import GarajeServicio

class AplicacionGaraje:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Garaje")
        self.root.geometry("520x360")
        self.root.resizable(False, False)

        self.servicio = GarajeServicio()

        self._construir_ui()

    def _construir_ui(self):
        cont = ttk.Frame(self.root, padding=10)
        cont.pack(fill=tk.BOTH, expand=True)

        titulo = ttk.Label(cont, text="Sistema Básico de Gestión de Garaje", font=("Segoe UI", 12, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0,10))

        ttk.Label(cont, text="Placa:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(cont, text="Marca:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(cont, text="Propietario:").grid(row=3, column=0, sticky=tk.W)

        self.entry_placa = ttk.Entry(cont, width=30)
        self.entry_marca = ttk.Entry(cont, width=30)
        self.entry_propietario = ttk.Entry(cont, width=30)

        self.entry_placa.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.entry_marca.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        self.entry_propietario.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)

        btn_agregar = ttk.Button(cont, text="Agregar vehículo", command=self.agregar_vehiculo)
        btn_limpiar = ttk.Button(cont, text="Limpiar", command=self.limpiar_campos)

        btn_agregar.grid(row=4, column=0, pady=8, sticky=tk.W)
        btn_limpiar.grid(row=4, column=1, pady=8, sticky=tk.W)

        # Tabla
        cols = ("Placa", "Marca", "Propietario")
        self.tabla = ttk.Treeview(cont, columns=cols, show="headings", height=8)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=150 if c != "Propietario" else 180)
        self.tabla.grid(row=5, column=0, columnspan=3, pady=(10,0), sticky="nsew")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(cont, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=5, column=3, sticky='ns')

        # Configurar grid
        cont.columnconfigure(2, weight=1)

    def agregar_vehiculo(self):
        placa = self.entry_placa.get()
        marca = self.entry_marca.get()
        propietario = self.entry_propietario.get()
        try:
            self.servicio.agregar_vehiculo(placa, marca, propietario)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.actualizar_tabla()
        self.limpiar_campos()

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for v in self.servicio.listar_vehiculos():
            self.tabla.insert("", "end", values=(v.placa, v.marca, v.propietario))

    def limpiar_campos(self):
        self.entry_placa.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_propietario.delete(0, tk.END)
        self.entry_placa.focus_set()
