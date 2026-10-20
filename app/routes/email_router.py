from fastapi import APIRouter, HTTPException, Depends, status
from app.services.email_service import EmailService
from app.models.email_model import ConfiguracaoEmpresaModel, EnviarEmailModel
from components import tokenAcess

router = APIRouter(
    prefix="/v1/email",
    tags=["Serviço de Email - Brevo"]
)

service = EmailService()

@router.post("/send")
def enviar_email(dados: EnviarEmailModel,
                 username: str = Depends(tokenAcess.token.verify_token)):
    try:
        resultado = service.enviar_email(dados)
        return resultado
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )
    except Exception as erro:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao enviar e-mail: {str(erro)}"
        )

@router.post("/config")
def salvar_configuracao_empresa(config: ConfiguracaoEmpresaModel,
                                username: str = Depends(tokenAcess.token.verify_token)):
    try:
        resultado = service.salvar_configuracao(config)
        return {
            "sucesso": True,
            "mensagem": "Configurações da empresa salvas com sucesso.",
            "dados": resultado
        }
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )
    except Exception as erro:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar configurações: {str(erro)}"
        )

@router.get("/config")
def buscar_configuracao_empresa(empresa_id: str,
                                username: str = Depends(tokenAcess.token.verify_token)):
    try:
        config = service.obter_configuracao(empresa_id)
        return {
            "sucesso": True,
            "dados": config
        }
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro)
        )
