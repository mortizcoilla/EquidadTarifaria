import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de rutas
errores_file = "resultados/resumen_errores_por_comuna_estacion.csv"
beneficios_file = "resultados/resumen_beneficios_aportes_por_comuna_eficiencia.csv"
clientes_file = "datos/clientes/clientes_simulados.csv"
output_dir = "resultados/visualizaciones/graficos"
os.makedirs(output_dir, exist_ok=True)

# Leer datos
errores_data = pd.read_csv(errores_file, sep=";")
beneficios_data = pd.read_csv(beneficios_file, sep=";")
clientes_data = pd.read_csv(clientes_file, sep=";")

# 1. Errores por Estación del Año
plt.figure(figsize=(12, 6))
sns.barplot(data=errores_data, x="estacion", y="error_inclusion", hue="comuna", ci=None, palette="Blues")
plt.title("Errores de Inclusión por Estación")
plt.ylabel("Errores de Inclusión")
plt.xlabel("Estación del Año")
plt.legend(title="Comuna", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f"{output_dir}/errores_inclusion_estacion.png")
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(data=errores_data, x="estacion", y="error_exclusion", hue="comuna", ci=None, palette="Oranges")
plt.title("Errores de Exclusión por Estación")
plt.ylabel("Errores de Exclusión")
plt.xlabel("Estación del Año")
plt.legend(title="Comuna", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f"{output_dir}/errores_exclusion_estacion.png")
plt.show()

# 2. Comparación de Consumo Diurno y Nocturno
plt.figure(figsize=(10, 6))
sns.boxplot(data=clientes_data, x="tipo_cliente", y="consumo_diurno", hue="estacion", palette="viridis")
plt.title("Distribución de Consumo Diurno por Tipo de Cliente")
plt.ylabel("Consumo Diurno (kWh)")
plt.xlabel("Tipo de Cliente")
plt.legend(title="Estación")
plt.tight_layout()
plt.savefig(f"{output_dir}/consumo_diurno_por_tipo.png")
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=clientes_data, x="tipo_cliente", y="consumo_nocturno", hue="estacion", palette="coolwarm")
plt.title("Distribución de Consumo Nocturno por Tipo de Cliente")
plt.ylabel("Consumo Nocturno (kWh)")
plt.xlabel("Tipo de Cliente")
plt.legend(title="Estación")
plt.tight_layout()
plt.savefig(f"{output_dir}/consumo_nocturno_por_tipo.png")
plt.show()

# 3. Impacto de la Eficiencia Energética
plt.figure(figsize=(12, 6))
sns.barplot(data=clientes_data, x="eficiencia_energetica", y="consumo_mensual", hue="tipo_cliente", ci=None, palette="muted")
plt.title("Impacto de la Eficiencia Energética en el Consumo Mensual")
plt.ylabel("Consumo Mensual (kWh)")
plt.xlabel("Eficiencia Energética")
plt.legend(title="Tipo de Cliente")
plt.tight_layout()
plt.savefig(f"{output_dir}/impacto_eficiencia_energetica.png")
plt.show()

# 4. Eventos Anómalos
eventos_data = clientes_data[clientes_data["evento_anomalo"].notnull()]
plt.figure(figsize=(10, 6))
sns.countplot(data=eventos_data, x="evento_anomalo", hue="tipo_cliente", palette="Set2")
plt.title("Frecuencia de Eventos Anómalos por Tipo de Cliente")
plt.ylabel("Frecuencia")
plt.xlabel("Evento Anómalo")
plt.legend(title="Tipo de Cliente")
plt.tight_layout()
plt.savefig(f"{output_dir}/frecuencia_eventos_anomalos.png")
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=eventos_data, x="evento_anomalo", y="consumo_mensual", palette="Set3")
plt.title("Impacto de Eventos Anómalos en el Consumo Mensual")
plt.ylabel("Consumo Mensual (kWh)")
plt.xlabel("Evento Anómalo")
plt.tight_layout()
plt.savefig(f"{output_dir}/impacto_eventos_anomalos.png")
plt.show()
