from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from uuid import UUID

class Postagem(BaseModel):
    postagem_id: UUID | str
    tipo_postagem: str
    data_postagem: Optional[datetime] = None
    data_validade: Optional[datetime] = None
    url_postagem: Optional[str] = None
    descricao: Optional[Any] = None
    ativo: bool = True
    categoria: Optional[str] = None

class PostagemInsert(BaseModel):
    empresa_id: str
    usuario_id: str
    tipo_postagem: str
    data_postagem: Optional[datetime] = None
    data_validade: Optional[datetime] = None
    url_postagem: Optional[str] = None
    descricao: Optional[Any] = None
    ativo: bool = True
    categoria: Optional[str] = None
