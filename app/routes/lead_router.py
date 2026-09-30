from fastapi import HTTPException, Depends, APIRouter
from app.models.lead_models import Leads, LeadsInsert
from app.services.lead_service import LeadService
from components import tokenAcess

router = APIRouter(
    prefix='/v1/leads',
    tags=['Leads']
)

service = LeadService()

@router.get('/')
def listar_leads(empresa_id: str,
                 usuario_id: str,
                username: str = Depends(tokenAcess.token.verify_token)):
    dleads = service.listar_lead(empresa_id, usuario_id)

    return dleads

@router.post('/register_leads')
def cadastrar_lead(pleads: LeadsInsert,
                username: str = Depends(tokenAcess.token.verify_token)):
    leads = service.validar_insert_lead(pleads)
    return {
        "sucesso": True,
        "dados": leads
    }