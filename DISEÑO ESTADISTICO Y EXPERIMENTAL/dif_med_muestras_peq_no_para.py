import pandas as pd
import numpy as np
from scipy.stats import rankdata

# Cargar los datos desde el archivo CSV
csv_path = 'DISEÑO ESTADISTICO Y EXPERIMENTAL/Human_Age_Prediction_Dataset.csv'
df = pd.read_csv(csv_path)

# Extraer la columna de pesos
weights = df['Weight (kg)']

# Para este ejemplo, usaremos n1 = 10 y n2 = 12
n1 = 10
n2 = 12

# Seleccionar las muestras (puedes ajustar cómo seleccionas estas muestras según tu análisis)
sample1 = weights.sample(n=n1, random_state=42)
sample2 = weights.sample(n=n2, random_state=24)

# Unir las dos muestras y calcular los rangos
combined_samples = np.concatenate([sample1, sample2])
ranks = rankdata(combined_samples)

# Dividir los rangos entre las dos muestras
ranks_sample1 = ranks[:n1]
ranks_sample2 = ranks[n1:]

# Calcular los rangos sumados para cada muestra
r1 = np.sum(ranks_sample1)  # Suma de los rangos de la primera muestra
r2 = np.sum(ranks_sample2)  # Suma de los rangos de la segunda muestra

# Cálculo de U1 y U2 usando las fórmulas proporcionadas
U1 = n1 * n2 + (n1 * (n1 + 1)) / 2 - r1
U2 = n1 * n2 + (n2 * (n2 + 1)) / 2 - r2

# Crear un DataFrame para mostrar los pesos y sus respectivos rangos
# Para manejar el problema de longitudes diferentes, ajustamos el tamaño
max_len = max(n1, n2)
sample1_values = list(sample1.values) + [np.nan] * (max_len - n1)
sample2_values = list(sample2.values) + [np.nan] * (max_len - n2)
ranks_sample1_values = list(ranks_sample1) + [np.nan] * (max_len - n1)
ranks_sample2_values = list(ranks_sample2) + [np.nan] * (max_len - n2)

ranks_df = pd.DataFrame({
    'Sample 1 (Peso)': sample1_values,
    'Rank Sample 1': ranks_sample1_values,
    'Sample 2 (Peso)': sample2_values,
    'Rank Sample 2': ranks_sample2_values
})

# Mostrar los resultados
print(f"Suma de rangos para la muestra 1 (r1): {r1}")
print(f"Suma de rangos para la muestra 2 (r2): {r2}")
print(f"U1: {U1}")
print(f"U2: {U2}")

# Imprimir el DataFrame con los pesos y los rangos
print("\nPesos y rangos correspondientes:")
print(ranks_df)
