import datetime

from pydantic import BaseModel

class ListaAgenda(BaseModel):
    empresa_id: str
    data_inicio: datetime.date
    data_final: datetime.date

class CadastroAgendamento(BaseModel):
    empresa_id: str
    usuario_responsavel_id: str
    agenda_id: str
    status_agendamento_id: str
    cliente_contato_id: str | None = None

    nome_contato: str | None = None
    telefone_contato: str | None = None
    email_contato: str | None = None
    cpf_cnpj_contato: str | None = None
    empresa_nome_contato: str | None = None
    observacao_contato: str | None = None

    e_contato_novo: int | None = None
    lembrete: bool | None = None
    observacao_agendamento: str | None = None