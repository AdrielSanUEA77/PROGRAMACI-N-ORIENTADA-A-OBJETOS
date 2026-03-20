
import tkinter as tk
from tkinter import ttk, messagebox

class AppTkinter(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.title("Registro de Visitantes")
        self.geometry("600x400")
        self.servicio = servicio

        tk.Label(self, text="Cédula:").pack()
        self.cedula_entry = tk.Entry(self)
        self.cedula_entry.pack()

        tk.Label(self, text="Nombre:").pack()
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Motivo:").pack()
        self.motivo_entry = tk.Entry(self)
        self.motivo_entry.pack()

        tk.Button(self, text="Registrar", command=self.registrar).pack()
        tk.Button(self, text="Eliminar", command=self.eliminar).pack()
        tk.Button(self, text="Limpiar", command=self.limpiar).pack()

        self.tabla = ttk.Treeview(self, columns=("cedula","nombre","motivo"), show="headings")
        for col in ("cedula","nombre","motivo"):
            self.tabla.heading(col, text=col.capitalize())
        self.tabla.pack(expand=True, fill="both")

    def registrar(self):
        ced = self.cedula_entry.get()
        nom = self.nombre_entry.get()
        mot = self.motivo_entry.get()
        if not ced or not nom or not mot:
            messagebox.showwarning("Error", "Completa todos los campos")
            return
        self.servicio.agregar_visitante(ced, nom, mot)
        self.actualizar_tabla()
        self.limpiar()
        messagebox.showinfo("OK", "Visitante registrado")

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Error", "Selecciona un visitante")
            return
        ced = self.tabla.item(sel[0])['values'][0]
        self.servicio.eliminar_visitante(ced)
        self.actualizar_tabla()

    def limpiar(self):
        self.cedula_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.motivo_entry.delete(0, tk.END)

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for v in self.servicio.obtener_visitantes():
            self.tabla.insert('', 'end', values=(v.cedula, v.nombre, v.motivo))
