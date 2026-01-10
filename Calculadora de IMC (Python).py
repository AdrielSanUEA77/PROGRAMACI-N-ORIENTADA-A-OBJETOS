
"""
Calculadora de IMC (Índice de Masa Corporal)

Este programa solicita datos básicos de una persona (nombre, edad, peso y altura),
calcula el IMC, determina su categoría (bajo peso, normal, sobrepeso u obesidad),
e informa si la persona es mayor de edad. Demuestra el uso de distintos tipos de datos:
- string: nombre
- int: edad
- float: peso y altura
- boolean: es_adulto

Convenciones:
- Identificadores en snake_case
- Funciones con nombres descriptivos
- Comentarios explicativos
"""

def calcular_imc(peso_kg: float, altura_m: float) -> float:
    """
    Calcula el IMC usando la fórmula: IMC = peso (kg) / (altura (m))^2
    Retorna el valor como float.
    """
    if altura_m <= 0:
        raise ValueError("La altura debe ser mayor que cero.")
    return peso_kg / (altura_m ** 2)


def clasificar_imc(valor_imc: float) -> str:
    """
    Clasifica el IMC según rangos comunes.
    Fuente de rangos de referencia (simplificados):
    - Bajo peso: IMC < 18.5
    - Normal: 18.5 ≤ IMC < 25
    - Sobrepeso: 25 ≤ IMC < 30
    - Obesidad: IMC ≥ 30
    """
    if valor_imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= valor_imc < 25:
        return "Normal"
    elif 25 <= valor_imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"


def es_mayor_de_edad(edad: int) -> bool:
    """
    Determina si la persona es mayor de edad (>= 18).
    Retorna un booleano.
    """
    return edad >= 18


def formatear_resultado(nombre: str, edad: int, peso_kg: float, altura_m: float, imc: float, categoria: str, mayor_de_edad: bool) -> str:
    """
    Devuelve un string con el reporte final formateado.
    """
    estado_mayoria = "Sí" if mayor_de_edad else "No"
    return (
        f"\n--- Reporte de IMC ---\n"
        f"Nombre           : {nombre}\n"
        f"Edad             : {edad} años (Mayor de edad: {estado_mayoria})\n"
        f"Peso             : {peso_kg:.2f} kg\n"
        f"Altura           : {altura_m:.2f} m\n"
        f"IMC              : {imc:.2f}\n"
        f"Clasificación    : {categoria}\n"
    )


def solicitar_float(mensaje: str) -> float:
    """
    Lee un número float desde consola con manejo simple de errores.
    """
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número (usa punto decimal).")


def solicitar_int(mensaje: str) -> int:
    """
    Lee un número entero desde consola con manejo simple de errores.
    """
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")


def main():
    """
    Punto de entrada del programa.
    Orquesta la obtención de datos, cálculo de IMC y la presentación del reporte.
    """
    print("=== Calculadora de IMC ===")
    nombre = input("Ingresa tu nombre: ").strip()  # string
    edad = solicitar_int("Ingresa tu edad (años): ")  # int
    peso_kg = solicitar_float("Ingresa tu peso (kg): ")  # float
    altura_m = solicitar_float("Ingresa tu altura (m): ")  # float

    try:
        imc = calcular_imc(peso_kg, altura_m)  # float
    except ValueError as err:
        print(f"Error en los datos: {err}")
        return

    categoria = clasificar_imc(imc)  # string
    mayor_de_edad = es_mayor_de_edad(edad)  # boolean

    reporte = formatear_resultado(nombre, edad, peso_kg, altura_m, imc, categoria, mayor_de_edad)
    print(reporte)


# Convención: ejecutar main() solo si el archivo se corre directamente
if __name__ == "__main__":
    main()
