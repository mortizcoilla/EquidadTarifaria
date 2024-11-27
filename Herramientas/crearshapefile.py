import os
import geopandas as gpd
from shapely.geometry import Polygon

# Configuración de rutas
output_dir = "/home/makabrus/Workspace/EquidadTarifaria/datos/geoespacial"
os.makedirs(output_dir, exist_ok=True)
shapefile_path = os.path.join(output_dir, "CSE_SANTIAGO_UV_RSH_FINAL.shp")

# Definir polígonos ficticios para las comunas
data = {
    "comuna": ["Santiago", "Ñuñoa", "Providencia", "Las Condes", "Vitacura"],
    "geometry": [
        Polygon([(-70.68, -33.45), (-70.65, -33.45), (-70.65, -33.43), (-70.68, -33.43)]),
        Polygon([(-70.66, -33.46), (-70.63, -33.46), (-70.63, -33.44), (-70.66, -33.44)]),
        Polygon([(-70.67, -33.47), (-70.64, -33.47), (-70.64, -33.45), (-70.67, -33.45)]),
        Polygon([(-70.69, -33.48), (-70.66, -33.48), (-70.66, -33.46), (-70.69, -33.46)]),
        Polygon([(-70.70, -33.49), (-70.67, -33.49), (-70.67, -33.47), (-70.70, -33.47)]),
    ],
}

# Crear GeoDataFrame
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Guardar el shapefile
gdf.to_file(shapefile_path)
print(f"Shapefile creado en: {shapefile_path}")
