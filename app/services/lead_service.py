from app.models.lead_models import Leads, LeadsInsert
from app.repositories.lead_repository import LeadRepository

class LeadService:
    def __init__(self):
        self.repository = LeadRepository()

    def listar_lead(self, empresa_id, usuario_id):
        if not empresa_id:
            return ValueError("O campo ID Empresa é obrigatório e não foi informado!")
        return self.repository.retorna_leads(empresa_id, usuario_id)

    def validar_insert_lead(self, plead: LeadsInsert):
        if not plead.empresa_id:
            return ValueError("O campo ID Empresa é obrigatório e não foi informado!")

        if not plead.usuario_responsavel_id:
            return ValueError("O campo ID Usuário Responsável é obrigatório e não foi informado!")

        return self.repository.inserir_lead(plead)

if __name__ == '__main__':
    repository = LeadService()

    empresa_id="75cc9dc2-7cf4-49e2-b21c-c285d50af99d"
    usuario_id="9b4ba383-4d69-4664-b1a5-8006fa5e8e2a"

    print(repository.listar_lead(empresa_id, usuario_id))