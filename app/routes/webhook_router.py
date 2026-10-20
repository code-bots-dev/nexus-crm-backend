from fastapi import APIRouter, Request, Query, Response, HTTPException, status
from app.services.wppMensagem_service import wppMensagemService

router = APIRouter(
    prefix="/webhook",
    tags=["Meta Webhook"]
)

service = wppMensagemService()

@router.get("")
@router.get("/")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    """
    Endpoint de verificação do Webhook pela Meta.
    A Meta envia: GET /webhook?hub.mode=subscribe&hub.challenge=...&hub.verify_token=...
    Retorna o hub.challenge em texto puro caso o token seja válido.
    """
    challenge = service.verificar_webhook(hub_mode, hub_challenge, hub_verify_token)
    return Response(content=str(challenge), media_type="text/plain", status_code=200)

@router.post("")
@router.post("/")
async def receber_notificacao_webhook(request: Request):
    """
    Endpoint que recebe notificações e mensagens enviadas pelos clientes no WhatsApp.
    A Meta envia: POST /webhook com payload JSON contendo 'entry' -> 'changes' -> 'value' -> 'messages'.
    """
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    service.processar_webhook_payload(payload)

    # A Meta exige retorno HTTP 200 rápido para confirmar recebimento do evento
    return {"status": "success", "message": "EVENT_RECEIVED"}
