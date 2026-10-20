import json

from app.repositories.base_repository import BaseRepository
from app.models.venda_model import InsertVendas

class VendaRepository(BaseRepository):

    def retorna_vendas(self, empresa_id: str):
        query = """
            SELECT
                vd.id AS id_venda,
                ct.nome AS cliente,
                ct.telefone,
                ct.email,
                vd.valor_total,
                vd.forma_pagamento_id,
                vd.created_at AS data_venda,
                fpg.descricao AS forma_pagamento,
            
                COALESCE(
                    jsonb_agg(
                        jsonb_build_object(
                            'produto_id', pro.id,
                            'nome', pro.nome,
                            'quantidade', pv.quantidade
                        )
                        ORDER BY pro.nome
                    ) FILTER (WHERE pro.id IS NOT NULL),
                    '[]'::jsonb
                ) AS produtos
            
            FROM public.vendas vd
            
            JOIN public.contatos ct
                ON ct.id = vd.cliente_id
                AND ct.empresa_id = vd.empresa_id
            
            LEFT JOIN public.forma_pagamento fpg
                ON fpg.id = vd.forma_pagamento_id
            
            LEFT JOIN public.produtos_vendas pv
                ON pv.id_venda = vd.id
            
            LEFT JOIN public.produtos pro
                ON pro.id = pv.id_produto
            
            WHERE vd.empresa_id = %s
            
            GROUP BY
                vd.id,
                ct.nome,
                ct.telefone,
                ct.email,
                vd.valor_total,
                vd.forma_pagamento_id,
                vd.created_at,
                fpg.descricao
            
            ORDER BY vd.created_at DESC;
        """

        return self.execute_query(
            query,
            (empresa_id,)
        )

    def retorna_venda_unica(self, venda_id: str):
        query = """
            SELECT
                vd.id AS id_venda,
                ct.nome AS cliente,
                ct.telefone,
                ct.email,
                vd.numero_pedido,
                vd.valor_total,
                vd.forma_pagamento_id,
                vd.created_at AS data_venda,
                fpg.descricao AS forma_pagamento,

                COALESCE(
                    jsonb_agg(
                        jsonb_build_object(
                            'produto_id', pro.id,
                            'nome', pro.nome,
                            'quantidade', pv.quantidade
                        )
                        ORDER BY pro.nome
                    ) FILTER (WHERE pro.id IS NOT NULL),
                    '[]'::jsonb
                ) AS produtos

            FROM public.vendas vd

            JOIN public.contatos ct
                ON ct.id = vd.cliente_id
                AND ct.empresa_id = vd.empresa_id

            LEFT JOIN public.forma_pagamento fpg
                ON fpg.id = vd.forma_pagamento_id

            LEFT JOIN public.produtos_vendas pv
                ON pv.id_venda = vd.id

            LEFT JOIN public.produtos pro
                ON pro.id = pv.id_produto

            WHERE vd.id = %s

            GROUP BY
                vd.id,
                ct.nome,
                ct.telefone,
                ct.email,
                vd.valor_total,
                vd.forma_pagamento_id,
                vd.created_at,
                fpg.descricao

            ORDER BY vd.created_at DESC;
        """

        return self.execute_query(
            query,
            (venda_id,)
        )

    def criar_venda(self, dVendas: InsertVendas):

        # Monta a lista de produtos para enviar como JSONB
        produtos_json = json.dumps(
            [
                {
                    "produto_id": str(p.produto_id),
                    "quantidade": p.quantidade
                }
                for p in dVendas.produtos
            ]
            if dVendas.produtos
            else []
        )

        empresa_nome = dVendas.empresa_nome or dVendas.emrepsa_nome

        query = """
            SELECT public.criar_vendas_com_contato(
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
                %s::jsonb
            )
        """

        return self.execute_query(
            query,
            (
                dVendas.empresa_id,
                dVendas.nome,
                dVendas.telefone,
                dVendas.forma_pagamento_id,
                dVendas.email,
                dVendas.cpf_cnpj,
                empresa_nome,
                dVendas.observacao_contato,
                dVendas.valor,
                dVendas.usuario_responsavel_id,
                produtos_json
            )
        )


    def retorna_formas_pagamento(self, empresa_id: str = None):

        query = """
            SELECT
                id,
                descricao
            FROM public.forma_pagamento
            WHERE empresa_id = %s
               OR %s IS NULL
        """

        return self.execute_query(
            query,
            (
                empresa_id,
                empresa_id
            )
        )


    def deletar_venda(self, empresa_id: str, vendas_id: str):

        query = """
            DELETE FROM public.vendas
            WHERE empresa_id = %s::uuid
              AND id = %s::uuid
        """

        return self.execute_query(
            query,
            (
                empresa_id,
                vendas_id
            )
        )