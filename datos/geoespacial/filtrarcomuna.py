import geopandas as gpd
import matplotlib.pyplot as plt

# Cargar el shapefile
shapefile_path = "datos/geoespacial/Comunas/comunas.shp"
gdf_comunas = gpd.read_file(shapefile_path)

# Inspeccionar valores únicos en la columna 'Region'
print("Valores únicos en la columna 'Region':")
print(gdf_comunas["Region"].unique())

# Filtrar las comunas de la Región Metropolitana
gdf_comunas_rm = gdf_comunas[gdf_comunas["Region"].str.contains("Metropolitana", case=False, na=False)]

# Verificar número de comunas seleccionadas
print(f"Número de comunas seleccionadas: {len(gdf_comunas_rm)}")

# Validar geometrías
print("Verificando geometrías inválidas...")
print(gdf_comunas_rm.is_valid.value_counts())

# Reparar geometrías inválidas (si las hay)
if not gdf_comunas_rm.is_valid.all():
    gdf_comunas_rm["geometry"] = gdf_comunas_rm["geometry"].buffer(0)

# Verificar CRS y reproyectar si es necesario
print("Sistema de referencia espacial (CRS):")
print(gdf_comunas_rm.crs)
if gdf_comunas_rm.crs != "EPSG:4326":
    gdf_comunas_rm = gdf_comunas_rm.to_crs("EPSG:4326")

# Guardar shapefile filtrado
output_path = "datos/geoespacial/comunas_rm.shp"
gdf_comunas_rm.to_file(output_path)
print(f"Shapefile con las comunas de la Región Metropolitana guardado en: {output_path}")

# Graficar las comunas
print("Generando mapa de las comunas filtradas...")
ax = gdf_comunas_rm.plot(edgecolor="black", figsize=(12, 12))
ax.set_title("Comunas de la Región Metropolitana")
plt.show()
