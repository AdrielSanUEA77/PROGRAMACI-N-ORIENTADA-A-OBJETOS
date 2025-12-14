
"""
Promedio semanal del clima (Programación Tradicional)
Descripción:
  - Pide temperaturas diarias de una semana.
  - Calcula y muestra el promedio semanal.
  - Enfoque funcional: funciones simples y claras.
"""
# Temperatura Adriel Sánchez
# Lista de días para mostrar mensajes amigables
DIAS_SEMANA = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo"
]

def leer_temperatura(dia):
    """
    Pide al usuario la temperatura de un día.
    Acepta coma o punto decimal. Valida que sea número.
    """
    while True:
        entrada = input(f"Ingrese la temperatura (°C) para {dia}: ").strip()
        entrada = entrada.replace(",", ".")  # Permitir 23,5
        try:
            return float(entrada)
        except ValueError:
            print(" Entrada inválida. Por favor, ingrese un número (ej. 22.5).")

def solicitar_temperaturas():
    """
    Recorre los días de la semana y guarda las temperaturas en una lista.
    """
    print("\n=== Registro de temperaturas de la semana ===")
    temperaturas = []
    for dia in DIAS_SEMANA:
        temp = leer_temperatura(dia)
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """
    Calcula el promedio de una lista de temperaturas.
    """
    return sum(temperaturas) / len(temperaturas)

def mostrar_resumen(temperaturas):
    """
    Muestra las temperaturas por día y el promedio semanal.
    """
    print("\n=== Resumen de la semana ===")
    for dia, temp in zip(DIAS_SEMANA, temperaturas):
        print(f"{dia}: {temp:.2f} °C")
    promedio = calcular_promedio(temperaturas)
    print(f"\n Promedio semanal: {promedio:.2f} °C")

def main():
    print("========================================")
    print(" Promedio semanal del clima (Tradicional)")
    print("========================================")
    temperaturas = solicitar_temperaturas()
    mostrar_resumen(temperaturas)

if __name__ == "__main__":
    main()
