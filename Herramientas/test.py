import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Leer shapefile
shapefile_path = "/home/makabrus/Workspace/EquidadTarifaria/datos/geoespacial/CSE_SANTIAGO_UV_RSH_FINAL.shp"
mapa = gpd.read_file(shapefile_path)

# Leer datos de consumo generados
consumo_path = "/home/makabrus/Workspace/EquidadTarifaria/datos/consumos_mensuales/Las Condes_consumos_mensuales.csv"
df = pd.read_csv(consumo_path, sep=";")

# Convertir a GeoDataFrame
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

# Resultados
print("Puntos de consumo que intersectan con los polígonos:")
print(gdf[gdf["intersecta"]])

print("\nPuntos de consumo que NO intersectan con los polígonos:")
print(gdf[~gdf["intersecta"]])
