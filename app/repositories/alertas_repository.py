import datetime

from app.repositories.base_repository import BaseRepository

class AlertasRepository(BaseRepository):
    def consulta_alertas_qualidade(self, empresa_id: str,
                                          page_size,
                                          offset):
        query = """
            select * 
            from public.alerta_qualidade_dados
            where 1=1
            and empresa_id = %s
            limit %s
            OFFSET %s
        """

        return self.execute_query(
            query,
            (
                empresa_id,
                page_size,
                offset
            )
        )

if __name__== '__main__':
    repository = AlertasRepository()
    dcliente = repository.consulta_alertas_qualidade('75cc9dc2-7cf4-49e2-b21c-c285d50af99d', 10, 0)
    print(dcliente)