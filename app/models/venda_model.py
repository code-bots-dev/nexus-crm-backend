from pydantic import BaseModel

class ItemProdutoVenda(BaseModel):
    produto_id: str
    quantidade: int

class InsertVendas(BaseModel):
    empresa_id: str
    cliente_id: str | None = None
    valor: float | int
    forma_pagamento_id: str
    nome: str
    telefone: str
    email: str
    cpf_cnpj: str | None = None
    empresa_nome: str | None = None
    emrepsa_nome: str | None = None
    observacao_contato: str | None = None
    usuario_responsavel_id: str
    produtos: list[ItemProdutoVenda] | None = None

class FormaPagamentoResponse(BaseModel):
    id: str
    descricao: str

class DeletarVenda(BaseModel):
    empresa_id: str
    vendas_id: str