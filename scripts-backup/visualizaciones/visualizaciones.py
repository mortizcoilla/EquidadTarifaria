import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de rutas
shapefile_path = "/home/makabrus/Workspace/EquidadTarifaria/datos/geoespacial/CSE_SANTIAGO_UV_RSH_FINAL.shp"
consumos_dir = "/home/makabrus/Workspace/EquidadTarifaria/datos/consumos_mensuales/"

# Leer shapefile
mapa = gpd.read_file(shapefile_path)

# Leer todos los archivos de consumos
consumos_files = [f for f in os.listdir(consumos_dir) if f.endswith("_consumos_mensuales.csv")]
df_list = []
for file in consumos_files:
    comuna = file.split("_")[0]
    df = pd.read_csv(os.path.join(consumos_dir, file), sep=";")
    df["comuna"] = comuna  # Añadir columna de comuna
    df_list.append(df)

# Unir todos los consumos en un solo DataFrame
df_consumos = pd.concat(df_list, ignore_index=True)

# Crear un GeoDataFrame a partir de los consumos
gdf_consumos = gpd.GeoDataFrame(
    df_consumos,
    geometry=gpd.points_from_xy(df_consumos["coord_x"], df_consumos["coord_y"]),
    crs="EPSG:4326"
)

# Análisis Estadístico
# Resumen de consumos por comuna
consumos_resumen = df_consumos.groupby("comuna")["consumo_mensual"].agg(["mean", "sum", "count"]).reset_index()
consumos_resumen.columns = ["Comuna", "Promedio Consumo", "Consumo Total", "Número de Clientes"]

# Distribución por tipo de cliente
distribucion_tarifa = df_consumos.groupby(["comuna", "clave_tarifa"])["consumo_mensual"].mean().unstack()

# Visualización 1: Mapa de clientes y consumo
fig, ax = plt.subplots(figsize=(12, 10))
mapa.plot(ax=ax, color="lightgrey", edgecolor="black", alpha=0.7)
gdf_consumos.plot(
    ax=ax,
    column="consumo_mensual",
    cmap="viridis",
    markersize=10,
    legend=True,
    legend_kwds={"label": "Consumo Mensual (kWh)", "orientation": "vertical"},
)
plt.title("Mapa de Clientes y Consumo Mensual")
plt.show()

# Visualización 2: Promedio de consumo por comuna
sns.barplot(x="Comuna", y="Promedio Consumo", data=consumos_resumen, palette="viridis")
plt.title("Promedio de Consumo Mensual por Comuna")
plt.ylabel("Consumo Promedio (kWh)")
plt.xlabel("Comuna")
plt.xticks(rotation=45)
plt.show()

# Visualización 3: Distribución de consumo por tipo de cliente
distribucion_tarifa.plot(kind="bar", figsize=(10, 7), colormap="viridis")
plt.title("Promedio de Consumo por Tipo de Cliente")
plt.ylabel("Consumo Promedio (kWh)")
plt.xlabel("Comuna")
plt.xticks(rotation=45)
plt.legend(title="Clave Tarifa")
plt.show()
