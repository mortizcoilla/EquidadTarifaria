import os

# Estructura de carpetas
estructura = {
    "datos": [
        "clientes",
        "consumos_mensuales",
        "consumos_semanales",
        "geoespacial"
    ],
    "scripts": [],
    "resultados": [
        "errores_por_comuna",
        "visualizaciones"
    ],
    "documentos": []
}

# Nombre del proyecto
nombre_proyecto = "proyecto_equidad_tarifaria"

def crear_estructura(base_dir, estructura):
    """
    Crea una estructura de carpetas basada en un diccionario.
    """
    for carpeta, subcarpetas in estructura.items():
        # Crear la carpeta principal
        carpeta_path = os.path.join(base_dir, carpeta)
        os.makedirs(carpeta_path, exist_ok=True)
        print(f"Carpeta creada: {carpeta_path}")
        
        # Crear subcarpetas
        for subcarpeta in subcarpetas:
            subcarpeta_path = os.path.join(carpeta_path, subcarpeta)
            os.makedirs(subcarpeta_path, exist_ok=True)
            print(f"Subcarpeta creada: {subcarpeta_path}")

# Crear estructura de carpetas
if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), nombre_proyecto)
    os.makedirs(base_dir, exist_ok=True)
    print(f"Directorio base creado: {base_dir}")
    crear_estructura(base_dir, estructura)

    # Mensaje final
    print("\nEstructura de carpetas generada exitosamente.")
