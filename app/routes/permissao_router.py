from fastapi import HTTPException, Depends, APIRouter
from app.models.permissao_model import RetornaPermissoes
from uuid import UUID
from components import tokenAcess

from app.services.permissao_service import PermissaoService

router = APIRouter(
    prefix="/v1/permissions",
    tags=["Permissões"]
)

service = PermissaoService()

@router.get("/")
def cadastrar_produto(empresa_id: str,
                    username: str = Depends(tokenAcess.token.verify_token)):
    try:
        p_cliente_id = service.listar_permissao(empresa_id)

        return p_cliente_id

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )