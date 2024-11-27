import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración
input_file = "resultados/beneficios_aportes.csv"
output_dir = "resultados/graficos"
os.makedirs(output_dir, exist_ok=True)

# Leer datos
data = pd.read_csv(input_file, sep=";")

# Beneficios y Aportes por comuna
plt.figure(figsize=(10, 6))
sns.barplot(x="comuna", y="ajuste_tarifario", data=data, ci=None)
plt.title("Beneficios y Aportes por Comuna")
plt.ylabel("Ajuste Tarifario (kWh)")
plt.xlabel("Comuna")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/beneficios_aportes_por_comuna.png")
plt.close()

# Distribución de errores
errores_data = data[["error_inclusion", "error_exclusion"]].sum()
plt.figure(figsize=(8, 6))
errores_data.plot(kind="bar", color=["red", "blue"])
plt.title("Errores de Inclusión y Exclusión")
plt.ylabel("Cantidad de Hogares")
plt.xticks([0, 1], ["Errores de Inclusión", "Errores de Exclusión"], rotation=0)
plt.tight_layout()
plt.savefig(f"{output_dir}/errores_inclusion_exclusion.png")
plt.close()
