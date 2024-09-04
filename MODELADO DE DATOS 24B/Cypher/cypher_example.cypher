Neo4j - Basics

202x/<MM>/<DD>


# ################

# Cypher ASCII Art

# ################

MATCH (p2:Person {name: "Tom Hanks"}) RETURN p2

MATCH ()-[a4:ACTED_IN {roles: ["Mr. White"]}]-() RETURN a4

MATCH (x)-[a4:ACTED_IN {roles: ["Mr. White"]}]-(y) RETURN x.name, x.title, a4.roles, y.name, y.title


# ###########

# Lock & Load

# ###########

:USE system;

CREATE DATABASE movies;


:USE movies;


LOAD CSV FROM 'https://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN count(*);


LOAD CSV FROM 'file:///movies/basics/movies.csv'

AS row

RETURN count(*);


LOAD CSV FROM 'https://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN * LIMIT 5;


LOAD CSV FROM 'file:///movies/basics/movies.csv'

AS row

RETURN * LIMIT 5;


LOAD CSV WITH HEADERS FROM 'https://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN row, keys(row) LIMIT 5;


LOAD CSV WITH HEADERS FROM 'file:///movies/basics/movies.csv'

AS row

RETURN row, keys(row) LIMIT 5;


LOAD CSV WITH HEADERS FROM 'https://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN row.title as title, toInteger(row.released) as released, row.tagline as tagline

ORDER BY released DESC LIMIT 10;


// constraints (schema in other words)

CREATE CONSTRAINT ON (m:Movie) ASSERT m.title IS UNIQUE;

CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE;


// load … and by all means try it multiple times

LOAD CSV WITH HEADERS FROM 'https://data.neo4j.com/intro/movies/movies.csv'

AS row

CREATE (m:Movie {title: row.title, released: toInteger(row.released), tagline: row.tagline});


// verify

MATCH (m:Movie) RETURN count(*);


// load

LOAD CSV WITH HEADERS FROM 'https://data.neo4j.com/intro/movies/people.csv'

AS row

CREATE (p:Person {name: row.name, born: toInteger(row.born)});

// verify

MATCH (p:Person) RETURN count(*);


// load

LOAD CSV WITH HEADERS FROM 'https://data.neo4j.com/intro/movies/actors.csv'

AS row

MATCH (p:Person {name: row.person })

MATCH (m:Movie {title: row.movie})

MERGE (p)-[actedIn:ACTED_IN]->(m)

ON CREATE SET actedIn.roles = split(row.roles,';');


// verify

MATCH(p:Person {name: "Tom Hanks"})-[a:ACTED_IN]-(m:Movie) RETURN p,a,m;


// load

LOAD CSV WITH HEADERS FROM 'https://data.neo4j.com/intro/movies/directors.csv' AS row

MATCH (p:Person {name: row.person })

MATCH (m:Movie {title: row.movie})

MERGE (p)-[:DIRECTED]->(m);


// verify

MATCH(p:Person {name: "Tom Hanks"})-[d:DIRECTED]-(m:Movie) RETURN p,d,m;



# ######

# Cypher

# ######

// Finding Tom

MATCH (p:Person {name: "Tom Hanks"})

RETURN p;

// Finding Tom too

MATCH (p:Person)

WHERE p.name = "Tom Hanks"

RETURN p;


// analyzing finding Tom

PROFILE MATCH (p:Person {name: "Tom Hanks"})

RETURN p;


// analyzing finding Tom too

PROFILE MATCH (p:Person)

WHERE p.name = "Tom Hanks"

RETURN p;


// analyzing without finding Tom

EXPLAIN MATCH (p:Person {name: "Tom Hanks"})

RETURN p;


// analyzing without finding Tom too

EXPLAIN MATCH (p:Person)

WHERE p.name = "Tom Hanks"

RETURN p;


// Did Tom act with Tom ?

MATCH (p1:Person)-[a1:ACTED_IN]-(m:Movie)-[a2:ACTED_IN]-(p2:Person)

WHERE p1.name = "Tom Hanks"

AND p2.name = "Tom Cruise"

RETURN p1.name, a1.roles, p2.name, a2.roles, m.title;


// Create myself as a trainer ...

CREATE (t:Trainer {name: "<name trainer>"});


