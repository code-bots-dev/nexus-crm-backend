from app.models.lead_models import LeadsInsert, Leads
from app.repositories.base_repository import BaseRepository

class LeadRepository(BaseRepository):
    def retorna_leads(self, empresa_id, usuario_id):
        query = """
                select co.nome as nome_contato,
                       co.telefone as telefone_contato,
                       co.email as email_contato,
                       co.status status_contato,
                       ld.origem as origem_lead,
                       ld.status as status_lead,
                       ld.valor_estimado,
                       usu.nome as usuario_responsavel,
                       usu.ativo as status_usuario,
                       em.nome as nome_empresa
                from public.leads ld 
                join public.empresas em 
                on em.id = ld.empresa_id
                join public.contatos co
                on co.id = ld.contato_id 
                join public.usuarios usu
                on usu.id = ld.usuario_responsavel_id
                where 1=1
                and em.id = %s
        """

        return self.execute_query(query,
                                  (empresa_id,)
                                  )

    def inserir_lead(self, pleads: LeadsInsert):
        query = """
        select public.criar_lead_com_contato(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """
        return self.execute_query(query,
                                  (pleads.empresa_id,
                                        pleads.nome,
                                        pleads.telefone,
                                        pleads.email,
                                        pleads.cpf_cnpj,
                                        pleads.emrepsa_nome,
                                        pleads.observacao_contato,
                                        pleads.usuario_responsavel_id,
                                        pleads.origem_lead,
                                        pleads.status_lead,
                                        pleads.valor_estimado,
                                        pleads.observacao_lead
                                   )
                                  )

if __name__ == '__main__':
    repository = LeadRepository()


    empresa_id="75cc9dc2-7cf4-49e2-b21c-c285d50af99d"
    usuario_id="9b4ba383-4d69-4664-b1a5-8006fa5e8e2a"

    print(repository.retorna_leads(empresa_id, usuario_id))