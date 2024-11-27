import geopandas as gpd

# Ruta al shapefile
shapefile_path = "datos/geoespacial/comunas_rm.shp"

try:
    # Leer shapefile
    print(f"Leyendo shapefile desde: {shapefile_path}")
    mapa = gpd.read_file(shapefile_path)
    
    # Mostrar las columnas disponibles
    print("\nColumnas disponibles en el shapefile:")
    print(mapa.columns)

    # Mostrar las primeras filas para inspeccionar el contenido
    print("\nPrimeras filas del shapefile:")
    print(mapa.head())

    # Verificar el sistema de referencia
    print("\nSistema de referencia espacial (CRS):")
    print(mapa.crs)
    
except Exception as e:
    print(f"Error al leer el shapefile: {e}")
