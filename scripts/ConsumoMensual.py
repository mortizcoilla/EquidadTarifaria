import rarfile
import pandas as pd
import os
import time
from shapely.geometry import Point
import numpy as np

# Función para truncar números a n decimales
def truncar(num, n=5):
    return float(int(num * (10**n)) / (10**n))

# Bandera para guardar archivos
save_files_flag = [1]

# Directorio actual
cwd = os.getcwd()

# Ruta del archivo base
directorio_archivo = cwd

# Cargar datos de clientes
clients_path = os.path.join(directorio_archivo, "data", "Archivo n1 v2.csv")
clients = pd.read_csv(clients_path, sep=";")

# Listas de tarifas
lista_residencial = [
    "NORMAL", "NORMAL CON EMISION DE BOLETA", "RESIDENCIAL",
    "HORARIA RESIDENCIAL 3", "THRF", "HORARIA RESIDENCIAL 1",
    "THR PLUS EMPLEADO", "THR PLUS", "PLAN POBLACION GUILLERMO EL CO",
    "VIUDAS C/TARIFA DESPUES DE 1980. R.METROP.", "THR PLUS EMPLEADO",
    "VIUDAS C/TARIFA ANTES 01", "EE/00 PENSIONADOS DIPREL S.A.",
    "EE/00 JUBILADOS DESPUES DE 1980 R. METROP.", "PROVISORIO BT",
    "CLAVE TARIFA POR DEFECTO BT1", "EE/00 PENDIONADOS ANTES 01",
    "EE/00 PENSIONADOS REGION METROPOLITANA", "HORARIA RESIDENCIAL 2",
    "VIUDAS C/TARIFA DESP. 01", "THRP CON DESCUENTO POR PLANILLA"
]
lista_no_residencial = [
    "CONSUMOS PROPIOS", "NORMAL CON EMISION DE FACTURA",
    "CONSUMO PRESENTE EN PUNTA", "CONSUMO ESPECIAL EMISION DE FA",
    "ALUMBRADO PUBLICO NORMAL", "CONSUMO PTE. EN PUNTA EMISION DE FACTURA",
    "NORMAL CON MEDIDA EN BT EMISION", "SERVICIOS EX MODULOS",
    "PLAN ORC CLTES NUEVOS", "BOMBEROS", "ALUMBRADO PUBLICO PARTICULAR",
    "MUNICIPAL", "PLAN ORC CLTES REINCORP.", "SERV. PARTICULARES DE CARGO FIS",
    "SERV NORMALIZADO CON ARRIENDO", "PLAN PRU CLIENTES REINCORPORAD",
    "CLAVE TARIFA POR DEFECTO BT43", "REMARCADORES", "COND. ESPECIAL PROVISORIO CONS",
    "LETREROS LUMINOSOS"
]

# Crear dataframes con las listas de tarifas
residencial = pd.DataFrame({"clave_tarifa": lista_residencial})
residencial["Tipo_consumo"] = "RESIDENCIAL"

no_residencial = pd.DataFrame({"clave_tarifa": lista_no_residencial})
no_residencial["Tipo_consumo"] = "NO RESIDENCIAL"

# Concatenar tipos de consumo
Tipo_consumo = pd.concat([residencial, no_residencial])

# Merge con los datos de clientes
clients = clients.merge(
    Tipo_consumo, how="inner", left_on="clave_tarifa", right_on="clave_tarifa"
)

# Limpieza de columnas innecesarias
clients.drop(columns=["Unnamed: 10", "Unnamed: 11"], errors="ignore", inplace=True)

# Limpieza de coordenadas
clients["coord_x"] = clients["coord_x"].str.replace(".", "")
clients["coord_x"] = clients["coord_x"].str[:3] + "." + clients["coord_x"].str[3:]
clients["coord_x"] = clients["coord_x"].astype(float).apply(truncar)

clients["coord_y"] = clients["coord_y"].str.replace(".", "")
clients["coord_y"] = clients["coord_y"].str[:3] + "." + clients["coord_y"].str[3:]
clients["coord_y"] = clients["coord_y"].astype(float).apply(truncar)

# Preparar series temporales
initial_day = "2019/01/01"
final_day = "2020/01/01"
hourly_step = "1H"

time_series_1 = pd.date_range(start=initial_day, end=final_day, freq=hourly_step)[:-1]
Periods_1 = time_series_1.to_period("M").drop_duplicates()
Months_str_1 = Periods_1.strftime("%Y_%m")

# Preparar series adicionales
initial_day_2 = "2019/03/02"
final_day_2 = "2019/05/31"

time_series_2 = pd.date_range(start=initial_day_2, end=final_day_2, freq=hourly_step)[:-1]
Periods_2 = time_series_2.to_period("M").drop_duplicates()
Months_str_2 = Periods_2.strftime("%Y_%m")

# Concatenar series
time_series = time_series_1.append(time_series_2)
Months_str = Months_str_1.append(Months_str_2)

# Guardar nombres de comunas
Comunas = set(clients["comuna"])
df_comunas = pd.DataFrame({"nombre": list(Comunas)})
df_comunas.to_csv(os.path.join(directorio_archivo, "nombre_comunas.csv"), sep=";")

# Configuración inicial de datos por comuna
Tabla_histo = pd.DataFrame()
No_data = {"TIL TIL"}
Comunas = Comunas.difference(No_data)

# Procesar archivos .rar por comuna
for comuna in Comunas:
    print(f"Procesando comuna: {comuna}")
    rar_file_path = os.path.join(directorio_archivo, "comunas_filtradas", f"{comuna}.rar")
    
    if not os.path.exists(rar_file_path):
        print(f"Archivo no encontrado: {rar_file_path}")
        continue
    
    rf = rarfile.RarFile(rar_file_path)
    file_names = [info.filename for info in rf.infolist()]
    database = []

    for file_name in file_names:
        if any(month_str in file_name for month_str in Months_str):
            print(f"Abriendo archivo: {file_name}")
            df = pd.read_csv(rf.open(file_name), sep=";")
            database.append(df)
    
    if not database:
        print(f"No se encontraron datos para la comuna: {comuna}")
        continue
    
    database = pd.concat(database)
    database["sampledate"] = pd.to_datetime(database["sampledate"])
    database = database.drop_duplicates(subset=["nro_medidor", "sampledate"])

    # Merge con datos de clientes
    database = database.merge(
        clients[["comuna", "Tipo_consumo", "coord_y", "coord_x", "nro_medidor"]],
        how="inner", on="nro_medidor"
    )
    
    # Exportar coordenadas
    database.to_csv(os.path.join(directorio_archivo, "coordenadas.csv"), index=False)

    # Calcular campos adicionales
    database["Hour"] = database["sampledate"].dt.hour
    database["Day of week"] = database["sampledate"].dt.dayofweek
    database["N week"] = database["sampledate"].dt.isocalendar().week
    database["Month"] = database["sampledate"].dt.month
    database["Year"] = database["sampledate"].dt.year
    database["weekend"] = database["Day of week"] >= 5
    database["value"] = database["value"].astype(float)

    # Exportar datos mensuales
    directory = os.path.join(directorio_archivo, "Tabla_consumos_clientes_mensual")
    os.makedirs(directory, exist_ok=True)
    csv_name = f"{comuna}_CONSUMOS_MENSUAL.csv"
    database.to_csv(os.path.join(directory, csv_name), sep=";", index=False)

print("Procesamiento completado.")
