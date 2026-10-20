from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConfiguracaoEmpresaModel(BaseModel):
    empresa_id: str
    key_api: Optional[str] = None
    data_inicio: Optional[datetime | str] = None
    data_final: Optional[datetime | str] = None
    key_api_pagamento: Optional[str] = None
    data_inicio_pagamento: Optional[datetime | str] = None
    data_final_pagamento: Optional[datetime | str] = None
    url_servidor_smtp: Optional[str] = None
    porta_smtp: Optional[int | float] = None
    key_api_email_smtp: Optional[str] = None

class EnviarEmailModel(BaseModel):
    empresa_id: str
    destinatario: Optional[str] = None
    assunto: str
    mensagem: Optional[str] = None
    email_remetente: Optional[str] = None
    nome_remetente: Optional[str] = None
    template: str
    is_html: bool = True

    venda_id: Optional[str] = None


