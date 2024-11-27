import pandas as pd
import random
import numpy as np

# Configuración de simulación
comunas = ["Las Condes", "Providencia", "Santiago", "Vitacura", "Ñuñoa", 
           "Puente Alto", "La Florida", "Maipú", "Quilicura", "Lo Barnechea"]
tipos_cliente = ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"]

# Parámetros ajustables
n_clientes_por_comuna = 500  # Número de clientes simulados por comuna
consumo_base = {"RESIDENCIAL": 150, "COMERCIAL": 300, "INDUSTRIAL": 1000}
variabilidad = {"RESIDENCIAL": 50, "COMERCIAL": 100, "INDUSTRIAL": 300}

# Generar datos simulados
data_simulada = []
for comuna in comunas:
    for _ in range(n_clientes_por_comuna):
        tipo_cliente = random.choice(tipos_cliente)
        consumo = round(np.random.normal(loc=consumo_base[tipo_cliente], scale=variabilidad[tipo_cliente]), 2)
        consumo = max(0, consumo)  # Evitar consumos negativos
        coord_x = round(random.uniform(-70.75, -70.5), 6)  # Coordenadas ficticias
        coord_y = round(random.uniform(-33.6, -33.4), 6)
        data_simulada.append([comuna, tipo_cliente, consumo, coord_x, coord_y])

# Crear DataFrame
df_simulada = pd.DataFrame(data_simulada, columns=["comuna", "tipo_cliente", "consumo_mensual", "coord_x", "coord_y"])

# Guardar en el archivo esperado por el flujo
output_file = "datos/clientes/clientes_simulados.csv"
df_simulada.to_csv(output_file, index=False)
print(f"Datos simulados generados y guardados en {output_file}")
