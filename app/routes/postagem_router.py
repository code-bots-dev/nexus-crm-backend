from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.models.postagem_model import PostagemInsert
from app.services.postagem_service import PostagemService
from components import tokenAcess

router = APIRouter(
    prefix="/v1/postagens",
    tags=["Postagens"]
)

service = PostagemService()

@router.get("/")
def buscar_postagens(
    empresa_id: str = Query(..., description="ID da empresa (obrigatório)"),
    usuario_id: Optional[str] = Query(None, description="ID do usuário (opcional)"),
    tipo_postagem: Optional[str] = Query(None, description="Tipo de postagem (ex: portifolio, artigo, blog)"),
    categoria: Optional[str] = Query(None, description="Categoria da postagem"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo (true/false)")
):
    try:
        postagens = service.listar_postagens(
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            tipo_postagem=tipo_postagem,
            categoria=categoria,
            ativo=ativo
        )

        return {
            "sucesso": True,
            #"total": len(postagens),
            "dados": postagens
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar postagens: {str(erro)}"
        )

@router.post("/register_postagem")
def cadastrar_postagem(postagem: PostagemInsert):
    try:
        resultado = service.cadastrar_postagem(postagem)
        return {
            "sucesso": True,
            "mensagem": "Postagem cadastrada com sucesso.",
            "dados": resultado
        }
    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao cadastrar postagem: {str(erro)}"
        )
