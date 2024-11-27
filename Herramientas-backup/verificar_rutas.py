import os

# Rutas clave
required_paths = [
    "datos/clientes/clientes_simulados.csv",
    "datos/geoespacial/CSE_SANTIAGO_UV_RSH_FINAL.shp",
    "datos/consumos_mensuales",
    "resultados",
    "resultados/visualizaciones/graficos"
]

# Verificar existencia
for path in required_paths:
    if os.path.exists(path):
        print(f"OK: {path} existe.")
    else:
        print(f"ERROR: {path} no existe.")
