
# services/banco_service.py
from __future__ import annotations
from typing import Dict, List
from models.cuenta import Cuenta

class BancoService:
    """
    Capa de servicios (separa la lógica del 'negocio' de los modelos).
    - Gestiona cuentas: registro, consulta, transferencias y aplicación de intereses.
    """

    def __init__(self) -> None:
        # Diccionario interno de cuentas: numero -> Cuenta
        self._cuentas: Dict[str, Cuenta] = {}

    def registrar_cuenta(self, cuenta: Cuenta) -> None:
        if cuenta.numero in self._cuentas:
            raise ValueError(f"Ya existe una cuenta con número {cuenta.numero}.")
        self._cuentas[cuenta.numero] = cuenta

    def obtener_cuenta(self, numero: str) -> Cuenta:
        try:
            return self._cuentas[numero]
        except KeyError:
            raise KeyError(f"No existe la cuenta con número {numero}.")

    def transferir(self, numero_origen: str, numero_destino: str, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto a transferir debe ser mayor a 0.")
        origen = self.obtener_cuenta(numero_origen)
        destino = self.obtener_cuenta(numero_destino)

        # Reutilizamos la lógica de retiro y depósito que ya valida reglas.
        origen.retirar(monto)
        destino.depositar(monto)

    def aplicar_intereses(self) -> dict[str, float]:
        """
        Recorre todas las cuentas y aplica intereses.
        Demostración de polimorfismo: cada cuenta responde distinto a aplicar_interes().
        Devuelve un mapeo: numero_cuenta -> interés_aplicado
        """
        resumen_intereses: dict[str, float] = {}
        for numero, cuenta in self._cuentas.items():
            interes = cuenta.aplicar_interes()
            resumen_intereses[nombre := numero] = interes
        return resumen_intereses

    def listar_resumenes(self) -> List[str]:
        """Devuelve resúmenes tipo string para mostrar en consola/GUI."""
        return [c.resumen() for c in self._cuentas.values()]
