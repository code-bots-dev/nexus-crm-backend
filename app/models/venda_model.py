from pydantic import BaseModel

class InsertVendas(BaseModel):
    empresa_id: str
    cliente_id: str
    valor: int
    forma_pagamento_id: str
    nome: str
    telefone: str
    email: str
    cpf_cnpj: str | None = None
    emrepsa_nome: str | None = None
    observacao_contato: str | None = None
    usuario_responsavel_id: str