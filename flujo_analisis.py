import subprocess

# Rutas de los scripts en la estructura actual
scripts = [
    "scripts/analisis/Errores.py",
    "scripts/analisis/calculo_metricas.py",
    "scripts/visualizaciones/visualizaciones_metricas.py"
]

for script in scripts:
    try:
        print(f"Ejecutando {script}...")
        subprocess.run(["python", script], check=True)
    except FileNotFoundError:
        print(f"ERROR: No se pudo encontrar el archivo {script}. Verifica su ubicación.")
        continue
    except subprocess.CalledProcessError as e:
        print(f"ERROR al ejecutar {script}: {e}")
        continue

print("Flujo de análisis completado.")
