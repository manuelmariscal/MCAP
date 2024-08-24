# ¿Qué son los Joins y cómo se utilizan?

Los `JOIN` son una operación en SQL que permite combinar filas de dos o más tablas basadas en una columna relacionada entre ellas. Este proceso es fundamental para manejar bases de datos relacionales, ya que facilita la recuperación de datos distribuidos en diferentes tablas.

## Tipos de Joins

1. **Inner Join**  
   El `INNER JOIN` devuelve las filas que tienen coincidencias en ambas tablas. Solo se devuelven las filas donde hay una coincidencia en las columnas especificadas en ambas tablas.

   **Sintaxis**:
   ```sql
   SELECT column_name(s)
   FROM table1
   INNER JOIN table2
   ON table1.column_name = table2.column_name;
   ```

   **Ejemplo**:
   Supongamos que tienes una tabla de `customers` y una tabla de `orders`. Para obtener una lista de todos los clientes que han realizado pedidos:

   ```sql
   SELECT customers.first_name, orders.order_date
   FROM customers
   INNER JOIN orders
   ON customers.id = orders.customer_id;
   ```

2. **Left Join (Left Outer Join)**  
   El `LEFT JOIN` devuelve todas las filas de la tabla de la izquierda (`table1`), y las filas coincidentes de la tabla de la derecha (`table2`). Si no hay coincidencia, las filas de la tabla de la izquierda todavía se muestran con `NULL` en las columnas de la tabla de la derecha.

   **Sintaxis**:
   ```sql
   SELECT column_name(s)
   FROM table1
   LEFT JOIN table2
   ON table1.column_name = table2.column_name;
   ```

   **Ejemplo**:
   Para obtener una lista de todos los clientes, independientemente de si han realizado un pedido o no:

   ```sql
   SELECT customers.first_name, orders.order_date
   FROM customers
   LEFT JOIN orders
   ON customers.id = orders.customer_id;
   ```

3. **Right Join (Right Outer Join)**  
   El `RIGHT JOIN` es similar al `LEFT JOIN`, pero devuelve todas las filas de la tabla de la derecha (`table2`), y las filas coincidentes de la tabla de la izquierda (`table1`). Si no hay coincidencia, las filas de la tabla de la derecha todavía se muestran con `NULL` en las columnas de la tabla de la izquierda.

   **Sintaxis**:
   ```sql
   SELECT column_name(s)
   FROM table1
   RIGHT JOIN table2
   ON table1.column_name = table2.column_name;
   ```

   **Ejemplo**:
   Si quieres obtener una lista de todos los pedidos, incluyendo aquellos que no tienen un cliente registrado:

   ```sql
   SELECT customers.first_name, orders.order_date
   FROM customers
   RIGHT JOIN orders
   ON customers.id = orders.customer_id;
   ```

### Joins Implícitos vs. Joins Explícitos

SQL permite realizar joins de dos maneras: de forma implícita y de forma explícita. Ambos métodos son funcionalmente equivalentes, pero el uso explícito es generalmente más claro y preferido por su legibilidad.

1. **Join Implícito**  
   En un join implícito, las tablas se listan en la cláusula `FROM`, separadas por comas, y las condiciones de join se especifican en la cláusula `WHERE`. Este estilo es menos claro ya que mezcla las condiciones de filtrado y de unión.

   **Sintaxis de Join Implícito**:
   ```sql
   SELECT *
   FROM A, B
   WHERE A.id = B.id;
   ```

   **Ejemplo con Tablas A y B**:
   ```sql
   SELECT *
   FROM customers, orders
   WHERE customers.id = orders.customer_id;
   ```

2. **Join Explícito**  
   Un join explícito usa las palabras clave `JOIN` y `ON` para especificar la tabla y las condiciones de unión, respectivamente. Este método es más claro ya que separa claramente las condiciones de unión de las condiciones de filtrado.

   **Sintaxis de Join Explícito**:
   ```sql
   SELECT *
   FROM A
   JOIN B
   ON A.id = B.id;
   ```

   **Ejemplo con Tablas A y B**:
   ```sql
   SELECT *
   FROM customers
   JOIN orders
   ON customers.id = orders.customer_id;
   ```

### Ejemplo de Consulta Avanzada con Joins

A continuación se muestra un ejemplo de cómo usar un join para calcular cuánto ha gastado cada cliente en total, ordenando los resultados por la cantidad total gastada en orden descendente:

```sql
SELECT
    first_name,
    last_name,
    SUM(amount) AS total_spent
FROM customers
JOIN orders
    ON customers.id = orders.customer_id
GROUP BY orders.customer_id
ORDER BY total_spent DESC;
```

**Explicación de la Consulta**:

- **JOIN**: La consulta combina las tablas `customers` y `orders` utilizando la columna `customer_id` para encontrar las órdenes relacionadas con cada cliente.
- **SUM(amount) AS total_spent**: La función de agregado `SUM()` suma el valor de todas las órdenes (`amount`) para cada cliente, y se usa un alias `total_spent` para dar un nombre claro a la columna resultante.
- **GROUP BY orders.customer_id**: Agrupa los resultados por el identificador de cliente, asegurando que la suma de los gastos se calcule por cada cliente individual.
- **ORDER BY total_spent DESC**: Ordena los resultados por la cantidad total gastada en orden descendente, mostrando primero a los clientes que han gastado más.

Este tipo de consulta es útil para realizar análisis de ventas y comprender mejor el comportamiento de compra de los clientes.
