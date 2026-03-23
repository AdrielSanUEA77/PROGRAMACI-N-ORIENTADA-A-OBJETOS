import tkinter as tk
from tkinter import ttk, messagebox
from servicios.tarea_servicio import TareaServicio

class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.servicio = TareaServicio()

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.evento_enter)

        frame_botones = tk.Frame(root)
        frame_botones.pack()

        tk.Button(frame_botones, text="Añadir Tarea", command=self.agregar).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Marcar Completada", command=self.completar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(root, columns=("ID", "Descripción"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack(pady=10)

        self.tree.bind("<Double-1>", self.evento_doble_click)

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for t in self.servicio.listar_tareas():
            estilo = "[Hecho] " if t.completada else ""
            self.tree.insert("", "end", values=(t.id, estilo + t.descripcion))

    def agregar(self):
        desc = self.entry.get().strip()
        if desc == "":
            messagebox.showwarning("Error", "Escribe una tarea.")
            return

        self.servicio.agregar_tarea(desc)
        self.entry.delete(0, tk.END)
        self.actualizar_lista()

    def completar(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Error", "Selecciona una tarea.")
            return

        id_tarea = int(self.tree.item(seleccionado[0])["values"][0])
        self.servicio.completar_tarea(id_tarea)
        self.actualizar_lista()

    def eliminar(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Error", "Selecciona una tarea.")
            return

        id_tarea = int(self.tree.item(seleccionado[0])["values"][0])
        self.servicio.eliminar_tarea(id_tarea)
        self.actualizar_lista()

    def evento_enter(self, event):
        self.agregar()

    def evento_doble_click(self, event):
        self.completar()
