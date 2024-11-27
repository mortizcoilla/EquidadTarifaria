import subprocess

# Lista de scripts a ejecutar en orden
scripts = [
    "scripts/analisis/BeneficiosAportes.py",
    "scripts/analisis/Errores.py",
    "scripts/analisis/calculo_metricas.py",
    "scripts/visualizaciones/visualizaciones_metricas.py"  # Cambiar al nombre correcto
]

# Ejecutar los scripts
for script in scripts:
    try:
        print(f"Ejecutando {script}...")
        subprocess.run(["python", script], check=True)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {script}. Verifica su ubicación.")
        continue
    except subprocess.CalledProcessError as e:
        print(f"ERROR al ejecutar {script}: {e}")
        continue

print("Flujo de análisis completado.")
