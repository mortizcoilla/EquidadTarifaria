import geopandas as gpd

# Ruta al shapefile de comunas
shapefile_comunas = "datos/geoespacial/Comunas/comunas.shp"

# Cargar el shapefile
gdf_comunas = gpd.read_file(shapefile_comunas)

# Verificar las primeras filas y columnas disponibles
print("Columnas disponibles en comunas.shp:")
print(gdf_comunas.columns)

# Visualizar las comunas
print("Ejemplo de datos:")
print(gdf_comunas.head())

# Graficar las comunas
gdf_comunas.plot(edgecolor="black", figsize=(12, 12))
