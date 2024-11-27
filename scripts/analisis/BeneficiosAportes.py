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
    print(f"Procesando datos para {comuna}...")
    
    try:
        data = pd.read_csv(os.path.join(input_dir, file), sep=";")
        
        # Validar columnas requeridas
        required_columns = ["consumo_diurno", "consumo_nocturno", "eficiencia_energetica"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"El archivo {file} no contiene las columnas requeridas: {missing_columns}")
        
        # Calcular consumo total
        data["consumo_total"] = data["consumo_diurno"] + data["consumo_nocturno"]

        # Clasificación de beneficiarios y aportantes
        data["beneficiario"] = data["consumo_total"] < promedio_nacional
        data["aporte"] = data["consumo_total"] > promedio_nacional

        # Cálculo de beneficios y aportes
        data["ajuste_tarifario"] = 0
        data.loc[data["beneficiario"], "ajuste_tarifario"] = (
            -data["consumo_total"] * beneficio_porcentaje / 100
        )
        data.loc[data["aporte"], "ajuste_tarifario"] = (
            data["consumo_total"] * aporte_porcentaje / 100
        )

        # Agregar comuna y guardar resultados
        data["comuna"] = comuna
        resultados.append(data)
    
    except Exception as e:
        print(f"ERROR: {e}. Saltando archivo {file}.")
        continue

# Consolidar y guardar
if resultados:
    resultados_df = pd.concat(resultados, ignore_index=True)
    resultados_df.to_csv(output_file, sep=";", index=False)
    print(f"Archivo generado: {output_file}")
else:
    print("No se generaron resultados debido a errores en los archivos de entrada.")
