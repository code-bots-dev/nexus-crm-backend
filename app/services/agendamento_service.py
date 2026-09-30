from app.models.agendamento_model import CadastroAgendamento, ListaAgenda
from app.repositories.agendamento_repository import AgendamentoRepository
import datetime

class AgendamentoService():
    def __init__(self):
        self.repository = AgendamentoRepository()

    def listar_agendamento(self,
                           empresa_id: str,
                           page: int,
                           page_size: int
                           ):
        offset = (page - 1) * page_size

        return self.repository.consulta_agendamentos(
            empresa_id,
            page_size,
            offset
        )

    def listar_agenda(self, dlistAgenda: ListaAgenda):
        return self.repository.consulta_agenda(
            dlistAgenda.empresa_id,
            dlistAgenda.data_inicio,
            dlistAgenda.data_final
        )

    def cadastrar_agendamento(self, dagendamento: CadastroAgendamento):
        if not dagendamento.empresa_id:
            return ValueError("Necessário informar o ID empresa!")

        return self.repository.inserir_agendamento(
            dagendamento
        )