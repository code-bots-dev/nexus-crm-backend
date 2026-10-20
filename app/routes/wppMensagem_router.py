from fastapi import HTTPException, APIRouter, Depends, Query, status, Request, Response
from uuid import UUID
import datetime

from app.services.wppMensagem_service import wppMensagemService
from app.models.wppMensagem_model import InsertMensager, EnviarMensagemWhatsapp
from components import tokenAcess

router = APIRouter(
    prefix="/v1/wppMensagem",
    tags=["WABA-WhatsApp"]
)

service = wppMensagemService()

@router.get("/templates")
def SendMensager(empresa_id: str,
                 username: str = Depends(tokenAcess.token.verify_token)):

    templates_existentes = service.templates_whatsapp(empresa_id)

    if not templates_existentes:
        raise HTTPException(
            status_code=404,
            detail="Nenhum template encontrado."
        )

    return {
        "sucesso": True,
        "dados": templates_existentes
    }

@router.get('/conversas')
def conversations(empresa_id: str,
                  usuario_id: str):
    conversas_existentes = service.listar_conversas(empresa_id,
                                                    usuario_id)

    if not conversas_existentes:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma conversa encontrado."
        )

    return {
        "sucesso": True,
        "dados": conversas_existentes
    }

@router.post('/insert_message')
def inserir_mensagem(dmensagem: InsertMensager,
                     username: str = Depends(tokenAcess.token.verify_token)):
    try:
        dadosService = service.inserir_mensagem(dmensagem)

    except Exception as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro: Nenhum dado inserido"
        )

    return "Dados inseridos com sucesso"

@router.post("/send_message")
def enviar_mensagem(dados: EnviarMensagemWhatsapp,
                    username: str = Depends(tokenAcess.token.verify_token)):
    """
    Envia uma mensagem de WhatsApp via Meta Cloud API.
    - tipo = 'text': Envia mensagem de texto livre ('mensagem' obrigatório).
    - tipo = 'template': Envia template aprovado na Meta ('template_name' obrigatório).
      Pode passar 'parametros' (lista para posicionais ou dicionário para nomeados)
      ou 'components' diretamente.
    """
    resultado = service.enviar_mensagem(dados)
    return {
        "sucesso": True,
        "mensagem": "Mensagem enviada com sucesso no WhatsApp!",
        "dados": resultado
    }

@router.get("/webhook")
def verificar_webhook_wpp(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    challenge = service.verificar_webhook(hub_mode, hub_challenge, hub_verify_token)
    return Response(content=str(challenge), media_type="text/plain", status_code=200)

@router.post("/webhook")
async def receber_webhook_wpp(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    service.processar_webhook_payload(payload)
    return {"status": "success", "message": "EVENT_RECEIVED"}