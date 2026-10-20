from app.core.conection_postegres_supabase import PostgreSQLConnection
from fastapi import HTTPException, status

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
        except Exception as e:
            connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao executar consulta no banco de dados: {str(e)}"
            )
        finally:
            connection.close()

if __name__ == '__main__':
    query = """
                    select em.nome as nome_empresa,
                           em.nome_fantasia,
                           em.cnpj,
                           em.email,
                           em.telefone,
                           em.status,
                           em.usa_whatsapp
                    from public.empresas em
                    where 1=1
                    and em.id = %s
                """
    repository = BaseRepository()

    dados = repository.execute_query(query, ('75cc9dc2-7cf4-49e2-b21c-c285d50af99s',))
    print(dados)