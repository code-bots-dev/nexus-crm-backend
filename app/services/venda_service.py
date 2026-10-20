from app.models.venda_model import InsertVendas
from app.repositories.venda_repository import VendaRepository

class VendaService:
    def __init__(self):
        self.repository = VendaRepository()

    def listar_vendas(self, empresa_id: str):
        dvendas = self.repository.retorna_vendas(empresa_id)
        # print(dvendas)
        if not dvendas:
            raise ValueError(f"Nenhuma venda encontrada para empresa {empresa_id}")

        return dvendas

    def cadastrar_vendas(self, pVendas: InsertVendas):
        if not pVendas.empresa_id:
            raise ValueError("Necessário informar o variável ID Empresa.")

        return self.repository.criar_venda(pVendas)

    def atualizar_vendas(self):
        pass

    def listar_formas_pagamento(self, empresa_id: str = None):
        return self.repository.retorna_formas_pagamento(empresa_id)

    def deletar_venda(self, empresa_id: str, vendas_id: str):
        if not empresa_id:
            raise ValueError("ID da empresa (empresa_id) é obrigatório.")
        if not vendas_id:
            raise ValueError("ID da venda (vendas_id) é obrigatório.")

        return self.repository.deletar_venda(empresa_id, vendas_id)

if __name__=='__main__':
    repository = VendaService()

    print(repository.listar_vendas("75cc9dc2-7cf4-49e2-b21c-c285d50af99d"))