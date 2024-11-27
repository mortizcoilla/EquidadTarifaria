import os
import pandas as pd
import random

input_file = "datos/clientes/clientes_simulados.csv"
output_dir = "datos/consumos_mensuales"
os.makedirs(output_dir, exist_ok=True)

# Leer clientes
clientes = pd.read_csv(input_file, sep=";")

# Generar consumos mensuales por comuna
for comuna in clientes["comuna"].unique():
    df_comuna = clientes[clientes["comuna"] == comuna]
    df_comuna["consumo_mensual"] = [random.randint(150, 400) for _ in range(len(df_comuna))]
    output_file = os.path.join(output_dir, f"{comuna}_consumos_mensuales.csv")
    df_comuna.to_csv(output_file, sep=";", index=False)
    print(f"Archivo generado para {comuna}: {output_file}")
