from dns.e164 import query

from app.repositories.base_repository import BaseRepository
from app.models.venda_model import InsertVendas

class VendaRepository(BaseRepository):

    def retorna_vendas(self, empresa_id: str):
        query = """
                select vd.id as id_venda,
                       ct.nome as cliente,
                       vd.valor_total,
                       vd.forma_pagamento_id,
                       vd.created_at as data_venda,
                       fpg.descricao as forma_pagamento
                from public.vendas vd
                join public.contatos ct 
                on ct.id = vd.cliente_id
                and ct.empresa_id = vd.empresa_id 
                left join public.forma_pagamento fpg 
                on fpg.id = vd.forma_pagamento_id
                where 1=1
                and vd.empresa_id = %s
        """
        return self.execute_query(query,
                                  (empresa_id,))

    def criar_venda(self, dVendas: InsertVendas):
        query = """
            select public.criar_vendas_com_contato(
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
                                  (dVendas.empresa_id,
                                          dVendas.nome,
                                          dVendas.telefone,
                                          dVendas.forma_pagamento_id,
                                          dVendas.email,
                                          dVendas.cpf_cnpj,
                                          dVendas.emrepsa_nome,
                                          dVendas.observacao_contato,
                                          dVendas.valor,
                                          dVendas.usuario_responsavel_id
                                          )
                                  )
