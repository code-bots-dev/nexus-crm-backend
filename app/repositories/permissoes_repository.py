from app.repositories.base_repository import BaseRepository
from app.models.permissao_model import RetornaPermissoes

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