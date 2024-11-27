import pandas as pd

# Rutas de los archivos
errores_file = "resultados/errores_inclusion_exclusion.csv"
beneficios_file = "resultados/beneficios_aportes.csv"

# Leer datos
errores_data = pd.read_csv(errores_file, sep=";")
beneficios_data = pd.read_csv(beneficios_file, sep=";")

# 1. Resumen de errores
inclusion_errors = errores_data["error_inclusion"].sum()
exclusion_errors = errores_data["error_exclusion"].sum()
total_errors = inclusion_errors + exclusion_errors

print("Resumen de Errores:")
print(f"Errores de Inclusión: {inclusion_errors}")
print(f"Errores de Exclusión: {exclusion_errors}")
print(f"Errores Totales: {total_errors}")

# 2. Errores por comuna
errores_por_comuna = errores_data.groupby("comuna")[["error_inclusion", "error_exclusion"]].sum()
print("\nErrores por Comuna:")
print(errores_por_comuna)

# Guardar el resumen por comuna (opcional)
errores_por_comuna.to_csv("resultados/resumen_errores_por_comuna.csv", sep=";")

# 3. Beneficios y aportes por comuna
beneficios_por_comuna = beneficios_data.groupby("comuna")["ajuste_tarifario"].sum()
print("\nBeneficios y Aportes por Comuna:")
print(beneficios_por_comuna)

# Guardar el resumen de beneficios/aportes por comuna (opcional)
beneficios_por_comuna.to_csv("resultados/resumen_beneficios_aportes_por_comuna.csv", sep=";")
