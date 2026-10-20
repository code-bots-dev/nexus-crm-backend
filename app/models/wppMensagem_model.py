from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from enum import Enum

class ReturnTemplate(BaseModel):
    empresa_id: str

class InsertMensager(BaseModel):
    empresa_id: str
    conversa_id: str
    usuario_id: str | None = None
    mensagem: str
    contato_id: str | None = None

class TipoMensagemWpp(str, Enum):
    TEXTO = "text"
    TEMPLATE = "template"

class EnviarMensagemWhatsapp(BaseModel):
    telefone: str
    tipo: TipoMensagemWpp = TipoMensagemWpp.TEXTO

    mensagem: Optional[str] = None
    preview_url: Optional[bool] = False

    template_name: Optional[str] = None
    language_code: Optional[str] = "pt_BR"
    parametros: Optional[Union[List[Any], Dict[str, Any]]] = None
    components: Optional[List[Dict[str, Any]]] = None

    empresa_id: Optional[str] = None
    usuario_id: Optional[str] = None
    conversa_id: Optional[str] = None
    contato_id: Optional[str] = None
