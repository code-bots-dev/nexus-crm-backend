from pathlib import Path
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.repositories.email_repository import EmailRepository
from app.repositories.venda_repository import VendaRepository
from app.models.email_model import ConfiguracaoEmpresaModel, EnviarEmailModel
import app.template_email

class EmailService:
    def __init__(self):
        self.repository = EmailRepository()
        self.vendas_repository = VendaRepository()

    def salvar_configuracao(self, config: ConfiguracaoEmpresaModel):
        if not config.empresa_id:
            raise ValueError("O campo empresa_id é obrigatório.")
        return self.repository.salvar_configuracao_empresa(config)

    def obter_configuracao(self, empresa_id: str):
        if not empresa_id:
            raise ValueError("O campo empresa_id é obrigatório.")
        config = self.repository.obter_configuracao_empresa(empresa_id)
        if not config:
            raise ValueError(f"Nenhuma configuração encontrada para a empresa {empresa_id}")
        return config

    def carregar_template(self, nome_template: str, **valores) -> str:
        caminho = (
                Path(__file__).resolve().parent.parent
                / "template_email"
                / nome_template
        )

        if not caminho.exists():
            raise FileNotFoundError(
                f"Template de e-mail não encontrado: {caminho}"
            )

        html = caminho.read_text(encoding="utf-8")

        for chave, valor in valores.items():
            html = html.replace(
                "{{ " + chave + " }}",
                str(valor if valor is not None else "")
            )

        return html

    def _enviar_via_brevo_api(self, api_key: str, email_remetente: str, nome_remetente: str,
                              destinatario: str, assunto: str, mensagem: str, is_html: bool = True):
        """
        Envia e-mail utilizando a API REST v3 da Brevo (HTTPS porta 443).
        Ideal para ambientes de nuvem como Render Free Tier onde portas SMTP diretas são bloqueadas/sofrem timeout.
        """
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }
        payload = {
            "sender": {
                "name": nome_remetente or "Nexus CRM",
                "email": email_remetente
            },
            "to": [
                {
                    "email": destinatario
                }
            ],
            "subject": assunto
        }

        if is_html:
            payload["htmlContent"] = mensagem
        else:
            payload["textContent"] = mensagem

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code in (200, 201, 202):
                return response.json()
            else:
                try:
                    err_data = response.json()
                    msg_erro = err_data.get("message") or str(err_data)
                except Exception:
                    msg_erro = response.text
                raise ValueError(f"Erro Brevo API ({response.status_code}): {msg_erro}")
        except requests.exceptions.RequestException as req_err:
            raise ValueError(f"Falha de conexão com a API da Brevo: {str(req_err)}")

    def enviar_email(self, dados: EnviarEmailModel):
        if not dados.empresa_id:
            raise ValueError("O campo empresa_id é obrigatório.")

        # Busca configurações da empresa
        config = self.repository.obter_configuracao_empresa(dados.empresa_id)
        if not config:
            raise ValueError(f"Configurações da empresa {dados.empresa_id} não foram encontradas no banco de dados.")

        host = config.get("url_servidor_smtp")
        porta = config.get("porta_smtp")
        usuario_smtp = config.get("usuario_smtp")
        senha_smtp = config.get("key_api_email_smtp")
        key_api_geral = config.get("api_key_brevo")

        api_key_brevo = config.get("api_key_brevo")

        # Busca dados da empresa na tabela public.empresas para definir remetente
        empresa = self.repository.obter_empresa(dados.empresa_id)
        if not empresa:
            raise ValueError(f"Empresa com ID {dados.empresa_id} não foi encontrada no banco de dados.")

        email_remetente = dados.email_remetente or empresa.get("email")
        if not email_remetente:
            raise ValueError(f"A empresa {dados.empresa_id} não possui e-mail cadastrado na tabela public.empresas.")

        nome_remetente = (
            dados.nome_remetente
            or empresa.get("nome_fantasia")
            or empresa.get("nome")
            or "Nexus CRM"
        )

        destinatario = dados.destinatario

        # Processamento do template e dados da venda
        vendas = None
        if dados.venda_id:
            vendas = self.vendas_repository.retorna_venda_unica(dados.venda_id)
            if vendas and not destinatario:
                destinatario = vendas[0].get('email')

        if not destinatario:
            raise ValueError("O e-mail do destinatário é obrigatório.")

        if not dados.assunto:
            raise ValueError("O assunto do e-mail é obrigatório.")

        if dados.mensagem is None and dados.template == "link_pagamento.html":
            mensagem = self.carregar_template(
                dados.template,
                nome_empresa=empresa.get("nome") or empresa.get("nome_fantasia") or "Nexus CRM",
                link_pagamento="https://sandbox.asaas.com/i/xrtxchkdjzbtjqo9",
                valor="R$ 1.500,00",
                data_vencimento="15/10/2026"
            )
        elif dados.mensagem is None and dados.template == "pedido_confirmado.html" and vendas:
            mensagem = self.carregar_template(
                dados.template,
                nome_empresa=empresa.get("nome") or empresa.get("nome_fantasia") or "Nexus CRM",
                nome_cliente=vendas[0].get('cliente', 'Cliente'),
                numero_pedido=vendas[0].get('numero_pedido', '—'),
                valor_total=f"R$ {float(vendas[0].get('valor_total') or 0):,.2f}".replace('.', 'X').replace(',', '.').replace('X', ','),
                link_pagamento="https://sandbox.asaas.com/i/xrtxchkdjzbtjqo9"
            )
        else:
            mensagem = dados.mensagem or ""

        # =========================================================================
        # 1. PRIORIDADE: Envio via API REST HTTPS da Brevo (Porta 443)
        # Totalmente imune ao bloqueio de portas SMTP do Render Free Tier
        # =========================================================================
        if api_key_brevo and (api_key_brevo.startswith("xkeysib-") or "brevo" in str(host).lower() or "sendinblue" in str(host).lower()):
            try:
                res_brevo = self._enviar_via_brevo_api(
                    api_key=api_key_brevo,
                    email_remetente=email_remetente,
                    nome_remetente=nome_remetente,
                    destinatario=destinatario,
                    assunto=dados.assunto,
                    mensagem=mensagem,
                    is_html=dados.is_html
                )
                return {
                    "sucesso": True,
                    "mensagem": "E-mail enviado com sucesso via Brevo API (HTTPS).",
                    "destinatario": destinatario,
                    "empresa_id": dados.empresa_id,
                    "mensagem_enviada": mensagem,
                    "template": dados.template,
                    "venda_id": dados.venda_id,
                    "message_id": res_brevo.get("messageId")
                }
            except Exception as e_api:
                # Se não houver configuração de host SMTP para fallback, propaga o erro da API
                if not host or not porta:
                    raise ValueError(f"Falha ao enviar e-mail via Brevo API: {str(e_api)}")
                print(f"[EmailService] Envio via Brevo API falhou ({e_api}), tentando fallback via SMTP...")

        # =========================================================================
        # 2. FALLBACK: Envio via SMTP clássico (caso não seja chave de API Brevo)
        # =========================================================================
        if not host or not porta or not usuario_smtp or not senha_smtp:
            raise ValueError("Configurações de envio incompletas no banco de dados.")

        try:
            porta_num = int(porta)
        except ValueError:
            raise ValueError("A porta SMTP cadastrada deve ser um número inteiro válido (ex: 587 ou 465).")

        msg = MIMEMultipart("alternative")
        msg["From"] = f"{nome_remetente} <{email_remetente}>"
        msg["To"] = destinatario
        msg["Subject"] = dados.assunto

        tipo_conteudo = "html" if dados.is_html else "plain"
        msg.attach(MIMEText(mensagem, tipo_conteudo, "utf-8"))

        try:
            if porta_num == 465:
                server = smtplib.SMTP_SSL(host, porta_num, timeout=10)
            else:
                server = smtplib.SMTP(host, porta_num, timeout=10)
                server.ehlo()
                server.starttls()
                server.ehlo()

            server.login(usuario_smtp, senha_smtp)
            server.sendmail(email_remetente, [destinatario], msg.as_string())
            server.quit()

            return {
                "sucesso": True,
                "mensagem": "E-mail aceito pelo servidor SMTP.",
                "destinatario": destinatario,
                "empresa_id": dados.empresa_id,
                "mensagem_enviada": mensagem,
                "template": dados.template,
                "venda_id": dados.venda_id
            }

        except smtplib.SMTPAuthenticationError:
            raise ValueError("Falha na autenticação SMTP. Verifique usuário e chave SMTP.")
        except smtplib.SMTPException as e:
            raise ValueError(f"Erro SMTP: {str(e)}")
        except Exception as e:
            raise ValueError(
                f"Falha ao enviar e-mail: {str(e)}. "
                f"Dica: Se o servidor estiver no Render Free, use a chave de API da Brevo para envio via HTTPS."
            )
