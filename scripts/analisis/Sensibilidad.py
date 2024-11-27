import rarfile
import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

# Configuración para UnRAR
rarfile.UNRAR_TOOL = r"C:\Users\cbustamante\Downloads\Trabajo de título\UnRAR.exe"

# Leer el shapefile con datos geoespaciales
mapa = gpd.read_file("CSE_SANTIAGO_UV_RSH_FINAL.shp")

# Variables iniciales
comuna = "HUECHURABA"
directorio_archivo = r"C:\Users\cbustamante\Downloads\Trabajo de título"
directory = os.path.join(directorio_archivo, "Tabla_consumos_clientes_mensual")
database_average_path = os.path.join(directory, f"{comuna}_CONSUMOS_MENSUAL.csv")

# Leer los datos de consumo mensual
database_average = pd.read_csv(database_average_path, sep=";").fillna(0)

# Cálculo de totales
database_average["total semana"] = database_average["counting weekday"] * database_average["value weekday"]
database_average["total fin de semana"] = database_average["counting weekend"] * database_average["value weekend"]
database_average["semana completa"] = database_average["total semana"] + database_average["total fin de semana"]
database_average["horas total"] = database_average["counting weekday"] + database_average["counting weekend"]

# Agrupación mensual
database_average_agrupado = database_average.groupby(
    ["nro_medidor", "comuna", "Month", "Tipo_consumo", "coord_y", "coord_x"]
).agg(
    {"total semana": "sum", "total fin de semana": "sum", "semana completa": "sum", "horas total": "sum"}
).reset_index()

# Cálculo del promedio mensual
database_average_agrupado["Promedio mensual"] = (
    database_average_agrupado["semana completa"] / database_average_agrupado["horas total"]
)

# Limpieza de columnas
database_average_agrupado = database_average_agrupado.drop(
    ["total semana", "total fin de semana", "semana completa", "horas total"], axis=1
)

# Agrupación anual
database_average_agrupado = database_average_agrupado.groupby(
    ["nro_medidor", "comuna", "coord_y", "coord_x"]
).agg({"Promedio mensual": "sum"}).reset_index()

database_average_agrupado["Promedio mensual anual"] = database_average_agrupado["Promedio mensual"] / 12

print("Número total de clientes:", len(set(database_average_agrupado["nro_medidor"])))

# Leer datos de consumo semanal
directory_2 = os.path.join(directorio_archivo, "Tabla_promedio_semanal")
consumo_semanal_path = os.path.join(directory_2, f"{comuna}_semanal.csv")
Consumo_semanal = pd.read_csv(consumo_semanal_path, sep=";")

print("Número de clientes en datos semanales:", len(set(Consumo_semanal["nro_medidor"])))

# Unir datos
results = database_average_agrupado.merge(Consumo_semanal, how="left", on="nro_medidor")
resultsNuevo = results[["nro_medidor", "Tipo_consumo"]].drop_duplicates()

# Filtrar consumidores residenciales
database_promedio_final_1 = database_average_agrupado.merge(resultsNuevo, how="left", on="nro_medidor")
database_promedio_final_1 = database_promedio_final_1[database_promedio_final_1["Tipo_consumo"] == "RESIDENCIAL"]
agrupado = database_promedio_final_1

print(f"Número de clientes residenciales en {comuna}:", len(set(agrupado["nro_medidor"])))

# Asignar unidad vecinal según ubicación geográfica
clientes = agrupado["nro_medidor"].unique()
poligonos = range(len(mapa))
df = pd.DataFrame(columns=[
    "nro_medidor", "comuna", "consumo_promedio", "coord_y", "coord_x",
    "I_unidad_v", "I_tramo_1", "I_tramo_2", "I_tramo_3", "I_tramo_4",
    "I_tramo_5", "I_tramo_6", "I_tramo_7", "I_total_uv"
])

for cliente in clientes:
    cliente_data = agrupado[agrupado["nro_medidor"] == cliente]
    y, x = cliente_data.iloc[0][["coord_y", "coord_x"]]

    for i in poligonos:
        punto = Point(x, y)
        if punto.within(mapa.iloc[i].geometry):
            fila = {
                "nro_medidor": cliente,
                "comuna": comuna,
                "consumo_promedio": cliente_data.iloc[0]["Promedio mensual anual"],
                "coord_y": y,
                "coord_x": x,
                "I_unidad_v": mapa.iloc[i]["I_unidad_v"],
                "I_tramo_1": mapa.iloc[i]["I_tramo_1"],
                "I_tramo_2": mapa.iloc[i]["I_tramo_2"],
                "I_tramo_3": mapa.iloc[i]["I_tramo_3"],
                "I_tramo_4": mapa.iloc[i]["I_tramo_4"],
                "I_tramo_5": mapa.iloc[i]["I_tramo_5"],
                "I_tramo_6": mapa.iloc[i]["I_tramo_6"],
                "I_tramo_7": mapa.iloc[i]["I_tramo_7"],
                "I_total_uv": mapa.iloc[i]["I_total_uv"]
            }
            df = df.append(fila, ignore_index=True)
            break

# Clasificación socioeconómica y ajuste por tramos
df["I_total_uv_dif"] = (((df["I_total_uv"] * 100) / 76.3) - df["I_total_uv"]) / 3
for tramo in ["I_tramo_5", "I_tramo_6", "I_tramo_7"]:
    df[tramo] += df["I_total_uv_dif"]

df["I_total_uv_superior"] = df["I_total_uv"] + (df["I_total_uv_dif"] * 3)

# Exportar resultados
df_output_path = os.path.join(directorio_archivo, f"{comuna}_resultados.csv")
df.to_csv(df_output_path, sep=";", index=False)

print("Resultados exportados a:", df_output_path)
print("Clientes procesados:", len(df))
