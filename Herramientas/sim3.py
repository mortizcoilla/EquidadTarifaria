import os
import pandas as pd
import random

input_file = "datos/clientes/clientes_simulados.csv"
output_dir = "datos/consumos_semanales"
os.makedirs(output_dir, exist_ok=True)

# Leer clientes
clientes = pd.read_csv(input_file, sep=";")

# Generar consumos semanales
for comuna in clientes["comuna"].unique():
    df_comuna = clientes[clientes["comuna"] == comuna]
    for semana in range(1, 5):
        df_comuna[f"semana_{semana}"] = [random.randint(30, 100) for _ in range(len(df_comuna))]
    output_file = os.path.join(output_dir, f"{comuna}_consumos_semanales.csv")
    df_comuna.to_csv(output_file, sep=";", index=False)
    print(f"Archivo generado para {comuna}: {output_file}")
