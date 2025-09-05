# Clustering

el clustering es la capacidad de diferenciar grupos de datos en función de características similares. Este proceso permite identificar patrones y estructuras dentro de grandes conjuntos de información, facilitando la toma de decisiones y la generación de conocimiento a partir de los datos analizados.

## puntos basicos para desempeñar una tarea de clustering es

1. seleccion de caracteristicas
2. eleccion de medida de proximidad
3. seleccion de criterio de clustering
4. seleccion de algoritmo de clustering
5. validacion de resultados
6. interpretacion de resultados

## aplicaciones del analisis de clusteres

1. reducir datos
2. generacion de hipotesis
3. testeo de hipotesis
4. prediccion en base a grupos

## definiciones de clustering

siendo x = {x1, x2, ..., xn} un conjunto de datos

definimos un cluster de X, R como un subconjunto de X tal que:

1. R no está vacío.
2. Para todo xi, xj en R, la similitud entre xi y xj es mayor que un umbral predefinido.
3. Para todo xi en R y xk en X \ R, la similitud entre xi y xk es menor que un umbral predefinido.
4. i es igual al número de subconjuntos en R.
5. la interseccion de 2 conjuntos R1 y R2 debe ser vacía. aplica solo para hard clustering
6. i no puede ser igual a j.

Esto implica que los elementos dentro de un clúster son más similares entre sí que con los de otros clústeres.

## definicion en terminos de conjuntos difusos

El clusterizado difuso permite que un elemento pertenezca a múltiples clústeres con diferentes grados de pertenencia. En lugar de asignar un elemento a un solo clúster, se le asigna un grado de pertenencia a cada clúster, lo que refleja la naturaleza difusa de la similitud entre los datos. Esto es especialmente útil en situaciones donde los límites entre clústeres no son claros o cuando los datos presentan solapamientos significativos.

Por ejemplo, en clustering difuso, la matriz de pertenencia se representa así:

|        | $C_1$         | $C_2$         | $\cdots$ | $C_k$         |
|--------|---------------|---------------|----------|---------------|
| $x_1$  | $\mu_{11}$    | $\mu_{12}$    | $\cdots$ | $\mu_{1k}$    |
| $x_2$  | $\mu_{21}$    | $\mu_{22}$    | $\cdots$ | $\mu_{2k}$    |
| $\vdots$ | $\vdots$   | $\vdots$      | $\ddots$ | $\vdots$      |
| $x_n$  | $\mu_{n1}$    | $\mu_{n2}$    | $\cdots$ | $\mu_{nk}$    |

Donde:

- $n$: número de elementos
- $k$: número de clústeres
- $\mu_{ij}$: grado de pertenencia del elemento $x_i$ al clúster $C_j$

Cada $\mu_{ij}$ toma un valor entre 0 y 1, indicando el grado de pertenencia de $x_i$ al clúster $C_j$.

## definición de disimilitud

la disimilitud en definición es una medida que cuantifica la diferencia entre dos objetos o elementos en un conjunto de datos. A diferencia de la similitud, que mide cuán parecidos son dos objetos, la disimilitud se enfoca en cuán diferentes son. Esta medida es fundamental en técnicas de análisis de datos, como el clustering, donde se busca agrupar objetos similares y separar aquellos que son distintos.

## definición de pesos por proximidad

Los pesos por proximidad son valores que se asignan a las conexiones o relaciones entre elementos en un conjunto de datos, basándose en la cercanía o similitud entre ellos. En el contexto del clustering, estos pesos pueden utilizarse para ajustar la influencia de cada elemento en la formación de clústeres, permitiendo que los algoritmos de clustering tengan en cuenta no solo la pertenencia a un clúster, sino también la fuerza de la relación entre los elementos.

Por ejemplo, en un grafo donde los nodos representan elementos y las aristas representan similitudes, los pesos por proximidad podrían ser utilizados para indicar cuán similares son dos elementos. Esto podría ayudar a mejorar la calidad del clustering al permitir que los algoritmos se centren en las relaciones más fuertes y relevantes.

