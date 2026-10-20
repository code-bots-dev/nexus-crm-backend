from app.repositories.postagem_repository import PostagemRepository
from app.models.postagem_model import PostagemInsert

class PostagemService:
    def __init__(self):
        self.repository = PostagemRepository()

    def listar_postagens(self,
                         empresa_id: str,
                         usuario_id: str | None = None,
                         tipo_postagem: str | None = None,
                         categoria: str | None = None,
                         ativo: bool | None = None):
        if not empresa_id:
            raise ValueError("O campo ID Empresa é obrigatório e não foi informado!")

        return self.repository.retorna_postagens(
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            tipo_postagem=tipo_postagem,
            categoria=categoria,
            ativo=ativo
        )

    def cadastrar_postagem(self, postagem: PostagemInsert):
        if not postagem.empresa_id:
            raise ValueError("O campo ID Empresa é obrigatório e não foi informado!")
        if not postagem.usuario_id:
            raise ValueError("O campo ID Usuário é obrigatório e não foi informado!")
        if not postagem.tipo_postagem:
            raise ValueError("O campo Tipo de Postagem é obrigatório e não foi informado!")

        return self.repository.inserir_postagem(postagem)