// cleanup

MATCH (t:Trainer) DETACH DELETE t;


// constraint (= schema)

CREATE CONSTRAINT ON (t:Trainer)

ASSERT t.name IS UNIQUE;


// create myself as the trainer

CREATE (:Trainer {name: "<name trainer>"});


// constraint (= schema)

CREATE CONSTRAINT ON (t:Training)

ASSERT t.title IS UNIQUE;


// create the training

CREATE (t:Training {title: "Basics"});


// create the relationship

MATCH (t:Training {title: "Basics"})

MATCH (tr:Trainer {name: "<name trainer>"})

MERGE (tr)-[te:TEACHES {location: "Online", date: "<date training>"}]->(t)

RETURN tr,te,t;


// What exactly am I doing here ?

MATCH (tr:Trainer {name: "Luis Salvador"})-[t:TEACHES]->(f:Training {title: "Basics"})

SET tr.age = <age trainer>, t.time = "<start time training>", f.duration = "02h00"

RETURN tr, t, f;



# ############################

# Return with a recommendation

# ############################


// Who should play with Tom

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m1)<-[:ACTED_IN]-(coActors:Person)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors:Person)

WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors)

AND tom <> cocoActors

RETURN cocoActors.name AS Recommended, count(*) AS Strength ORDER BY Strength DESC;


// Who should play with Tom (why it's wrong)

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m1)<-[:ACTED_IN]-(coActors:Person)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors:Person)

WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors)

AND tom <> cocoActors

RETURN cocoActors.name AS Recommended, collect(coActors.name) as thisiswrong, count(*) AS Strength ORDER BY Strength DESC;


// Who should play with Tom (improved)

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m1)<-[:ACTED_IN]-(coActors:Person)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors:Person)

WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors)

AND tom <> cocoActors

RETURN cocoActors.name AS Recommended, collect(DISTINCT coActors.name), count(DISTINCT coActors.name) AS Strength ORDER BY Strength DESC;



—------------------------------


Plain text version


—-------------------------------


Neo4j Webinar Spain - Basics

202x/<MM>/<DD>

 

# ################

# Cypher ASCII Art

# ################

MATCH (p2:Person {name: "Tom Hanks"}) RETURN p2

MATCH ()-[a4:ACTED_IN {roles: ["Mr. White"]}]-() RETURN a4

MATCH (x)-[a4:ACTED_IN {roles: ["Mr. White"]}]-(y) RETURN x.name, x.title, a4.roles, y.name, y.title

 

# ###########

# Lock & Load

# ###########

:USE system;

CREATE DATABASE movies;

 

:USE movies;

 

LOAD CSV FROM 'http://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN count(*);

 

LOAD CSV FROM 'file:///movies/basics/movies.csv'

AS row

RETURN count(*);

 

LOAD CSV FROM 'http://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN * LIMIT 5;

 

LOAD CSV FROM 'file:///movies/basics/movies.csv'

AS row

RETURN * LIMIT 5;

 

LOAD CSV WITH HEADERS FROM 'http://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN row, keys(row) LIMIT 5;

 

LOAD CSV WITH HEADERS FROM 'file:///movies/basics/movies.csv'

AS row

RETURN row, keys(row) LIMIT 5;

 

LOAD CSV WITH HEADERS FROM 'http://data.neo4j.com/intro/movies/movies.csv'

AS row

RETURN row.title as title, toInteger(row.released) as released, row.tagline as tagline

ORDER BY released DESC LIMIT 10;

 

// constraints (schema in other words)

CREATE CONSTRAINT ON (m:Movie) ASSERT m.title IS UNIQUE;

CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE;

 

// load … and by all means try it multiple times

LOAD CSV WITH HEADERS FROM 'http://data.neo4j.com/intro/movies/movies.csv'

AS row

CREATE (m:Movie {title: row.title, released: toInteger(row.released), tagline: row.tagline});

 

// verify

MATCH (m:Movie) RETURN count(*);

 

// load

LOAD CSV WITH HEADERS FROM 'http://data.neo4j.com/intro/movies/people.csv'

AS row

CREATE (p:Person {name: row.name, born: toInteger(row.born)});

// verify

