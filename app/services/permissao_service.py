from app.repositories.permissoes_repository import PermissoesRepository
from app.models.permissao_model import RetornaPermissoes

class PermissaoService:

    def __init__(self):
        self.repository = PermissoesRepository()

    def listar_permissao(self, empresa_id):
        if not empresa_id:
            return ValueError(f"Necessário informar o Id da empresa")

        return self.repository.consultar_permissoes(empresa_id)