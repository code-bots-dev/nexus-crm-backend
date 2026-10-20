from app.services.venda_service import VendaService
from fastapi import APIRouter, HTTPException, Depends
from app.models.venda_model import InsertVendas, DeletarVenda
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
            "mensagem": "Venda cadastrada com sucesso.",
            "id": p_vendas_id
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

@router.get('/forma_pagamento')
def buscar_formas_pagamento(empresa_id: str = None,
                            username: str = Depends(tokenAcess.token.verify_token)):
    formas_pagamento = service.listar_formas_pagamento(empresa_id)

    if not formas_pagamento:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma forma de pagamento encontrada."
        )

    return {
        "sucesso": True,
        "dados": formas_pagamento
    }

@router.delete('/delete_sales')
def deletar_vendas(delVenda: DeletarVenda,
                  username: str = Depends(tokenAcess.token.verify_token)):
    try:
        service.deletar_venda(delVenda.empresa_id, delVenda.vendas_id)

        return {
            "sucesso": True,
            "mensagem": "Venda deletada com sucesso.",
            "id": delVenda.vendas_id
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )