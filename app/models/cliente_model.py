from pydantic import BaseModel

class CadastroCliente(BaseModel):
    empresa_id: str
    nome: str
    telefone: str
    email: str
    status: str
    cep: str | None = None
    nome_rua: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    uf: str | None = None

class CadastrarEnderecoCliente(BaseModel):
    contatos_id: str
    rua: str
    numero: str | None = None
    complemento: str | None = None
    bairro: str
    estado: str
    cidade: str
    cep: str
    pais: str | None = None

class AtualizarCliente(BaseModel):
    empresa_id: str | None = None
    contatos_id: str | None = None
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None
    cpf_cnpj: str | None = None
    empresa_nome: str | None = None
    observacao_contato: str | None = None
    status: str | None = None
    cep: str | None = None
    nome_rua: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    uf: str | None = None

class DeletarCliente(BaseModel):
    empresa_id: str | None = None
    contatos_id: str | None = None