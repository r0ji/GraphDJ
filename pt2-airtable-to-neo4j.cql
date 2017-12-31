// AIRTABLE TO NEO4J (CYPHER)
// Loads Airtable data into Neo4J using the APOC library
// Connects songs together by key, suggesting mixing possibilities

// Constraints
CREATE CONSTRAINT ON (t:Track) ASSERT t.name IS UNIQUE;
CREATE CONSTRAINT ON (k:Key) ASSERT k.name IS UNIQUE;

// Import Favorites table (nodes)
WITH "https://api.airtable.com/v0/appXYZ/Favorites?api_key=keyXYZ" AS url_Favorites
CALL apoc.load.json(url_Favorites) YIELD value
UNWIND value.records AS track
MERGE (t:Track {name:track.fields.Name, artist: track.fields.Artist, airID:track.fields.`Spotify ID`})
FOREACH (x IN track.fields.Tempo | SET t.bpm = track.fields.Tempo)
FOREACH (x IN track.fields.CAM | SET t.CAM = track.fields.CAM)
FOREACH (x IN track.fields.uCAM | SET t.uCAM = track.fields.uCAM)
FOREACH (x IN track.fields.dCAM | SET t.dCAM = track.fields.dCAM)
FOREACH (x IN track.fields.aCAM | SET t.aCAM = track.fields.aCAM)
MERGE (k:Key {name:track.fields.CAM})
MERGE (t)-[:IN_KEY]->(k)

// RELATIONSHIPS (simple)
MATCH (t:Track), (k:Key), (ku:Key)
WHERE k.name = t.CAM AND ku.name = t.uCAM
MERGE (k)-[:MIX]-(ku)

MATCH (t:Track), (k:Key), (ka:Key)
WHERE k.name = t.CAM AND ka.name = t.aCAM
MERGE (k)-[:SWITCH]-(ka)

// RELATIONSHIPS (complex)

MATCH (t:Track), (k:Key), (ku:Key)
WHERE k.name = t.CAM AND ku.name = t.uCAM
MERGE (k)-[:MIX_UP]->(ku)

MATCH (t:Track), (k:Key), (kd:Key)
WHERE k.name = t.CAM AND kd.name = t.dCAM
MERGE (k)-[:MIX_DOWN]->(kd)

MATCH (t:Track), (k:Key), (ka:Key)
WHERE k.name = t.CAM AND ka.name = t.aCAM
MERGE (k)-[:MIX_ACROSS]->(ka)

// NOTES BELOW

// Create subl symlink
// $ ln -s "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl" /usr/local/bin/subl

// Authorize APOC commands
// $ subl /Users/rojwan/Documents/Neo4j/.neo4j.conf
// add line: dbms.security.procedures.unrestricted=apoc.*

// DROP TABLE: MATCH (n) DETACH DELETE n
// DROP SCHEMA: CALL apoc.schema.assert({}, {})
// DROP ALL : MATCH (n) DETACH DELETE n ; CALL apoc.schema.assert({}, {})
