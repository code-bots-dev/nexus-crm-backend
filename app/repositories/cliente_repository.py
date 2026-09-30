from dns.e164 import query

from app.models.cliente_model import CadastroCliente, CadastrarEnderecoCliente, AtualizarCliente, DeletarCliente
from app.repositories.base_repository import BaseRepository

class ClienteRepository(BaseRepository):
    def consultar_cliente(self, empresa_id,
                                cpf_cnpj: str,
                                telefone: str,
                                page_size,
                                offset
                          ):
        query = """
            select ct.id,
                   ct.nome,
                   ct.telefone,
                   ct.email,
                   ct.cpf_cnpj,
                   ct.status,
                   ct.created_at
            from public.contatos ct
            where 1=1
            and ct.empresa_id = %s
            and (ct.cpf_cnpj = %s or %s is null)
	        and (ct.telefone = %s or %s is null)
            order by ct.created_at desc,
                     ct.nome                     
            limit %s
            OFFSET %s
        """
        return self.execute_query(
            query,
            (
                empresa_id,
                cpf_cnpj,
                cpf_cnpj,
                telefone,
                telefone,
                page_size,
                offset
            )
        )

    def inserir_cliente(self,
                         cliente: CadastroCliente):
        query_insert = """
                INSERT INTO public.contatos (empresa_id,nome,telefone,email,status)
                VALUES(%s, %s, %s, %s, %s)
            """
        return self.execute_query(query_insert, (cliente.empresa_id,
                                                 cliente.nome,
                                                 cliente.telefone,
                                                 cliente.email,
                                                 cliente.status)
                                  )

    def inserir_endereco_contato(self,
                                 pEndContato: CadastrarEnderecoCliente
                                 ):
        pass

    def atualizar_cliente(self, pAtualizaCliente: AtualizarCliente):
        query = """
            select public.atualiza_contato(
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

        return self.execute_query(query, (
            pAtualizaCliente.empresa_id,
            pAtualizaCliente.contatos_id,
            pAtualizaCliente.nome,
            pAtualizaCliente.telefone,
            pAtualizaCliente.email,
            pAtualizaCliente.cpf_cnpj,
            pAtualizaCliente.empresa_nome,
            pAtualizaCliente.observacao_contato,
            pAtualizaCliente.status,
        ))
        # return query

    def consultar_status_cliente(self, cliente_id):
        query = """
            select status 
            from public.contatos
            where 1=1
            and id = %s
        """
        return self.execute_query(query, (cliente_id,))

    def deletar_cliente(self, delCliente: DeletarCliente):
        query = """
            select public.deletar_cliente(%s, %s)
        """
        return self.execute_query(query, (delCliente.contatos_id, delCliente.empresa_id))

if __name__ == '__main__':
    repository = ClienteRepository()

    dcliente = repository.consultar_status_cliente('761a27c7-dfe1-444b-b089-e581db013322')
    print(dcliente[0]['status'])