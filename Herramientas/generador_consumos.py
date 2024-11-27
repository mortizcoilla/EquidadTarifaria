import os
import pandas as pd
import numpy as np

# Rutas de entrada y salida
clientes_input = "datos/clientes/clientes_simulados.csv"
consumos_mensuales_dir = "datos/consumos_mensuales"
consumos_semanales_dir = "datos/consumos_semanales"

os.makedirs(consumos_mensuales_dir, exist_ok=True)
os.makedirs(consumos_semanales_dir, exist_ok=True)

# Cargar datos de clientes
print(f"Cargando datos de clientes desde: {clientes_input}")
df_clientes = pd.read_csv(clientes_input, sep=";")

# Generar consumos mensuales
print("Generando consumos mensuales...")
for comuna in df_clientes["comuna"].unique():
    df_comuna = df_clientes[df_clientes["comuna"] == comuna].copy()
    
    # Dividir consumo mensual en consumo diurno y nocturno
    df_comuna["consumo_diurno"] = df_comuna["consumo_mensual"] * 0.6  # 60% del consumo total
    df_comuna["consumo_nocturno"] = df_comuna["consumo_mensual"] * 0.4  # 40% del consumo total
    
    # Crear archivo mensual con columna 'eficiencia_energetica'
    output_file = os.path.join(consumos_mensuales_dir, f"{comuna}_consumos_mensuales.csv")
    df_comuna[[
        "comuna", "consumo_diurno", "consumo_nocturno", 
        "tipo_cliente", "socioeconomico", "evento_anomalo", "eficiencia_energetica"
    ]].to_csv(output_file, sep=";", index=False)
    print(f"Archivo mensual generado para {comuna}: {output_file}")

# Generar consumos semanales
print("Generando consumos semanales...")
for comuna in df_clientes["comuna"].unique():
    df_comuna = df_clientes[df_clientes["comuna"] == comuna].copy()
    
    # Calcular consumos semanales basados en consumo mensual
    df_comuna["consumo_diurno"] = df_comuna["consumo_mensual"] * 0.6
    df_comuna["consumo_nocturno"] = df_comuna["consumo_mensual"] * 0.4
    for semana in range(1, 5):
        df_comuna[f"semana_{semana}_diurno"] = (df_comuna["consumo_diurno"] / 4) + np.random.uniform(-10, 10, len(df_comuna))
        df_comuna[f"semana_{semana}_nocturno"] = (df_comuna["consumo_nocturno"] / 4) + np.random.uniform(-10, 10, len(df_comuna))
    
    # Crear archivo semanal
    output_file = os.path.join(consumos_semanales_dir, f"{comuna}_consumos_semanales.csv")
    columnas = ["comuna", "socioeconomico", "tipo_cliente", "evento_anomalo", "eficiencia_energetica"] + \
               [f"semana_{semana}_diurno" for semana in range(1, 5)] + \
               [f"semana_{semana}_nocturno" for semana in range(1, 5)]
    df_comuna[columnas].to_csv(output_file, sep=";", index=False)
    print(f"Archivo semanal generado para {comuna}: {output_file}")

print("¡Consumos mensuales y semanales generados con éxito!")
