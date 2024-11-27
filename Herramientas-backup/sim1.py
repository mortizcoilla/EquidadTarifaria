import os
import pandas as pd
import random

output_dir = "datos/clientes"
os.makedirs(output_dir, exist_ok=True)

# Comunas compatibles con el shapefile
comunas = ["Santiago", "Ñuñoa", "Providencia", "Las Condes", "Vitacura"]

# Generar datos simulados
clientes = []
for i in range(100):
    coord_x = random.uniform(-70.68, -70.65)  # Longitudes en grados decimales
    coord_y = random.uniform(-33.47, -33.44)  # Latitudes en grados decimales
    comuna = random.choice(comunas)
    clientes.append({
        "nro_medidor": f"1000{i}",
        "comuna": comuna,
        "clave_tarifa": "RESIDENCIAL" if random.random() > 0.5 else "NO_RESIDENCIAL",
        "coord_x": coord_x,
        "coord_y": coord_y,
    })

# Guardar datos en CSV
output_file = os.path.join(output_dir, "clientes_simulados.csv")
pd.DataFrame(clientes).to_csv(output_file, sep=";", index=False)
print(f"Archivo generado: {output_file}")
