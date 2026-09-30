from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from app.models.produto import Produtos, UpdateProduto
from app.services.produto_service import ProdutoService
from components import tokenAcess

router = APIRouter(
    prefix="/v1/products",
    tags=["Produtos"]
)

service = ProdutoService()

@router.get("/")
def buscar_produtos(empresa_id: str,
                    username: str = Depends(tokenAcess.token.verify_token)
                    ):

    produtos = service.listar_produtos(empresa_id)

    if not produtos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum produto encontrado."
        )

    return {
        "sucesso": True,
        "dados": produtos
    }

@router.post("/register_product")
def cadastrar_produto(produto: Produtos,
                    username: str = Depends(tokenAcess.token.verify_token)):
    try:
        produto_id = service.cadastrar_produto(produto)

        return {
            "sucesso": True,
            "mensagem": "Produto cadastrado com sucesso.",
            "id": produto_id
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

@router.put("/update_product")
def atualizar_produto(data_update: UpdateProduto,
                    username: str = Depends(tokenAcess.token.verify_token)):
    try:
        produto_id = service.atualizar_produtos(data_update)

        return {
            "sucesso": True,
            "mensagem": "Produto atualizado com sucesso.",
            "id": produto_id
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )