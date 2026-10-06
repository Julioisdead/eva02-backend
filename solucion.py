"""
Fase 1 y 2 - Reserva de horas en una barberia
decidir() contiene la regla de decision, para que Django la pueda
importar sin volver a escribirla. El resto (pedir datos, guardar en
JSON, mostrar tabla) solo corre si el archivo se ejecuta directo.
"""

import json
import os
from tabulate import tabulate

HORA_APERTURA = 9
HORA_CIERRE = 19
ARCHIVO_DATOS = "datos.json"


def decidir(hora_solicitada, cupos_disponibles):
    """Aplica la regla de decision y devuelve (estado, motivo).

    El dato invalido se revisa primero, si no nunca se alcanza a revisar.
    """
    if cupos_disponibles < 0 or hora_solicitada < 0 or hora_solicitada > 23:
        return "Rechazado", "Dato invalido: cupos negativos u hora fuera de rango"
    elif hora_solicitada < HORA_APERTURA or hora_solicitada >= HORA_CIERRE:
        return "Rechazado", "Fuera de horario: el local atiende de 9 a 19 hrs"
    elif cupos_disponibles == 0:
        return "Rechazado", "Sin cupos disponibles en ese bloque"
    else:
        return "Aceptado", "Hora dentro de horario y con cupos disponibles"


def guardar_registro(nombre, hora_solicitada, estado, motivo):
    """Agrega un registro a datos.json, conservando los anteriores."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS) as f:
            registros = json.load(f)
    else:
        registros = []

    registros.append({
        "nombre": nombre,
        "hora_solicitada": hora_solicitada,
        "estado": estado,
        "motivo": motivo,
    })

    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(registros, f, indent=2)

    return registros


if __name__ == "__main__":
    # Paso 1 y 2: pedir los datos de entrada (input() siempre entrega texto)
    nombre = input("Nombre del cliente: ")
    hora_solicitada = int(input("Hora solicitada (0-23): "))
    cupos_disponibles = int(input("Cupos disponibles en ese bloque: "))

    # Paso 3: regla de decision (definida arriba en decidir())
    estado, motivo = decidir(hora_solicitada, cupos_disponibles)

    # Paso 4: mostrar el resultado con el motivo
    print(f"\n{nombre}: {estado}")
    print(f"Motivo: {motivo}")

    # Guardar el registro y mostrar el resumen acumulado en tabla
    registros = guardar_registro(nombre, hora_solicitada, estado, motivo)
    print("\nResumen de solicitudes:")
    print(tabulate(registros, headers="keys"))
