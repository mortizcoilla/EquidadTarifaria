import pandas as pd

# Configuración
input_file = "resultados/beneficios_aportes.csv"
output_file = "resultados/errores_inclusion_exclusion.csv"

# Leer datos
data = pd.read_csv(input_file, sep=";")

# Clasificación de errores (ejemplo basado en columnas disponibles)
data["error_inclusion"] = (data["beneficiario"] == False) & (data["consumo_mensual"] < 150)
data["error_exclusion"] = (data["beneficiario"] == True) & (data["consumo_mensual"] >= 150)

# Resumen de resultados
errores_resumen = {
    "errores_inclusion": data["error_inclusion"].sum(),
    "errores_exclusion": data["error_exclusion"].sum(),
    "total_hogares": len(data),
}

print("Errores calculados:", errores_resumen)

# Guardar resultados
data.to_csv(output_file, sep=";", index=False)
print(f"Errores guardados en: {output_file}")
