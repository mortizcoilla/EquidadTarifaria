import pandas as pd
import random

# Datos simulados
comunas = ["Santiago", "Ñuñoa", "Providencia", "Las Condes", "Vitacura"]
tarifas = ["RESIDENCIAL", "NO_RESIDENCIAL"]
num_clientes = 100  # Número de clientes simulados

# Generar datos
data = {
    "nro_medidor": [f"100{str(i).zfill(3)}" for i in range(1, num_clientes + 1)],
    "comuna": [random.choice(comunas) for _ in range(num_clientes)],
    "clave_tarifa": [random.choice(tarifas) for _ in range(num_clientes)],
    "Tipo_consumo": ["RESIDENCIAL" if t == "RESIDENCIAL" else "NO_RESIDENCIAL" for t in tarifas],
    "coord_x": [round(random.uniform(-70.7, -70.5), 6) for _ in range(num_clientes)],
    "coord_y": [round(random.uniform(-33.6, -33.4), 6) for _ in range(num_clientes)],
}

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar archivo
df.to_csv("Archivo n1 v2.csv", sep=";", index=False)
print("Archivo 'Archivo n1 v2.csv' generado.")
