MATCH (m:Medium {type: "video"}) RETURN COUNT((:Comment)-[:COMMENTED_ON_MEDIA]->(m)) // 1985
MATCH (m:Medium {type: "image"}) RETURN COUNT((:Comment)-[:COMMENTED_ON_MEDIA]->(m)) // 187
MATCH (m:Medium {type: "sidecar"}) RETURN COUNT((:Comment)-[:COMMENTED_ON_MEDIA]->(m)) // 139