- Norma Manhattan o distancia L1: mide la distancia entre dos puntos en un espacio n-dimensional sumando las diferencias absolutas de sus coordenadas. Es útil en situaciones donde se desea enfatizar las diferencias en una sola dimensión. La fórmula es: $$d(x, y) = \sum_{i=1}^{n} |x_i - y_i|$$

- Norma Euclidiana o distancia L2: mide la distancia directa entre dos puntos en un espacio n-dimensional utilizando el teorema de Pitágoras. Es la medida de distancia más comúnmente utilizada y es adecuada para datos continuos. La fórmula es: $$d(x, y) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$

- Norma de Chebyshev o distancia L∞: mide la distancia entre dos puntos en un espacio n-dimensional tomando el valor máximo de las diferencias absolutas de sus coordenadas. Es útil en situaciones donde se desea enfatizar la dimensión más diferente. La fórmula es: $$d(x, y) = \max_{i=1}^{n} |x_i - y_i|$$

- Norma de Minkowski: es una generalización de las normas anteriores y se define como: $$d(x, y) = \left( \sum_{i=1}^{n} |x_i - y_i|^p \right)^{1/p}$$ donde $p$ es un parámetro que define la norma específica (por ejemplo, $p=1$ para la norma Manhattan y $p=2$ para la norma Euclidiana).

- Distancia de Hamming: mide la diferencia entre dos cadenas de igual longitud contando el número de posiciones en las que los elementos correspondientes son diferentes. Es especialmente útil en el análisis de datos categóricos o binarios. La fórmula es: $$d(x, y) = \sum_{i=1}^{n} \mathbb{1}(x_i \neq y_i)$$ donde $\mathbb{1}$ es la función indicadora que vale 1 si $x_i \neq y_i$ y 0 en caso contrario.

- Vectores de valores mixtos: en situaciones donde los datos contienen tanto características numéricas como categóricas, se pueden utilizar medidas de disimilitud que tengan en cuenta ambos tipos de datos. Por ejemplo, se puede combinar la distancia Euclidiana para las características numéricas con la distancia de Hamming para las características categóricas, utilizando un enfoque ponderado para calcular la disimilitud total entre dos elementos. La fórmula podría ser: $$d(x, y) = \alpha \cdot d_{num}(x, y) + (1 - \alpha) \cdot d_{cat}(x, y)$$ donde $d_{num}$ es la distancia Euclidiana para las características numéricas, $d_{cat}$ es la distancia de Hamming para las características categóricas, y $\alpha$ es un peso que determina la importancia relativa de cada tipo de característica.

## Pérdida de datos

En caso de que un vector presente perdida de datos o le falle alguna característica:

1. Se puede descartar siempre y cuando el número de vectores restantes sea suficiente para mantener la validez del análisis.
2. Para cada par de componentes $x_i$ y $x_j$ en el vector, se puede calcular la disimilitud utilizando solo las características presentes en ambos vectores. Esto implica ignorar las características faltantes y centrarse en las que están disponibles para realizar el análisis.

## Funciones de proximidad

- maxima: $$d_{max}(x, y) = \max_{i=1}^{n} |x_i - y_i|$$
- minima: $$d_{min}(x, y) = \min_{i=1}^{n} |x_i - y_i|$$
- promedio: $$d_{prom}(x, y) = \frac{1}{n} \sum_{i=1}^{n} |x_i - y_i|$$

## Real Valued Vectors

Los vectores de valores reales son aquellos que contienen características numéricas continuas. En el contexto de la disimilitud y la proximidad, se pueden aplicar diversas métricas para cuantificar las diferencias entre estos vectores. Algunas de las métricas más comunes incluyen:

- Distancia Euclidiana: $$d(x, y) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$
- Distancia Manhattan: $$d(x, y) = \sum_{i=1}^{n} |x_i - y_i|$$
- Distancia de Chebyshev: $$d(x, y) = \max_{i=1}^{n} |x_i - y_i|$$

## Norma Manhattan

## Coeficiente de correlación de Pearson

## Distancia de Hamming

## Producto interno 