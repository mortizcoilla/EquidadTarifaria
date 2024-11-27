import pandas as pd
import os

# Configuración
input_dir = "datos/consumos_mensuales"
output_file = "resultados/beneficios_aportes.csv"
os.makedirs("resultados", exist_ok=True)

# Umbrales y parámetros
promedio_nacional = 150  # kWh/mes
beneficio_porcentaje = 15  # Descuento para beneficiarios
aporte_porcentaje = 5      # Incremento para aportantes

# Leer datos
files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
resultados = []

for file in files:
    comuna = file.split("_")[0]
    data = pd.read_csv(os.path.join(input_dir, file), sep=";")
    
    # Clasificación de beneficiarios y aportantes
    data["beneficiario"] = data["consumo_mensual"] < promedio_nacional
    data["aporte"] = data["consumo_mensual"] > promedio_nacional
    
    # Cálculo de beneficios y aportes
    data["ajuste_tarifario"] = 0
    data.loc[data["beneficiario"], "ajuste_tarifario"] = (
        -data["consumo_mensual"] * beneficio_porcentaje / 100
    )
    data.loc[data["aporte"], "ajuste_tarifario"] = (
        data["consumo_mensual"] * aporte_porcentaje / 100
    )
    
    # Agregar resultados
    data["comuna"] = comuna
    resultados.append(data)

# Consolidar y guardar
resultados_df = pd.concat(resultados, ignore_index=True)
resultados_df.to_csv(output_file, sep=";", index=False)
print(f"Resultados guardados en {output_file}")
