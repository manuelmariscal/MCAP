import pandas as pd
from scipy.stats import binom
from math import comb

# Paso 1: Establecer los parámetros
n = 100     # Tamaño de la muestra
p = 0.35    # Probabilidad de éxito (evento favorable)
q = 0.65    # Probabilidad de fracaso (evento desfavorable)
N = 12      # Número total de observaciones para calcular E(N)

# Lista para almacenar los resultados
resultados = []

for y in range(n + 1):
    C = comb(n, y)           # Cálculo de combinaciones C(n, y)
    p_y = p ** y             # p^Y
    q_n_y = q ** (n - y)     # q^(n - Y)
    P_Y = C * p_y * q_n_y    # Probabilidad P(Y)
    E_N = P_Y * N            # Valor esperado E(N) para N observaciones
    Aprox_Y = round(E_N)     # Aproximación entera de E(N)
    
    resultados.append({
        'Y': y,
        'C(8, Y)': C,
        'p^Y': p_y,
        'q^(n-Y)': q_n_y,
        'P(Y)': P_Y,
        'E(N) N=12': E_N,
        'Approx. Y': Aprox_Y
    })

# Crear el DataFrame con las columnas en el orden deseado
tabla_probabilidades = pd.DataFrame(resultados)
tabla_probabilidades = tabla_probabilidades[['Y', 'C(8, Y)', 'p^Y', 'q^(n-Y)', 'P(Y)', 'E(N) N=12', 'Approx. Y']]

# Redondear las columnas numéricas para mejorar la legibilidad
tabla_probabilidades['p^Y'] = tabla_probabilidades['p^Y'].round(6)
tabla_probabilidades['q^(n-Y)'] = tabla_probabilidades['q^(n-Y)'].round(6)
tabla_probabilidades['P(Y)'] = tabla_probabilidades['P(Y)'].round(6)
tabla_probabilidades['E(N) N=12'] = tabla_probabilidades['E(N) N=12'].round(6)

# Mostrar la tabla
print(tabla_probabilidades)

# Exportar la tabla a Excel
tabla_probabilidades.to_excel('tabla_probabilidades.xlsx', index=False)
