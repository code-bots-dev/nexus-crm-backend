import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class Lead(BaseModel):
    name: str
    email: str = None
    phone: str = None
    company: str = None
    origin: str = None
    status: str = "new"
    notes: str = None

class Sales(BaseModel):
    name: str
    email: str = None
    phone: str = None
    idProduct: str = None
    amount: int = None
    value: int = None
    status: str = "new"
    notes: str = None

class LoginData(BaseModel):
    username: str
    password: str

class CreateProduct(BaseModel):
    nome: str
    preco_base: float
    promocao: bool
    categoria: str
    id_empresa: float
    min_desconto: float
    max_desconto: float
    ativo: bool

class Endereco(BaseModel):
    cep: str
    rua: str
    bairro: str
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

class CreateClient(BaseModel):
    nome: str
    cpf: str
    data_nascimento: Optional[str] = None
    email: str
    sexo: str
    telefone: str
    enderecos: Endereco

class CreateLead(BaseModel):
    nome: str
    empresa: str = Field(alias="Empresa")
    email: EmailStr = Field(alias="e-mail")
    telefone: Optional[str] = None
    situacao: str = Field(alias="Situação")
    criacao: datetime
    origem: Optional[str] = Field(default=None, alias="Origem")

    class Config:
        populate_by_name = True

class UpdateClient(BaseModel):
    # id_cliente: str
    data: dict = None

class UpdateLeads(BaseModel):
    data: dict = None