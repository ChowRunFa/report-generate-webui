from py2neo import Graph

# 连接Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))

# delete_nodes_query = "MATCH (n) DETACH DELETE n"
# graph.run(delete_nodes_query)

# 查询节点数量
node_count_query = "MATCH (n) RETURN count(n) AS node_count"
node_count_result = graph.run(node_count_query).evaluate()
print("节点总数：", node_count_result)

# 查询关系数量
relationship_count_query = "MATCH ()-[r]->() RETURN count(r) AS relationship_count"
relationship_count_result = graph.run(relationship_count_query).evaluate()
print("关系总数：", relationship_count_result)