
"""
Promedio semanal del clima (POO, versión simple)
- Clase DiaClima: representa la temperatura de un día (encapsulamiento con propiedades).
- Clase SemanaClima: contiene 7 DiaClima, pide datos y calcula el promedio (requiere todos los días).
- Subclase SemanaClimaFlexible: herencia + polimorfismo; su promedio ignora días sin dato.

Cómo ejecutar:
    python clima_poo_simple.py
"""

# Adriel Sanchez clima POO
# Clase que representa un día
# ----------------------------
class DiaClima:
    def __init__(self, nombre_dia: str, temperatura: float | None = None):
        self._nombre_dia = nombre_dia       # atributo "privado" por convención
        self._temperatura = None
        if temperatura is not None:
            self.temperatura = temperatura   # usa el setter para validar

    @property
    def nombre_dia(self) -> str:
        """Nombre del día (solo lectura)."""
        return self._nombre_dia

    @property
    def temperatura(self) -> float | None:
        """Temperatura del día (°C). Puede ser None si no hay dato."""
        return self._temperatura

    @temperatura.setter
    def temperatura(self, valor: float) -> None:
        """Valida y asigna la temperatura (encapsulamiento)."""
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise TypeError("La temperatura debe ser numérica.")
        # Rango razonable, puedes ajustarlo si deseas
        if -80.0 <= valor <= 60.0:
            self._temperatura = valor
        else:
            raise ValueError("Temperatura fuera de rango (-80 a 60 °C).")

    def pedir_al_usuario(self) -> None:
        """Solicita la temperatura por consola para este día."""
        while True:
            entrada = input(f"Ingrese la temperatura (°C) para {self.nombre_dia}: ").strip()
            entrada = entrada.replace(",", ".")  # permitir 23,5
            try:
                self.temperatura = entrada
                break
            except (TypeError, ValueError) as e:
                print(f"⚠️  {e}. Intente nuevamente.")

    def __str__(self) -> str:
        temp = f"{self.temperatura:.2f} °C" if self.temperatura is not None else "sin dato"
        return f"{self.nombre_dia}: {temp}"


# ------------------------------------
# Clase base para la semana de clima
# ------------------------------------
class SemanaClima:
    DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def __init__(self):
        # Composición: SemanaClima "contiene" 7 DiaClima
        self._dias = [DiaClima(nombre) for nombre in self.DIAS]

    @property
    def dias(self):
        """Lista de objetos DiaClima (solo lectura)."""
        return self._dias

    def ingresar_temperaturas(self) -> None:
        """Pide temperatura para cada día."""
        print("\n=== Registro de temperaturas (POO) ===")
        for dia in self._dias:
            dia.pedir_al_usuario()

    def promedio(self) -> float:
        """
        Calcula el promedio semanal.
        En la clase base, exige que TODOS los días tengan dato (política estricta).
        """
        if any(d.temperatura is None for d in self._dias):
            raise RuntimeError("Faltan temperaturas. Complete todos los días.")
        return sum(d.temperatura for d in self._dias) / len(self._dias)

    def resumen(self) -> str:
        """Resumen de la semana con el promedio (si está disponible)."""
        lineas = [str(d) for d in self._dias]
        try:
            prom = self.promedio()
            lineas.append(f" Promedio semanal: {prom:.2f} °C")
        except RuntimeError as e:
            lineas.append(f"⚠ {e}")
        return "\n".join(lineas)


# --------------------------------------------------
# Subclase que demuestra herencia y polimorfismo
# --------------------------------------------------
class SemanaClimaFlexible(SemanaClima):
    def promedio(self) -> float:
        """
        Polimorfismo: redefine el cálculo de promedio para
        ignorar los días sin dato en lugar de exigirlos.
        """
        temps = [d.temperatura for d in self._dias if d.temperatura is not None]
        if not temps:
            raise RuntimeError("No hay temperaturas para calcular el promedio.")
        return sum(temps) / len(temps)


# ---------------------
# Punto de entrada
# ---------------------
def main():
    print("==================================")
    print(" Promedio semanal del clima (POO) ")
    print("==================================")
    # Usa la versión base (estricta)
    semana = SemanaClima()
    semana.ingresar_temperaturas()
    print("\n=== Resumen (estricto) ===")
    print(semana.resumen())

    # Demostración rápida de la versión flexible (herencia + polimorfismo)
    print("\n=== Resumen (flexible, ignora faltantes) ===")
    semana_flexible = SemanaClimaFlexible()
    # Para mostrar el polimorfismo, no pedimos todos los días:
    semana_flexible.dias[0].temperatura = 22.0  # Lunes
    semana_flexible.dias[1].temperatura = 24.5  # Martes
    # El resto quedan sin dato (None)
    print(semana_flexible.resumen())

if __name__ == "__main__":
    main()

