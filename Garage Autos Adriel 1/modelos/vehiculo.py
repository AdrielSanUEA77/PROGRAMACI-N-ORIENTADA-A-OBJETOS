class Vehiculo:
    def __init__(self, placa, marca, propietario):
        self.placa = placa.strip()
        self.marca = marca.strip()
        self.propietario = propietario.strip()

    def __str__(self):
        return f"{self.placa} - {self.marca} - {self.propietario}"
