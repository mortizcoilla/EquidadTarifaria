import os
import pandas as pd

# Configuración de rutas
directorio_archivo = os.getcwd()
clients_path = os.path.join(directorio_archivo, "datos", "clientes", "clientes_simulados.csv")
output_dir = os.path.join(directorio_archivo, "datos", "consumos_mensuales")
os.makedirs(output_dir, exist_ok=True)

# Leer datos de clientes
print(f"Leyendo datos desde: {clients_path}")
clients = pd.read_csv(clients_path, sep=";")

# Convertir coordenadas a strings y eliminar puntos
clients["coord_x"] = clients["coord_x"].astype(str).str.replace(".", "", regex=False)
clients["coord_y"] = clients["coord_y"].astype(str).str.replace(".", "", regex=False)

# Calcular el consumo mensual promedio (simulado aquí como ejemplo)
num_registros = len(clients)
clients["consumo_mensual"] = [round(150 + i % 50, 2) for i in range(num_registros)]

# Clasificar tipo de consumo
clients["Tipo_consumo"] = clients["clave_tarifa"].apply(lambda x: "RESIDENCIAL" if x == "RESIDENCIAL" else "NO_RESIDENCIAL")

# Guardar resultados por comuna
for comuna in clients["comuna"].unique():
    comuna_data = clients[clients["comuna"] == comuna]
    output_path = os.path.join(output_dir, f"{comuna}_consumos_mensuales.csv")
    comuna_data.to_csv(output_path, sep=";", index=False)
    print(f"Archivo generado para {comuna}: {output_path}")

print("\nProceso completado: ConsumoMensual.py")
