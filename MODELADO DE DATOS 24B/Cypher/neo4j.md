# Bases de Datos Basadas en Grafos neo4j

## Teoría de Grafos 

Un grafo es una colección de objetos en la que cada uno tiene una serie de relaciones con otros objetos

La tecnologia de grafos repreenta relaciones de fatos de una forma intuitiva

![alt text](images/neo4jexamples.png)

Neo4j es una base de datos nativa, dnde tneemos herramientas de desarrollo y herraientas de visualización.

El lenguaje utilzado es cypher, es declarativo y es de tipo Java.

![alt text](images/ne4j_native.png)

## Modelos Relacionales vs Modelos de Grafos

Con los modelos relacionales, las consulatas se vuelven mas costosas en el ambito computacional mientras mas grande sea la DB

![alt text](images/relacionalesvsgrafos.png)

Que es lo que utilizamos? En las bases de datos esto es lo que se coloca en caché:

En cada nodo obtener la relación y hacer match con los punteros dentro de la tabla de la base de datos.

El modelo se plantea de manera sencilla, ya que se le puede llamar que "El modelo del pizarron es nuestro modelo fisico"
Con lo cual una vez dibujado el trazo y la manera de obtener los datos de un princiipo puede conllevar muy pocos cambios.

## El modelo de grafo de propiedades

### ¿Qué contienen?

- Nodos
    - Pueden tener etiquetas para clasificarse
    - Las etiquetas tienen indices nativos
- Relaciones
    - Relacionan nodos por tipo y direccion
- Propiedades
    - Atributos de nodos y relaciones
    - Persistidos como clave/valor
    - Pueden tener índices o índices compuestos

![alt text](images/propiedadesGRAFOS.png)

## ¿Qué es CYPHER?

Es un lenguaje de consulta potente y expresivo

![alt text](images/cypher_beginner.png)

Las consultas se pueden crear de manera direccional o bidireccional utilizando las flechas de consulta hacia el lado donde exista o existan las relaciones.

## Graph Data Science

Es una ciencia de datos cuando las relaciones se importan

![alt text](images/GDS.png)

Existen distitnos tipos de algoritmos para los grafos:

![alt text](images/GDS_ALGORITHM.png)
