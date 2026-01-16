
# models/cuenta.py
from __future__ import annotations
from abc import ABC, abstractmethod
from .cliente import Cliente

class Cuenta(ABC):
    """
    Clase base abstracta (Herencia/Polimorfismo).
    - Define interfaz común y comportamiento compartido para cuentas.
    - Encapsulación: __saldo es privado; se accede de forma controlada.
    """

    def __init__(self, numero: str, titular: Cliente, saldo_inicial: float = 0.0):
        self._numero = numero          # Atributo protegido (convención: un guion bajo)
        self._titular = titular
        self.__saldo = 0.0             # Atributo privado (name mangling: dos guiones bajos)

        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.__saldo = float(saldo_inicial)

    # ===== Encapsulación: acceso de solo lectura al saldo =====
    @property
    def saldo(self) -> float:
        """Saldo como propiedad de solo lectura (no se puede asignar directamente)."""
        return self.__saldo

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def titular(self) -> Cliente:
        return self._titular

    # ===== Operaciones comunes =====
    def depositar(self, monto: float) -> None:
        """Acredita fondos de manera controlada."""
        if monto <= 0:
            raise ValueError("El depósito debe ser mayor a 0.")
        self.__saldo += float(monto)

    # Métodos 'protegidos' para cambiar el saldo internamente
    def _debitar(self, monto: float) -> None:
        self.__saldo -= float(monto)

    def _acreditar(self, monto: float) -> None:
        self.__saldo += float(monto)

    # ===== Polimorfismo: cada cuenta implementa su propia lógica =====
    @abstractmethod
    def retirar(self, monto: float) -> None:
        """Cada tipo de cuenta define cómo se retira dinero (puede haber reglas distintas)."""
        pass

    @abstractmethod
    def calcular_interes(self) -> float:
        """Cada tipo de cuenta calcula el interés de forma diferente (o no aplica)."""
        pass

    def aplicar_interes(self) -> float:
        """
        Método plantilla: usa el cálculo polimórfico y, si hay interés positivo,
        lo acredita. Devuelve el interés aplicado.
        """
        interes = self.calcular_interes()
        if interes > 0:
            self._acreditar(interes)
        return interes

    def resumen(self) -> str:
        """Representación amigable del estado de la cuenta."""
        return (
            f"{self.__class__.__name__} {self._numero} | "
            f"Titular: {self._titular.nombre} | Saldo: ${self.saldo:,.2f}"
        )


class CuentaAhorros(Cuenta):
    """
    Hereda de Cuenta.
    - No permite sobregiros.
    - Gana intereses mensuales simples según tasa anual.
    """

    def __init__(self, numero: str, titular: Cliente, saldo_inicial: float = 0.0, tasa_anual: float = 0.05):
        super().__init__(numero, titular, saldo_inicial)
        if tasa_anual < 0:
            raise ValueError("La tasa anual no puede ser negativa.")
        self.tasa_anual = float(tasa_anual)

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El retiro debe ser mayor a 0.")
        if monto > self.saldo:
            raise ValueError("Fondos insuficientes en cuenta de ahorros.")
        self._debitar(monto)

    def calcular_interes(self) -> float:
        # Interés mensual simple: saldo * (tasa_anual / 12)
        interes = self.saldo * (self.tasa_anual / 12.0)
        return round(interes, 2)


class CuentaCorriente(Cuenta):
    """
    Hereda de Cuenta.
    - Permite sobregiro hasta un límite.
    - No genera intereses positivos (para simpleza).
      (Opcionalmente, se podría cobrar interés si el saldo es negativo.)
    """

    def __init__(
        self,
        numero: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        sobregiro_maximo: float = 200.0,
        costo_sobregiro: float = 1.0,
    ):
        super().__init__(numero, titular, saldo_inicial)
        if sobregiro_maximo < 0:
            raise ValueError("El sobregiro máximo no puede ser negativo.")
        if costo_sobregiro < 0:
            raise ValueError("El costo de sobregiro no puede ser negativo.")
        self.sobregiro_maximo = float(sobregiro_maximo)
        self.costo_sobregiro = float(costo_sobregiro)

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El retiro debe ser mayor a 0.")
        saldo_posterior = self.saldo - monto
        if saldo_posterior < -self.sobregiro_maximo:
            raise ValueError("Límite de sobregiro excedido en cuenta corriente.")
        self._debitar(monto)

        # Si quedó en negativo, cobra una pequeña comisión por sobregiro.
        if self.saldo < 0:
            self._debitar(self.costo_sobregiro)

    def calcular_interes(self) -> float:
        # Por simplicidad, no genera intereses positivos.
        return 0.0

