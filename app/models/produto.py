from pydantic import BaseModel

class Produtos(BaseModel):
    empresa_id: str
    codigo: str
    nome: str
    descricao: str
    categoria: str
    preco: float
    estoque: int
    imagem_url: str

class UpdateProduto(BaseModel):
    nome: str
    descricao: str
    categoria: str
    preco: float
    estoque: int
    imagem_url: str
    ativo: bool = True
    id_produto: str
