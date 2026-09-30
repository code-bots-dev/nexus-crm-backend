from app.repositories.base_repository import BaseRepository
from app.models.produto import Produtos, UpdateProduto

class ProdutoRepository(BaseRepository):

    def buscar_todos_por_id_empresa(self, empresa_id):
        query = """
            SELECT
                *
            FROM public.produtos
            WHERE empresa_id = %s
        """
        return self.execute_query(query, (empresa_id,))

    def inserir_produto_por_id_empresa(self,
                                       produto: Produtos
                                       ):
        query = """
            INSERT INTO public.produtos (empresa_id, codigo, nome, descricao, categoria, preco, estoque, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        return self.execute_query(query, (produto.empresa_id,
                                                 produto.codigo,
                                                 produto.nome,
                                                 produto.descricao,
                                                 produto.categoria,
                                                 produto.preco,
                                                 produto.estoque,
                                                 produto.imagem_url
                                          )
                                  )

    def atualizar_produtos(self, data_update: UpdateProduto):
        query = """
                UPDATE public.produtos
                SET preco=%s,
                    estoque=%s,
                    nome=%s,
                    descricao=%s,
                    imagem_url=%s,
                    categoria=%s,
                    ativo=%s
                WHERE id=%s
            """
        return self.execute_query(query, (data_update.preco,
                                          data_update.estoque,
                                          data_update.nome,
                                          data_update.descricao,
                                          data_update.imagem_url,
                                          data_update.categoria,
                                          data_update.ativo,
                                          data_update.id_produto
                                          )
                                  )

if __name__=='__main__':
    repository = ProdutoRepository()

    produtos = repository.buscar_todos_por_id_empresa(
        "75cc9dc2-7cf4-49e2-b21c-c285d50af99d"
    )

    print(produtos)

    inserindo_produc = repository.inserir_produto_por_id_empresa(
        "75cc9dc2-7cf4-49e2-b21c-c285d50af99d",
        "2000403",
        "CABOTINE DE GRES EDT F. 100ML",
        "Cabotine de Grès é um perfume Floral Feminino. Cabotine foi lançado em 1990. O perfumista que assina esta fragrância é Jean Claude Delville. As notas de topo são: Coentro, Flor de Laranjeira, Cássia, Groselha Preta, Ameixa, Tangerina e Pêssego. As notas de coração são: Tuberosa, Jacinto, Cravo, Jasmim, Gengibre, Ylang Ylang, Rosa, Frésia, Íris, Heliotrópio e Violeta. As notas de fundo são: Civeta, Almíscar, Vetiver, Groselha Preta, Sândalo, Cedro, Âmbar, Fava Tonka e Baunilha.",
        "Perfumes",
        "157",
        "10",
        None
    )
    print(inserindo_produc)