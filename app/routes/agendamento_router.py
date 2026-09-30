from fastapi import HTTPException, APIRouter, Depends, Query
from uuid import UUID
import datetime

from app.models.agendamento_model import CadastroAgendamento, ListaAgenda
from app.services.agendamento_service import AgendamentoService
from components import tokenAcess

router = APIRouter(
    prefix="/v1/agendamento",
    tags=["Agendamentos"]
)

service = AgendamentoService()

@router.get("/")
def buscar_agendamento(empresa_id: str,
                    page: int = Query(1, ge=1),
                    page_size: int = Query(20, ge=1, le=100),
                    username: str = Depends(tokenAcess.token.verify_token)
                    ):

    agendamento = service.listar_agendamento(empresa_id,
                                            page,
                                            page_size
                                             )

    if not agendamento:
        raise HTTPException(
            status_code=404,
            detail="Nenhum agendamento encontrado."
        )

    return {
        "sucesso": True,
        "dados": agendamento
    }

@router.get("/agenda/")
def buscar_agenda(
    dlistAgenda: ListaAgenda = Depends(),
    username: str = Depends(tokenAcess.token.verify_token)
):
    agenda = service.listar_agenda(dlistAgenda)

    if not agenda:
        raise HTTPException(
            status_code=404,
            detail="Nenhum agendamento encontrado."
        )

    return {
        "sucesso": True,
        "dados": agenda
    }

@router.post('/register_agendamentos')
def cadastrar_agendamento(dagendamento: CadastroAgendamento,
                username: str = Depends(tokenAcess.token.verify_token)):
    agendamento = service.cadastrar_agendamento(dagendamento)
    return {
        "sucesso": True,
        "dados": agendamento
    }
