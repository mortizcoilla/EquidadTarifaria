import os
import pandas as pd
import matplotlib.pyplot as plt

# Rutas de los archivos
errores_file = "resultados/resumen_errores_por_comuna.csv"
beneficios_file = "resultados/resumen_beneficios_aportes_por_comuna.csv"
output_dir = "resultados/visualizaciones/graficos"  # Carpeta para guardar gráficos
os.makedirs(output_dir, exist_ok=True)

# Leer datos
errores_data = pd.read_csv(errores_file, sep=";", index_col="comuna")
beneficios_data = pd.read_csv(beneficios_file, sep=";", index_col="comuna")

# 1. Gráfico de errores por comuna
errores_data.plot(kind="bar", figsize=(10, 6), color=["red", "blue"])
plt.title("Errores por Comuna")
plt.ylabel("Cantidad de Errores")
plt.xlabel("Comuna")
plt.xticks(rotation=45)
plt.legend(["Errores de Inclusión", "Errores de Exclusión"])
plt.tight_layout()
plt.savefig("resultados/graficos/errores_por_comuna.png")
plt.show()

# 2. Gráfico de beneficios y aportes por comuna
beneficios_data.plot(kind="bar", figsize=(10, 6), color="skyblue", legend=False)
plt.title("Beneficios y Aportes por Comuna")
plt.ylabel("Ajuste Tarifario (kWh)")
plt.xlabel("Comuna")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("resultados/graficos/beneficios_aportes_por_comuna.png")
plt.show()