MATCH (p:Person) RETURN count(*);

 

// load

LOAD CSV WITH HEADERS FROM 'http://data.neo4j.com/intro/movies/actors.csv'

AS row

MATCH (p:Person {name: row.person })

MATCH (m:Movie {title: row.movie})

MERGE (p)-[actedIn:ACTED_IN]->(m)

ON CREATE SET actedIn.roles = split(row.roles,';');

 

// verify

MATCH(p:Person {name: "Tom Hanks"})-[a:ACTED_IN]-(m:Movie) RETURN p,a,m;

 

// load

LOAD CSV WITH HEADERS FROM 'http://data.neo4j.com/intro/movies/directors.csv' AS row

MATCH (p:Person {name: row.person })

MATCH (m:Movie {title: row.movie})

MERGE (p)-[:DIRECTED]->(m);

 

// verify

MATCH(p:Person {name: "Tom Hanks"})-[d:DIRECTED]-(m:Movie) RETURN p,d,m;

 

 

# ######

# Cypher

# ######

// Finding Tom

MATCH (p:Person {name: "Tom Hanks"})

RETURN p;

// Finding Tom too

MATCH (p:Person)

WHERE p.name = "Tom Hanks"

RETURN p;

 

// analyzing finding Tom

PROFILE MATCH (p:Person {name: "Tom Hanks"})

RETURN p;

 

// analyzing finding Tom too

PROFILE MATCH (p:Person)

WHERE p.name = "Tom Hanks"

RETURN p;

 

// analyzing without finding Tom

EXPLAIN MATCH (p:Person {name: "Tom Hanks"})

RETURN p;

 

// analyzing without finding Tom too

EXPLAIN MATCH (p:Person)

WHERE p.name = "Tom Hanks"

RETURN p;

 

// Did Tom act with Tom ?

MATCH (p1:Person)-[a1:ACTED_IN]-(m:Movie)-[a2:ACTED_IN]-(p2:Person)

WHERE p1.name = "Tom Hanks"

AND p2.name = "Tom Cruise"

RETURN p1.name, a1.roles, p2.name, a2.roles, m.title;

 

// Create myself as a trainer ...

CREATE (t:Trainer {name: "<name trainer>"});

 

// cleanup

MATCH (t:Trainer) DETACH DELETE t;

 

// constraint (= schema)

CREATE CONSTRAINT ON (t:Trainer)

ASSERT t.name IS UNIQUE;

 

// create myself as the trainer

CREATE (:Trainer {name: "<name trainer>"});

 

// constraint (= schema)

CREATE CONSTRAINT ON (t:Training)

ASSERT t.title IS UNIQUE;

 

// create the training

CREATE (t:Training {title: "Basics"});

 

// create the relationship

MATCH (t:Training {title: "Basics"})

MATCH (tr:Trainer {name: "<name trainer>"})

MERGE (tr)-[te:TEACHES {location: "Online", date: "<date training>"}]->(t)

RETURN tr,te,t;

 

// What exactly am I doing here ?

MATCH (tr:Trainer {name: "Luis Salvador"})-[t:TEACHES]->(f:Training {title: "Basics"})

SET tr.age = <age trainer>, t.time = "<start time training>", f.duration = "02h00"

RETURN tr, t, f;

 

 

# ############################

# Return with a recommendation

# ############################

 

// Who should play with Tom

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m1)<-[:ACTED_IN]-(coActors:Person)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors:Person)

WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors)

AND tom <> cocoActors

RETURN cocoActors.name AS Recommended, count(*) AS Strength ORDER BY Strength DESC;

 

// Who should play with Tom (why it's wrong)

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m1)<-[:ACTED_IN]-(coActors:Person)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors:Person)

WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors)

AND tom <> cocoActors

RETURN cocoActors.name AS Recommended, collect(coActors.name) as thisiswrong, count(*) AS Strength ORDER BY Strength DESC;

 

// Who should play with Tom (improved)

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m1)<-[:ACTED_IN]-(coActors:Person)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors:Person)

WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors)

AND tom <> cocoActors

RETURN cocoActors.name AS Recommended, collect(DISTINCT coActors.name), count(DISTINCT coActors.name) AS Strength ORDER BY Strength DESC;

 

 


