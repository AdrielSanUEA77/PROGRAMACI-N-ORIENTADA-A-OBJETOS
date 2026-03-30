
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.tarea_servicio import TareaServicio

class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title('Lista de Tareas - Semana 15')
        self.servicio = TareaServicio()

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda e: self.agregar())

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text='Añadir', command=self.agregar).grid(row=0, column=0, padx=4)
        tk.Button(frame, text='Completar', command=self.completar).grid(row=0, column=1, padx=4)
        tk.Button(frame, text='Eliminar', command=self.eliminar).grid(row=0, column=2, padx=4)

        self.tree = ttk.Treeview(root, columns=('ID', 'Descripción'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.pack(pady=10)

        self.root.bind('<c>', lambda e: self.completar())
        self.root.bind('<C>', lambda e: self.completar())
        self.root.bind('<Delete>', lambda e: self.eliminar())
        self.root.bind('<d>', lambda e: self.eliminar())
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def actualizar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for t in self.servicio.listar_tareas():
            estado = '[✔] ' if t.completada else ''
            self.tree.insert('', 'end', values=(t.id, estado + t.descripcion))

    def agregar(self):
        desc = self.entry.get().strip()
        if not desc:
            messagebox.showwarning('Error', 'Ingrese una tarea')
            return
        self.servicio.agregar_tarea(desc)
        self.entry.delete(0, tk.END)
        self.actualizar()

    def completar(self):
        sel = self.tree.selection()
        if not sel: return
        id_t = int(self.tree.item(sel[0])['values'][0])
        self.servicio.completar_tarea(id_t)
        self.actualizar()

    def eliminar(self):
        sel = self.tree.selection()
        if not sel: return
        id_t = int(self.tree.item(sel[0])['values'][0])
        self.servicio.eliminar_tarea(id_t)
        self.actualizar()
