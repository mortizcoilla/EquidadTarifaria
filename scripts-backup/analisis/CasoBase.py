import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Configuración de rutas
directorio_archivo = os.getcwd()

# Ruta del shapefile
geo_dir = os.path.join(directorio_archivo, "datos", "geoespacial")
shapefile_path = os.path.join(geo_dir, "CSE_SANTIAGO_UV_RSH_FINAL.shp")

# Ruta de entrada y salida
consumos_path = os.path.join(directorio_archivo, "datos", "consumos_mensuales")
output_dir = os.path.join(directorio_archivo, "resultados", "errores_por_comuna")
os.makedirs(output_dir, exist_ok=True)

# Leer shapefile
print(f"Leyendo shapefile desde: {shapefile_path}")
try:
    mapa = gpd.read_file(shapefile_path)
except FileNotFoundError:
    print(f"Error: El archivo {shapefile_path} no existe.")
    exit(1)

# Leer consumos mensuales
files = [f for f in os.listdir(consumos_path) if f.endswith("_consumos_mensuales.csv")]

for file in files:
    comuna = file.split("_")[0]
    file_path = os.path.join(consumos_path, file)
    
    print(f"Procesando datos para la comuna: {comuna} desde {file_path}")
    df = pd.read_csv(file_path, sep=";")

    # Ajustar el escalado de las coordenadas (dividir por 1 millón)
    df["coord_x"] = df["coord_x"].astype(float) / 1e6
    df["coord_y"] = df["coord_y"].astype(float) / 1e6

    # Convertir coordenadas en puntos geoespaciales
    gdf = gpd.GeoDataFrame(
        df,
        geometry=[Point(xy) for xy in zip(df["coord_x"], df["coord_y"])],
        crs="EPSG:4326"
    )
    
    # Asegurar que CRS coincidan
    if gdf.crs != mapa.crs:
        gdf = gdf.to_crs(mapa.crs)

    # Verificar intersección
    gdf["intersecta"] = gdf.geometry.apply(lambda x: mapa.intersects(x).any())
    if not gdf["intersecta"].any():
        print(f"Advertencia: Ninguna geometría de los datos de {comuna} intersecta con los polígonos del shapefile.")
        continue

    # Unión espacial
    gdf_merged = gpd.sjoin(gdf, mapa, how="left", predicate="intersects")

    # Verificar que 'CSE' está presente
    if "CSE" not in gdf_merged.columns:
        raise ValueError(f"La columna 'CSE' no está presente después de la unión espacial para {comuna}.")

    # Identificar errores de asignación
    gdf_merged["error"] = gdf_merged["CSE"].isnull()
    errores = gdf_merged[gdf_merged["error"]]

    # Guardar resultados
    output_file = os.path.join(output_dir, f"{comuna}_errores.csv")
    errores.to_csv(output_file, sep=";", index=False)
    print(f"Errores guardados en: {output_file}")

print("\nProceso completado: CasoBase.py")
