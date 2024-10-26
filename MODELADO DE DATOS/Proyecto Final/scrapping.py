import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import os
import re

# Definir el path donde se guardarán los CSV
file_path = r'MODELADO DE DATOS 24B\Proyecto Final\liga_data_csv'

# Crear el directorio si no existe
if not os.path.exists(file_path):
    os.makedirs(file_path)

# Función para limpiar y simplificar los encabezados de los DataFrames sin perder información importante
def clean_headers(df):
    new_columns = []
    for col in df.columns:
        # Eliminar cualquier número irrelevante pero mantener nombres de columnas relevantes
        clean_col = re.sub(r'\d+', '', col)  # Eliminar números
        clean_col = re.sub(r'_', ' ', clean_col)  # Reemplazar guión bajo por espacio
        clean_col = clean_col.strip()  # Quitar espacios al inicio o final
        new_columns.append(clean_col)
    df.columns = new_columns
    return df

# Función para ajustar valores numéricos con formato adecuado, ignorando columnas que no sean numéricas
def clean_numeric_values(df):
    for col in df.columns:
        # Verificar si la columna tiene valores que pueden convertirse a numéricos
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir a números si es posible
        except (ValueError, TypeError):
            # Si no es posible convertir a numérico, continuar sin modificar la columna
            print(f"Columna '{col}' no es numérica, se omite su conversión.")
    return df

# Función para cargar, limpiar y guardar los CSV en el directorio especificado
def process_csv_files(directory):
    # Listar todos los archivos CSV en el directorio
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            full_path = os.path.join(directory, filename)
            try:
                # Cargar el archivo CSV
                df = pd.read_csv(full_path)
                # Limpiar los encabezados
                df_cleaned = clean_headers(df)
                # Ajustar los valores numéricos
                df_cleaned = clean_numeric_values(df_cleaned)
                # Guardar el archivo nuevamente en el directorio especificado con los encabezados corregidos
                df_cleaned.to_csv(os.path.join(file_path, filename), index=False)
                print(f"Archivo '{filename}' procesado y guardado correctamente en '{file_path}'.")
            except Exception as e:
                print(f"Error procesando el archivo '{filename}': {e}")

# URL de la página que contiene todas las tablas de estadísticas avanzadas
url = "https://fbref.com/es/comps/31/Liga-MX-Estadisticas"

# Realizamos la solicitud HTTP
response = requests.get(url)

# Comprobamos que la conexión fue exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # IDs de las tablas que necesitamos extraer
    table_ids = [
        'stats_squads_standard_for',
        'stats_squads_shooting_for',
        'stats_squads_passing_for',
        'stats_squads_possession_for',
        'stats_squads_defense_for',
        'stats_squads_playing_time_for',
        'stats_squads_keeper_for',
        'stats_squads_misc_for'
    ]

    all_data = {}

    # Recorrer cada ID de tabla y extraer los datos
    for table_id in table_ids:
        # Encontrar la tabla por su ID
        table = soup.find('table', id=table_id)

        if table:
            # Obtener el nombre de la tabla de su caption
            caption = table.find('caption')
            table_name = caption.text.strip() if caption else 'Unknown_Table'

            # Leer la tabla directamente con pandas, manejando encabezados de múltiples niveles
            table_html = str(table)
            df = pd.read_html(StringIO(table_html), header=[1, 2])[0]

            # Aplanar los encabezados de múltiples niveles
            df.columns = ['_'.join(col).strip() for col in df.columns.values]

            # Eliminar columnas duplicadas o vacías si las hay
            df = df.loc[:, ~df.columns.duplicated()]

            # Limpiar los encabezados
            df_cleaned = clean_headers(df)
            # Ajustar los valores numéricos
            df_cleaned = clean_numeric_values(df_cleaned)

            # Guardar el DataFrame en el diccionario
            all_data[table_name] = df_cleaned
            print(f"Tabla '{table_name}' extraída correctamente.")
        else:
            print(f"Tabla con ID '{table_id}' no encontrada.")

    # Guardar todas las tablas en archivos CSV
    for name, df in all_data.items():
        filename = name.replace(' ', '_').replace('/', '_').replace(':', '').lower() + '.csv'
        df.to_csv(os.path.join(file_path, filename), index=False)
        print(f"Tabla guardada como '{filename}' en '{file_path}'.")

    # Procesar todos los CSV para garantizar que los encabezados y valores estén bien formateados
    process_csv_files(file_path)  # Procesar los archivos guardados en el nuevo directorio

else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
