import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

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

# Paso 5: Eliminar más variables con baja variabilidad o alta correlación
# Para simplificar el modelo, eliminamos algunas variables más
variables_a_eliminar = ['Weight_(kg)', 'Hearing_Ability_(dB)', 'Vision_Sharpness', 
                        'Smoking_Status', 'Pollution_Exposure', 'Sun_Exposure']
df = df.drop(columns=variables_a_eliminar)

# Paso 6: Crear la fórmula ANOVA con las variables corregidas
formula = ('Age ~ C(Gender) + C(Hypertension) + C(Cholesterol) + C(Physical_Activity_Level) + '
           'BMI + C(Alcohol_Consumption) + C(Diet) + C(Chronic_Diseases) + '
           'C(Mental_Health_Status) + C(Education_Level) + C(Income_Level)')

# Paso 7: Construir el modelo ANOVA utilizando la fórmula simplificada
model = ols(formula, data=df).fit()

# Paso 8: Realizar la prueba ANOVA y obtener la tabla ANOVA
anova_table = sm.stats.anova_lm(model, typ=2)

# Paso 9: Imprimir la tabla ANOVA
print("\n--- Cálculo de ANOVA para las variables corregidas ---\n")
print(anova_table)

# Paso 10: Explicar los valores clave
# a) Suma de cuadrados entre los grupos (SCG)
print(f"Suma de cuadrados entre los grupos (SCG) para cada variable:\n{anova_table['sum_sq']}")

# b) Grados de libertad (df)
print(f"Grados de libertad (df) para cada variable:\n{anova_table['df']}")

# c) Cuadrados medios (SCM)
anova_table['mean_sq'] = anova_table['sum_sq'] / anova_table['df']
print(f"Cuadrados medios (SCM) para cada variable:\n{anova_table['mean_sq']}")

# d) Estadístico F
anova_table['F_calculated'] = anova_table['mean_sq'] / (anova_table['sum_sq']['Residual'] / anova_table['df']['Residual'])
print(f"Estadístico F calculado para cada variable:\n{anova_table['F_calculated']}")

# e) Valor p
print(f"Valores p para cada variable:\n{anova_table['PR(>F)']}")

# f) Cálculo del valor crítico de F
from scipy.stats import f

# Grados de libertad entre los grupos (v1) y dentro de los grupos (v2)
df_between = anova_table['df'].dropna().sum() - anova_table['df']['Residual']
df_within = anova_table['df']['Residual']
alpha = 0.05
f_critical = f.ppf(1 - alpha, df_between, df_within)

print(f"\nValor crítico de F con un nivel de significancia de {alpha}: {f_critical}")

# g) Comparar el estadístico F con el valor crítico
anova_table['Significant'] = anova_table['F_calculated'] > f_critical
print(f"\n¿Son los factores significativos (F_calculado > F_critico)?\n{anova_table['Significant']}")
