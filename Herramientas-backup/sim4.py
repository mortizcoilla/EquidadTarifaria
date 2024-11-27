import os
import pandas as pd
import geopandas as gpd
import random
from shapely.geometry import Point

# Configuración de rutas
shapefile_path = "/home/makabrus/Workspace/EquidadTarifaria/datos/geoespacial/CSE_SANTIAGO_UV_RSH_FINAL.shp"
output_dir = "/home/makabrus/Workspace/EquidadTarifaria/datos/consumos_mensuales"
os.makedirs(output_dir, exist_ok=True)

# Leer shapefile
print(f"Leyendo shapefile desde: {shapefile_path}")
mapa = gpd.read_file(shapefile_path)

# Confirmar CRS
if mapa.crs is None:
    raise ValueError("El shapefile no tiene un sistema de referencia espacial definido.")
if mapa.crs.to_string() != "EPSG:4326":
    print("El CRS del shapefile no es EPSG:4326. Convirtiendo...")
    mapa = mapa.to_crs("EPSG:4326")

# Generar puntos dentro de polígonos
def generar_puntos_aleatorios(polygon, n):
    minx, miny, maxx, maxy = polygon.bounds
    puntos = []
    while len(puntos) < n:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        punto = Point(x, y)
        if polygon.contains(punto):
            puntos.append(punto)
    return puntos

# Generar puntos por comuna con columnas adicionales
if "comuna" not in mapa.columns:
    raise ValueError("El shapefile no contiene una columna llamada 'comuna'.")

for comuna in mapa["comuna"].unique():
    poligono = mapa[mapa["comuna"] == comuna].geometry.unary_union
    print(f"Generando puntos para la comuna: {comuna}")
    puntos = generar_puntos_aleatorios(poligono, 50)  # Generar 50 puntos por comuna
    data = {
        "coord_x": [p.x for p in puntos],
        "coord_y": [p.y for p in puntos],
        "comuna": [comuna] * len(puntos),
        "clave_tarifa": ["RESIDENCIAL" if random.random() > 0.5 else "NO_RESIDENCIAL" for _ in puntos],
        "consumo_mensual": [random.randint(150, 400) for _ in puntos],
    }
    output_file = os.path.join(output_dir, f"{comuna}_consumos_mensuales.csv")
    pd.DataFrame(data).to_csv(output_file, sep=";", index=False)
    print(f"Archivo generado: {output_file}")
