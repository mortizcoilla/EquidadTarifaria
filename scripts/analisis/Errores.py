import pandas as pd
import numpy as np

# Configuración
input_file = "resultados/beneficios_aportes.csv"
output_file = "resultados/errores_inclusion_exclusion.csv"

# Leer datos
print(f"Cargando datos desde {input_file}...")
data = pd.read_csv(input_file, sep=";")

# Validar columnas esperadas
if "consumo_diurno" not in data.columns or "consumo_nocturno" not in data.columns:
    raise ValueError("Las columnas 'consumo_diurno' y 'consumo_nocturno' son obligatorias.")

# Calcular el consumo total
data["consumo_total"] = data["consumo_diurno"] + data["consumo_nocturno"]

# Calcular percentiles para determinar umbrales dinámicos
umbral_inferior = data["consumo_total"].quantile(0.25)  # Clientes con consumo menor al 25%
umbral_superior = data["consumo_total"].quantile(0.75)  # Clientes con consumo mayor al 75%

# Definir errores con umbrales dinámicos
data["error_inclusion"] = (data["beneficiario"] == False) & (data["consumo_total"] < umbral_inferior)
# Recalcular errores con umbrales ajustados
data["error_exclusion"] = (data["beneficiario"] == True) & (data["consumo_total"] >= umbral_superior * 0.85)


# Asignar estación si no existe
if "estacion" not in data.columns:
    print("Advertencia: Columna 'estacion' no encontrada. Asignando valores simulados.")
    data["mes"] = np.random.randint(1, 13, size=len(data))
    data["estacion"] = data["mes"].map({
        12: "verano", 1: "verano", 2: "verano",
        3: "otoño", 4: "otoño", 5: "otoño",
        6: "invierno", 7: "invierno", 8: "invierno",
        9: "primavera", 10: "primavera", 11: "primavera"
    })

# Guardar resultados
print(f"Guardando errores en {output_file}...")
data.to_csv(output_file, sep=";", index=False)
print("Errores calculados y guardados exitosamente.")
