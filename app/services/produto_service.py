from app.repositories.produto_repository import ProdutoRepository
from app.models.produto import Produtos, UpdateProduto

class ProdutoService:

    def __init__(self):
        self.repository = ProdutoRepository()

    def listar_produtos(self, empresa_id: str):
        return self.repository.buscar_todos_por_id_empresa(empresa_id)

    def atualizar_produtos(self, data_update: UpdateProduto):
        return self.repository.atualizar_produtos(data_update)

    def cadastrar_produto(self, produto: Produtos):
        if produto.empresa_id is None:
            return ValueError("Campo código da empresa(empresa_id) é obrigatório e não foi informado.")
        if produto.preco <0:
            return ValueError("Valor do produto não pode ser menor que 0.")
        if produto.estoque < 0:
            raise ValueError("O estoque não pode ser negativo.")

        return self.repository.inserir_produto_por_id_empresa(produto)