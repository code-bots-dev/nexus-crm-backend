from fastapi import HTTPException, APIRouter, Depends, Query
from uuid import UUID
from app.models.cliente_model import CadastroCliente, AtualizarCliente, DeletarCliente
from components import tokenAcess
from app.services.cliente_service import ClienteService
from app.repositories.cliente_repository import ClienteRepository

router = APIRouter(
    prefix="/v1/cliente",
    tags=["Clientes"]
)

service = ClienteService()
cRepository = ClienteRepository()

@router.get("/")
def buscar_clientes(empresa_id: str,
                    cpf_cnpj: str = None,
                    telefone: str = None,
                    page: int = Query(1, ge=1),
                    page_size: int = Query(20,ge=1, le=100),
                    username: str = Depends(tokenAcess.token.verify_token)
                    ):

    clientes = service.listar_cliente(empresa_id,
                                      cpf_cnpj,
                                      telefone,
                                      page,
                                      page_size)



    if not clientes:
        raise HTTPException(
            status_code=404,
            detail="Nenhum cliente encontrado."
        )

    return {
        "sucesso": True,
        "dados": clientes
    }

@router.post("/register_client")
def cadastrar_produto(cliente: CadastroCliente,
                    username: str = Depends(tokenAcess.token.verify_token)):
    try:
        p_cliente_id = service.cadastrar_cliente(cliente)

        return {
            "sucesso": True,
            "mensagem": "Cliente cadastrado com sucesso.",
            "id": p_cliente_id
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

@router.put("/update_client")
def atualizar_cliente(cliente: AtualizarCliente,
                    username: str = Depends(tokenAcess.token.verify_token)):

    try:
        status_cliente = cRepository.consultar_status_cliente(cliente.contatos_id)
        if status_cliente[0]['status'] != 'ATIVO':
            return {
                "sucesso": False,
                "mensagem": "Cliente não está Ativo",
                "id": cliente.contatos_id
            }

        p_cliente_id = service.ser_atualizar_cliente(cliente)

        return {
            "sucesso": True,
            "mensagem": "Cliente atualizado com sucesso.",
            "id": p_cliente_id
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

@router.delete("/delete_client")
def deletar_cliente(delCliente: DeletarCliente,
                    username: str = Depends(tokenAcess.token.verify_token)
                    ):
    try:
        status_cliente = cRepository.consultar_status_cliente(delCliente.contatos_id)
        if status_cliente[0]['status'] != 'ATIVO':
            return {
                "sucesso": False,
                "mensagem": "Cliente não está Ativo",
                "id": delCliente.contatos_id
            }

        p_cliente_id = service.ser_deletar_cliente(delCliente)

        return {
            "sucesso": True,
            "mensagem": "Cliente deletado com sucesso.",
            "id": p_cliente_id
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )