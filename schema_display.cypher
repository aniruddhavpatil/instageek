MERGE (a1:account {name: "IUB_account"})
MERGE (a2:account {name: "IUB_follower"})
MERGE (m:medium {name: "Medium"})
MERGE (c:comment {name: "Comment"})
MERGE (a1)-[:POSTED]->(m)
MERGE (c)-[:COMMENTED_ON_MEDIA]->(m)
MERGE (a2)-[:COMMENTED]->(c)
MERGE (a2)-[:FOLLOWS]->(a1)