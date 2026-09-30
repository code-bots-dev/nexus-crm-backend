from app.services.venda_service import VendaService
from fastapi import APIRouter, HTTPException, Depends
from app.models.venda_model import InsertVendas
from components import tokenAcess

router = APIRouter(
    prefix='/v1/vendas',
    tags=['Vendas']
)

service = VendaService()

@router.get('/')
def buscar_vendas(empresa_id: str,
                  username: str = Depends(tokenAcess.token.verify_token)
                  ):
    vendas = service.listar_vendas(empresa_id)

    if not vendas:
        raise HTTPException(
            status_code=404,
            detail="Nenhum cliente encontrado."
        )

    return {
        "sucesso": True,
        "dados": vendas
    }

@router.post('/register_sales')
def cadastrar_vendas(dvendas: InsertVendas,
                    username: str = Depends(tokenAcess.token.verify_token)):
    try:
        p_vendas_id = service.cadastrar_vendas(dvendas)

        return {
            "sucesso": True,
            "mensagem": "Cliente cadastrado com sucesso.",
            "id": p_vendas_id
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )