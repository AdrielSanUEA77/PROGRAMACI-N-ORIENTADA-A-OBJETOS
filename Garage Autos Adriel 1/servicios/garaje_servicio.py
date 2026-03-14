from modelos.vehiculo import Vehiculo

class GarajeServicio:
    def __init__(self):
        self.vehiculos = []

    def agregar_vehiculo(self, placa, marca, propietario):
        if not placa or not marca or not propietario:
            raise ValueError("Todos los campos son obligatorios")
        # Validación simple de placa
        if len(placa) < 5:
            raise ValueError("La placa debe tener al menos 5 caracteres")
        # Evitar duplicados por placa
        if any(v.placa.lower() == placa.lower() for v in self.vehiculos):
            raise ValueError("Ya existe un vehículo con esa placa")
        vehiculo = Vehiculo(placa, marca, propietario)
        self.vehiculos.append(vehiculo)
        return vehiculo

    def listar_vehiculos(self):
        return list(self.vehiculos)

    def limpiar(self):
        self.vehiculos.clear()
