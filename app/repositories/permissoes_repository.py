from app.repositories.base_repository import BaseRepository
from app.models.permissao_model import RetornaPermissoes
import uuid

from fastapi import HTTPException, status

class PermissoesRepository(BaseRepository):
    def consultar_permissoes(self, empresa_id):
        query = """
            select mn.nome as menu,
                   mn.ordem as ordem_menu,
                   sbn.nome as sub_menu,
                   sbn.icone as icone_sub_menu,
                   sbn.rota as rota_caminho_html,
                   sbn.ordem as ordem_sub_menu
            from public.menus mn 
            join public.sub_menus sbn
            on sbn.menu_id = mn.id
            join public.empresa_menus em
            on em.menu_id = mn.id
            where 1=1
            and sbn.ativo is true
            and em.ativo is true
            and mn.ativo is true 
            and em.empresa_id = %s
            order by mn.ordem asc, sbn.ordem asc
        """

        return self.execute_query(query, (empresa_id,))

    def consultar_dados_empresa(self, empresa_id):
        try:
            uuid.UUID(str(empresa_id))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O ID fornecido não é um UUID válido: {empresa_id}"
            )
        query = """
                select em.nome as nome_empresa,
                       em.nome_fantasia,
                       em.cnpj,
                       em.email,
                       em.telefone,
                       em.status,
                       em.usa_whatsapp
                from public.empresas em
                where 1=1
                and em.id = %s
            """
        try:
            dados_empresa = self.execute_query(query, (empresa_id,))
        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha na consulta de dados empresa! Erro: {str(erro)}"
            )
        if not dados_empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dados da empresa não localizado para {empresa_id}!"
            )
        return dados_empresa

if __name__ == '__main__':
    repository = PermissoesRepository()

    dados = repository.consultar_dados_empresa("75cc9dc2-7cf4-49e2-b21c-c285d50af99f")
    print(dados)