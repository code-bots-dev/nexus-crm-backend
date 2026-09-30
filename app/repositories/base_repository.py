from app.core.conection_postegres_supabase import PostgreSQLConnection

class BaseRepository:
    def __init__(self):
        self.database = PostgreSQLConnection()

    def execute_query(self, query, params=None):
        connection = self.database.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                if cursor.description:
                    colunas = [desc[0] for desc in cursor.description]
                    return [
                        dict(zip(colunas, row))
                        for row in cursor.fetchall()
                    ]
                return None
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()