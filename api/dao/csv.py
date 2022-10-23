from api import NotFoundException


class CsvDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """

    def __init__(self, driver):
        self.driver = driver

    """
    This method should return a paginated list of People (actors or directors),
    with an optional filter on the person's name based on the `q` parameter.

    Results should be ordered by the `sort` parameter and limited to the
    number passed as `limit`.  The `skip` variable should be used to skip a
    certain number of rows.
    """

    # tag::all[]
    def all(self, q, sort='name', order='ASC', limit=6, skip=0):
        # Get a list of people from the database
        def get_all_people(tx, q, sort, order, limit, skip):
            cypher = "MATCH (p:Person) "

            # If q is set, use it to filter on the name property
            if q is not None:
                cypher += "WHERE p.name CONTAINS $q"
            # Remember to use double braces to replace the braces in the Cypher query {{ }}
            cypher += """
            RETURN p {{ .* }} AS person
            ORDER BY p.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            result = tx.run(cypher, q=q, sort=sort, order=order, limit=limit, skip=skip)

            return [row.get("person") for row in result]

        with self.driver.session() as session:
            return session.read_transaction(get_all_people, q, sort, order, limit, skip)

    # end::all[]

    """
    Find a user by their ID.

    If no user is found, a NotFoundError should be thrown.
    """

    # tag::findById[]
    def find_by_id(self, id):
        # Find a user by their ID
        def get_person(tx, id):
            row = tx.run("""
                MATCH (p:Person {tmdbId: $id})
                RETURN p {
                    .*,
                    actedCount: size((p)-[:ACTED_IN]->()),
                    directedCount: size((p)-[:DIRECTED]->())
                } AS person
            """, id=id).single()

            if row == None:
                raise NotFoundException()

            return row.get("person")

        with self.driver.session() as session:
            return session.read_transaction(get_person, id)

    # end::findById[]

    """
    Get a list of similar people to a Person, ordered by their similarity score
    in descending order.
    """

    # tag::getSimilarPeople[]
    def get_similar_people(self, id, limit=6, skip=0):
        # Get a list of similar people to the person by their id
        def get_similar_people(tx, id, skip, limit):
            result = tx.run("""
                MATCH (:Person {tmdbId: $id})-[:ACTED_IN|DIRECTED]->(m)<-[r:ACTED_IN|DIRECTED]-(p)
                RETURN p {
                    .*,
                    actedCount: size((p)-[:ACTED_IN]->()),
                    directedCount: size((p)-[:DIRECTED]->()),
                    inCommon: collect(m {.tmdbId, .title, type: type(r)})
                } AS person
                ORDER BY size(person.inCommon) DESC
                SKIP $skip
                LIMIT $limit
            """, id=id, skip=skip, limit=limit)

            return [row.get("person") for row in result]

        with self.driver.session() as session:
            return session.read_transaction(get_similar_people, id, skip, limit)

    # end::getSimilarPeople[]

    def load_csv(self, db_name, csv_file, limit):
        # Create a Session for the `db_name` database
        session = self.driver.session(database=db_name)

        def load_csv_work(tx, csv_file, limit):
            cypher = """
                        LOAD CSV WITH HEADERS FROM 'file:///$csv_file' AS row
                        RETURN row 
                        LIMIT $limit
                """
            return tx.run(cypher, csv_file=csv_file, limit=limit)

        # Create a node within a write transaction
        record = session.write_transaction(load_csv_work, csv_file, limit).single()

        # Get the `source` values from record
        source = record["source"]

        # Close the session
        session.close()

        # Return the property from the node
        return source
