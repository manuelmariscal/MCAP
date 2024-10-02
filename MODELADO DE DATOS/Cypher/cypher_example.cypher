// Connect to the Neo4j database
CALL dbms.connect('bolt://localhost:7687', 'username', 'password') YIELD connection AS conn

// Create a new node with a label and properties
CREATE (n:Person {name: 'John', age: 30, city: 'New York'})

// Create a relationship between two nodes
MATCH (a:Person {name: 'John'}), (b:Person {name: 'Jane'})
CREATE (a)-[:FRIEND]->(b)

// Retrieve all nodes with a specific label
MATCH (n:Person)
RETURN n

// Retrieve nodes with a specific property value
MATCH (n:Person {age: 30})
RETURN n

// Retrieve nodes connected by a specific relationship
MATCH (a)-[:FRIEND]->(b)
RETURN a, b

// Update a node's property value
MATCH (n:Person {name: 'John'})
SET n.age = 35

// Delete a node and its relationships
MATCH (n:Person {name: 'John'})
DETACH DELETE n

// Create additional nodes with more fields
CREATE (n1:Person {name: 'Alice', age: 25, city: 'London'})
CREATE (n2:Person {name: 'Bob', age: 35, city: 'Paris'})
CREATE (n3:Person {name: 'Charlie', age: 28, city: 'Berlin'})
CREATE (n4:Person {name: 'David', age: 32, city: 'Tokyo'})
CREATE (n5:Person {name: 'Eve', age: 29, city: 'Sydney'})
CREATE (n6:Person {name: 'Frank', age: 31, city: 'Los Angeles'})
CREATE (n7:Person {name: 'Grace', age: 27, city: 'Toronto'})

// Create random relationships between nodes
MATCH (a:Person), (b:Person)
WHERE a <> b AND rand() < 0.5
CREATE (a)-[:FRIEND]->(b)