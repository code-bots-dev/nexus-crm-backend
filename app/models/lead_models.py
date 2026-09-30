from pydantic import BaseModel

class Leads(BaseModel):
    empresa_id: str
    usuario_id: str | None = None

class LeadsInsert(BaseModel):
    empresa_id: str
    nome: str
    telefone: str
    email: str
    cpf_cnpj: str | None = None
    emrepsa_nome: str | None = None
    observacao_contato: str | None = None
    usuario_responsavel_id: str
    origem_lead: str
    status_lead: str
    valor_estimado: float
    observacao_lead: str | None = None