import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Paso 1: Cargar el dataset
csv_path = 'DISEÑO ESTADISTICO Y EXPERIMENTAL/Human_Age_Prediction_Dataset.csv'
df = pd.read_csv(csv_path)

# Paso 2: Renombrar la columna 'Age (years)' a 'Age' si es necesario
df.rename(columns={'Age (years)': 'Age'}, inplace=True)

# Paso 3: Crear variables adicionales necesarias
df['Hypertension'] = df['Blood Pressure (s/d)'].apply(lambda x: 1 if int(x.split('/')[0]) >= 140 or int(x.split('/')[1]) >= 90 else 0)
df['Cholesterol'] = df['Cholesterol Level (mg/dL)'].apply(lambda x: 1 if x > 200 else 0)
df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

# Paso 4: Reemplazar espacios en los nombres de las columnas por guiones bajos
df.columns = df.columns.str.replace(' ', '_')

# Paso 5: Convertir variables categóricas a numéricas si no lo están ya (esto es necesario para el análisis de correlación)
categorical_columns = ['Smoking_Status', 'Alcohol_Consumption', 'Diet', 'Chronic_Diseases', 'Medication_Use', 
                       'Family_History', 'Cognitive_Function', 'Mental_Health_Status', 'Sleep_Patterns', 
                       'Stress_Levels', 'Pollution_Exposure', 'Sun_Exposure', 'Education_Level', 'Income_Level']

for col in categorical_columns:
    df[col] = df[col].astype('category').cat.codes

# Paso 6: Eliminar columnas no numéricas o irrelevantes para el análisis
df_numeric = df.select_dtypes(include=[np.number])

# Paso 7: Calcular la matriz de correlación
correlation_matrix = df_numeric.corr()

# Paso 8: Visualización de la matriz de correlación
plt.figure(figsize=(14, 12))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matriz de Correlación entre Variables')
plt.show()

# Paso 9: Imprimir la matriz de correlación para identificar multicolinealidad
print("Matriz de correlación:")
print(correlation_matrix)
