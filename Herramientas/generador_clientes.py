import os
import pandas as pd
import geopandas as gpd
import random
from shapely.geometry import Point
import numpy as np

# Rutas de entrada y salida
shapefile_path = "datos/geoespacial/comunas_rm.shp"
clientes_output = "datos/clientes/clientes_simulados.csv"

os.makedirs("datos/clientes", exist_ok=True)

# Leer shapefile
print(f"Leyendo shapefile desde: {shapefile_path}")
mapa = gpd.read_file(shapefile_path)

if mapa.crs is None or mapa.crs.to_string() != "EPSG:4326":
    print("Corrigiendo CRS a EPSG:4326...")
    mapa = mapa.to_crs("EPSG:4326")

# Poblaciones estimadas para las 52 comunas
poblaciones = {
    "Cerrillos": 85, "Cerro Navia": 132, "Conchalí": 152, "El Bosque": 164,
    "Estación Central": 147, "Huechuraba": 113, "Independencia": 93, "La Cisterna": 95,
    "La Florida": 366, "La Granja": 116, "La Pintana": 190, "La Reina": 96,
    "Las Condes": 249, "Lo Barnechea": 100, "Lo Espejo": 113, "Lo Prado": 107,
    "Macul": 112, "Maipú": 534, "Ñuñoa": 208, "Pedro Aguirre Cerda": 107,
    "Peñalolén": 241, "Providencia": 142, "Pudahuel": 232, "Quilicura": 222,
    "Quinta Normal": 104, "Recoleta": 170, "Renca": 149, "San Joaquín": 99,
    "San Miguel": 121, "San Ramón": 102, "Santiago": 404, "Vitacura": 89,
    "Puente Alto": 608, "Pirque": 27, "San José de Maipo": 19, "Colina": 176,
    "Lampa": 94, "Tiltil": 19, "San Bernardo": 332, "Buin": 103, "Calera de Tango": 30,
    "Paine": 96, "Melipilla": 136, "Curacaví": 40, "María Pinto": 14,
    "San Pedro": 11, "Talagante": 74, "El Monte": 39, "Isla de Maipo": 36,
    "Padre Hurtado": 63, "Peñaflor": 95, "Alhué": 7
}

# Distribución proporcional de clientes
n_clientes_total = 20000
total_poblacion = sum(poblaciones.values())
n_clientes_por_comuna = {k: int(v / total_poblacion * n_clientes_total) for k, v in poblaciones.items()}

# Generar clientes por comuna
def generar_clientes(comuna, polygon, n_clientes):
    minx, miny, maxx, maxy = polygon.bounds
    data = []
    while len(data) < n_clientes:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        punto = Point(x, y)
        if polygon.contains(punto):
            socioeconomico = random.choice(["bajo", "medio", "alto"])
            eficiencia = random.choice(["bajo", "medio", "alto"])
            tipo_cliente = random.choice(["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"])
            renovable = random.random() < 0.1
            estacion = random.choice(["invierno", "verano", "otoño", "primavera"])
            evento = random.choices(
                [None, "corte", "pico"],
                weights=[0.98, 0.01, 0.01],
                k=1
            )[0]

            # Generar consumo mensual controlado
            consumo_mensual = np.random.normal(loc=200 if tipo_cliente == "RESIDENCIAL" else 500, scale=50)
            consumo_mensual = max(50, consumo_mensual)  # Evitar consumos negativos

            # Ajuste por eficiencia y renovable
            if eficiencia == "alto":
                consumo_mensual *= 0.8
            if renovable:
                consumo_mensual *= 0.9

            # Calcular consumo diurno y nocturno
            consumo_diurno = consumo_mensual * 0.6
            consumo_nocturno = consumo_mensual * 0.4

            data.append([
                comuna, socioeconomico, eficiencia, renovable, tipo_cliente,
                estacion, consumo_mensual, consumo_diurno, consumo_nocturno, x, y, evento
            ])
    return data

# Crear datos para todas las comunas
clientes_totales = []
for idx, row in mapa.iterrows():
    comuna = row["Comuna"]
    poligono = row.geometry
    n_clientes = n_clientes_por_comuna.get(comuna, 500)
    print(f"Generando {n_clientes} clientes para comuna: {comuna}")
    clientes_totales.extend(generar_clientes(comuna, poligono, n_clientes))

# Guardar clientes simulados
df_clientes = pd.DataFrame(clientes_totales, columns=[
    "comuna", "socioeconomico", "eficiencia_energetica", "renovable", "tipo_cliente", 
    "estacion", "consumo_mensual", "consumo_diurno", "consumo_nocturno", "coord_x", "coord_y", "evento_anomalo"
])
df_clientes.to_csv(clientes_output, index=False, sep=";")
print(f"Archivo de clientes generado: {clientes_output}")
