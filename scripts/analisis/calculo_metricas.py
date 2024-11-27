import pandas as pd

# Configuración
beneficios_file = "resultados/beneficios_aportes.csv"
errores_file = "resultados/errores_inclusion_exclusion.csv"
output_comuna_eficiencia = "resultados/resumen_beneficios_aportes_por_comuna_eficiencia.csv"
output_errores_comuna = "resultados/resumen_errores_por_comuna_estacion.csv"

# Leer datos de beneficios y errores
print(f"Cargando datos de beneficios desde {beneficios_file}...")
beneficios_data = pd.read_csv(beneficios_file, sep=";")
print(f"Cargando datos de errores desde {errores_file}...")
errores_data = pd.read_csv(errores_file, sep=";")

# Manejo de columna 'estacion'
if "estacion" not in errores_data.columns:
    print("Advertencia: 'estacion' no encontrada. Asignando 'desconocido'.")
    errores_data["estacion"] = "desconocido"

# Resumen de beneficios y aportes por comuna y eficiencia energética
print("Calculando beneficios y aportes por comuna y eficiencia energética...")
beneficios_por_comuna_eficiencia = beneficios_data.groupby(["comuna", "eficiencia_energetica"])[["ajuste_tarifario"]].sum()

# Guardar resultados de beneficios por comuna
beneficios_por_comuna_eficiencia.to_csv(output_comuna_eficiencia, sep=";")
print(f"Resumen guardado en {output_comuna_eficiencia}.")

# Resumen de errores por comuna y estación
print("Calculando errores por comuna y estación...")
errores_por_comuna = errores_data.groupby(["comuna", "estacion"])[["error_inclusion", "error_exclusion"]].sum()

# Guardar resultados de errores por comuna
errores_por_comuna.to_csv(output_errores_comuna, sep=";")
print(f"Resumen guardado en {output_errores_comuna}.")
