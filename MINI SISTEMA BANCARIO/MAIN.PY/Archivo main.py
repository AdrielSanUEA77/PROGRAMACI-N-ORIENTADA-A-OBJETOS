
# -*- coding: utf-8 -*-
"""
Mini Sistema Bancario en un solo archivo (POO en Python)
Autor: Adriel Sánchez

Este script demuestra:
- HERENCIA: CuentaAhorros y CuentaCorriente heredan de Cuenta.
- ENCAPSULACIÓN: __saldo es privado en Cuenta; acceso controlado con properties y métodos.
- POLIMORFISMO: retirar() y calcular_interes() se implementan distinto en cada tipo de cuenta.
- SEPARACIÓN LÓGICA: Incluye una clase de "servicios" (BancoService) en el mismo archivo.
- DEMOSTRACIÓN: En main() se crean instancias, se operan y se muestran resultados.

Ejecución:
    python poo_banco_unico.py
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List


# =========================
#        MODELOS
# =========================
class Cliente:
    """
    Clase de dominio simple para representar a un titular/cliente.
    """
    def __init__(self, nombre: str, cedula: str):
        self.nombre = nombre
        self.cedula = cedula

    def __str__(self) -> str:
        return f"{self.nombre} (C.I.: {self.cedula})"


class Cuenta(ABC):
    """
    Clase base abstracta (Herencia + Polimorfismo).
    - Define interfaz común (retirar, calcular_interes) y comportamiento compartido (depositar, aplicar_interes).
    - ENCAPSULACIÓN: __saldo es privado; sólo se modifica a través de métodos controlados.
    """

    def __init__(self, numero: str, titular: Cliente, saldo_inicial: float = 0.0):
        self._numero = numero          # Atributo "protegido" por convención (un guion bajo).
        self._titular = titular
        self.__saldo = 0.0             # Atributo PRIVADO (name mangling: dos guiones bajos).

        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.__saldo = float(saldo_inicial)

    # ----- Encapsulación: propiedades solo lectura -----
    @property
    def saldo(self) -> float:
        """Saldo expuesto como solo lectura."""
        return self.__saldo

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def titular(self) -> Cliente:
        return self._titular

    # ----- Operaciones comunes -----
    def depositar(self, monto: float) -> None:
        """Acredita fondos de manera controlada."""
        if monto <= 0:
            raise ValueError("El depósito debe ser mayor a 0.")
        self.__saldo += float(monto)

    # Métodos 'protegidos' para modificar el saldo desde dentro de la clase/jerarquía
    def _debitar(self, monto: float) -> None:
        self.__saldo -= float(monto)

    def _acreditar(self, monto: float) -> None:
        self.__saldo += float(monto)

    # ----- Polimorfismo: implementación distinta según el tipo de cuenta -----
    @abstractmethod
    def retirar(self, monto: float) -> None:
        """Cada tipo de cuenta define sus reglas de retiro."""
        raise NotImplementedError

    @abstractmethod
    def calcular_interes(self) -> float:
        """Cada tipo de cuenta calcula el interés de forma distinta (o no aplica)."""
        raise NotImplementedError

    def aplicar_interes(self) -> float:
        """
        Método plantilla: calcula el interés de forma polimórfica y, si es positivo,
        lo acredita al saldo. Retorna el interés aplicado.
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
    - Permite sobregiro hasta un límite.
    - No genera intereses positivos (simplificado). Cobra una comisión al caer en negativo.
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

        # Si quedó en negativo, cobra comisión de sobregiro
        if self.saldo < 0:
            self._debitar(self.costo_sobregiro)

    def calcular_interes(self) -> float:
        # Por simplicidad, 0 (no gana intereses positivos)
        return 0.0


# =========================
#        SERVICIOS
# =========================
class BancoService:
    """
    Capa de servicios: orquesta operaciones sin mezclar lógica de negocio con los modelos.
    """
    def __init__(self) -> None:
        # Diccionario interno: numero -> Cuenta
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
        # Reutiliza reglas de cada cuenta (polimorfismo en retirar()) y depósito controlado
        origen.retirar(monto)
        destino.depositar(monto)

    def aplicar_intereses(self) -> Dict[str, float]:
        """
        Aplica intereses a todas las cuentas.
        Devuelve: { numero_cuenta: interes_aplicado }
        """
        resumen: Dict[str, float] = {}
        for numero, cuenta in self._cuentas.items():
            interes = cuenta.aplicar_interes()
            resumen[numero] = interes
        return resumen

    def listar_resumenes(self) -> List[str]:
        return [c.resumen() for c in self._cuentas.values()]


