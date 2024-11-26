import rarfile
import pandas as pd
import os
import time
from shapely.geometry import Point
import geopandas as gpd
import numpy as np

# Configuración de la herramienta UNRAR
rarfile.UNRAR_TOOL = r"C:\Users\cbustamante\Downloads\Trabajo de título\UnRAR.exe"

# Leer archivo shapefile con información geoespacial
mapa = gpd.read_file("CSE_SANTIAGO_UV_RSH_FINAL.shp")  # Modifica la ruta si es necesario

# Configuración inicial
comuna = "CONCHALÍ"
directorio_archivo = r"C:\Users\cbustamante\Downloads\Trabajo de título"
directory = os.path.join(directorio_archivo, "Tabla_consumos_clientes_mensual")

# Leer base de datos de promedio mensual
database_average_path = os.path.join(directory, f"{comuna}_CONSUMOS_MENSUAL.csv")
database_average = pd.read_csv(database_average_path, sep=";")
database_average = database_average.fillna(0)

# Calcular totales y promedios
database_average["total semana"] = (
    database_average["counting weekday"] * database_average["value weekday"]
)
database_average["total fin de semana"] = (
    database_average["counting weekend"] * database_average["value weekend"]
)
database_average["semana completa"] = (
    database_average["total semana"] + database_average["total fin de semana"]
)
database_average["horas total"] = (
    database_average["counting weekday"] + database_average["counting weekend"]
)

# Agrupar por medidor y calcular promedio mensual anual
database_average_agrupado = database_average.groupby(
    ["nro_medidor", "comuna", "Month", "Tipo_consumo", "coord_y", "coord_x"]
).agg(
    {
        "total semana": "sum",
        "total fin de semana": "sum",
        "semana completa": "sum",
        "horas total": "sum",
    }
).reset_index()

database_average_agrupado["Promedio mensual"] = (
    database_average_agrupado["semana completa"]
    / database_average_agrupado["horas total"]
)
database_average_agrupado = database_average_agrupado.drop(
    ["total semana", "total fin de semana", "semana completa", "horas total"], axis=1
)

database_average_agrupado = database_average_agrupado.groupby(
    ["nro_medidor", "comuna", "coord_y", "coord_x"]
).agg({"Promedio mensual": "sum"}).reset_index()

database_average_agrupado["Promedio mensual anual"] = (
    database_average_agrupado["Promedio mensual"] / 12
)

print("Number of clients:", len(set(database_average_agrupado["nro_medidor"])))

# Leer consumo semanal y mergear con resultados
directory_2 = os.path.join(directorio_archivo, "Tabla_promedio_semanal")
Consumo_semanal_path = os.path.join(directory_2, f"{comuna}_semanal.csv")
Consumo_semanal = pd.read_csv(Consumo_semanal_path, sep=";")
print("Number of clients:", len(set(Consumo_semanal["nro_medidor"])))

results = database_average_agrupado.merge(Consumo_semanal, how="left", on="nro_medidor")
resultsNuevo = pd.DataFrame()
resultsNuevo["nro_medidor"] = results["nro_medidor"]
resultsNuevo["Tipo_consumo"] = results["Tipo_consumo"]

# Filtrar datos residenciales
database_promedio_final_1 = database_average_agrupado.merge(
    resultsNuevo, how="left", on="nro_medidor"
)
database_promedio_final_1 = database_promedio_final_1[
    database_promedio_final_1["Tipo_consumo"] == "RESIDENCIAL"
]

# Asignación de unidad vecinal
agrupado = database_promedio_final_1
clientes = list(range(len(set(agrupado["nro_medidor"]))))
poligonos = list(range(len(mapa)))
df = pd.DataFrame(
    columns=[
        "nro_medidor",
        "comuna",
        "consumo_promedio",
        "coord_y",
        "coord_x",
        "I_unidad_v",
        "I_tramo_1",
        "I_tramo_2",
        "I_tramo_3",
        "I_tramo_4",
        "I_tramo_5",
        "I_tramo_6",
        "I_tramo_7",
        "I_total_uv",
    ]
)

# Iterar clientes y poligonos
for cliente in clientes:
    for i in poligonos:
        y = agrupado.iloc[cliente]["coord_y"]
        x = agrupado.iloc[cliente]["coord_x"]
        nro_medidor = agrupado.iloc[cliente]["nro_medidor"]
        consumo_promedio = agrupado.iloc[cliente]["Promedio mensual anual"]

        # Atributos geoespaciales
        I_unidad_v = mapa.iloc[i]["I_unidad_v"]
        punto = Point(x, y)
        if punto.within(mapa.iloc[i].geometry):
            tramos = {f"I_tramo_{j}": mapa.iloc[i][f"I_tramo_{j}"] for j in range(1, 8)}
            I_total_uv = mapa.iloc[i]["I_total_uv"]
            df = df.append(
                {
                    **{"nro_medidor": nro_medidor, "comuna": comuna, "consumo_promedio": consumo_promedio, "coord_y": y, "coord_x": x, "I_unidad_v": I_unidad_v, "I_total_uv": I_total_uv},
                    **tramos,
                },
                ignore_index=True,
            )

# Exportar resultados
output_dir = os.path.join(directorio_archivo, "Errores_por_comuna")
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, f"{comuna}_RESULTADOS.csv"), sep=";", index=False)

print("Procesamiento completado.")
