from app.repositories.alertas_repository import AlertasRepository
import datetime


class AlertasService():
    def __init__(self):
        self.repository = AlertasRepository()

    def listar_alertas_qualidade(self,
                           empresa_id: str,
                           page: int,
                           page_size: int
                           ):
        offset = (page - 1) * page_size

        return self.repository.consulta_alertas_qualidade(
            empresa_id,
            page_size,
            offset
        )