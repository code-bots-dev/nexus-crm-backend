from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente_model import CadastroCliente, AtualizarCliente, CadastrarEnderecoCliente, DeletarCliente

class ClienteService:

    def __init__(self):
        self.repository = ClienteRepository()

    def listar_cliente(self, empresa_id: str,
                           cpf_cnpj: str,
                           telefone: str,
                           page: int,
                           page_size: int):
        offset = (page - 1) * page_size

        return self.repository.consultar_cliente(empresa_id,
                                                 cpf_cnpj,
                                                 telefone,
                                                 page_size,
                                                 offset
                                                 )

    def cadastrar_cliente(self, cliente: CadastroCliente):
        if cliente.empresa_id is None:
            return ValueError("Campo código da empresa(empresa_id) é obrigatório e não foi informado.")

        return self.repository.inserir_cliente(cliente)

    def ser_atualizar_cliente(self,
                              pAtualizaCliente: AtualizarCliente
                              ):

        status_cliente = self.repository.consultar_status_cliente(pAtualizaCliente.contatos_id)

        # return status_cliente
        if status_cliente[0]['status'] != 'ATIVO':
            return ValueError("Cliente não pode ser atualizado foi está INATIVO.")

        return self.repository.atualizar_cliente(pAtualizaCliente)

    def ser_deletar_cliente(self,
                            delCliente: DeletarCliente,
                            ):
        if not delCliente.contatos_id or delCliente.contatos_id == None:
            return ValueError("É necessário informar o cliente.")

        return self.repository.deletar_cliente(delCliente)

if __name__ == '__main__':
    service = ClienteService()

    dados_cli = AtualizarCliente(
        empresa_id="75cc9dc2-7cf4-49e2-b21c-c285d50af99d",
        contatos_id="761a27c7-dfe1-444b-b089-e581db013322",
        nome="Abdiel Filipe Zier",
        telefone="83998777071",
        email="marcos.zier@gmail.com",
        cpf_cnpj="70183674104",
        empresa_nome=None,
        observacao_contato=None,
        status="INATIVO"
    )
    print(service.ser_atualizar_cliente(dados_cli))