# =========================
#     DEMOSTRACIÓN MAIN
# =========================
def main() -> None:
    print("=== Mini Sistema Bancario (POO en Python) ===")
    print("Autor: Adriel Sánchez\n")

    # 1) Instancias de Cliente
    adriel = Cliente("Adriel Sánchez", "1234567890")
    ana = Cliente("Ana Pérez", "0987654321")

    # 2) Cuentas (Herencia + atributos)
    cta_adriel = CuentaAhorros("AHO-001", adriel, saldo_inicial=500.0, tasa_anual=0.06)
    cta_ana = CuentaCorriente("COR-001", ana, saldo_inicial=100.0, sobregiro_maximo=150.0)

    # 3) Servicio del banco (separación de responsabilidades)
    banco = BancoService()
    banco.registrar_cuenta(cta_adriel)
    banco.registrar_cuenta(cta_ana)

    print("-- Estado inicial --")
    for r in banco.listar_resumenes():
        print(r)

    # 4) Operaciones de ejemplo
    print("\n-- Depósito y retiro --")
    cta_adriel.depositar(250.0)
    print("Depósito de $250.00 en cuenta de ahorros de Adriel.")
    cta_ana.retirar(220.0)
    print("Retiro de $220.00 en cuenta corriente de Ana (si queda negativa, cobra comisión).")

    # 5) Transferencia
    print("\n-- Transferencia de $100.00 de Adriel a Ana --")
    banco.transferir("AHO-001", "COR-001", 100.0)

    # 6) Intereses (Polimorfismo)
    print("\n-- Aplicar intereses (polimorfismo) --")
    intereses = banco.aplicar_intereses()
    for numero, interes in intereses.items():
        print(f"Interés aplicado a {numero}: ${interes:,.2f}")

    print("\n-- Estado final --")
    for r in banco.listar_resumenes():
        print(r)


# -------------------------
#   OPCIONAL: MENÚ CLI
# -------------------------
# Si prefieres jugar con un menú por consola, descomenta la llamada a run_menu()
# y comenta la llamada a main() en el bloque if __name__ == "__main__".
def run_menu() -> None:
    """
    Menú simple de consola (opcional), para interactuar con el sistema.
    """
    banco = BancoService()
    clientes: Dict[str, Cliente] = {}

    def crear_cliente() -> None:
        nombre = input("Nombre del cliente: ").strip()
        cedula = input("Cédula: ").strip()
        if cedula in clientes:
            print("Ya existe un cliente con esa cédula.")
            return
        clientes[cedula] = Cliente(nombre, cedula)
        print("Cliente creado.")

    def crear_cuenta() -> None:
        if not clientes:
            print("Primero crea un cliente.")
            return
        cedula = input("Cédula del titular: ").strip()
        titular = clientes.get(cedula)
        if not titular:
            print("No existe un cliente con esa cédula.")
            return
        numero = input("Número de cuenta: ").strip()
        tipo = input("Tipo (A=ahorros / C=corriente): ").strip().upper()
        saldo_ini = float(input("Saldo inicial: ").strip() or "0")
        if tipo == "A":
            tasa = float(input("Tasa anual (ej. 0.05): ").strip() or "0.05")
            cuenta = CuentaAhorros(numero, titular, saldo_ini, tasa)
        elif tipo == "C":
            sobregiro = float(input("Sobregiro máx (ej. 200): ").strip() or "200")
            costo = float(input("Costo sobregiro (ej. 1): ").strip() or "1")
            cuenta = CuentaCorriente(numero, titular, saldo_ini, sobregiro, costo)
        else:
            print("Tipo inválido.")
            return
        banco.registrar_cuenta(cuenta)
        print("Cuenta creada.")

    def depositar() -> None:
        num = input("Cuenta destino: ").strip()
        monto = float(input("Monto a depositar: ").strip())
        banco.obtener_cuenta(num).depositar(monto)
        print("Depósito realizado.")

    def retirar() -> None:
        num = input("Cuenta origen: ").strip()
        monto = float(input("Monto a retirar: ").strip())
        banco.obtener_cuenta(num).retirar(monto)
        print("Retiro realizado.")

    def transferir() -> None:
        o = input("Cuenta origen: ").strip()
        d = input("Cuenta destino: ").strip()
        m = float(input("Monto: ").strip())
        banco.transferir(o, d, m)
        print("Transferencia realizada.")

    def aplicar_intereses() -> None:
        res = banco.aplicar_intereses()
        for n, i in res.items():
            print(f"{n} -> interés aplicado: ${i:,.2f}")

    acciones = {
        "1": crear_cliente,
        "2": crear_cuenta,
        "3": depositar,
        "4": retirar,
        "5": transferir,
        "6": aplicar_intereses,
        "7": lambda: print("\n".join(banco.listar_resumenes()) or "Sin cuentas."),
    }

    while True:
        print("\n=== Menú Banco (POO) ===")
        print("1) Crear cliente")
        print("2) Crear cuenta")
        print("3) Depositar")
        print("4) Retirar")
        print("5) Transferir")
        print("6) Aplicar intereses")
        print("7) Listar cuentas")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta pronto.")
            break
        try:
            accion = acciones.get(op)
            if accion:
                accion()
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Por defecto corre la DEMO automática:
    main()


