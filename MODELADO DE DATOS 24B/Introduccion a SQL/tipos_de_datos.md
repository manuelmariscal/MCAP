# Tipos de Datos

Los bits son unidades binarias de la cuales podemos hacer uso de combinaciones. Los tipos de datos nos pueden dar la noción del estado de una objeto.
Estos se miden en potencias de 2, y el mas común es a la octava potencia, refiriendonos a conjuntos de 8 bits, lo cual equivale e 1 byte.

Los tipos de variables justamente representan estas correciones a las posibles ambigüedades, para tener identificado la variable par asignarle un espacio en la memoria.

## Tipos de datos en SQL

CHAR vs VARCHAR
CHAR es de tamañp fjo
VARCHAR es de tamaño variable

INT
INT son numeros enteros

DECIMAL
DECIMAL(dpigitos totales, dígitos despues del puonto)
DECIMAL(5,4)
Por ejemplo:

3.1415

CAST es una conversion temporal de un tipo de dato por ejemplo:

## Tipos de relaciones

- 1:1 - uno a uno
- 1:M - uno a muchos
- M:N - muchos a muchos

### (1:M) Órdenes y Clientes

- **Nombre y apellido del cliente**
- **Email del cliente**
- **Fecha de compra**
- **Precio de la orden de compra**

#### Usando una tabla

- ¿Qué sucede si un cliente vuelve a realizar otra orden?
- ¿Qué sucede si un cliente se registra pero no compra?

## (1:M) Órdenes y Clientes

### Customer
- *customer_id* <--
- first_name
- last_name
- email

### Order
- *order_id*
- order_date
- amount
- **customer_id** <--

**Tabla**  
*Primary Key*  
**Foreign Key**

## (1:M) Órdenes y Clientes

```sql
CREATE TABLE customers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders(
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    amount DECIMAL(8,2),
    customer_id INT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);
```


### Explicación de las Tablas

- **Tabla `customers`**: Esta tabla contiene la información básica de los clientes, como su nombre, apellido y correo electrónico. La clave primaria es `id`, que es un identificador único para cada cliente y se incrementa automáticamente.

    - **Columnas importantes**:
        - `id`: Identificador único de cada cliente.
        - `first_name` y `last_name`: Nombres y apellidos de los clientes. Útil para identificar a los clientes de manera personalizada.
        - `email`: Dirección de correo electrónico del cliente, crucial para comunicación y marketing.

    - **Columnas menos importantes**: En este caso, todas las columnas son relevantes para la identificación y contacto con el cliente. Sin embargo, podría considerarse menos relevante `first_name` o `last_name` individualmente si solo se requiere una identificación básica, pero normalmente ambos son importantes.

- **Tabla `orders`**: Esta tabla contiene información sobre las órdenes de compra realizadas por los clientes. También incluye un campo de clave foránea `customer_id` que referencia al `id` en la tabla `customers`, estableciendo así una relación uno-a-muchos (1:M) entre clientes y órdenes.

    - **Columnas importantes**:
        - `id`: Identificador único de cada orden.
        - `order_date`: Fecha en la que se realizó la orden. Es importante para análisis de comportamiento de compra a lo largo del tiempo.
        - `amount`: Cantidad monetaria de la orden, fundamental para análisis financiero y ventas.
        - `customer_id`: Relaciona cada orden con un cliente específico, esencial para rastrear las compras de cada cliente.

    - **Columnas menos importantes**: Similar a la tabla de clientes, todas las columnas son importantes para el seguimiento y análisis de órdenes. En este caso, ninguna columna puede considerarse de baja importancia ya que todas son esenciales para entender las transacciones.

### Datos de Interés

1. **Historial de compras por cliente**: Relacionando las tablas `customers` y `orders` podemos analizar cuántas órdenes ha realizado cada cliente y qué cantidad han gastado en total.
2. **Análisis de ventas por fecha**: Usando `order_date`, se pueden observar tendencias de compra, temporadas altas de ventas y patrones de comportamiento.
3. **Identificación de clientes activos vs. inactivos**: Clientes con múltiples órdenes versus aquellos que solo han registrado una cuenta sin compras (`customer_id` presente en `customers` pero no en `orders`).

### Datos Menos Relevantes

- En este esquema, cada columna aporta información clave para el propósito de gestionar clientes y órdenes. No hay datos innecesarios, pero la importancia de cada campo dependerá de las preguntas específicas que se deseen responder con los datos.
