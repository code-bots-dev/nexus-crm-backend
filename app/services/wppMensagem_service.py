from fastapi import HTTPException, status

from app.repositories.permissoes_repository import PermissoesRepository
from app.repositories.wppMensagem_repository import WppMensagemRepository
from app.models.wppMensagem_model import InsertMensager, EnviarMensagemWhatsapp

class wppMensagemService:
    def __init__(self):
        self.permissoesRepository = PermissoesRepository()
        self.wppMensagemRepository = WppMensagemRepository()

    def templates_whatsapp(self, empresa_id: str):
        dadosEmpresa = self.permissoesRepository.consultar_dados_empresa(empresa_id)

        if not dadosEmpresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dados da empresa {empresa_id} não localizados!"
            )

        try:
            if dadosEmpresa[0]['status'] == 'ATIVO':
                return self.wppMensagemRepository.lista_template()

        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Falha ao comunicar com API do WhatsApp: {str(erro)}"
            )

    def enviar_mensagem(self, dados: EnviarMensagemWhatsapp):
        if dados.empresa_id:
            dadosEmpresa = self.permissoesRepository.consultar_dados_empresa(dados.empresa_id)

            if not dadosEmpresa:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Dados da empresa {dados.empresa_id} não localizados!"
                )

            if dadosEmpresa[0].get('status') != 'ATIVO':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A empresa {dados.empresa_id} está inativa no sistema."
                )

        return self.wppMensagemRepository.enviar_mensagem_whatsapp(dados)

    def listar_conversas(self,
                         empresa_id: str,
                         usuario_id: str):
        dadosEmpresa = self.permissoesRepository.consultar_dados_empresa(empresa_id)

        if not dadosEmpresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dados da empresa {empresa_id} não localizados!"
            )

        try:
            dados_conversa = self.wppMensagemRepository.consultar_conversas(empresa_id, usuario_id)

        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Dados não localizados"
            )

        return dados_conversa

    def inserir_mensagem(self, dmensagem: InsertMensager):
        dadosEmpresa = self.permissoesRepository.consultar_dados_empresa(dmensagem.empresa_id)

        if not dadosEmpresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dados da empresa {dmensagem.empresa_id} não localizados!"
            )

        try:
            dados_mensagem = self.wppMensagemRepository.inserir_menagem(dmensagem)

        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Dados não localizados"
            )

        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"Dados Inseridos com sucesso!\n"
                   f"{dados_mensagem}"
        )

    def verificar_webhook(self, mode: str, challenge: str, token: str):
        import os
        verify_token = os.getenv("META_VERIFY_TOKEN", "nexus_crm_token_2026")
        if mode == "subscribe" and token == verify_token:
            return challenge

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token de verificação do Webhook inválido."
        )

    def processar_webhook_payload(self, payload: dict):
        resultados = []
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})

                # Mapeia contatos recebidos no payload
                contacts_map = {}
                for c in value.get("contacts", []):
                    wa_id = c.get("wa_id")
                    profile_name = c.get("profile", {}).get("name")
                    if wa_id:
                        contacts_map[wa_id] = profile_name

                # Processa mensagens recebidas de clientes
                messages = value.get("messages", [])
                for msg in messages:
                    from_number = msg.get("from")
                    msg_id = msg.get("id")
                    msg_type = msg.get("type")
                    profile_name = contacts_map.get(from_number)

                    texto = ""
                    if msg_type == "text":
                        texto = msg.get("text", {}).get("body", "")
                    elif msg_type == "interactive":
                        inter = msg.get("interactive", {})
                        if "button_reply" in inter:
                            texto = inter["button_reply"].get("title", "[Resposta de Botão]")
                        elif "list_reply" in inter:
                            texto = inter["list_reply"].get("title", "[Item de Lista]")
                        else:
                            texto = "[Interação]"
                    elif msg_type == "button":
                        texto = msg.get("button", {}).get("text", "[Botão]")
                    elif msg_type == "image":
                        legenda = msg.get("image", {}).get("caption")
                        texto = f"[Imagem: {legenda}]" if legenda else "[Imagem recebida]"
                    elif msg_type == "audio":
                        texto = "[Áudio do WhatsApp]"
                    elif msg_type == "video":
                        texto = "[Vídeo do WhatsApp]"
                    elif msg_type == "document":
                        filename = msg.get("document", {}).get("filename", "documento")
                        texto = f"[Documento: {filename}]"
                    elif msg_type == "sticker":
                        texto = "[Figurinha]"
                    elif msg_type == "location":
                        loc = msg.get("location", {})
                        texto = f"[Localização: {loc.get('latitude')}, {loc.get('longitude')}]"
                    else:
                        texto = f"[{msg_type}]"

                    if from_number and texto:
                        res = self.wppMensagemRepository.salvar_mensagem_recebida(
                            de_telefone=from_number,
                            nome_contato=profile_name,
                            texto_mensagem=texto,
                            message_id=msg_id
                        )
                        resultados.append(res)

                # Processa atualizações de status das mensagens enviadas (sent, delivered, read, failed)
                statuses = value.get("statuses", [])
                for st in statuses:
                    st_id = st.get("id")
                    st_status = st.get("status")
                    if st_id and st_status:
                        self.wppMensagemRepository.atualizar_status_mensagem(st_id, st_status)

        return resultados

if __name__ == '__main__':
    service = wppMensagemService()

    dados = service.templates_whatsapp('81203764-3a09-4c70-8044-5ef5395ae229')
    print(dados)