import pandas as pd
import numpy as np

# Cargar el dataset desde la ruta proporcionada
csv_path = 'DISEÑO ESTADISTICO Y EXPERIMENTAL/Human_Age_Prediction_Dataset.csv'
df = pd.read_csv(csv_path)

# Filtrar las columnas de interés: Género, Hipertensión y Colesterol
df = df[['Gender', 'Blood Pressure (s/d)', 'Cholesterol Level (mg/dL)', 'BMI']]

# Convertir la presión arterial en hipertensión (1 si sistólica >= 140 o diastólica >= 90, 0 en caso contrario)
df['Hypertension'] = df['Blood Pressure (s/d)'].apply(lambda x: 1 if int(x.split('/')[0]) >= 140 or int(x.split('/')[1]) >= 90 else 0)

# Crear la variable 'Cholesterol' como colesterol alto si el nivel es mayor a 200
df['Cholesterol'] = df['Cholesterol Level (mg/dL)'].apply(lambda x: 1 if x > 200 else 0)

# Filtrar el género como variable categórica (0 para mujeres, 1 para hombres)
df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

# a) Obtener la suma de cada población
suma_genero = df.groupby('Gender')['BMI'].sum()
suma_hipertension = df.groupby('Hypertension')['BMI'].sum()
suma_colesterol = df.groupby('Cholesterol')['BMI'].sum()

# b) Anotar el tamaño de cada población
tamano_genero = df.groupby('Gender')['BMI'].count()
tamano_hipertension = df.groupby('Hypertension')['BMI'].count()
tamano_colesterol = df.groupby('Cholesterol')['BMI'].count()

# c) Calcular la media de cada muestra
media_genero = df.groupby('Gender')['BMI'].mean()
media_hipertension = df.groupby('Hypertension')['BMI'].mean()
media_colesterol = df.groupby('Cholesterol')['BMI'].mean()

# d) Suma de los cuadrados de las observaciones
sum_sq_genero = df.groupby('Gender')['BMI'].apply(lambda x: np.sum(x**2))
sum_sq_hipertension = df.groupby('Hypertension')['BMI'].apply(lambda x: np.sum(x**2))
sum_sq_colesterol = df.groupby('Cholesterol')['BMI'].apply(lambda x: np.sum(x**2))

# e) Suma de cuadrados corregida (SCY), utilizando la media general de BMI
media_general = df['BMI'].mean()
SCY_genero = np.sum((df.groupby('Gender')['BMI'].mean() - media_general) ** 2 * tamano_genero)
SCY_hipertension = np.sum((df.groupby('Hypertension')['BMI'].mean() - media_general) ** 2 * tamano_hipertension)
SCY_colesterol = np.sum((df.groupby('Cholesterol')['BMI'].mean() - media_general) ** 2 * tamano_colesterol)

# f) Suma de cuadrados del error (SCE)
SCE_genero = df.groupby('Gender')['BMI'].apply(lambda x: np.sum((x - x.mean()) ** 2)).sum()
SCE_hipertension = df.groupby('Hypertension')['BMI'].apply(lambda x: np.sum((x - x.mean()) ** 2)).sum()
SCE_colesterol = df.groupby('Cholesterol')['BMI'].apply(lambda x: np.sum((x - x.mean()) ** 2)).sum()

# g) Grados de libertad
v_genero = len(df['Gender'].unique()) - 1
v_hipertension = len(df['Hypertension'].unique()) - 1
v_colesterol = len(df['Cholesterol'].unique()) - 1

v_error_genero = len(df) - len(df['Gender'].unique())
v_error_hipertension = len(df) - len(df['Hypertension'].unique())
v_error_colesterol = len(df) - len(df['Cholesterol'].unique())

# h) Cuadrados medios (SCM y CME)
SCM_genero = SCY_genero / v_genero
SCM_hipertension = SCY_hipertension / v_hipertension
SCM_colesterol = SCY_colesterol / v_colesterol

CME_genero = SCE_genero / v_error_genero
CME_hipertension = SCE_hipertension / v_error_hipertension
CME_colesterol = SCE_colesterol / v_error_colesterol

# i) Estadístico de prueba F
F_genero = SCM_genero / CME_genero
F_hipertension = SCM_hipertension / CME_hipertension
F_colesterol = SCM_colesterol / CME_colesterol

# Imprimir los resultados
print("\nSuma de cuadrados entre grupos (SCY):")
print(f"Género: {SCY_genero}")
print(f"Hipertensión: {SCY_hipertension}")
print(f"Colesterol: {SCY_colesterol}")

print("\nSuma de cuadrados del error (SCE):")
print(f"Género: {SCE_genero}")
print(f"Hipertensión: {SCE_hipertension}")
print(f"Colesterol: {SCE_colesterol}")

print("\nCuadrados medios entre grupos (SCM):")
print(f"Género: {SCM_genero}")
print(f"Hipertensión: {SCM_hipertension}")
print(f"Colesterol: {SCM_colesterol}")

print("\nCuadrados medios del error (CME):")
print(f"Género: {CME_genero}")
print(f"Hipertensión: {CME_hipertension}")
print(f"Colesterol: {CME_colesterol}")

print("\nEstadístico de prueba F:")
print(f"Género: {F_genero}")
print(f"Hipertensión: {F_hipertension}")
print(f"Colesterol: {F_colesterol}")
