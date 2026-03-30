
from modelos.tarea import Tarea

class TareaServicio:
    def __init__(self):
        self.tareas = []
        self.next_id = 1

    def agregar_tarea(self, descripcion):
        tarea = Tarea(self.next_id, descripcion)
        self.tareas.append(tarea)
        self.next_id += 1
        return tarea

    def completar_tarea(self, id_tarea):
        for t in self.tareas:
            if t.id == id_tarea:
                t.completada = not t.completada
                return True
        return False

    def eliminar_tarea(self, id_tarea):
        for t in self.tareas:
            if t.id == id_tarea:
                self.tareas.remove(t)
                return True
        return False

    def listar_tareas(self):
        return self.tareas
