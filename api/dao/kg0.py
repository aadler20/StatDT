import time
import pandas as pd


def insert_data(conn, query, rows):
    start = time.time()
    res = conn.query(query, {'rows': rows.to_dict('records')})
    result = {"time": time.time() - start}
    print(result)

    return result


def add_kg(rows, conn):
    # (:source)-[:edge]-(:target)
    # knot: source target
    # relation: edge
    query_string = """
        UNWIND $rows AS row
        MERGE (s:Source {name: row.source}) ON CREATE SET s.name = row.source
        MERGE (t:Target {name: row.target}) ON CREATE SET t.name = row.target
        MERGE (s)-[r:Relation {relation: row.edge}]->(t)
        RETURN count(*) as total
    """

    return insert_data(conn, query_string, rows)


def query_data(conn):
    query_string = """
        MATCH (t:Target)
        RETURN t.name, SIZE(()-[:Relation]->(t)) AS inDegree 
        ORDER BY inDegree DESC LIMIT 20
        """
    top_cat_df = pd.DataFrame([dict(_) for _ in conn.query(query_string)])
    return top_cat_df


def query_data1(conn):
    query_string = """
        MATCH (s:Source) 
        RETURN s.name, SIZE((s)-[:Relation]->()) AS inDegree 
        ORDER BY inDegree DESC LIMIT 20
        """
    result = conn.query(query_string)
    for record in result:
        print(record['s.name'], record['inDegree'])


def kg_all(conn):
    query_string = """
        MATCH (s:Source)-[r:Relation]->(t:Target) 
        RETURN s.name as source, r.relation as edge, t.name as target 
        """
    kg_df = pd.DataFrame([dict(_) for _ in conn.query(query_string)])
    return kg_df
