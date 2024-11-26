num_medidores = 100
comunas = ["Santiago", "Ñuñoa", "Providencia"]

data = {
    "nro_medidor": [f"100{str(i).zfill(3)}" for i in range(1, num_medidores + 1)],
    "Month": [random.randint(1, 12) for _ in range(num_medidores)],
    "counting weekday": [random.randint(20, 23) for _ in range(num_medidores)],
    "value weekday": [round(random.uniform(10, 15), 2) for _ in range(num_medidores)],
    "counting weekend": [random.randint(8, 10) for _ in range(num_medidores)],
    "value weekend": [round(random.uniform(8, 12), 2) for _ in range(num_medidores)],
    "Tipo_consumo": ["RESIDENCIAL" for _ in range(num_medidores)],
}

# Guardar archivo para una comuna
for comuna in comunas:
    df = pd.DataFrame(data)
    df.to_csv(f"{comuna}_CONSUMOS_MENSUAL.csv", sep=";", index=False)
    print(f"Archivo '{comuna}_CONSUMOS_MENSUAL.csv' generado.")
