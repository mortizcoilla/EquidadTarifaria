import os
import pandas as pd
import geopandas as gpd
import random
from shapely.geometry import Point

shapefile_path = "datos/geoespacial/CSE_SANTIAGO_UV_RSH_FINAL.shp"
output_dir = "datos/consumos_mensuales"
os.makedirs(output_dir, exist_ok=True)

# Leer shapefile
mapa = gpd.read_file(shapefile_path)

# Generar puntos dentro de polígonos
def generar_puntos(polygon, n):
    minx, miny, maxx, maxy = polygon.bounds
    puntos = []
    while len(puntos) < n:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        punto = Point(x, y)
        if polygon.contains(punto):
            puntos.append(punto)
    return puntos

# Generar puntos por comuna
for comuna in mapa["comuna"].unique():
    poligono = mapa[mapa["comuna"] == comuna].geometry.union_all()
    puntos = generar_puntos(poligono, 50)
    data = {"coord_x": [p.x for p in puntos], "coord_y": [p.y for p in puntos]}
    output_file = os.path.join(output_dir, f"{comuna}_consumos_mensuales.csv")
    pd.DataFrame(data).to_csv(output_file, sep=";", index=False)
    print(f"Archivo generado para {comuna}: {output_file}")
