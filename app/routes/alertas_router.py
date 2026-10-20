from fastapi import HTTPException, APIRouter, Depends, Query
from uuid import UUID
import datetime

from app.services.alertas_service import AlertasService
from components import tokenAcess

router = APIRouter(
    prefix="/v1/alertas",
    tags=["Alertas Qualidade"]
)

service = AlertasService()

@router.get("/")
def buscar_alertas_qualiadade(empresa_id: str,
                    page: int = Query(1, ge=1),
                    page_size: int = Query(20, ge=1, le=100),
                    username: str = Depends(tokenAcess.token.verify_token)
                    ):

    alerta_qualidade = service.listar_alertas_qualidade(
                                            empresa_id,
                                            page,
                                            page_size
                                             )

    if not alerta_qualidade:
        raise HTTPException(
            status_code=404,
            detail="Nenhum Alerta de Qualidade encontrado."
        )

    return {
        "sucesso": True,
        "dados": alerta_qualidade
    }