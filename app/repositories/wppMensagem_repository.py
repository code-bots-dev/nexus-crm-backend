import datetime
import os
import uuid
import re

from fastapi import HTTPException, status
from app.repositories.base_repository import BaseRepository
from app.models.wppMensagem_model import InsertMensager, EnviarMensagemWhatsapp, TipoMensagemWpp

import requests
from dotenv import load_dotenv

load_dotenv()

version = os.getenv("META_VERSION")
waba_id = os.getenv("META_WABA_ID")
phone_number_id = os.getenv("META_PHONE_NUMBER_ID")
user_access_token = os.getenv("META_USER_ACESS_TOKEN")

headers = {
    "Authorization": f"Bearer {user_access_token}"
}

class WppMensagemRepository(BaseRepository):
    def lista_template(self):
        send_mensager = requests.get(f"https://graph.facebook.com/"
                                     f"{version}/"
                                     f"{waba_id}/message_templates",
                                     headers=headers
                                     )
        return send_mensager.json()

    def enviar_mensagem_whatsapp(self, dados: EnviarMensagemWhatsapp):
        """
        Envia mensagem de WhatsApp usando a Meta Cloud API (graph.facebook.com).
        Suporta mensagem de texto livre ou template aprovado na Meta.
        """
        if not phone_number_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A variável de ambiente META_PHONE_NUMBER_ID não foi configurada."
            )

        # 1. Sanitizar número de telefone (apenas dígitos)
        telefone_limpo = re.sub(r"\D", "", str(dados.telefone))
        if not telefone_limpo or len(telefone_limpo) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Número de telefone inválido: '{dados.telefone}'"
            )

        # 2. Montar o payload conforme a documentação oficial da Meta Cloud API
        if dados.tipo == TipoMensagemWpp.TEXTO or str(dados.tipo).lower() == "text":
            if not dados.mensagem or not dados.mensagem.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Para mensagens do tipo 'text', o campo 'mensagem' é obrigatório e não pode ser vazio."
                )

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": telefone_limpo,
                "type": "text",
                "text": {
                    "preview_url": bool(dados.preview_url),
                    "body": dados.mensagem
                }
            }

        elif dados.tipo == TipoMensagemWpp.TEMPLATE or str(dados.tipo).lower() == "template":
            if not dados.template_name or not dados.template_name.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Para mensagens do tipo 'template', o campo 'template_name' é obrigatório."
                )

            template_obj = {
                "name": dados.template_name,
                "language": {
                    "code": dados.language_code or "pt_BR"
                }
            }

            # Caso o usuário envie a estrutura completa de components
            if dados.components:
                template_obj["components"] = dados.components
            # Caso envie lista de parâmetros posicionais ou dict de parâmetros nomeados
            elif dados.parametros is not None:
                if isinstance(dados.parametros, list):
                    template_obj["components"] = [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": str(p)} for p in dados.parametros
                            ]
                        }
                    ]
                elif isinstance(dados.parametros, dict):
                    template_obj["components"] = [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "parameter_name": str(k), "text": str(v)}
                                for k, v in dados.parametros.items()
                            ]
                        }
                    ]

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": telefone_limpo,
                "type": "template",
                "template": template_obj
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de mensagem inválido: '{dados.tipo}'. Tipos válidos: 'text' ou 'template'."
            )

        # 3. Requisição para o endpoint da Meta Cloud API
        url = f"https://graph.facebook.com/{version}/{phone_number_id}/messages"
        json_headers = {
            "Authorization": f"Bearer {user_access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=json_headers, json=payload, timeout=20)
            res_json = response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Falha de conexão com a API da Meta: {str(e)}"
            )

        # 4. Tratar possíveis erros da Meta
        if response.status_code >= 400:
            error_data = res_json.get("error", {})
            error_msg = error_data.get("message", "Erro desconhecido na Meta API")
            error_code = error_data.get("code")
            error_subcode = error_data.get("error_subcode")
            error_details = f"Erro Meta API (HTTP {response.status_code}): {error_msg}"
            if error_code:
                error_details += f" (Código: {error_code}, Subcódigo: {error_subcode})"
            raise HTTPException(
                status_code=response.status_code if response.status_code < 500 else status.HTTP_502_BAD_GATEWAY,
                detail=error_details
            )

        # 5. Se informado empresa_id e conversa_id, registrar a mensagem enviada no histórico (public.mensagens)
        if dados.empresa_id and dados.conversa_id:
            try:
                texto_salvar = dados.mensagem if dados.tipo == "text" else f"[Template: {dados.template_name}]"
                query = """
                    insert into public.mensagens(empresa_id, conversa_id, usuario_id, mensagem, status, contato_id)
                    values(%s, %s, %s, %s, %s, %s)
                """
                self.execute_query(query, (
                    dados.empresa_id,
                    dados.conversa_id,
                    dados.usuario_id,
                    texto_salvar,
                    "ENVIADA",
                    dados.contato_id
                ))
            except Exception:
                # O envio pela Meta foi concluído com sucesso, falha de log no banco não impede o retorno
                pass

        return res_json

    def consultar_conversas(self,
                            empresa_id: str,
                            usuario_id: str):
        try:
            uuid.UUID(str(empresa_id))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O ID fornecido não é um UUID válido: {empresa_id}"
            )

        query = """
                select 
                       c.id as conversa_id,
                       ct.nome as nome_contato,
                       ct.telefone,
                       c.canal,
                       usu.nome as nome_usuario,
                       usu.email as email_usuario,
                       c.status as status_conversa,

                       COALESCE(
                           json_agg(
                                json_build_object(
                                    'mensagem', m.mensagem,
                                    'status', m.status,
                                    'template_id', m.template_id,
                                    'data_envio', m.created_at
                                )
                           ) FILTER (WHERE m.id IS NOT NULL
                                     AND m.usuario_id IS NOT NULL
                           ), '[]'
                       ) as mensagens_enviadas,
                       
                       COALESCE(
                           json_agg(
                               json_build_object(
                                   'mensagem', m.mensagem,
                                   'status', m.status,
                                   'data_envio', m.created_at
                               )
                           ) FILTER (WHERE m.id IS NOT NULL
                                     AND m.contato_id IS NOT NULL
                           ), '[]'
                       ) as mensagens_recebidas

                from public.conversas c
                join public.contatos ct
                  on ct.id = c.contato_id
                join public.usuarios usu
                  on usu.id = c.usuario_responsavel_id
                left join public.mensagens m
                  on m.conversa_id = c.id 
                  and m.empresa_id = ct.empresa_id
                where 1=1
                and c.empresa_id = %s
                and usu.id = %s

                -- O Group By agrupa tudo que NÃO é mensagem, formando a lista na coluna 'mensagens'
                group by 
                    c.id, ct.nome, ct.telefone, c.canal, 
                    usu.nome, usu.email, c.status
            """

        try:
            dados_conversa = self.execute_query(query, (empresa_id, usuario_id))
        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha interna ao consultar banco de dados. Erro: {str(erro)}"
            )

        if not dados_conversa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhuma conversa encontrada para a empresa {empresa_id} e usuário {usuario_id}"
            )

        return dados_conversa

    def inserir_menagem(self, dmensagem: InsertMensager):
        try:
            query = """
                    insert into public.mensagens(empresa_id, conversa_id, usuario_id, mensagem, contato_id)
                    values(%s, %s, %s, %s, %s)
                """

            dadosInsert = self.execute_query(query, (dmensagem.empresa_id,
                                                            dmensagem.conversa_id,
                                                            dmensagem.usuario_id,
                                                            dmensagem.mensagem,
                                                            dmensagem.contato_id,
                                                     )
                                             )
        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Não localizado dados para {dmensagem.empresa_id}"
            )

        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail= f"Dados Inseridos com sucesso!"
        )

    def salvar_mensagem_recebida(self, de_telefone: str, nome_contato: str | None, texto_mensagem: str, message_id: str | None = None):
        """
        Salva uma mensagem recebida via Webhook da Meta no banco de dados:
        1. Localiza ou cria o contato pelo telefone
        2. Localiza ou cria a conversa aberta
        3. Insere a mensagem em public.mensagens com status 'RECEBIDA'
        4. Atualiza a data da última mensagem na conversa
        """
        telefone_limpo = re.sub(r"\D", "", str(de_telefone))
        telefone_sem_55 = telefone_limpo[2:] if telefone_limpo.startswith("55") and len(telefone_limpo) > 10 else telefone_limpo

        # 1. Busca contato existente
        busca_contato_query = """
            select id, empresa_id, nome, telefone
            from public.contatos
            where telefone = %s or telefone = %s or %s like '%%' || telefone
            order by created_at desc
            limit 1
        """
        contato = self.execute_query(busca_contato_query, (telefone_limpo, telefone_sem_55, telefone_limpo))

        if contato and len(contato) > 0:
            contato_id = contato[0]["id"]
            empresa_id = contato[0]["empresa_id"]
        else:
            # Seleciona empresa ativa padrão
            empresa_query = "select id from public.empresas where status = 'ATIVO' order by created_at desc limit 1"
            empresas = self.execute_query(empresa_query)
            empresa_id = empresas[0]["id"] if empresas else "75cc9dc2-7cf4-49e2-b21c-c285d50af99d"

            nome_salvar = nome_contato.strip() if nome_contato and nome_contato.strip() else f"WhatsApp {telefone_limpo}"
            insert_contato_query = """
                insert into public.contatos (empresa_id, nome, telefone, status)
                values (%s, %s, %s, 'ATIVO')
                returning id
            """
            novo_contato = self.execute_query(insert_contato_query, (empresa_id, nome_salvar, telefone_limpo))
            contato_id = novo_contato[0]["id"]

        # 2. Busca conversa aberta ou cria uma nova
        busca_conversa_query = """
            select id, usuario_responsavel_id
            from public.conversas
            where contato_id = %s and empresa_id = %s and status = 'ABERTA'
            order by updated_at desc
            limit 1
        """
        conversa = self.execute_query(busca_conversa_query, (contato_id, empresa_id))

        if conversa and len(conversa) > 0:
            conversa_id = conversa[0]["id"]
        else:
            usuario_query = "select id from public.usuarios where empresa_id = %s and ativo = true order by created_at asc limit 1"
            usuarios = self.execute_query(usuario_query, (empresa_id,))
            usuario_id = usuarios[0]["id"] if usuarios else None

            insert_conversa_query = """
                insert into public.conversas (empresa_id, contato_id, usuario_responsavel_id, canal, status, ultima_mensagem_at)
                values (%s, %s, %s, 'WhatsApp', 'ABERTA', now())
                returning id
            """
            nova_conversa = self.execute_query(insert_conversa_query, (empresa_id, contato_id, usuario_id))
            conversa_id = nova_conversa[0]["id"]

        # 3. Insere a mensagem recebida
        insert_msg_query = """
            insert into public.mensagens (empresa_id, conversa_id, contato_id, usuario_id, mensagem, status, created_at)
            values (%s, %s, %s, NULL, %s, 'RECEBIDA', now())
            returning id
        """
        msg_salva = self.execute_query(insert_msg_query, (empresa_id, conversa_id, contato_id, texto_mensagem))

        # 4. Atualiza timestamp da conversa
        update_conversa_query = """
            update public.conversas
            set ultima_mensagem_at = now(), updated_at = now()
            where id = %s
        """
        self.execute_query(update_conversa_query, (conversa_id,))

        return {
            "mensagem_id": msg_salva[0]["id"] if msg_salva else None,
            "conversa_id": conversa_id,
            "contato_id": contato_id,
            "empresa_id": empresa_id
        }

    def atualizar_status_mensagem(self, message_id: str, status_meta: str):
        status_map = {
            "sent": "ENVIADA",
            "delivered": "ENTREGUE",
            "read": "LIDA",
            "failed": "FALHA"
        }
        return status_map.get(status_meta.lower(), status_meta.upper())

if __name__ == '__main__':
    repository = WppMensagemRepository()

    dadosMensagem = InsertMensager(
        empresa_id = "75cc9dc2-7cf4-49e2-b21c-c285d50af99d",
        conversa_id = "5232ebd2-9297-4360-83c6-c967e21c5525",
        usuario_id = "9b4ba383-4d69-4664-b1a5-8006fa5e8e2a",
        mensagem = ("Boa tarde\n"
                    "Como posso te ajudar hoje?"),
        contato_id = None
    )

    # dados = repository.lista_template()
    dados = repository.inserir_menagem(dadosMensagem)
    print(dados)